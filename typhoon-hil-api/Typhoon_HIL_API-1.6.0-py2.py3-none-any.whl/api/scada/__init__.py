# -*- coding: utf-8
#
# SCADA API
#
#
# This file is a part of Typhoon HIL API library.
#
# Typhoon HIL API is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function, unicode_literals

import os

from typhoon.api.scada.stub import clstub

__all__ = ["panel"]


class ScadaAPI(object):
    """
    SCADA API (Application Programming Interface) allows interfacing to the
    underlying HIL SCADA model.
    """

    def __init__(self):
        super(ScadaAPI, self).__init__()

    def load_panel(self, panel_file):
        """
        Load the provided HIL SCADA Panel (.cus) file.

        Args:
            panel_file (str): full path to the HIL SCADA Panel (.cus) file

        Returns:
            None

        Raises:
            ScadaAPIException: In case `panel_file` argument is invalid.
            ScadaAPIException: In case provided Panel file cannot be opened.

        **Example:**

        .. literalinclude:: scada_api_examples/load.example
           :language: python
           :lines: 2-
        """

        return clstub().load_panel(panel_file=os.path.abspath(panel_file))

    def save_panel(self):
        """
        Save currently opened Panel to the same Panel file.

        Returns:
            None

        Raises:
            ScadaAPIException: In case the Panel file is not opened.
            ScadaAPIException: In case the opened Panel cannot be saved.

        **Example:**

        .. literalinclude:: scada_api_examples/save.example
           :language: python
           :lines: 2-
        """
        return clstub().save_panel()

    def save_panel_as(self, save_to):
        """
        Save the currently opened Panel to a new Panel file.

        Args:
            save_to (str): full path where opened Panel need to be saved

        Returns:
            None

        Raises:
            ScadaAPIException: In case the Panel file is not opened.
            ScadaAPIException: In case `save_to` argument is invalid.
            ScadaAPIException: In case the opened Panel cannot be saved.

        **Example:**

        .. literalinclude:: scada_api_examples/save_as.example
           :language: python
           :lines: 2-
        """
        return clstub().save_panel_as(save_to=os.path.abspath(save_to))

    def set_property_value(self, widget_handle, prop_name, prop_value):
        """
        Set a new value for the widget property.

        Args:
            widget_handle (WidgetHandle): The widget handle used as a widget identifier.
            prop_name (str): The name of property that you want to change.
                The list of all property names can be found in the
                ``typhoon.api.scada.const`` module or listed in the section
                `SCADA API constants`_


                .. note::
                    Not all widget properties can be changed by SCADA API.
                    For detailed information witch properties can be changed
                    for a specific widget, please consult
                    :doc:`Available Widget Properties </widget_prop>` section.

            prop_value (object): A new property value that need to be set.

                .. note::
                    Type of value that need to be set depends of which property is
                    being changed. More details can be found in the
                    :doc:`Available Widget Properties </widget_prop>` section.

        Returns:
            None

        Raises:
            ScadaAPIException: In case the Panel file is not opened.
            ScadaAPIException: In case any of ``widget_handle``, ``prop_name`` or
                ``prop_value`` arguments are invalid.
            ScadaAPIException: In case the widget identified by ``widget_handle`` cannot
                be found in opened Panel.
            ScadaAPIException: In case widget doesn't have property with
                given ``prop_name``.

        **Example:**

        .. literalinclude:: scada_api_examples/change_prop.example
           :language: python
           :lines: 2-
        """
        return clstub().set_property_value(widget_handle=widget_handle,
                                           prop_name=prop_name,
                                           prop_value=prop_value)

    def get_property_value(self, widget_handle, prop_name):
        """
        Returns the value of a given property for the given widget handle.

        Args:
            widget_handle (WidgetHandle): The widget handle used as a widget identifier.
            prop_name (str): The name of a property.
                The list of all property names can be found in ``typhoon.api.scada.const``
                module or listed in the section `SCADA API constants`_


                .. note::
                    Not all widget properties can be changed by SCADA API.
                    For detailed information witch properties can be changed
                    for a specific widget, please consult
                    :doc:`Available Widget Properties </widget_prop>` section.

        Returns:
            property value (object): value can be arbitrary type
                depending of the type of widget and property. More details can be found in
                the :doc:`Available Widget Properties </widget_prop>` section.
        Raises:
            ScadaAPIException: In case ``widget_handle`` and ``prop_name`` arguments
                are invalid
            ScadaAPIException: In case the widget does not have the property with given
                the ``prop_name``
            ScadaAPIException: In case the Panel is not specified
            ScadaAPIException: In case the widget identified by the ``widget_handle``
                cannot be found in the opened Panel.

        **Example:**

        .. literalinclude:: scada_api_examples/get_prop.example
           :language: python
           :lines: 2-
        """

        return clstub().get_property_value(widget_handle=widget_handle,
                                           prop_name=prop_name)

    def get_widget_by_id(self, widget_id):
        """
        Returns the widget handle for the widget with a given widget ID.

        Args:
            widget_id (str): Widget ID

        Returns:
            handle to widget (WidgetHandle): A handle to the widget with the given
                ``widget_id`` that can be used as a widget identifier.

        Raises:
            ScadaAPIException: In case the Panel file is not opened.
            ScadaAPIException: In case the ``widget_id`` argument is invalid.
            ScadaAPIException: In case the widget with the given id cannot be found in
                the loaded Panel.

        **Example:**

        .. literalinclude:: scada_api_examples/get_widget.example
           :language: python
           :lines: 2-
        """

        return clstub().get_widget_by_id(widget_id=widget_id)


panel = ScadaAPI()
