"""Graphical interactors.

"""

import campy.graphics.gobjects as gobjects
import campy.private.platform as _platform

from campy.graphics.gevents import *

class GInteractor(gobjects.GObject):
    """Superclass of all graphical interactors.

    In most applications, interactors will be added to one region in a
    :class:`GWindow`, but interactors can also be placed in specific positions
    in a :class:`GCompound` (or the :class:`GWindow`'s default top :class:`GCompound`)
    just like any other :class:`GObject`.
    """
    def __init__(self, action_command=""):
        """Initialize a :class:`GInteractor` with an action command.

        The action command is returned as part of the GActionEvent.

        :param action_command: The action command for this interactor.
        """
        # TODO(sredmond): Remove action_command as a concept from Python actions.
        gobjects.GObject.__init__(self)
        self._action_command = action_command

    @property
    def action_command(self):
        """Get or set the action command to the indicated string.

        If the string is nonempty, activating the interactor generates a GActionEvent.

        :param str command: The action command to set or get.
        """
        # TODO(sredmond): Do we really not activate an event when the string is empty?
        return self._action_command

    @action_command.setter
    def action_command(self, action_command):
        self._action_command = action_command
        # _platform.Platform().ginteractor_set_action_command(self, action_command)

    # TODO(sredmond): Solve resizable problem.

    # def setSize(self, width=0.0, height=0.0, size = None):
    #     '''
    #     Changes the size of the interactor to the specified width and height.

    #     @type width: float
    #     @type height: float
    #     @type size: GDimension, overrides width and height parameters
    #     @rtype: void
    #     '''
    #     if(size != None):
    #         width = size.width
    #         height = size.height
    #     _platform.Platform().gobject_set_size(self, width, height)

    # def setBounds(self, x=0.0, y=0.0, width=0.0, height=0.0, rect = None):
    #     '''
    #     Changes the bounds of the interactor to the specified values.

    #     @type x: float
    #     @type y: float
    #     @type width: float
    #     @type height: float
    #     @type rect: GRectangle
    #     @param rect: bounding GRectangle, overrides x, y ,width and height
    #     @rtype: void
    #     '''
    #     if(rect != None):
    #         x,y,width,height = rect
    #     self.setLocation(x, y)
    #     self.setSize(width, height)

    # @property
    # def bounds(self):
    #     return self._bounds

    def getBounds(self):
        '''
        Returns the bounding GRectangle of the GInteractor

        @rtype: GRectangle
        '''
        size = _platform.Platform().getSize(self)
        return _gtypes.GRectangle(self.x, self.y, size.getWidth(), size.getHeight())

class GButton(GInteractor):
    """An onscreen button.

    The following program displays a button that, when pressed, generates the
    message: "Please do not press this button again!" (credit Douglas Adams)::

        window = GWindow()
        button = GButton("RED BUTTON")
        window.add_to_region(button, "SOUTH")

        @button.onclick
        def chastise(event):
            print("Please do not press this button again.")
            event.button.disable()
    """
    def __init__(self, label):
        """Construct a GButton with the specified label.

        :param str label: A label for this GButton.
        """
        super().__init__()
        self.label = label
        self.disabled = False

        # Collection of
        self._listeners = []

        # Tell the underlying platform to construct this object.
        _platform.Platform().gbutton_constructor(self)

    def onclick(self, function):
        self._listeners.append(function)
        return function

    def add_click_handler(self, function):
        self._listeners.append(function)

    def remove_click_handler(self, function):
        try:
            self._listeners.remove(function)
            return True
        except ValueError:
            return False

    def _click(self, event):
        """Default click implementation doesn't do anything."""
        for listener in self._listeners:
            listener(event)

    def click(self):
        # Make an event to pass to click handler.
        event = GActionEvent(None, None, None)
        self._click(event)

    def enable():
        self.disabled = False

    def disable():
        self.disabled = True


class GCheckBox(GInteractor):
    """An onscreen check box.

    Clicking once on the check box selects it; clicking again removes the
    selection.

    If a GCheckBox has an action command, clicking on the box generates a
    GActionEvent.
    """

    def __init__(self, label):
        """
        Creates a GCheckBox with the specified label.

        In contrast to the GButton constructor, this constructor does not set an
        action command.

        :param str label: A label for this GCheckBox.
        """
        super().__init__()
        self.label = label
        _platform.Platform().gcheckbox_constructor(self, label)


    @property
    def selected(self):
        """Get or set whether the checkbox is selected.

        :param bool state: Whether the checkbox is selected.
        """
        return _platform.Platform().gcheckbox_is_selected(self)

    @selected.setter
    def selected(self, state):
        return _platform.Platform().gcheckbox_set_selected(self, state)

    def __str__(self):
        return 'GCheckBox("{}")'.format(self.label)

