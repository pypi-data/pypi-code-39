"""Generate a Tk from upon a Gui schema.

A GUI schema is a JSON-Schema dictionnary,
with tags require and existifs added to declare explicit cyclic depenencies
"""

from tkinter import filedialog as Tk_filedlg
from tkinter import Variable as Tk_Variable
from tkinter import Canvas as Tk_Canvas
from tkinter import  Label as Tk_Label
from tkinter import Menu as Tk_Menu
# from tkinter import Button as Tk_Button
from tkinter import ttk
from tkinter import Tk
from glob import glob
import inspect
import json
import os
from PIL import ImageTk, Image


BG_COLOR = '#%02x%02x%02x' % (227, 225, 221)
WIDTH_UNIT = 300
LINE_HEIGHT = 22
BASE_DIR = inspect.getfile(inspect.currentframe())
BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))


def _load_icons():
    icons_dir = os.path.join(BASE_DIR,'otinker_images')
    icons_pattern = '_icon.gif'
    icons_files = glob('%s/*%s'%(icons_dir, icons_pattern))
    icons = dict()
    for k in icons_files:
        key = os.path.basename(k).replace(icons_pattern, '')
        icons[key] = ImageTk.PhotoImage(Image.open(k))
    return icons

def load_json_schema(json_file):
    """ Loading json schema into a dictionnary"""
    with open(json_file, "r") as fin:
        schema = json.load(fin)
    return schema

def redirect_widgets(schema, root_frame):
    if "properties" in schema:
        print("WWW", root_frame)
        return OTContainerWidget(schema, root_frame)
    elif "oneOf"in schema:
        return OTXorWidget(schema, root_frame)
    elif "enum" in schema:
        return OTChoice(schema, root_frame)
    elif "type" in schema:
        if schema['type'] == 'integer':
            return OTInteger(schema, root_frame)
        elif schema['type'] == 'number':
            return OTNumber(schema, root_frame)
        elif schema['type'] == 'boolean':
            return OTBoolean(schema, root_frame)
        elif schema["type"] == "string":
            if "ot_type" in schema:
                if schema["ot_type"] == "desc":
                    return OTDescription(schema, root_frame)
                elif schema["ot_type"] == "file":
                    return OTFileBrowser(schema, root_frame)
        elif schema["type"] == "array":
            return array_widget(schema, root_frame)
    else:
        return OTEmpty(schema, root_frame)

##

class TkinterObjectEncoder(json.JSONEncoder):
    """Adapr JSON encoder to Tkinter types"""
    def default(self, obj):
        """Ovveride the default encoder."""
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return json.JSONEncoder.default(self, obj)

        elif isinstance(obj, (OTInteger, OTNumber, OTBoolean,
                              OTChoice, OTContainerWidget,
                              OTXorWidget, OTDescription,
                              OTTabWidget, OTFileBrowser)):
            return obj.get()
        else:
            raise NotImplementedError()

class LocalValidationError(Exception):
    pass

class _OTVarFactory():
    def __init__(self, schema, root_frame, holder_nlines=1):
        self._tkvar = Tk_Variable()
        if "default" in schema:
            self._tkvar.set(schema['default'])
        if "title" in schema:
            title = schema['title']
        else:
            title = schema['name']
        self._holder = ttk.Frame(root_frame,
                                 name=schema["name"],
                                 width=WIDTH_UNIT,
                                 height=holder_nlines * LINE_HEIGHT)
        self._label = Tk_Label(self._holder,
                               text=title,
                               background=BG_COLOR,
                               justify="right",
                               wraplength=int(0.5*WIDTH_UNIT))

        self._holder.pack(side="top", fill="x")

    def get(self):
        raise NotImplementedError()

