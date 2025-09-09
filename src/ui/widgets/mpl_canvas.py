from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

class MplCanvas(FigureCanvasQTAgg):
    """reusable Matplotlib canvas"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

        self.annot = self.axes.annotate("", xy=(0,0), xytext=(-20,20),
                                        textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="w"),
                                        arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def on_motion(self, event):
        if event.inaxes != self.axes:
            return

        visible = self.annot.get_visible()
        
        for line in self.axes.get_lines():
            cont, ind = line.contains(event)
            if cont:
                x, y = self.get_closest_point(line, event.xdata)
                self.annot.xy = (x, y)
                text = f"({x:.2f}, {y:.2f})"
                self.annot.set_text(text)
                self.annot.get_bbox_patch().set_alpha(0.4)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
                return

        if visible:
            self.annot.set_visible(False)
            self.fig.canvas.draw_idle()

    def get_closest_point(self, line, xdata):
        x, y = line.get_data()
        index = np.searchsorted(x, xdata)
        
        if index == 0:
            return x[0], y[0]
        if index == len(x):
            return x[-1], y[-1]

        x_left, x_right = x[index-1], x[index]
        y_left, y_right = y[index-1], y[index]

        if (xdata - x_left) < (x_right - xdata):
            return x_left, y_left
        else:
            return x_right, y_right