from PyQt6.QtWidgets import ( QWidget, QComboBox, QHBoxLayout, QVBoxLayout, QLabel)

class OhmPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI



    def setupUI(self):
        #layout
        ohm_layout = QVBoxLayout()
        self.setLayout(ohm_layout)
        ohm_layout.setContentsMargins(20, 10, 20, 20)
        ohm_layout.setSpacing(10)

        ohmlabel = QLabel("Ohms Law page")
        ohm_layout.addWidget(ohmlabel)