class _OTEntry(_OTVarFactory):
    def __init__(self, schema, root_frame):
        super().__init__(schema, root_frame, holder_nlines=2)
        self._inits_entry()

    def _inits_entry(self):
        self._status = Tk_Label(self._holder,
                                text="no status yet",
                                background=BG_COLOR,
                                foreground="red",
                                justify="left",
                                compound="left",
                                wraplength=WIDTH_UNIT,
                                width=WIDTH_UNIT)
        self._entry = ttk.Entry(self._holder, textvariable=self._tkvar)
        self._entry.place(relwidth=0.5, relx=0.5, rely=0.5, anchor="sw")
        self._status.place(relx=0.5, rely=0.5, anchor="n")
        self._label.place(relx=0.5, rely=0.5, anchor="se")
        self._tkvar.trace('w', self._update_status_callback)

    def _update_status_callback(self, *args):
        self.validate()
        return None

    def validate(self):
        icons = _load_icons()
        try:
            self.get()
            self._status.config(text='', image='')
        except:
            txt = 'Invalid input "%s"'%(self._entry.get())
            self._status.config(text=txt, fg='red', image=icons['invalid'])
            raise LocalValidationError()#add descriptors, verbose

class OTInteger(_OTEntry):
    def get(self):
        return int(self._tkvar.get())

    def set(self, value):
        try:
            int_val = int(value)
            self._tkvar.set(int_val)
        except:
            raise LocalValidationError()


class OTNumber(_OTEntry):
    def get(self):
        return float(self._tkvar.get())

    def set(self, value):
        try:
            float_val = float(value)
            self._tkvar.set(float_val)
        except:
            raise LocalValidationError()


class OTBoolean(_OTVarFactory):
    def __init__(self, schema, root_frame):
        super().__init__(schema, root_frame, holder_nlines=1)
        self._label.place(relx=0.5, rely=0.5, anchor="e")

        self._cbutt = ttk.Checkbutton(self._holder, variable=self._tkvar)
        self._cbutt.place(relx=0.5, rely=0.5, anchor="w")
        self._tkvar.trace('w', self._update_bool_value)

    def get(self):
        return bool(int(self._tkvar.get()))

    def _update_bool_value(self, *args):
        pass

    def set(self, value):
        self._tkvar.set(value)

class OTChoice(_OTVarFactory):
    def __init__(self, schema, root_frame):
        n_lines = max(len(schema["enum"]), 1)
        super().__init__(schema, root_frame, holder_nlines=n_lines)
        self._holder.pack_configure(side="bottom", fill="x")

        title = schema["name"]
        if "title" in schema:
            title = schema["title"]

        self._label.configure(text=title)
        rel_step = 1./n_lines
        current_rely = 1*rel_step

        self._label.place(relx=0.5, rely=current_rely, anchor="se")

        titles = schema["enum"]
        if "enum_titles" in schema:
            titles = schema["enum_titles"]

        for value, title in zip(schema["enum"], titles):
            rdBtn = ttk.Radiobutton(self._holder,
                                    text=title,
                                    value=value,
                                    variable=self._tkvar)
            rdBtn.place(relx=0.5, rely=current_rely, anchor="sw")
            current_rely += rel_step

        self._tkvar.trace('w', self._update_radio_value)

    def get(self):
        return self._tkvar.get()

    def _update_radio_value(self, *args):
        pass

    def set(self, value):
        self._tkvar.set(value)


class OTDescription(_OTVarFactory):
    def __init__(self, schema, root_frame):
        super().__init__(schema, root_frame, holder_nlines=1)
        del self._tkvar
        self._holder.pack_configure(side="bottom", fill="x")
        self._label.config(justify="left",
                           text=schema["default"],
                           wraplength=WIDTH_UNIT*0.8)
        self._label.pack(side="bottom", fill="x")

    def get(self):
        return self._label['text']

    def set(self, value):
        if value is not None:
            self._label.configure(text=value)

class OTEmpty(_OTVarFactory):
    def __init__(self, schema, root_frame):
        super().__init__(schema, root_frame, holder_nlines=1)
        del self._tkvar
        del self._holder
        info = []
        for item in ["name", "title", "type", "ot_type"]:
            if item in schema:
                info.append(item + " = " + schema[item])
        self._label.configure(text="\n".join(info))
        self._label.pack(side="top", padx=2, pady=2)

    def get(self):
        return None

