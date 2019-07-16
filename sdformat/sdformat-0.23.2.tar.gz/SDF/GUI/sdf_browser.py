#! python

"""
SDF file browser.
------------------------------------------------------------------------------
    Copyright (C) 2017-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from SDF.GUI.controller.browser_controller import BrowserController, HOME


def main():
    app = QApplication([])
    app.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)
    sdf_obj = None
    if sys.argv.count("--debug"):
        import logging
        logging.basicConfig(level=logging.DEBUG)                        
    gui = BrowserController(sdf_obj)
    gui.show()
    if not os.path.isdir(HOME + '/.sdf'):
        os.makedirs(HOME + '/.sdf')
    sys.exit(app.exec_())

    
if __name__ == "__main__":
    main()
