from PyQt6.QtWidgets import (QMessageBox, QWidget, QVBoxLayout, QLabel, QComboBox, QFrame, QDialogButtonBox,
                             QLineEdit, QHBoxLayout, QFormLayout, QPushButton, QDialog, QButtonGroup)
from numpy import ma

from src.ui.style.pagestyling import set_dropdown_style, set_lineEdit_style, setLabelStyle, setButtonStyle
from src.core.calculations.unit_factors import beam_dropdown_units

class pinnedSupportDialogue(QDialog):
    def __init__(self, unit_system, beam_model):
        super().__init__()
        self.unit_system = unit_system
        self.beam_model = beam_model
        self.setWindowTitle("Add Pinned Support")
        self.setGeometry(300,300,600,400)
        self.setupUI()

    def setupUI(self):

        location_layout = QHBoxLayout()

        #get unit
        units = beam_dropdown_units[self.unit_system]
        length_unit = list(units['Length'].values())[0]

        location_label = QLabel("Location: x --->")
        setLabelStyle(location_label)
        location_layout.addWidget(location_label)

        self.pin_support_location_input = QLineEdit()
        self.pin_support_location_input.setMaximumWidth(300)
        set_lineEdit_style(self.pin_support_location_input)
        location_layout.addWidget(self.pin_support_location_input)

        #use unit
        location_unit_label = QLabel(length_unit)
        setLabelStyle(location_unit_label)
        location_layout.addWidget(location_unit_label)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        #main layout 
        main_layout = QVBoxLayout()
        main_layout.addLayout(location_layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def accept(self):
        print("DEBUG: accept called")
        text = self.pin_support_location_input.text()
        if not text:
            QMessageBox.critical(self, "Input Error", "Location input is required.")
            return
        try:
            x_pos = float(text)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Location must be a number.")
            return

        if not (0 <= x_pos <= self.beam_model.length):
            QMessageBox.critical(self, "Input Error", f"Location must be between 0 and {self.beam_model.length}.")
            return

        support_type = "pinned"
        new_node_idx = self.beam_model.insert_node_at_position(x_pos)
        self.beam_model.add_support(new_node_idx, support_type)
        super().accept()


class rollerSupportDialogue(QDialog):
    def __init__(self, unit_system, beam_model):
        super().__init__()
        self.unit_system = unit_system
        self.beam_model = beam_model
        self.setWindowTitle("Add Roller Support")
        self.setGeometry(300,300,600,400)
        self.setupUI()

    def setupUI(self):

        location_layout = QHBoxLayout()

        #get unit
        units = beam_dropdown_units[self.unit_system]
        length_unit = list(units['Length'].values())[0]

        location_label = QLabel("Location: x--->")
        setLabelStyle(location_label)
        location_layout.addWidget(location_label)

        self.roller_support_location_input = QLineEdit()
        self.roller_support_location_input.setMaximumWidth(300)
        set_lineEdit_style(self.roller_support_location_input)
        location_layout.addWidget(self.roller_support_location_input)

        location_unit_label = QLabel(length_unit)
        setLabelStyle(location_unit_label)
        location_layout.addWidget(location_unit_label)


        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        #main layout 
        main_layout = QVBoxLayout()
        main_layout.addLayout(location_layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def accept(self):
        print("DEBUG: accept called")
        text = self.roller_support_location_input.text()
        if not text:
            QMessageBox.critical(self, "Input Error", "Location input is required.")
            return
        try:
            x_pos = float(text)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Location must be a number.")
            return

        if not (0 <= x_pos <= self.beam_model.length):
            QMessageBox.critical(self, "Input Error", f"Location must be between 0 and {self.beam_model.length}.")
            return

        support_type = "roller"
        new_node_idx = self.beam_model.insert_node_at_position(x_pos)
        self.beam_model.add_support(new_node_idx, support_type)
        super().accept()


class fixedSupportDialogue(QDialog):
    def __init__(self, unit_system, beam_model):
        super().__init__()
        self.unit_system = unit_system
        self.beam_model = beam_model
        self.setWindowTitle("Add Fixed Support")
        self.setGeometry(300,300,600,400)
        self.setupUI()

    def setupUI(self):

        form_layout = QHBoxLayout()

        fixed_location_label = QLabel("Location:")
        setLabelStyle(fixed_location_label)
        form_layout.addWidget(fixed_location_label)

        #checkable buttons
        left_position_btn = QPushButton("LEFT")
        left_position_btn.setCheckable(True)
        setButtonStyle(left_position_btn)
        form_layout.addWidget(left_position_btn)

        right_position_btn = QPushButton("RIGHT") 
        right_position_btn.setCheckable(True)
        setButtonStyle(right_position_btn)
        form_layout.addWidget(right_position_btn)

        #button group
        self.fixed_btn_group = QButtonGroup(self)
        self.fixed_btn_group.setExclusive(True)
        self.fixed_btn_group.addButton(left_position_btn, 0)
        self.fixed_btn_group.addButton(right_position_btn, 1)


        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        #main layout 
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def accept(self):
        checked_id = self.fixed_btn_group.checkedId()
        if checked_id == 0: #left
            x_pos = 0.0
        elif checked_id == 1: #right
            x_pos = self.beam_model.length
        else:
            QMessageBox.critical(self,"Selection Error", "Must select LEFT or RIGHT")
            return

        
        
        support_type = "fixed"
        node_index = self.beam_model.insert_node_at_position(x_pos)
        self.beam_model.add_support(node_index, support_type)
        super().accept()


class addPointLoadDialogue(QDialog):
    def __init__(self, unit_system, beam_model):
        super().__init__()
        self.unit_system = unit_system
        self.beam_model = beam_model
        self.setWindowTitle("Add Point Load")
        self.setGeometry(300,300,600,400)
        self.setupUI()

    def setupUI(self):

        #get unit(s)
        units = beam_dropdown_units[self.unit_system]
        length_unit = list(units['Length'].values())[0]
        force_magnitude_unit = list(units['PointLoad'].values())[0]

        #location
        location_layout = QHBoxLayout()

        location_label = QLabel("Location: x --->")
        setLabelStyle(location_label)
        location_layout.addWidget(location_label)

        
        self.pointload_location_input = QLineEdit()
        self.pointload_location_input.setMaximumWidth(300)
        set_lineEdit_style(self.pointload_location_input)
        location_layout.addWidget(self.pointload_location_input)


        location_unit_label = QLabel(length_unit)
        setLabelStyle(location_unit_label)
        location_layout.addWidget(location_unit_label)


        #magnitude
        magnitude_layout = QHBoxLayout()

        magnitude_label = QLabel("Magnitude:      ")
        setLabelStyle(magnitude_label)
        magnitude_layout.addWidget(magnitude_label)


        self.pointload_mag_input = QLineEdit()
        self.pointload_mag_input.setMaximumWidth(300)
        set_lineEdit_style(self.pointload_mag_input)
        magnitude_layout.addWidget(self.pointload_mag_input)

        mag_unit_label = QLabel(force_magnitude_unit)
        setLabelStyle(mag_unit_label)
        magnitude_layout.addWidget(mag_unit_label)




        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        #main layout 
        main_layout = QVBoxLayout()
        main_layout.addLayout(location_layout)
        main_layout.addLayout(magnitude_layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def accept(self):
        print("DEBUG: accept called")
        location_text = self.pointload_location_input.text()
        magnitude_text = self.pointload_mag_input.text()
        if not location_text:
            QMessageBox.critical(self, "Input Error", "Location input is required.")
            return
        if not magnitude_text:
            QMessageBox.critical(self, "Input Error", "Magnitude input is required.")
            return
        try:
            x_pos = float(location_text)
            magnitude = float(magnitude_text)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Location and Magnitude must be a number.")
            return

        if not (0 <= x_pos <= self.beam_model.length):
            QMessageBox.critical(self, "Input Error", f"Location must be between 0 and {self.beam_model.length}.")
            return

        
        new_node_idx = self.beam_model.insert_node_at_position(x_pos)
        self.beam_model.add_point_load(new_node_idx, magnitude, moment=False)
        super().accept()

class addMomentLoadDialogue(QDialog):
    def __init__(self, unit_system, beam_model):
        super().__init__()        
        self.unit_system = unit_system
        self.beam_model = beam_model
        self.setWindowTitle("Add Moment Load")
        self.setGeometry(300,300,600,400)
        self.setupUI()

    def setupUI(self):

        #get unit(s)
        units = beam_dropdown_units[self.unit_system]
        length_unit = list(units['Length'].values())[0]
        moment_magnitude_unit = list(units['MomentLoad'].values())[0]

        #location
        location_layout = QHBoxLayout()

        location_label = QLabel("Location: x --->")
        setLabelStyle(location_label)
        location_layout.addWidget(location_label)

        
        self.moment_location_input = QLineEdit()
        self.moment_location_input.setMaximumWidth(300)
        set_lineEdit_style(self.moment_location_input)
        location_layout.addWidget(self.moment_location_input)


        location_unit_label = QLabel(length_unit)
        setLabelStyle(location_unit_label)
        location_layout.addWidget(location_unit_label)


        #magnitude
        magnitude_layout = QHBoxLayout()

        magnitude_label = QLabel("Magnitude:      ")
        setLabelStyle(magnitude_label)
        magnitude_layout.addWidget(magnitude_label)


        self.moment_mag_input = QLineEdit()
        self.moment_mag_input.setMaximumWidth(300)
        set_lineEdit_style(self.moment_mag_input)
        magnitude_layout.addWidget(self.moment_mag_input)

        moment_mag_unit_label = QLabel(moment_magnitude_unit)
        setLabelStyle(moment_mag_unit_label)
        magnitude_layout.addWidget(moment_mag_unit_label)




        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        #main layout 
        main_layout = QVBoxLayout()
        main_layout.addLayout(location_layout)
        main_layout.addLayout(magnitude_layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def accept(self):
        print("DEBUG: accept called")
        location_text = self.moment_location_input.text()
        magnitude_text = self.moment_mag_input.text()
        if not location_text:
            QMessageBox.critical(self, "Input Error", "Location input is required.")
            return
        if not magnitude_text:
            QMessageBox.critical(self, "Input Error", "Magnitude input is required.")
            return
        try:
            x_pos = float(location_text)
            magnitude = float(magnitude_text)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Location and Magnitude must be a number.")
            return

        if not (0 <= x_pos <= self.beam_model.length):
            QMessageBox.critical(self, "Input Error", f"Location must be between 0 and {self.beam_model.length}.")
            return

        
        new_node_idx = self.beam_model.insert_node_at_position(x_pos)
        self.beam_model.add_point_load(new_node_idx, magnitude, moment=True)
        super().accept()

class addDistLoadDialogue(QDialog):
    def __init__(self, unit_system, beam_model):
        super().__init__()
        self.unit_system = unit_system
        self.beam_model = beam_model

        self.setWindowTitle("Add Distributed Load")
        self.setGeometry(300,300,600,400)
        self.setupUI()

    def setupUI(self):

        #get unit(s)
        units = beam_dropdown_units[self.unit_system]
        length_unit = list(units['Length'].values())[0]
        distr_magnitude_unit = list(units['distributedLoad'].values())[0]

        #start location
        start_location_layout = QHBoxLayout()

        start_location_label = QLabel("START Location: x --->")
        setLabelStyle(start_location_label)
        start_location_layout.addWidget(start_location_label)

        self.start_location_input = QLineEdit()
        self.start_location_input.setMaximumWidth(300)
        set_lineEdit_style(self.start_location_input)
        start_location_layout.addWidget(self.start_location_input)

        start_location_unit = QLabel(length_unit)
        setLabelStyle(start_location_unit)
        start_location_layout.addWidget(start_location_unit)

        #start magnitude
        start_mag_layout = QHBoxLayout()

        start_mag_label = QLabel("START Magnitude:       ")
        setLabelStyle(start_mag_label)
        start_mag_layout.addWidget(start_mag_label)

        self.start_mag_input = QLineEdit()
        self.start_mag_input.setMaximumWidth(300)
        set_lineEdit_style(self.start_mag_input)
        start_mag_layout.addWidget(self.start_mag_input)

        start_mag_unit = QLabel(distr_magnitude_unit)
        setLabelStyle(start_mag_unit)
        start_mag_layout.addWidget(start_mag_unit)

        #end location
        end_location_layout = QHBoxLayout()

        end_location_label = QLabel("END Location: x--->    ")
        setLabelStyle(end_location_label)
        end_location_layout.addWidget(end_location_label)

        self.end_location_input = QLineEdit()
        self.end_location_input.setMaximumWidth(300)
        set_lineEdit_style(self.end_location_input)
        end_location_layout.addWidget(self.end_location_input)

        end_location_unit = QLabel(length_unit)
        setLabelStyle(end_location_unit)
        end_location_layout.addWidget(end_location_unit)

        #end magnitude
        end_magnitude_layout = QHBoxLayout()

        end_mag_label = QLabel("END Magnitude:          ")
        setLabelStyle(end_mag_label)
        end_magnitude_layout.addWidget(end_mag_label)

        self.end_mag_input = QLineEdit()
        self.end_mag_input.setMaximumWidth(300)
        set_lineEdit_style(self.end_mag_input)
        end_magnitude_layout.addWidget(self.end_mag_input)

        end_mag_unit = QLabel(distr_magnitude_unit)
        setLabelStyle(end_mag_unit)
        end_magnitude_layout.addWidget(end_mag_unit)


        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        #main layout 
        main_layout = QVBoxLayout()
        main_layout.addLayout(start_location_layout)
        main_layout.addLayout(start_mag_layout)
        main_layout.addLayout(end_location_layout)
        main_layout.addLayout(end_magnitude_layout)
        main_layout.addWidget(buttons)
        self.setLayout(main_layout)

    def accept(self):
        #user input 
        start_location_text = self.start_location_input.text()
        end_location_text = self.end_location_input.text()
        w0_text = self.start_mag_input.text()
        wL_text = self.end_mag_input.text()

        if not all([start_location_text, end_location_text, w0_text, wL_text]):
            QMessageBox.critical(self, "Input Error", "All fields are required.")
            return

        try:
            start_location = float(start_location_text)
            end_location = float(end_location_text)
            w0 = float(w0_text)
            wL = float(wL_text)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "All inputs must be numbers.")
            return

        if not (0 <= start_location <= self.beam_model.length and 0 <= end_location <= self.beam_model.length):
            QMessageBox.critical(self, "Input Error", f"Locations must be between 0 and {self.beam_model.length}.")
            return

        if start_location >= end_location:
            QMessageBox.critical(self, "Input Error", "Start location must be less than end location.")
            return

        node_positions = self.beam_model.get_node_positions()

        #insert nodes 
        start_node_idx = self.beam_model.insert_node_at_position(start_location)
        end_node_idx = self.beam_model.insert_node_at_position(end_location)

        #find elements between start_node_idx and end_node_idx (left to right)
        for elem in self.beam_model.elements:
            n_start = elem.node_start.index
            n_end = elem.node_end.index

            if n_start >= start_node_idx and n_end <= end_node_idx:
                # Calculate the physical positions of the element's start and end nodes
                x_elem_start = node_positions[n_start]
                x_elem_end = node_positions[n_end]

                # Interpolate w0 and wL for the current element
                w0_elem = interpolate_w(x_elem_start, start_location, end_location, w0, wL)
                wL_elem = interpolate_w(x_elem_end, start_location, end_location, w0, wL)

                self.beam_model.add_distributed_load(elem.index, w0_elem, wL_elem)

        super().accept()

def interpolate_w(x, x0, x1, w0, w1):
    """Linearly interpolate load value at position x between x0 and x1."""
    return w0 + (w1 - w0) * (x - x0) / (x1 - x0)