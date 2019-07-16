"""
@package SDF.GUI.view.image_preview_widget

QWidget to display an image.
------------------------------------------------------------------------------
    Copyright (C) 2016-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

    
class PlotPreviewWidget(QWidget):
    """
    Widget featuring a matplotlib figure (and axis), 
    to display the image contained in sdf_data_img objects.
    """
    def __init__(self, parent):
        """
        Constructor.
        @param parent (Pointer to) Parent widget.
        """
        super(PlotPreviewWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Initializes all widgets (buttons, labels, etc.) displayed
        on this widget.
        """
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        figure = plt.figure()
        self.canvas = FigureCanvas(figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        toolbar = NavigationToolbar(self.canvas, self)
        vbox.addWidget(toolbar)
        vbox.addWidget(self.canvas)
        self.ax = figure.add_subplot(1, 1, 1)
        figure.subplots_adjust(
            top=0.96, bottom=0.08,
            left=0.08, right=0.96)
