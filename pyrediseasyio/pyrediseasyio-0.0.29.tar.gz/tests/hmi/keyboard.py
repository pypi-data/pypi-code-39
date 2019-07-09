from dominate import document
from dominate.tags import div, button
from collections import namedtuple
import gettext

_ = gettext.gettext

Btn = namedtuple("Btn", "cls val action")

keys = [
    Btn('number-button', _("1"), 1),
    Btn('number-button', _("2"), 2),
    Btn('number-button', _("3"), 3),
    Btn('action-button', _("Del"), 'Del'),
    Btn('number-button', _("4"), 4),
    Btn('number-button', _("5"), 5),
    Btn('number-button', _("6"), 6),
    Btn('action-button', _("Clear"), 'Clear'),
    Btn('number-button', _("7"), 7),
    Btn('number-button', _("8"), 8),
    Btn('number-button', _("9"), 9),
    Btn('action-button', _("Cancel"), 'Cancel'),
    Btn('number-button plus-minus-button', _("+/-"), 'Sign'),
    Btn('number-button', _("0"), 0),
    Btn('number-button decimal_button', _("."), 'Dec'),
    Btn('action-button ok-button', _("Ok"), 'Ok')
]

def keyboard(doc: document):
    with doc.body:
        with div(cls="easyio_number_keyboard"):
            with div(cls='grid-container'):
                div("Title", cls = "title")
                div(0, cls='entry', id="easy_io_number_keyboard_entry")
                div('', cls='original')

                for key in keys:
                    button(key.val, cls=key.cls, onclick=f"EasyIoNumericEntryKeyPressed('{key.action}')")

                div('', cls='max')
                div('', cls='min')
