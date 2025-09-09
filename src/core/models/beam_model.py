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
        current_pos = 0.0
        for elem in self.elements:
            current_pos += elem.L
            x_positions.append(current_pos)
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
        self.K.fill(0)
        self.F.fill(0)
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
        self.d.fill(0)
        self.d[self.free_dofs] = np.linalg.solve(self.K_ff, self.F_f)
        self.reactions = self.K @ self.d - self.F

    def get_plot_results(self, num_points_per_element=2):
        x_plot = []
        v_plot = []  # Displacements
        s_plot = []  # Slopes
        shear_plot = []
        moment_plot = []

        node_positions = self.get_node_positions()

        for i, elem in enumerate(self.elements):
            dof_map = elem.dof_map()
            d_elem = self.d[dof_map]
            w0, wL = self.distributed_loads.get(i, (0, 0))

            x_start = node_positions[elem.node_start.index]
            
            x_local = np.linspace(0, elem.L, num_points_per_element)
            x_global = x_start + x_local

            # Displacement and Slope
            v_local, s_local = elem.shape_functions(x_local, d_elem)
            v_plot.extend(v_local)
            s_plot.extend(s_local)
            x_plot.extend(x_global)

            # Shear and Moment
            shear_local, moment_local = elem.internal_forces(x_local, d_elem, w0, wL)
            shear_plot.extend(shear_local)
            moment_plot.extend(moment_local)

        return {
            "node_positions": x_plot,
            "displacements": v_plot,
            "slopes": s_plot,
            "shear_forces": shear_plot,
            "bending_moments": moment_plot,
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
        # Equivalent nodal forces for a linearly distributed load
        return np.array([
            -((L/20) * (7*w0 + 3*wL)),
            -((L**2/60) * (3*w0 + 2*wL)),
            -((L/20) * (3*w0 + 7*wL)),
            ((L**2/60) * (2*w0 + 3*wL))
        ])

    def shape_functions(self, x, d_elem):
        L = self.L
        v1, th1, v2, th2 = d_elem

        N1 = 1 - 3*(x/L)**2 + 2*(x/L)**3
        N2 = x * (1 - 2*(x/L) + (x/L)**2)
        N3 = 3*(x/L)**2 - 2*(x/L)**3
        N4 = x * ((x/L)**2 - (x/L))

        v_x = v1*N1 + th1*N2 + v2*N3 + th2*N4

        # Derivatives for slope
        dN1_dx = (-6*x/L**2) + (6*x**2/L**3)
        dN2_dx = 1 - 4*x/L + 3*x**2/L**2
        dN3_dx = (6*x/L**2) - (6*x**2/L**3)
        dN4_dx = 3*x**2/L**2 - 2*x/L

        s_x = v1*dN1_dx + th1*dN2_dx + v2*dN3_dx + th2*dN4_dx
        
        return v_x, s_x

    def internal_forces(self, x, d_elem, w0, wL):
        L = self.L
        k_local = self.stiffness_matrix()
        f_load_local = self.distributed_load_vector(w0, wL)
        f_elem = k_local @ d_elem - f_load_local

        V_start = f_elem[0]
        M_start = f_elem[1]

        # Contribution from distributed load at distance x
        V_dist = (w0 * x) + ((wL - w0) * x**2 / (2 * L))
        M_dist = (w0 * x**2 / 2) + ((wL - w0) * x**3 / (6 * L))

        # Shear and moment along the element
        V_x = V_start - V_dist
        M_x = M_start + V_start * x - M_dist

        return V_x, M_x
