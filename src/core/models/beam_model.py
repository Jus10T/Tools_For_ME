import numpy as np

class BeamModel:
    def __init__(self, length, num_elements, EI, unit_sys, poi=None):
        self.length = length
        self.num_elements = num_elements
        self.EI = EI 
        self.unit_system = unit_sys
        self.nodes = [Node(i) for i in range(num_elements + 1 )]

        #discretize the beam model into elements
        self.elements = [
            BeamElement(i, self.nodes[i], self.nodes[i + 1], EI, length / num_elements)
            for i in range(num_elements)
        ]

        if poi is not None:
            self.insert_node_at_position(poi)

        self.supports = {} #node_index: 'fixed'/'pinned'/'roller'
        self.point_loads = {} # dof_index: load
        self.distributed_loads = {} #element_index : (w0, wL)
        self.ndof = 2 * len(self.nodes)
        self.K = np.zeros((self.ndof, self.ndof))
        self.F = np.zeros(self.ndof)
        self.d = np.zeros(self.ndof)

    def get_node_positions(self):
        x_positions = [0.00]
        for elem in self.elements:
            x_positions.append(x_positions[-1] + elem.L)
        return x_positions

    def insert_node_at_position(self, x_pos, tol = 1e-6): # tol --> tolerance 
        x_positions = self.get_node_positions()

        #check if node exists
        for i, x in enumerate(x_positions):
            if abs(x - x_pos) < tol:
                return i #return existing node index
        
        #find element to split
        for e_idx, elem in enumerate(self.elements):
            x_start = x_positions[elem.node_start.index]
            x_end = x_positions[elem.node_end.index]
            if x_start < x_pos < x_end:
                break
        else:
            raise ValueError(f"x = {x_pos} is outside the beam domain.")
        
        #Create new node
        new_node_index = len(self.nodes)
        new_node = Node(new_node_index)
        self.nodes.insert(elem.node_end.index, new_node)

        #  Split the element
        L1 = x_pos - x_start
        L2 = x_end - x_pos
        ei = elem.EI

        e1 = BeamElement(len(self.elements), elem.node_start, new_node, ei, L1)
        e2 = BeamElement(len(self.elements) + 1, new_node, elem.node_end, ei, L2)

        # 5. Replace old element with the two new elements
        self.elements.pop(e_idx)
        self.elements.insert(e_idx, e2)
        self.elements.insert(e_idx, e1)

        #  Re-index all nodes and elements
        for i, node in enumerate(self.nodes):
            node.index = i
            node.dofs = [2 * i, 2 * i + 1]

        for i, elem in enumerate(self.elements):
            elem.index = i

        #  Rebuild global DOFs and matrices
        self.ndof = 2 * len(self.nodes)
        self.K = np.zeros((self.ndof, self.ndof))
        self.F = np.zeros(self.ndof)
        self.d = np.zeros(self.ndof)

        return new_node_index

    def add_support(self, node_index, support_type):
        self.supports[node_index] = support_type


    def add_point_load(self, node_index, value, moment=False):
        dof = 2 * node_index + (1 if moment else 0)
        # Apply negative for downward force convention
        load_value = -value if not moment else value
        self.point_loads[dof] = self.point_loads.get(dof, 0) + load_value

    def add_moment_load(self, node_index, moment_value):
        self.add_point_load(node_index, moment_value, moment=True)

    def add_distributed_load(self, element_index, w0, wL):
        self.distributed_loads[element_index] = (w0, wL)

    def assemble(self):
        for elem in self.elements:
            k_local = elem.stiffness_matrix()
            dof_map = elem.dof_map()
            for i in range(4):
                for j in range(4):
                    self.K[dof_map[i], dof_map[j]] += k_local[i, j]

            if elem.index in self.distributed_loads:
                w0, wL = self.distributed_loads[elem.index]
                f_local = elem.distributed_load_vector(w0, wL)
                for i in range(4):
                    self.F[dof_map[i]] += f_local[i]

        for dof, load in self.point_loads.items():
            self.F[dof] += load

    def apply_boundary_conditions(self):
        self.prescribed_dofs = []
        for node_index, support in self.supports.items():
            if support in ['fixed', 'pinned', 'roller']: # constraining vertical displacement
                self.prescribed_dofs.append(2 * node_index)
            if support == 'fixed':                       # constraining rotational displacememt
                self.prescribed_dofs.append(2 * node_index + 1)

        self.free_dofs = [i for i in range(self.ndof) if i not in self.prescribed_dofs]
        self.K_ff = self.K[np.ix_(self.free_dofs, self.free_dofs)]
        self.F_f = self.F[self.free_dofs]

    def solve(self):
        self.d[self.free_dofs] = np.linalg.solve(self.K_ff, self.F_f)
        self.reactions = self.K @ self.d - self.F

    def print_results(self):
        print("Nodal Displacements:")
        node_positions = self.get_node_positions()
        for i in range(len(self.nodes)):
            x_pos = node_positions[i]
            v = self.d[2*i]
            theta = self.d[2*i+1]
            print(f"Node {i} (x={x_pos:.2f}): v = {v:.6e}, θ = {theta:.6e}")
        print("\nSupport Reactions:")
        for i in self.prescribed_dofs:
            # Determine if it's a force or moment reaction for clearer output
            node_idx = i // 2
            x_pos = node_positions[node_idx]
            if i % 2 == 0:
                # Vertical force reaction
                print(f"Reaction Force at Node {node_idx} (x={x_pos:.2f}): R = {self.reactions[i]:.2f}")
            else:
                # Moment reaction
                print(f"Reaction Moment at Node {node_idx} (x={x_pos:.2f}): M = {self.reactions[i]:.2f}")

        print("\nInternal Shear and Moment:")
        shear, moment = self.calculate_shear_and_moment()
        for i in range(len(self.nodes)):
            x_pos = node_positions[i]
            print(f"Node {i} (x={x_pos:.2f}): Shear = {shear[i]:.2f}, Moment = {moment[i]:.2f}")

    def calculate_shear_and_moment(self):
        """Calculates shear and moment at each node using element-level results."""
        num_nodes = len(self.nodes)
        shear = np.zeros(num_nodes)
        moment = np.zeros(num_nodes)

        for i, elem in enumerate(self.elements):
            dof_map = elem.dof_map()
            d_elem = self.d[dof_map]
            k_local = elem.stiffness_matrix()
            w0, wL = self.distributed_loads.get(i, (0, 0))
            f_load_local = elem.distributed_load_vector(w0, wL)
            f_elem = k_local @ d_elem - f_load_local

            if i == 0:
                shear[i] = f_elem[0]
                moment[i] = f_elem[1]

            shear[i+1] = -f_elem[2]
            moment[i+1] = f_elem[3]
            
        return shear, moment
    
    def get_results(self):
        displacements = self.d[0::2] #deflection
        slopes = self.d[1::2] #beam slope

        shear, moment = self.calculate_shear_and_moment() #internal forces and bending moments
        node_positions = self.get_node_positions()

        return {
            "node_positions": node_positions,
            "displacements": displacements,
            "slopes": slopes,
            "shear_forces": shear,
            "bending_moments": moment,
            "unit_system": self.unit_system
        }





class Node:
    def __init__(self, index):
        self.index = index
        self.dofs = [2 * index, 2 * index + 1 ] #vertical, rotation


class BeamElement: 
    def __init__(self, index, node_start, node_end, EI, L):
        self.index = index
        self.node_start = node_start
        self.node_end = node_end
        self.EI = EI
        self.L = L

    def stiffness_matrix(self):
        L, EI = self.L, self.EI
        coeff = EI / L**3
        return coeff * np.array([
            [12,    6*L,   -12,   6*L],
            [6*L,  4*L**2, -6*L,  2*L**2],
            [-12,  -6*L,   12,  -6*L],
            [6*L,  2*L**2, -6*L,  4*L**2],
        ])
    
    def dof_map(self):
        return self.node_start.dofs + self.node_end.dofs
    
    def distributed_load_vector(self, w0, wL):
        L = self.L
        return np.array([
            (L/20) * (7*w0 + 3*wL),
            (L**2/60) * (3*w0 + 2*wL),
            (L/20) * (3*w0 + 7*wL),
            -(L**2/60) * (2*w0 + 3*wL)
        ])
        