class GSlider(GInteractor):
    """An onscreen slider.

    Dragging
    """

    def __init__(self, min_value=0, max_value=100, starting_value=50):
        """Create a horizontal GSlider.

        The client can specify a minimum value, maximum value, and starting
        value.

        :param int min_value: The minimum value of this GSlider.
        :param int max_value: The maximum value of this GSlider. Should be >=
            min_value, but this is not currently enforced.
        :param int starting_value: The starting value of this GSlider. Should be
            between min_value and max_value. If not, is set to min_value.
        """
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        # TODO(sredmond): Error check that max_value >= min_value.
        if not min_value <= starting_value <= max_value:
            starting_value = min_value
        _platform.Platform().gslider_constructor(self, min_value, max_value, starting_value)

    @property
    def value(self):
        """Get or set the current value of the GSlider.

        :param int value: The value of the GSlider.
        """
        return _platform.Platform().gslider_get_value(self)

    @value.setter
    def value(self, new_value):
        _platform.Platform().gslider_set_value(self, value)

    def __str__(self):
        return "GSlider(value={}, min={}, max={})".format(self.value, self.min_value, self.max_value)


class GTextField(GInteractor):
    """An onscreen text field for entering short text strings.

    Hitting RETURN in a text field generates a :class:`GActionEvent`.
    """

    def __init__(self, width=10):
        """Create a text field with a maximum width.

        A :class:`GActionEvent` is generated whenever the user presses the
        RETURN key while this interactor has focus.

        :param width: The maximum number of characters this field can hold.
        """
        super().__init__(self)
        self._width = width
        _platform.Platform().gtextfield_constructor(self)

    @property
    def text(self):
        """Get or set the contents of this :class:`GTextField`."""
        return _platform.Platform().gtextfield_get_text(self)

    @text.setter
    def text(self, content):
        _platform.Platform().gtextfield_set_text(self, content)

    def __str__(self):
        return "GTextField(text={}, width={})".format(self.text, self.width)


class GChooser(GInteractor):
    """A list of selectable items.

    You can construct a :class:`GChooser` with an ordered collection of items,
    or :meth:`add` and :meth:`remove` items after construction::

        size_chooser = GChooser('Small', 'Medium', 'Large')
        size_chooser.add_item('X-Large')
        size_chooser.remove_item('Medium')

    To get the selected item::

        size_chooser = GChooser('Small', 'Medium', 'Large')
        selected = size_chooser.selected_item
    """

    def __init__(self, *items):
        """Create a :class:`GChooser`, optionally with some items.

        These items are supplied as extra positional arguments::

            size_chooser = GChooser('Small', 'Medium', 'Large')

        To construct a :class:`GChooser` from a collection of elements, unpack
        the elements into the constructor::

            options = ('Small', 'Medium', 'Large')
            size_chooser = GChooser(*options)

        A :class:`GActionEvent` is generated each time the user selects an item.
        """
        super().__init__(self)
        self._items = list(items)

        _platform.Platform().gchooser_constructor(self)

    def add_item(self, item):
        """Add a new option to this :class:`GChooser`.

        :param item: The new item to add to this :class:`GChooser`.
        """
        self._items.append(item)
        _platform.Platform().gchooser_add_item(self, item)

    def remove_item(self, item):
        """Remove an option from this :class:`GChooser`.

        :param item: The item to remove from this :class:`GChooser`.
        :return: Whether the item was removed.
        """
        try:
            self._items.remove(item)
            _platform.Platform().gchooser_remove_item(self, item)
            return True
        except ValueError:
            return False

    @property
    def selected_item(self):
        """Get or set the currently selected item of this :class:`GChooser`.

        Setting the selected item to something not in this :class:`GChooser`'s
        list of items results in no change.
        """
        return _platform.Platform().gchooser_get_selected_item(self)

    @selected_item.setter
    def selected_item(self, item):
        if item not in self._items:
            return

        _platform.Platform().gchooser_set_selected_item(self, item)

    def __str__(self):
        return "GChooser(items={})".format(self._items)

if __name__ == '__main__':
    from campy.graphics.gwindow import GWindow
    window = GWindow()
    button = GButton("Hello!")
    button.add_click_handler(lambda event: print(event.__dict__))
    window.add(button)
