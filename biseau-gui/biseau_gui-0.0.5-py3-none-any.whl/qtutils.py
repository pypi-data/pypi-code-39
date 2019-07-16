

from PySide2.QtWidgets import QMenu, QToolButton, QActionGroup


def add_menubutton(parent, name='', menuitems:[(str, callable)]=(), on_clicked=None, icon=None, toolbar=None, mainmenu=None, menu_is_choice:bool=False, default:int or str=None) -> (QToolButton, QActionGroup):
    """Create a button with integrated menu, add it to given toolbar if given,
    and internal menu to given mainmenu if given, then return the button.

    parent -- the parent of the button
    name -- text of the button
    menuitems -- iterable of arguments for QMenu.addAction, to populate button's menu
    on_clicked -- slot to connect to button.clicked
    icon -- icon of the button
    toolbar -- the toolbar to which the menubutton must be added
    mainmenu -- the QMenu to which the submenu must be added, under the name 'name'
    menu_is_choice -- if true, menuitems describes mutually exclusive values
    default -- if menu_is_choice, defines the index or the name of the default value
    return -- the button and, if menu_is_choice, the QActionGroup

    """
    # Create the button and its submenu
    button_menu = QMenu(name, parent)
    if menu_is_choice:
        group = QActionGroup(parent)
        for idx, args in enumerate(menuitems):
            action = group.addAction(*args)
            action.setCheckable(True)
            if default == args[0] or default == idx:
                action.setChecked(True)
        button_menu.addActions(group.actions())
    else:
        group = None
        for args in menuitems:
            button_menu.addAction(*args)

    button = QToolButton(parent)
    button.setMenu(button_menu)
    button.setPopupMode(QToolButton.MenuButtonPopup)
    if icon: button.setIcon(icon)
    if name: button.setText(name)
    if on_clicked: button.clicked.connect(on_clicked)
    # Add it to the toolbar and to the mainmenu if given
    if toolbar: toolbar.addWidget(button)
    if mainmenu: mainmenu.addMenu(button_menu)
    return button, group
