# python-qsettingswidget
# Copyright (C) 2019  LoveIsGrief
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QCheckBox
from qsettingswidget.converters.converter import Signals, Converter
from qsettingswidget.converters.simple_converter import Info


class QCheckBoxConverter(Converter):
    @classmethod
    def can_convert(cls, widget):
        return isinstance(widget, QCheckBox)

    @classmethod
    def get(cls, widget):
        return widget.checkState()

    @classmethod
    def set(cls, widget, value):
        return widget.setCheckState(int(value))

    @classmethod
    def signal(cls, widget, signal_enum):
        return widget.stateChanged

