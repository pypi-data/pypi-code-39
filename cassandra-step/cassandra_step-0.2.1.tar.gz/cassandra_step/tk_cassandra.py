# -*- coding: utf-8 -*-

"""The graphical part of a Cassandra step"""

import seamm
from seamm_util import ureg, Q_, units_class  # noqa: F401
import seamm_widgets as sw  # noqa: F401
import Pmw
import pprint  # noqa: F401
import tkinter as tk
import tkinter.ttk as ttk


class TkCassandra(seamm.TkNode):
    """The graphical part of a Cassandra step in a MolSSI flowchart.

    """

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=None,
        y=None,
        w=None,
        h=None
    ):
        '''Initialize a node

        Keyword arguments:
        '''
        self.dialog = None

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=None,
            y=None,
            w=200,
            h=50
        )

    def create_dialog(self):
        """Create the dialog!"""
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            master=self.toplevel,
            title='Edit Energy step',
            command=self.handle_dialog
        )
        self.dialog.withdraw()
        P = self.node.parameters

        # The tabbed notebook
        notebook = ttk.Notebook(self.dialog.interior())
        notebook.pack(side='top', fill=tk.BOTH, expand=1)
        self._widget['notebook'] = notebook

        # # Main frame holding the widgets
        self["general"] = ttk.Frame(notebook)
        notebook.add(self["general"], text='General information', sticky=tk.NW)
        self["thermo_state"] = ttk.Frame(notebook)
        notebook.add(
            self["thermo_state"], text='Thermodynamic state', sticky=tk.NW
        )
        self["initial_config"] = ttk.Frame(notebook)
        notebook.add(
            self["initial_config"], text='Initial configuration', sticky=tk.NW
        )
        self["energy_calc"] = ttk.Frame(notebook)
        notebook.add(
            self["energy_calc"], text='Energy calculation', sticky=tk.NW
        )
        self["probability"] = ttk.Frame(notebook)
        notebook.add(self["probability"], text='Probabilities', sticky=tk.NW)
        self["outputs"] = ttk.Frame(notebook)
        notebook.add(self["outputs"], text='Outputs', sticky=tk.NW)
        self["other"] = ttk.Frame(notebook)
        notebook.add(self["other"], text='Other', sticky=tk.NW)

        row = 0
        for k, v in P.items():
            # print(v['group'], k)
            self[k] = P[k].widget(self[v["group"]])
            self[k].grid(row=row, column=0, sticky=tk.W)
            row += 1

            # sw.align_labels(
            #     (self[k])
            # )

        # bindings...

    def reset_dialog(self, widget=None):
        """Layout the widgets in the dialog

        This initial function simply lays them out row by rows with
        aligned labels. You may wish a more complicated layout that
        is controlled by values of some of the control parameters.
        """

        # Remove any widgets previously packed
        # frame = self['frame']
        # for slave in frame.grid_slaves():
        #     slave.grid_forget()

        # # Shortcut for parameters
        # P = self.node.parameters

        # # keep track of the row in a variable, so that the layout is flexible
        # # if e.g. rows are skipped to control such as 'method' here
        # row = 0
        # widgets = []
        # for key in P:
        #     self[key].grid(row=row, column=0, sticky=tk.EW)
        #     widgets.append(self[key])
        #     row += 1

        # # Align the labels
        # sw.align_labels(widgets)
        pass

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Cassandra input
        """
        if self.dialog is None:
            self.create_dialog()

        self.dialog.activate(geometry='centerscreenfirst')

    def handle_dialog(self, result):
        """Handle the closing of the edit dialog

        What to do depends on the button used to close the dialog. If
        the user closes it by clicking the 'x' of the dialog window,
        None is returned, which we take as equivalent to cancel.
        """
        if result is None or result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result)
            )

        self.dialog.deactivate(result)
        # Shortcut for parameters
        P = self.node.parameters

        # Get the values for all the widgets. This may be overkill, but
        # it is easy! You can sort out what it all means later, or
        # be a bit more selective.
        for key in P:
            P[key].set_from_widget()

    def handle_help(self):
        """Not implemented yet ... you'll need to fill this out!"""
        print('Help not implemented yet for Cassandra!')