class OTContainerWidget():
    def __init__(self, schema, root_frame, n_width=1):
        self.data = dict()
        title = ""
        if "title" in schema:
            title = schema["title"]

        self._holder = ttk.LabelFrame(root_frame,
                                      text=title,
                                      name=schema["name"],
                                      relief="sunken",
                                      width=n_width*WIDTH_UNIT)

        """Forcing the widget size"""
        self._forceps = ttk.Frame(self._holder,
                                  width=n_width*WIDTH_UNIT,
                                  height=1)


        self._holder.pack(side="top", fill="x",
                          padx=2, pady=2, expand=False)

        self._forceps = ttk.Frame(self._holder,
                                  width=WIDTH_UNIT,
                                  height=1)
        self._forceps.pack(side="top")

        # CHILDREN

        for name_child in schema["properties"]:
            schm_child = schema["properties"][name_child]
            self.data[name_child] = redirect_widgets(schm_child, self._holder)

    def get(self):
        return self.data

class OTXorWidget():

    def _MenuBtnCallback(self, name_child, child_schema):
        for child_widget in self._xor_holder.winfo_children():
            child_widget.destroy()

        ct = OTContainerWidget(child_schema, self._xor_holder)

        title = name_child
        if "title" in child_schema:
            title = child_schema["title"]
        self._Menu_bt.configure(text=title)

        self.data = dict()
        self.data[name_child] = ct.get()


    def set(self, value_dict):

        name = list(value_dict.keys())[0]
        for oneof_item in self._schema["oneOf"]:
            name_child = oneof_item["required"][0]
            if name_child == name:
                child_schema = oneof_item["properties"][name_child]
                break
        self._MenuBtnCallback(name_child, child_schema)
        for name_widget in self.data[name_child]:
            if self.data[name_child][name_widget] is not None:
                self.data[name_child][name_widget]\
                .set(value_dict[name][name_widget])


    def __init__(self, schema, root_frame, n_width=1):
        self.data = dict()
        self._schema = schema
        title = self._schema["name"]
        if "title" in self._schema:
            title = self._schema["title"]

        self._holder = ttk.LabelFrame(root_frame,
                                      text=title,
                                      name=self._schema["name"],
                                      relief="sunken",
                                      width=n_width*WIDTH_UNIT)

        self._forceps = ttk.Frame(self._holder,
                                  width=n_width*WIDTH_UNIT,
                                  height=1)
        self._Menu_bt = ttk.Menubutton(self._holder,
                                       text="None")

        self._xor_holder = ttk.Frame(self._holder)

        self._holder.pack(side="top", fill="x",
                          padx=2, pady=2, expand=False)
        self._forceps.pack(side="top")
        self._Menu_bt.pack(side="top")
        self._xor_holder.pack(side="top", fill="x",
                              padx=2, pady=2, expand=False)

        self._Menu_bt.menu = Tk_Menu( elf._Menu_bt, tearoff=False)
        self._Menu_bt["menu"] = self._Menu_bt.menu

        for oneof_item in self._schema["oneOf"]:
            name_child = oneof_item["required"][0]
            child_schema = oneof_item["properties"][name_child]

            title = name_child
            if "title" in child_schema:
                title = child_schema["title"]

            self._Menu_bt.menu.add_command(label=title,
                                           command=lambda \
                                           nam=name_child,
                                           ch_s=child_schema:
                                           self._MenuBtnCallback(nam, ch_s))

    def get(self):
        return self.data



