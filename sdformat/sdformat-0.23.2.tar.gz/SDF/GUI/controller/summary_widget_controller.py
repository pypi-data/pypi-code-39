"""
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
from ..view.summary_widget import SummaryWidget
from ..view import sdf_parameters_browser
from ..view.styles import style_sheet
from ...sdf_par import sdf_par


class SummaryWidgetController(SummaryWidget):

    def __init__(self):
        SummaryWidget.__init__(self)
    
    def display_sdf_object(self, sdf_obj):
        """
        Updates all labels and texts to show information on the given sdf_object.
        @param sdf_obj (Pointer to) sdf_object .
        """
        self.sdf_obj = sdf_obj
        self.sdf_name.setText(str(sdf_obj.name.value))

        ## get number of parameters:        
        n_par, n_blocks, n_par_in_blocks = self.get_number_of_parameters(sdf_obj.par)

        param_str = "<b>%i</b> parameters, " % n_par
        param_str += "<b>%i</b> parameter-blocks, " % n_blocks
        param_str += "<b>%i</b> parameters in total" % n_par_in_blocks
        self.sdf_parameters.setText(param_str)

        instr_str = "<b>%i</b> instruments" % len(sdf_obj.instrument)
        self.sdf_instruments.setText(instr_str)

        samples_str = "<b>%i</b> samples" % len(sdf_obj.sample)
        self.sdf_samples.setText(samples_str)

        self.sample_clickable = (len(sdf_obj.sample) > 0)
        self.instrument_clickable = (len(sdf_obj.instrument) > 0)
        self.parameters_clickable = (n_par > 0 or n_blocks > 0)
                
    def get_number_of_parameters(self, par):
        """
        Method to return the number of parameters in given list of parameters.
        Number of parameters are returned separated in number of top-level
        parameters, blocks, and parameters in blocks and lower levels.
        @param par List of sdf_par instances.
        @return Tuple with 3 items: 
          (1) Number of top-level parameters,
          (2) number of parameter blocks,
          (3) number of parameters in blocks.
        """
        n_par = 0
        n_blocks = 0 
        n_par_in_blocks = 0
        for p in par:
            if type(p.value) == list:
                n_blocks += 1
                _n = self.get_number_of_parameters(p.value)
                n_par_in_blocks = n_par_in_blocks + _n[0] + _n[2]
            else:                
                n_par += 1
        return n_par, n_blocks, n_par_in_blocks

    def _popup_parameter_widget(self):
        """
        Pops up a widget displaying details on the object's parameters.
        """
        if self.parameters_clickable:
            popup_par = sdf_parameters_browser.SDFParameterPopup(
                self, self.sdf_obj.name.value, self.sdf_obj.par)
            popup_par.setStyleSheet(style_sheet)
            popup_par.show()
            
            self.par_popups.append(popup_par)

    def _popup_instrument_widget(self):
        """
        NOT IMPLEMENTED YET.
        Pops up a widget displaying details on the object's instruments.
        """
        if self.instrument_clickable:
            copy_of_instrument_as_par = sdf_par('instrument-copy',
                                                self.sdf_obj.instrument[0].par)
            popup_instr = sdf_parameters_browser.SDFParameterPopup(
                self, self.sdf_obj.name.value, [copy_of_instrument_as_par])
            popup_instr.setStyleSheet(style_sheet)
            popup_instr.show()
            self.par_popups.append(popup_instr)

    def _popup_sample_widget(self):
        """
        NOT IMPLEMENTED YET.
        Pops up a widget displaying details on the object's samples.
        """
        if self.sample_clickable:
            pass
