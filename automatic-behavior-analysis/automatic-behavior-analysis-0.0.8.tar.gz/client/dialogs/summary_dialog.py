import csv
import json
import tkinter
from tkinter import messagebox, ttk, filedialog
from util.numpy_encoder import NumpyEncoder

class SummaryDialog(object):
    def __init__(self, summary, output_filename_base):
        self.summary = summary
        self.output_filename_base = output_filename_base
        root = self.root = tkinter.Tk()
        root.title('Summary')
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        # main frame
        main_frame = tkinter.Frame(root)
        # main_frame.pack(ipadx=2, ipady=2, padx=2, pady=8, fill='both', expand=True)
        main_frame.grid(ipadx=2, ipady=2, padx=2, pady=8, sticky='wsne')
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # tree view
        def insert_item(tree, item, key, parent_key):
            if item.get('hidden'): return
            value = item['value']
            tree_key = parent_key + '/' + key
            tree_values = ('', '', tree_key, parent_key)
            # print("Inserting item: tree key: {}, parent_key: {}, key: {}, value: {}".format(repr(tree_key), repr(parent_key), repr(key), repr(value)))

            if type(value) is dict:
                add_dict_items(tree, value, tree_key)
            elif type(value) is list:
                add_list_items(tree, value, tree_key)
            else:
                ratio = item.get('ratio')
                percent = '' if ratio is None else '{:.3g}'.format(ratio * 100)
                unit = item.get('unit')
                if unit: value = "{:.3g} {}".format(value, unit)
                tree_values = (value, percent, tree_key, parent_key)
                tree.insert('', 'end', tree_key, text=item['label'], values=tree_values)

        def add_dict_items(tree, container, parent_key=''):
                for key, item in container.items():
                    insert_item(tree, item, key, parent_key)

        def add_list_items(tree, container, parent_key=''):
            for index, item in enumerate(container):
                    insert_item(tree, item, str(index), parent_key)

        tree = ttk.Treeview(main_frame)
        # tree['columns'] = ('value', 'percent', key', 'parent_key')
        tree['columns'] = ('value', 'percent')
        tree.heading("#0", text="Parameter")
        tree.column("#0", width=300, stretch=True)
        tree.heading('value', text="Value")
        tree.column('value', width=100)
        tree.heading('percent', text="%")
        tree.column('percent', width=100)
        # tree.heading('key', text="Key")
        # tree.column('key', width=200)
        # tree.heading('parent_key', text="Parent key")
        # tree.column('parent_key', width=200)
        add_dict_items(tree, summary)
        tree.grid(row=0, column=0, padx=4, pady=(4, 0), sticky='wnse')

        # button frame
        button_frame = tkinter.Frame(main_frame)
        button_frame.grid(row=1, column=0, padx=4, pady=(4, 0), sticky='wse')

        # buttons
        def add_button(text, command):
            button = tkinter.Button(button_frame, width=8, text=text, command=command)
            button.bind('<KeyPress-Return>', func=command) # trigger action when user presses enter
            button.pack(side='left')

        add_button("Done", self.clicked_ok)
        add_button("Export JSON", self.export_json)
        add_button("Export CSV", self.export_csv)

        # close dialog if user pressed escape
        root.bind('<KeyPress-Escape>', func=self.clicked_ok)

        # roughly center the box on screen
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        xp = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        yp = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        geom = (root.winfo_width(), root.winfo_height(), xp, yp)
        root.geometry('{0}x{1}+{2}+{3}'.format(*geom))
        # call self.close_mod when the close button is pressed
        root.protocol("WM_DELETE_WINDOW", self.clicked_ok)
        # a trick to activate the window (on windows 7)
        root.deiconify()

    def clicked_ok(self, event=None):
        self.root.quit()

    def export_json(self, event=None):
        f = filedialog.asksaveasfile(
            mode='w',
            filetypes=(("JSON file", ".json"), ("All files", "*.*")),
            initialfile=self.output_filename_base + "-summary.json")
        if not f: return
        try:
            output = json.dumps(self.summary, cls=NumpyEncoder, indent=2)
            # print(output)
            f.write(output)
        finally:
            f.close()

    def export_csv(self, event=None):
        def double_get(item, key1, key2, default_value=None):
            child = item.get(key1)
            return child.get(key2, default_value) if child else default_value

        def transpose(summary, result):
            dog_statistics = double_get(summary, 'dog_statistics', 'value')
            if not dog_statistics: return result
            for item in dog_statistics:
                item = item.get('value')
                if not item: continue
                result.append({
                    'name': double_get(item, 'dog_name', 'value', ''),
                    'present': double_get(item, 'num_frames_with_dog', 'value', 0),
                    'present_ratio': double_get(item, 'num_frames_with_dog', 'ratio', 0),
                    'asleep': double_get(item, 'num_frames_with_dog_asleep', 'value', 0),
                    'asleep_ratio': double_get(item, 'num_frames_with_dog_asleep', 'ratio', 0),
                    'asleep_unit': double_get(item, 'num_frames_with_dog_asleep', 'unit', 0),
                    'total': double_get(summary, 'num_frames_total', 'value', 0)
                })
            return result

        f = filedialog.asksaveasfile(
            mode='w',
            filetypes=(("CSV file", ".csv"), ("All files", "*.*")),
            initialfile=self.output_filename_base + "-summary.csv")
        if not f: return
        try:
            name = f.name
            f.close()
            f = open(name, mode='w', newline='')
            fieldnames = ['name', 'present', 'present_ratio', 'asleep', 'asleep_ratio', 'asleep_unit', 'total']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in transpose(self.summary, []):
                print("row: {}".format(item))
                writer.writerow(item)
        finally:
            f.close()

    @staticmethod
    def show(summary, output_filename_base):
        """Create an instance of a SummaryDialog, and display formatted data to user.
        summary = data to display
        """
        dialog = SummaryDialog(summary, output_filename_base)
        dialog.root.mainloop()
        dialog.root.destroy()