class OTTabWidget():
    def __init__(self, schema, notebook):
        self.data = dict()
        self._notebook = notebook
        self._tab = ttk.Frame(self._notebook, name=schema["name"])
        self._notebook.add(self._tab, text=schema["title"])
        # SCROLL FORM
        _scroll_f = ttk.Frame(self._tab)
        _scroll_f.pack(side="top", fill="both", expand=True)
        _scroll_f.columnconfigure(0, weight=1)
        _scroll_f.columnconfigure(1, weight=0)
        _scroll_f.rowconfigure(0, weight=1)
        _scroll_f.rowconfigure(1, weight=0)
        self._can_scroll = Tk_Canvas(_scroll_f,
                                     background=BG_COLOR,
                                     highlightbackground=BG_COLOR,
                                     highlightcolor=BG_COLOR)

        self._can_scroll.configure(width=1000, height=300)
        _scroll_vert = ttk.Scrollbar(_scroll_f,
                                     orient="vertical",
                                     command=self._can_scroll.yview)
        self._can_scroll.configure(yscrollcommand=_scroll_vert.set)
        _scroll_horz = ttk.Scrollbar(_scroll_f, orient="horizontal",
                                     command=self._can_scroll.xview)
        self._can_scroll.configure(xscrollcommand=_scroll_horz.set)
        self._can_scroll.grid(row=0, column=0, sticky="news")
        _scroll_vert.grid(row=0, column=1, sticky="ns")
        _scroll_horz.grid(row=1, column=0, sticky="we")

        self._out_frame = ttk.Frame(self._can_scroll)

        self._can_scroll.create_window((0, 0),
                                       window=self._out_frame,
                                       anchor='nw')
        # FOOTER
        _footer_f = ttk.Frame(self._tab)
        _footer_f.pack(side="top", fill="both", padx=2, pady=3)

        # button_var = StringVar(value="dummy info")
        _button_lb = ttk.Label(_footer_f, text="button_var")
        _button_bt = ttk.Button(_footer_f, text="Process")
        _button_bt.pack(side="right", padx=2, pady=2)
        _button_lb.pack(side="right", padx=2, pady=2)

        # CHILDREN
        for name in schema["properties"]:
            self.data[name] = redirect_widgets(
                                schema["properties"][name],
                                self._out_frame)

        self._out_frame.bind("<Configure>", self._update_canvas_bbox_from_inside)

    def _update_canvas_bbox_from_inside(self, event=None):
        """Smart grid upon widget size.

        Regrid the object according to the width of the window
        """
        self._can_scroll.configure(scrollregion=self._can_scroll.bbox("all"))
        ncols = max(int(self._notebook.winfo_width()/WIDTH_UNIT + 0.5), 1)
        height = 0
        for children in self._out_frame.winfo_children():
            height += children.winfo_height()
        limit_depth = height / ncols
        max_depth = 0
        x_pos = 10 + 0*WIDTH_UNIT
        y_pos = 10
        for children in self._out_frame.winfo_children():
            children.place(x=x_pos,
                           y=y_pos,
                           anchor="nw")
            y_pos += children.winfo_height() + 2

            if y_pos > limit_depth and ncols > 1:
                max_depth = y_pos
                x_pos += WIDTH_UNIT + 20
                y_pos = 10
            else:
                max_depth = height
        self._out_frame.configure(height=max_depth+40,
                                  width=ncols*(WIDTH_UNIT+20)+20)

    def get(self):
        return self.data

class OTFileBrowser(_OTVarFactory):
    def __init__(self, schema, root_frame):
        super().__init__(schema, root_frame, holder_nlines=2)


        title = schema['name']
        if "title" in schema:
            title = schema['title']
        self._title = title

        self._filter = []
        self._isdirectory = False
        if 'ot_filter' in schema:
            filters = schema['ot_filter']
            if 'directory' in filters:
                self._isdirectory = True
            else:
                for f in filters:
                    filetype = ("%s files"%f, "*.%s"%(f))
                    self._filter.append(filetype)

        self._holder.pack_configure(side="bottom", fill="x")
        self._label.config(justify="left",
                           text=self._title,
                           wraplength=WIDTH_UNIT*0.8)

        self._label.place(relx=0.5, rely=0.5, anchor="se")

        self._path = ttk.Entry(self._holder,
                               textvariable=self._tkvar,
                               state='disabled',
                               foreground='black')
        self._path.place(relx=0.4, rely=0.5, anchor="n")

        self._btn = ttk.Button(self._holder,
                               text="Browse",
                               width=5,
                               command=self._browse)


        self._btn.place(relx=0.98, rely=0.5, anchor="e")

    def _browse(self, event=None):
        if self._isdirectory:
            path = Tk_filedlg.askdirectory(initialdir=os.getcwd(),
                                              title=self._title)
        else:
            path = Tk_filedlg.askopenfilename(initialdir=os.getcwd(),
                                                 title=self._title,
                                                 filetypes=self._filter)
        self._tkvar.set(path)

    def get(self):
        return  self._tkvar.get()

    def set(self, value):
        self._tkvar.set(value)

