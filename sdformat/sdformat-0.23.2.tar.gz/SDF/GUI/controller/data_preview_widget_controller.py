"""
Controller for preview widget.
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
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from ..view.data_preview_widget import DataPreviewWidget


class DataPreviewWidgetController(DataPreviewWidget):
    def __init__(self):
        DataPreviewWidget.__init__(self)

    def display_sdf_object(self, obj):
        """
        Function to update shwon information to match given sdf_object.
        @param obj (Pointer to) sdf_object.
        """
        self.sdf_obj = obj
        if not self.show_preview:
            return
        if not obj.IsDataset():
            plt.cla()
            self.preview_widget.canvas.draw()
            return
        if obj.value.ID == 'sdf-data-img':
            self.preview_widget.plot_image(
                obj.value.GetImgAsArray(), [], {'cmap': 'gray'})
        elif obj.value.ID in ['sdf-data-sc', 'sdf-data-mc']:            
            self.preview_widget.plot_lines(obj.value.data, None, True, [], [])
        else:                
            plt.cla()
            self.preview_widget.canvas.draw()                

    def toggle_show_preview(self, state):
        if state == Qt.Checked:
            self.show_preview = True
            if self.sdf_obj is None:
                return
            self.display_sdf_object(self.sdf_obj)
        else:
            self.show_preview = False
            self.preview_widget.ax.clear()
            self.preview_widget.canvas.draw()
