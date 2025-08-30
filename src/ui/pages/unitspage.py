from PyQt6.QtWidgets import ( QWidget, QVBoxLayout, 
                             QHBoxLayout, QComboBox, QLabel, 
                             QFrame, QPushButton, QLineEdit)
from PyQt6.QtGui import QDoubleValidator

from src.ui.style.pagestyling import set_dropdown_style, set_lineEdit_style
from src.core.calculations.unit_factors import (length_factors, area_factors, mass_factors,
                                stress_factors, energy_factors, time_factors,
                                unit_types_abrv)


class UnitSolverPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.length_factors = length_factors
        self.area_factors = area_factors
        self.mass_factors = mass_factors
        self.stress_factors = stress_factors
        self.energy_factors = energy_factors
        self.time_factors = time_factors

        #connect unit conversion signals
        self.input_unit_box.textChanged.connect(self.perform_conversion)
        self.input_dropdown.currentTextChanged.connect(self.perform_conversion)
        self.result_dropdown.currentTextChanged.connect(self.perform_conversion)

        #connect label updating
        self.input_dropdown.currentTextChanged.connect(self.update_unit_labels)
        self.result_dropdown.currentTextChanged.connect(self.update_unit_labels)
        self.unit_classes.currentTextChanged.connect(self.update_unit_labels)

        self.update_unit_labels()




    def setupUI(self):

        #layout
        unit_layout = QVBoxLayout()
        self.setLayout(unit_layout)
        unit_layout.setContentsMargins(20, 10, 20, 20)
        unit_layout.setSpacing(10)

    
        #unit class dropdown
        self.unit_classes = QComboBox()
        self.unit_classes.setObjectName("unitclasses")
        self.unit_classes.setFixedSize(250, 60)

        set_dropdown_style(self.unit_classes)


        #converter layout 
        converterlayout = QHBoxLayout()


        #input layout
        input_layout = QVBoxLayout()
        input_box_Hlayout = QHBoxLayout()

        self.input_unit_box = QLineEdit()
        self.input_unit_box.setPlaceholderText("0")
        self.input_unit_box.setFocus()
        self.input_unit_box.setObjectName("inputLineEdit")
        set_lineEdit_style(self.input_unit_box)

        self.input_label = QLabel("from:")
        self.input_label.setStyleSheet("font-weight: bold")

        
        input_box_Hlayout.addWidget(self.input_unit_box)
        input_box_Hlayout.addWidget(self.input_label)


        #input dropbox
        self.input_dropdown = QComboBox()
        set_dropdown_style(self.input_dropdown)


        #result layout
        result_layout = QVBoxLayout()

        result_box_Hlayout = QHBoxLayout()

        self.result_unit_box = QLineEdit()
        self.result_unit_box.setPlaceholderText("0")
        self.result_unit_box.setFocus()
        self.result_unit_box.setReadOnly(True)
        set_lineEdit_style(self.result_unit_box)

        self.result_label = QLabel("to:")
        self.result_label.setStyleSheet("font-weight: bold")



        result_box_Hlayout.addWidget(self.result_unit_box)
        result_box_Hlayout.addWidget(self.result_label)



        #result  dropbox
        self.result_dropdown = QComboBox()
        set_dropdown_style(self.result_dropdown)

        #make line edits only take numbers
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setDecimals(10)

        self.input_unit_box.setValidator(validator)
        self.result_unit_box.setValidator(validator)

        #add 
        input_layout.addLayout(input_box_Hlayout)
        input_layout.addWidget(self.input_dropdown)

        
        result_layout.addLayout(result_box_Hlayout)
        result_layout.addWidget(self.result_dropdown)


        

        self.input_dropdown.setMaximumWidth(700)
        self.input_dropdown.setMinimumWidth(300)

        self.result_dropdown.setMaximumWidth(700)
        self.result_dropdown.setMinimumWidth(300)

        #add input and result to converter layout
        converterlayout.addLayout(input_layout)
        converterlayout.addStretch()
        converterlayout.addLayout(result_layout)

        #add
        unit_layout.addWidget(self.unit_classes)
        unit_layout.addStretch()
        unit_layout.addLayout(converterlayout)
        unit_layout.addStretch()

        self.units = {"Length": ['nanometers','millimeters', 'centimeters', 'meters', 'kilometers', 'inches', 'feet', 'yards','miles' ],
                      "Area": ['millimeters²','centimeters²', 'meters²', "kilometers²", 'inches²', 'feet²', 'miles²', 'Acres' ],
                       "Mass / Weight": ['milligrams', 'centigrams', 'grams', 'kilograms', "metric tonnes",'newtons', 'kilonewtons', 'ounces', 'pounds', 'kip', 'US Tons'],
                       "Temperature": ['celsius', 'fahrenheit', 'kelvin', 'rankine'],
                       "Pressure / Stress": ['atmospheres', 'bars', 'pascals', 'kilopascals', 'megapascals', 'pounds/inches²','kips/inches²', 'torr' ], 
                       "Energy" : [ 'joules', 'kilojoules', 'foot-pound', 'british thermal unit', 'calories', 'kilowatt-hours'],
                       "Time": ['milliseconds','seconds', 'minutes', 'hours', 'days', 'weeks'],
                       "Moment of Inertia (I)": ['millimeters⁴', 'meters⁴', 'inches⁴', 'feet⁴']
                       }
        
        #populate unit class dropdown
        self.unit_classes.addItems(list(self.units.keys()))

        #connect signal to update bottom lists
        self.unit_classes.currentTextChanged.connect(self.update_unit_dropdowns)

        firstclass = self.unit_classes.currentText()
        self.update_unit_dropdowns(firstclass)






    def update_unit_dropdowns(self, category):
        """Update the second dropdown based on the selected category"""
        # Clear the current items
        self.input_dropdown.clear()
        self.result_dropdown.clear()
        
        # Add new items based on selected category
        if category in self.units:
            self.input_dropdown.addItems(self.units[category])
            self.result_dropdown.addItems(self.units[category])
        
        self.input_unit_box.clear()
        self.result_unit_box.clear()




    def perform_conversion(self):
        try:
            value = float(self.input_unit_box.text())
        except ValueError:
            self.result_unit_box.setText("")
            return
        category = self.unit_classes.currentText()
        input_unit = self.input_dropdown.currentText()
        result_unit = self.result_dropdown.currentText()

        
        if category == "Length": factors = self.length_factors
        elif category == "Area": factors = self.area_factors
        elif category == "Mass / Weight": factors = self.mass_factors
        elif category == "Pressure / Stress": factors = self.stress_factors
        elif category == "Energy": factors = self.energy_factors
        elif category == "Time": factors = self.time_factors
        elif category == "Temperature": 
            result_value = self.convert_temp(value, input_unit, result_unit)
            if result_value is None:
                self.result_unit_box.setText("N/A")
            else:
                self.result_unit_box.setText(f"{result_value:,.3f}")
            return

        else:
            self.result_unit_box.setText("N/A")

        if input_unit not in factors or result_unit not in factors:
            self.result_unit_box.setText("N/A")
            return
        
        #convert and put into result
        base_value = value * factors[input_unit]
        result_value = base_value / factors[result_unit]
        self.result_unit_box.setText(f"{result_value:,.8g}")



    def convert_temp(self, value, from_unit, to_unit):
        #convert to celsius 
        if from_unit == "celsius":
            c = value
        elif from_unit == "fahrenheit":
            c = (value - 32) * 5/9
        elif from_unit == "kelvin":
            c = value - 273.15
        elif from_unit == "rankine":
            c = (value - 491.67) * 5/9
        else:
            return None
        #convert from celsius to target
        if to_unit == "celsius":
            return c
        elif to_unit == "fahrenheit":
            return c * 9/5 + 32
        elif to_unit == "kelvin":
            return c + 273.15
        elif to_unit == "rankine":
            return (c + 273.15) * 9/5
        else:
            return None
        
    def get_abbrev(self, category, unit):
        #iterate through each layer of the dict
        for system in ['English', 'Metric/SI']:
            cat_dict = unit_types_abrv.get(system,{}).get(category,{})
            abbr = cat_dict.get(unit)
            if abbr:
                return abbr
        return unit
        
    def update_unit_labels(self):
        category = self.unit_classes.currentText()
        input_unit = self.input_dropdown.currentText()
        result_unit = self.result_dropdown.currentText()
        self.input_label.setText(f"{self.get_abbrev(category, input_unit)}")
        self.result_label.setText(f"{self.get_abbrev(category, result_unit)}")