from PyQt6.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar 
from src.ui.widgets.mpl_canvas import MplCanvas
from src.core.calculations.unit_factors import beam_dropdown_units

class ResultsDialog(QDialog):
    def __init__(self, results_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Beam Analysis Results")
        self.setMinimumSize(800, 600)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot(results_data)
    def plot(self, data):
        self.canvas.fig.clear()
        units = beam_dropdown_units[data['unit_system']]
        len_unit = list(units['Length'].values())[0]
        force_unit = list(units['PointLoad'].values())[0]
        moment_unit = list(units['MomentLoad'].values())[0]

        ax1 = self.canvas.fig.add_subplot(221)
        ax2 = self.canvas.fig.add_subplot(222)
        ax3 = self.canvas.fig.add_subplot(223)
        ax4 = self.canvas.fig.add_subplot(224)

        x = data['node_positions']
        ax1.plot(x, data['displacements'], 'r-')
        ax1.set_title("Deflection")
        ax1.set_ylabel(f"Deflection [{len_unit}]")
        ax1.grid(True)

        ax2.plot(x, data['slopes'], 'b-')
        ax2.set_title("Slope")
        ax2.set_ylabel("Slope [rad]")
        ax2.grid(True)

        ax3.plot(x, data['shear_forces'], 'g-')
        ax3.set_title("Shear Force")
        ax3.set_ylabel(f"Shear [{force_unit}]")
        ax3.set_xlabel(f"Position [{len_unit}]")
        ax3.grid(True)

        ax4.plot(x, data['bending_moments'], 'm-')
        ax4.set_title("Bending Moment")
        ax4.set_ylabel(f"Moment [{moment_unit}]")
        ax4.set_xlabel(f"Position [{len_unit}]")
        ax4.grid(True)

        self.canvas.fig.tight_layout()
        self.canvas.draw()