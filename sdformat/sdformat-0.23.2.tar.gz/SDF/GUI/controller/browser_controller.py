"""
Browser controller.
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
import pickle
import os
from PyQt5.QtWidgets import QFileDialog, QApplication
from ..view.browser import SDFBrowser
from ...file_io import sdf_load
HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")


class BrowserController(SDFBrowser):

    def __init__(self, sdf_obj=None):
        SDFBrowser.__init__(self, sdf_obj)

    def do_open(self):
        """
        Open an sdf file. Parse sdf file to model.
        """
        fname, _ = QFileDialog.getOpenFileName(self, 'read sdf file',
                                               self.values['files']['last_opened'], '*.sdf')
        if not fname:
            return
        sdf_obj = sdf_load.sdf_load(fname)
        self.model.parse_sdf_obj(sdf_obj)
        self.values['files']['last_opened'] = fname

    def set_value(self, key, value):
        """
        Set value in the widget's parameter dictionary.
        """
        self.values[key] = value

    def closeEvent(self, event):
        """
        On closing the window, saves parameters stored in the
        widget's parameter dictionary (SDFBrowser.values).
        """
        geometry = self.frameGeometry()
        geometry_as_list = [geometry.x(), geometry.y(), geometry.width(), geometry.height()]
        self.values['display']['geometry'] = geometry_as_list
        with open(HOME + '/.sdf/browserdefaults.pkl', 'wb') as f:
            pickle.dump(self.values, f, pickle.HIGHEST_PROTOCOL)                
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication([])
    sdf_obj = None
    if len(sys.argv) > 1:
        sdf_obj = sdf_load.sdf_load(sys.argv[1])
    gui = BrowserController(sdf_obj)
    gui.show()

    if not os.path.isdir(HOME + '/.sdf'):
        os.makedirs(HOME + '/.sdf')
    sys.exit(app.exec_())