class OTGUI():
    def __init__(self, schema):

        self.schema = schema
        self._root = Tk()
        style = ttk.Style()
        style.theme_use("clam")

        self._root.title(self.schema["name"])
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)


        self._main_frame = ttk.Frame(self._root, padding="3 3 12 12")
        self._main_frame.grid(column=0, row=0, sticky="news")
        self._notebook = ttk.Notebook(self._main_frame, name='tab_holder')
        self._notebook.pack(fill="both", padx=2, pady=3, expand=True)

        ttk.Style().configure("TNotebook", background=BG_COLOR)

        self._init_file_menu()
        self._init_gui()
        self._root.mainloop()

    def _init_file_menu(self):

        icons = _load_icons()
        self._menubar = Tk_Menu(self._root)
        self._filemenu = Tk_Menu(self._menubar, tearoff=0)

        self._filemenu.add_command(label="New  (Ctrl+N)",
                                   image=icons['new'],
                                   compound='left',
                                   command=self._menu_new_command)


        self._filemenu.add_command(label="Load  (Ctrl+O)",
                                   image=icons['load'],
                                   compound='left',
                                   command=self._menu_load_command)



        self._filemenu.add_command(label="Save  (Ctrl+S)",
                                   image=icons['save'],
                                   compound='left',
                                   command=self._menu_save_command)

        self._filemenu.add_separator()


        self._filemenu.add_command(label="Quit   (Ctrl+W)",
                                   image=icons['quit'],
                                   compound='left',
                                   command=self._menu_quit_command)

        self._menubar.add_cascade(label="File", menu=self._filemenu)

        self._helpmenu = Tk_Menu(self._menubar, tearoff=0)


        self._helpmenu.add_command(label="About",
                                   image=icons['about'],
                                   compound='left',
                                   command=self._menu_about_command)

        self._menubar.add_cascade(label="Help", menu=self._helpmenu)

        self._root.bind('<Control-o>', self._menu_load_command)
        self._root.bind('<Control-s>', self._menu_save_command)
        self._root.bind('<Control-n>', self._menu_new_command)
        self._root.bind('<Control-w>', self._menu_quit_command)
        self._root.config(menu=self._menubar)



    def _init_gui(self):
        self.data = dict()
        for name in self.schema["properties"]:
            # self.data[name] = dict()
            # tab(self.schema["properties"][name],
            #     self._notebook,
            #     self.data[name])
            schema_child = self.schema["properties"][name]
            self.data[name] = OTTabWidget(schema_child, self._notebook)

    def _menu_quit_command(self, event=None):
        self._root.quit()

    def _menu_new_command(self, event=None):
        self._init_gui()


    def _menu_load_command(self, event=None):
        # try:
        state = Tk_filedlg.askopenfilename(
                        initialdir=os.getcwd(),
                        title="Select file",
                        filetypes=(("OpenTea json files", "*.otsv"),
                                   ("All files", "*.*")))

        state = load_json_schema(state)

        for name_tab in self.schema["properties"]:
            schema_tab = self.schema["properties"][name_tab]
            for name_element in schema_tab['properties']:
                schema_element = schema_tab['properties'][name_element]
                if "properties" in schema_element:
                    schema_widget = schema_element['properties']
                    for name_widget in schema_widget:
                        value = state[name_tab]\
                                     [name_element] \
                                     [name_widget]
                        if self.data[name_tab] \
                                .data[name_element] \
                                .data[name_widget] is not None:

                            self.data[name_tab] \
                                .data[name_element] \
                                .data[name_widget] \
                                .set(value)

                elif "oneOf"in schema_element:
                    if state[name_tab][name_element] is not None:
                        value = state[name_tab][name_element]
                        self.data[name_tab].data[name_element].set(value)
                elif "enum" in schema_element:
                    # pass
                    print("enum : %s/%s"%(name_tab, name_element))
                    print(self.data[name_tab].data[name_element])


    def _menu_save_command(self, event=None):
        try:
            file_types = (("OpenTea json files", "*.otsv"),
                          ("All files", "*.*"))
            output = Tk_filedlg.asksaveasfilename(initialdir=os.getcwd(),
                                                  title="Select file",
                                                  defaultextension='.otsv',
                                                  filetypes=file_types)

            if output is not '':
                dump = json.dumps(self.data, indent=4,
                                  cls=TkinterObjectEncoder)
                with open(output, 'w') as fout:
                    fout.writelines(dump)

        except:
            print('smthng went wrong while saving')


    def _menu_about_command(self):
        print('about')


