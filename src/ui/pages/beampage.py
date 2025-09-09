import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QFrame, QDialogButtonBox,
                             QLineEdit, QHBoxLayout, QFormLayout, QPushButton, QDialog, QButtonGroup,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QIcon, QPixmap, QDoubleValidator

from PyQt6.QtCore import Qt, QPointF, QRectF, pyqtSignal, QSize



from src.ui.style.pagestyling import set_dropdown_style, set_lineEdit_style, setLabelStyle, setButtonStyle, set_table_style
from src.core.calculations.unit_factors import (beam_dropdown_units)
from src.ui.dialogs.beamdialogs import (pinnedSupportDialogue, rollerSupportDialogue, fixedSupportDialogue,
                                    addPointLoadDialogue, addMomentLoadDialogue, addDistLoadDialogue)
from src.core.models.beam_model import BeamModel, BeamElement
from src.ui.dialogs.results_dialog import ResultsDialog

class BeamPage(QWidget):
    def __init__(self):
        super().__init__()
       #self.beam_model = BeamModel()
        self.setupUI()


    def setupUI(self):
        # pagelayout
        beam_layout = QVBoxLayout()
        self.setLayout(beam_layout)
        beam_layout.setContentsMargins(20, 10, 20, 20)
        beam_layout.setSpacing(10)

        #unit drop down
        self.beam_unit_drop = QComboBox()
        set_dropdown_style(self.beam_unit_drop)
        self.beam_unit_drop.setFixedSize(250, 60)
        self.beam_unit_drop.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.beam_unit_drop.setObjectName("beam_unit_drop")
        self.beam_unit_drop.addItems(["English", "Metric / SI"])

        #info H layout (input + table)
        self.info_layout = QHBoxLayout()

        #table layout
        self.table_layout = QVBoxLayout()

        self.beam_table_header = QLabel("NO ACTIVE BEAMS")
        setLabelStyle(self.beam_table_header)
        self.beam_table_header.setObjectName("beam_table_header")
        #self.table_layout.addWidget(self.beam_table_header)


        #input layout
        input_layout = QVBoxLayout()
        

        #model setup form
        model_setup_layout = QVBoxLayout()

        #model header
        model_header = QLabel("Beam Model:  x -->")
        model_header.setObjectName("modelheader")
        setLabelStyle(model_header)

        # Add horizontal line under the "Beam Model:" label
        add_separator1 = QFrame()
        add_separator1.setFrameShape(QFrame.Shape.HLine)
        add_separator1.setFrameShadow(QFrame.Shadow.Sunken)
        add_separator1.setMaximumHeight(1)
        add_separator1.setMaximumWidth(500)
        add_separator1.setStyleSheet("background-color: #cccccc;")


        #length

        length_layout = QHBoxLayout()

        self.length_label = QLabel("Length")
        setLabelStyle(self.length_label)
        self.length_label.setObjectName("length_label")
        self.length_label.setFixedSize(160, 50)
        length_layout.addWidget(self.length_label)

        self.length_lineEdit = QLineEdit()
        set_lineEdit_style(self.length_lineEdit)
        self.length_lineEdit.setValidator(QDoubleValidator())
        self.length_lineEdit.setObjectName("length_lineEdit")
        self.length_lineEdit.setMaximumWidth(300)
        length_layout.addWidget(self.length_lineEdit)

        self.length_unit_label = QLabel()
        setLabelStyle(self.length_unit_label)
        length_layout.addWidget(self.length_unit_label)

        length_layout.addStretch()


        #modulus

        modulus_layout = QHBoxLayout()

        self.modulus_label = QLabel("Modulus of Elasticity")
        setLabelStyle(self.modulus_label)
        self.modulus_label.setObjectName("modulus_label")
        self.modulus_label.setFixedSize(160, 50)
        modulus_layout.addWidget(self.modulus_label)

        self.modulus_lineEdit = QLineEdit()
        set_lineEdit_style(self.modulus_lineEdit)
        self.modulus_lineEdit.setValidator(QDoubleValidator())
        self.modulus_lineEdit.setObjectName("modulus_lineEdit")
        self.modulus_lineEdit.setMaximumWidth(300)
        modulus_layout.addWidget(self.modulus_lineEdit)

        self.modulus_unit_label = QLabel()
        setLabelStyle(self.modulus_unit_label)
        modulus_layout.addWidget(self.modulus_unit_label)

        modulus_layout.addStretch()


        #inertia

        inertia_layout = QHBoxLayout()

        self.inertia_label = QLabel("Moment of Inertia")
        setLabelStyle(self.inertia_label)
        self.inertia_label.setObjectName("inertia_label")
        self.inertia_label.setFixedSize(160, 50)
        inertia_layout.addWidget(self.inertia_label)

        self.inertia_lineEdit = QLineEdit()
        set_lineEdit_style(self.inertia_lineEdit)
        self.inertia_lineEdit.setValidator(QDoubleValidator())
        self.inertia_lineEdit.setObjectName("inertia_lineEdit")
        self.inertia_lineEdit.setMaximumWidth(300)
        inertia_layout.addWidget(self.inertia_lineEdit)

        self.inertia_unit_label = QLabel()
        setLabelStyle(self.inertia_unit_label)
        inertia_layout.addWidget(self.inertia_unit_label)

        inertia_layout.addStretch()

        #poi

        poi_layout = QHBoxLayout()

        self.poi_label = QLabel("Point of Interest")
        setLabelStyle(self.poi_label)
        self.poi_label.setObjectName("poi_label")
        self.poi_label.setFixedSize(160, 50)
        poi_layout.addWidget(self.poi_label)

        self.poi_lineEdit = QLineEdit()
        set_lineEdit_style(self.poi_lineEdit)
        self.poi_lineEdit.setValidator(QDoubleValidator())
        self.poi_lineEdit.setObjectName("poi_lineEdit")
        self.poi_lineEdit.setMaximumWidth(300)
        poi_layout.addWidget(self.poi_lineEdit)

        self.poi_unit_label = QLabel()
        setLabelStyle(self.poi_unit_label)
        poi_layout.addWidget(self.poi_unit_label)

        poi_layout.addStretch()

        #make button
        self.make_beam = QPushButton("MAKE")
        self.make_beam.setObjectName("makeBeamButton")
        self.make_beam.setMaximumSize(500, 50)
        self.make_beam.setContentsMargins(0, 30, 0, 20)
        setButtonStyle(self.make_beam)

        self.make_beam.clicked.connect(self.create_beam_model)

        #add to form
        model_setup_layout.addStretch(stretch=1)
        model_setup_layout.addWidget(model_header)
        model_setup_layout.addWidget(add_separator1)
        model_setup_layout.addLayout(length_layout)
        model_setup_layout.addLayout(modulus_layout)
        model_setup_layout.addLayout(inertia_layout)
        model_setup_layout.addLayout(poi_layout)
        model_setup_layout.addSpacing(25)
        model_setup_layout.addWidget(self.make_beam)
        model_setup_layout.addStretch(stretch=1)
        model_setup_layout.setSpacing(0)





        # add butons
        buttons_vlayout = QVBoxLayout()

        #support layout
        support_layout = QHBoxLayout()

        #load layout
        load_layout = QHBoxLayout()

        add_label = QLabel("Add:")
        setLabelStyle(add_label)
        add_label.setObjectName("add_label")
    
        # Add horizontal line under the "Add:" label
        add_separator = QFrame()
        add_separator.setFrameShape(QFrame.Shape.HLine)
        add_separator.setFrameShadow(QFrame.Shadow.Sunken)
        add_separator.setMaximumHeight(1)
        add_separator.setMaximumWidth(500)
        add_separator.setStyleSheet("background-color: #cccccc;")

        supports_label = QLabel("Supports:")
        setLabelStyle(supports_label)
        supports_label.setObjectName("supports_label")
        

        add_pinned_btn = QPushButton()
        add_pinned_btn.setObjectName("pinned_support_btn")
        setButtonStyle(add_pinned_btn)
        add_pinned_btn.setIcon(QIcon(QPixmap("Equations-for-ME/assets/icons/pinnedicon.png")))
        add_pinned_btn.setIconSize(QSize(40, 40))
        add_pinned_btn.setMaximumWidth(150)
        add_pinned_btn.setMinimumWidth(150)
        add_pinned_btn.clicked.connect(self.open_pinned_support_dialog)


        add_roller_btn = QPushButton()
        add_roller_btn.setObjectName("roller_support_btn")
        setButtonStyle(add_roller_btn)
        add_roller_btn.setIcon(QIcon(QPixmap("Equations-for-ME/assets/icons/rollericon.png")))
        add_roller_btn.setIconSize(QSize(40, 40))
        add_roller_btn.setMaximumWidth(150)
        add_roller_btn.setMinimumWidth(150)

        add_roller_btn.clicked.connect(self.open_roller_support_dialog)


        add_fixed_btn = QPushButton()
        add_fixed_btn.setObjectName("fixed_support_btn")
        setButtonStyle(add_fixed_btn)
        add_fixed_btn.setIcon(QIcon(QPixmap("Equations-for-ME/assets/icons/fixedicon.png")))
        add_fixed_btn.setIconSize(QSize(40, 40))
        add_fixed_btn.setMaximumWidth(150)
        add_fixed_btn.setMinimumWidth(150)
        add_fixed_btn.clicked.connect(self.open_fixed_support_dialog)

        loads_label = QLabel("Loads:")
        setLabelStyle(loads_label)
        loads_label.setObjectName("loads_label")


        add_point_btn = QPushButton()
        add_point_btn.setObjectName("point_load_btn")
        setButtonStyle(add_point_btn)
        add_point_btn.setIcon(QIcon(QPixmap("Equations-for-ME/assets/icons/pointloadicon.png")))
        add_point_btn.setIconSize(QSize(40, 30))
        add_point_btn.setMaximumWidth(150)
        add_point_btn.setMinimumWidth(150)

        add_point_btn.clicked.connect(self.open_pointload_dialog)


        add_moment_btn = QPushButton()
        add_moment_btn.setObjectName("moment_load_btn")
        setButtonStyle(add_moment_btn)
        add_moment_btn.setIcon(QIcon(QPixmap("Equations-for-ME/assets/icons/momentloadicon.png")))
        add_moment_btn.setIconSize(QSize(40, 30))
        add_moment_btn.setMaximumWidth(150)
        add_moment_btn.setMinimumWidth(150)

        add_moment_btn.clicked.connect(self.open_momentload_dialog)


        add_dist_btn = QPushButton()
        add_dist_btn.setObjectName("distributed_load_btn")
        setButtonStyle(add_dist_btn)
        add_dist_btn.setIcon(QIcon(QPixmap("Equations-for-ME/assets/icons/distloadicon.png")))
        add_dist_btn.setIconSize(QSize(40, 30))
        add_dist_btn.setMaximumWidth(150)
        add_dist_btn.setMinimumWidth(150)

        add_dist_btn.clicked.connect(self.open_distload_dialog)

        #add to support layout
        support_layout.addWidget(add_pinned_btn)
        support_layout.addWidget(add_roller_btn)
        support_layout.addWidget(add_fixed_btn)
        support_layout.addStretch(stretch=1)
        support_layout.setSpacing(20)


        #add to load layout
        load_layout.addWidget(add_point_btn)
        load_layout.addWidget(add_moment_btn)
        load_layout.addWidget(add_dist_btn)
        load_layout.addStretch(stretch=1)
        load_layout.setSpacing(20)

        #add to button layout
        buttons_vlayout.addWidget(add_label)
        buttons_vlayout.addWidget(add_separator)
        buttons_vlayout.addWidget(supports_label)
        buttons_vlayout.addLayout(support_layout)
        buttons_vlayout.addWidget(loads_label)
        buttons_vlayout.addLayout(load_layout)
        buttons_vlayout.addSpacing(50)
        buttons_vlayout.setSpacing(2)  # Set spacing between objects to 2px

        #add to input layout
        input_layout.addLayout(model_setup_layout)
        input_layout.addLayout(buttons_vlayout)

        #add to info layout
        self.info_layout.addLayout(input_layout)
        self.info_layout.addLayout(self.table_layout)
        self.info_layout.addSpacing(75)


        #add to page
        beam_layout.addWidget(self.beam_unit_drop)
        beam_layout.addLayout(self.info_layout)

        # Initialize empty beam table
        self.create_empty_beam_table()

        self.beam_unit_drop.currentTextChanged.connect(self.update_beam_labels)
        self.update_beam_labels(self.beam_unit_drop.currentText())

        #below table
        model_buttons_layout = QHBoxLayout()

        #RUN BUTTON
        self.run_btn = QPushButton("RUN")
        self.run_btn.setObjectName("runbutton")
        setButtonStyle(self.run_btn)
        model_buttons_layout.addWidget(self.run_btn)
        self.run_btn.clicked.connect(self.run_analysis)

        #clear button
        self.clear_button = QPushButton("CLEAR")
        self.clear_button.setObjectName("clearbutton")
        setButtonStyle(self.clear_button)
        model_buttons_layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_beam_model_and_ui)

        #add to table layout
        self.table_layout.addWidget(self.beam_table_header)
        self.table_layout.addWidget(self.beam_table)
        self.table_layout.addLayout(model_buttons_layout)
     

    def run_analysis(self):
        """Assembles the model, applies boundary conditions, solves, and prints results."""
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            print("Cannot run analysis: Beam model not created yet.")
            return

        print("--- Running Beam Analysis ---")
        self.beam_model.assemble()
        self.beam_model.apply_boundary_conditions()
        self.beam_model.solve()

        results = self.beam_model.get_plot_results()
        dialog = ResultsDialog(results, self)
        dialog.exec()

        #self.beam_model.print_results()
        print("--- Analysis Complete ---")

    def update_beam_labels(self, system):
        units = beam_dropdown_units[system]
        length_unit = list(units['Length'].values())[0]
        modulus_unit = list(units['Elastic Modulus'].values())[0]
        inertia_unit = list(units['Moment of Inertia'].values())[0]
        point_load_unit = list(units['PointLoad'].values())[0]
        self.length_unit_label.setText(f"[ {length_unit} ]")
        self.modulus_unit_label.setText(f"[ {modulus_unit} ]")
        self.inertia_unit_label.setText(f"[ {inertia_unit} ]")
        self.poi_unit_label.setText(f"[ {length_unit} ]")
        self.beam_table.setHorizontalHeaderLabels([f'Location [ {length_unit} ]', f'Magnitude [ {point_load_unit} ]', 'Support', 'Load'])

    def show_error_dialog(self, message):
        dialog = QDialog(self)
        dialog.setWindowTitle("Error")
        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)
        dialog.setLayout(layout)
        dialog.exec()

    def open_pinned_support_dialog(self):
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.show_error_dialog('no active beam model yet')
            return
        unit_system = self.beam_unit_drop.currentText()
        dialog = pinnedSupportDialogue(unit_system, self.beam_model)
        dialog.exec()
        self.make_beam_table()

    def open_roller_support_dialog(self):
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.show_error_dialog('no active beam model yet')
            return
        unit_system = self.beam_unit_drop.currentText()
        dialog = rollerSupportDialogue(unit_system, self.beam_model)
        dialog.exec()
        self.make_beam_table()

    def open_fixed_support_dialog(self):
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.show_error_dialog('no active beam model yet')
            return
        unit_system = self.beam_unit_drop.currentText()
        dialog = fixedSupportDialogue(unit_system, self.beam_model)
        dialog.exec()
        self.make_beam_table()

    def open_pointload_dialog(self):
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.show_error_dialog('no active beam model yet')
            return
        unit_system = self.beam_unit_drop.currentText()

        dialog = addPointLoadDialogue(unit_system, self.beam_model)  
        dialog.exec()
        self.make_beam_table()  

    def open_momentload_dialog(self):
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.show_error_dialog('no active beam model yet')
            return
        unit_system = self.beam_unit_drop.currentText()

        dialog = addMomentLoadDialogue(unit_system, self.beam_model)
        dialog.exec()
        self.make_beam_table()

    def open_distload_dialog(self):
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.show_error_dialog('no active beam model yet')
            return
        unit_system = self.beam_unit_drop.currentText()

        dialog = addDistLoadDialogue(unit_system, self.beam_model)
        dialog.exec()
        self.make_beam_table()

    def create_empty_beam_table(self):
        """Create an empty beam table that shows when the page loads"""
        self.beam_table = QTableWidget()
        self.beam_table.setColumnCount(4)
        self.beam_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.beam_table.setRowCount(0)  # Start with no rows
        self.beam_table.setMaximumHeight(800) 
        self.beam_table.setMinimumWidth(700)
        self.beam_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        set_table_style(self.beam_table)

        #self.table_layout.addWidget(self.beam_table)


    def make_beam_table(self):
        """Update the beam table with current beam model data"""
        if not hasattr(self, 'beam_model') or self.beam_model is None:
            self.beam_table.setRowCount(0)
            return

        self.beam_table.setRowCount(0)
        node_positions = self.beam_model.get_node_positions()
        row_count = 0

        # Supports
        for node_idx, support_type in sorted(self.beam_model.supports.items()):
            self.beam_table.insertRow(row_count)
            location = node_positions[node_idx] if node_idx < len(node_positions) else "?"
            self.beam_table.setItem(row_count, 0, QTableWidgetItem(f"{location:.2f}"))
            self.beam_table.setItem(row_count, 1, QTableWidgetItem(""))
            self.beam_table.setItem(row_count, 2, QTableWidgetItem(support_type))
            self.beam_table.setItem(row_count, 3, QTableWidgetItem(""))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, idx=node_idx: self.delete_support(idx))
            self.beam_table.setCellWidget(row_count, 4, delete_btn)
            row_count += 1

        # Point Loads and Moments
        for dof_idx, value in sorted(self.beam_model.point_loads.items()):
            self.beam_table.insertRow(row_count)
            node_idx = dof_idx // 2
            is_moment = (dof_idx % 2 == 1)
            location = node_positions[node_idx] if node_idx < len(node_positions) else "?"
            load_type = "Moment" if is_moment else "Point Load"
            
            self.beam_table.setItem(row_count, 0, QTableWidgetItem(f"{location:.2f}"))
            self.beam_table.setItem(row_count, 1, QTableWidgetItem(f"{value:.2f}"))
            self.beam_table.setItem(row_count, 2, QTableWidgetItem(""))
            self.beam_table.setItem(row_count, 3, QTableWidgetItem(load_type))

            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, idx=dof_idx: self.delete_point_load(idx))
            self.beam_table.setCellWidget(row_count, 4, delete_btn)
            row_count += 1

        # Distributed Loads (grouped)
        dist_loads = self.beam_model.distributed_loads
        elements = self.beam_model.elements
        
        sorted_elem_indices = sorted(dist_loads.keys())
        grouped = []
        if sorted_elem_indices:
            group_start = sorted_elem_indices[0]
            group_end = group_start
            w0_group, _ = dist_loads[group_start]
            _, wL_prev = dist_loads[group_start]

            for idx in sorted_elem_indices[1:]:
                w0, wL = dist_loads[idx]
                if idx == group_end + 1 and abs(w0 - wL_prev) < 1e-8:
                    group_end = idx
                    wL_prev = wL
                else:
                    grouped.append((group_start, group_end, w0_group, wL_prev))
                    group_start = idx
                    group_end = idx
                    w0_group = w0
                    wL_prev = wL
            grouped.append((group_start, group_end, w0_group, wL_prev))

            for group_start, group_end, w0, wL in grouped:
                self.beam_table.insertRow(row_count)
                elem_start = elements[group_start]
                elem_end = elements[group_end]
                x_start = node_positions[elem_start.node_start.index]
                x_end = node_positions[elem_end.node_end.index]
                location = f"[{x_start:.2f} | {x_end:.2f}]"
                magnitude = f"[{w0:.2f} | {wL:.2f}]"
                
                self.beam_table.setItem(row_count, 0, QTableWidgetItem(location))
                self.beam_table.setItem(row_count, 1, QTableWidgetItem(magnitude))
                self.beam_table.setItem(row_count, 2, QTableWidgetItem(""))
                self.beam_table.setItem(row_count, 3, QTableWidgetItem("Distributed Load"))

                delete_btn = QPushButton("Delete")
                delete_btn.clicked.connect(lambda checked, start=group_start, end=group_end: self.delete_dist_load_group(start, end))
                self.beam_table.setCellWidget(row_count, 4, delete_btn)
                row_count += 1

    def delete_support(self, node_idx):
        if self.beam_model and node_idx in self.beam_model.supports:
            del self.beam_model.supports[node_idx]
            self.make_beam_table()

    def delete_point_load(self, dof_idx):
        if self.beam_model and dof_idx in self.beam_model.point_loads:
            del self.beam_model.point_loads[dof_idx]
            self.make_beam_table()

    def delete_dist_load_group(self, start_idx, end_idx):
        if self.beam_model:
            keys_to_delete = [i for i in range(start_idx, end_idx + 1) if i in self.beam_model.distributed_loads]
            for key in keys_to_delete:
                del self.beam_model.distributed_loads[key]
            self.make_beam_table()

        

    
    def create_beam_model(self):
        #get input values
        length_text = self.length_lineEdit.text()
        modulus_text = self.modulus_lineEdit.text()
        inertia_text = self.inertia_lineEdit.text()
        poi_text = self.poi_lineEdit.text()
        unit_sys = self.beam_unit_drop.currentText()

        #error handling
        errors = []
        if not length_text:
            errors.append("Length is required")
        if not modulus_text:
            errors.append("Modulus of Elasticity is required")
        if not inertia_text:
            errors.append("Moment of Inertia is required")

        try:
            length = float(length_text)
        except ValueError:
            errors.append("Length must be a number.")

        try:
            modulus = float(modulus_text)
        except ValueError:
            errors.append("Modulus of Elasticity must be a number.")

        try:
            inertia = float(inertia_text)
        except ValueError:
            errors.append("Moment of Inertia must be a number.")

        poi = None
        if poi_text:
            try:
                poi = float(poi_text)
                if not (0 < poi < length):
                    errors.append("Point of Interest must be within the beam's length.")
            except ValueError:
                errors.append("Point of Interest must be a number.")

        # You may want to add a default or input for num_elements
        num_elements = 4  # Example default, or get from an input

        if errors:
            # Show error message using dialog popup
            error_message = "Beam model creation failed:\n\n" + "\n".join(f"• {err}" for err in errors)
            self.show_error_dialog(error_message)
            return

        EI = modulus * inertia

        #discretization to create at least 10 elements
        #target element length = .5 units
        target_element_length = 0.5
        min_elements = 10
        num_elements = max(int(length / target_element_length), min_elements)

        self.beam_model = BeamModel(length, num_elements, EI, unit_sys, poi=poi)
        self.make_beam_table()
        self.update_beam_table_header()
        print(f"Beam model created with {num_elements} elements!")

    def update_beam_table_header(self):
        length_unit = list(beam_dropdown_units[self.beam_unit_drop.currentText()]['Length'].values())[0]
        if self.beam_model is None:
            self.beam_table_header.setText("NO ACTIVE BEAMS")
        else:
            self.beam_table_header.setText(f"BEAM MODEL IS {self.beam_model.length} [{length_unit}] LONG")

    def clear_beam_model_and_ui(self):
        """Clears the beam model, input fields, and the table."""
        self.beam_model = None

        # Clear input fields
        self.length_lineEdit.clear()
        self.modulus_lineEdit.clear()
        self.inertia_lineEdit.clear()
        self.poi_lineEdit.clear()

        # Clear the table
        self.beam_table.setRowCount(0)

        # Update header
        self.update_beam_table_header()

        print("Beam model and UI cleared.")

    