###########################################################

# TO DO
# - Loading saved state : soft pain in the a*s
# enum / one of
# - Array widget : should be fine
    # - Convert to class
    # - Append to list of load/save
    # - Enhance functionnalities

# - Exceptions class : Make it more verbose
# - Documentation : Get inspired from previous impl
# - liniting : yes am coding like a pig; 
# - clean up : wiping sh*t

###########################################################


def array_widget(schema, root_frame):
    """Triggers an array apprearance.

    Parameters :
    ------------
    schema : a GUI schema
    root_frame : a Tk frame holder

    Output:
    -------
    A dynamic  array widget
    """
    title = ""
    if "title" in schema:
        title = schema["title"]

    holder = ttk.LabelFrame(root_frame,
                            text=title,
                            name=schema["name"],
                            relief="sunken",
                            width=2*WIDTH_UNIT)

    holder.pack(side="top", fill="x", padx=2, pady=2, expand=False)

    forceps = ttk.Frame(holder, width=2*WIDTH_UNIT, height=1)

    array_tv = ttk.Treeview(holder,
                            selectmode="browse",
                            height=15)
    scroll_vert = ttk.Scrollbar(holder,
                                orient="vertical",
                                command=array_tv.yview)
    array_tv.configure(yscrollcommand=scroll_vert.set)

    switchform = ttk.LabelFrame(holder,
                                width=WIDTH_UNIT,
                                labelanchor="n")

    forceps.grid(column=0, row=1, columnspan=3)
    scroll_vert.grid(column=1, row=1, sticky="news")
    array_tv.grid(column=0, row=1, sticky="news")
    switchform.grid(column=2, row=1, rowspan=2, sticky="news")

    item_schema = schema["items"]["properties"]

    array_tv["columns"] = tuple(item_schema.keys())
    col_width = int(WIDTH_UNIT/(len(array_tv["columns"])+1))
    array_tv.column("#0", width=col_width)

    vals = tuple("col"+str(j) for j in range(len(array_tv["columns"])))
    for key in item_schema:
        title = key
        if "title" in item_schema[key]:
            title = item_schema[key]["title"]
        array_tv.column(key, width=col_width)
        array_tv.heading(key, text=title)

    for i in range(50):
        array_tv.insert("",
                        "end",
                        iid="line_"+str(i),
                        text="line "+str(i),
                        values=vals)

    def line_select(key, title):
        """Trigger the line selection event."""
        for child_widget in switchform.winfo_children():
            child_widget.destroy()
        switchform.configure(text=title)
        for element in item_schema:
            redirect_widgets(element,
                             item_schema[element], 
                             switchform)

    def simple_click(event):
        """Handle a simple click on treeview."""
        # col = array_tv.identify_column(event.x)
        row = array_tv.identify_row(event.y)
        line_select(row, row)

    array_tv.bind("<Button-1>", simple_click)


def main_otinker(schema):
    """Startup the gui generation.

    Inputs :
    --------
    schema : dictionary compatible with json-schema

    Outputs :
    ---------
    a tkinter GUI
    """
    OTGUI(schema)

if __name__ == "__main__":
    SCHEMA = load_json_schema("schema.json")
    main_otinker(SCHEMA)
