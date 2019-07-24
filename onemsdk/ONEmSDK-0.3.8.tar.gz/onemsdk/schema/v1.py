from __future__ import annotations

from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Schema

from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import (FormTag, SectionTag, LiTag, PTag, BrTag, UlTag,
                            ATag, HeaderTag, FooterTag, InputTag)
from onemsdk.parser.tag import InputTagType


class MenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class MenuItem(BaseModel):
    """
    An item in a menu. Depending on its type, a menu item can be either an option (type=option) or an option separator (type=content)
    """
    type: MenuItemType = Schema(
        ...,
        description='The type of the menu item.'
    )
    description: str = Schema(
        ...,
        description='The displayed text of a menu item.'
    )
    method: str = Schema(
        None,
        description='The HTTP method called when the menu item is selected.'
    )
    path: str = Schema(
        None,
        description='The path called when the menu item is selected.'
    )

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]) -> Union[MenuItem, None]:
        if isinstance(tag, str):
            description = tag
        else:
            description = tag.render()

        if not description:
            return None

        type = MenuItemType.content
        method = None
        path = None

        if isinstance(tag, LiTag) and isinstance(tag.children[0], ATag):
            atag: ATag = tag.children[0]
            method = atag.attrs.method
            path = atag.attrs.href
            type = MenuItemType.option

        return MenuItem(type=type, description=description, method=method, path=path)


class Menu(BaseModel):
    """
    A top level component that permits displaying a navigable menu or a plain text.
    """
    type: str = Schema(
        'menu',
        description='The type of the Menu object is always "menu"',
        const=True
    )
    body: List[MenuItem] = Schema(..., description='The body/content of the menu')
    header: str = Schema(None, description='The header of the menu.')
    footer: str = Schema(None, description='The header of the menu.')

    @classmethod
    def from_tag(cls, section_tag: SectionTag) -> Menu:
        body = []
        header = None
        footer = None

        for child in section_tag.children:
            if isinstance(child, UlTag):
                body.extend([MenuItem.from_tag(li) for li in child.children])
            elif isinstance(child, HeaderTag):
                header = child.render()
            elif isinstance(child, FooterTag):
                footer = child.render()
            else:
                body.append(MenuItem.from_tag(child))

        return Menu(
            header=header or section_tag.attrs.header,
            footer=footer or section_tag.attrs.footer,
            body=list(filter(None, body))
        )


class FormItemContentType(str, Enum):
    string = 'string'
    date = 'date'
    datetime = 'datetime'


class FormItemContent(BaseModel):
    """
    Component used to ask a user for a certain type of free input
    """
    type: FormItemContentType = Schema(
        ...,
        description='The type of data expected from the user'
    )
    name: str = Schema(
        ...,
        description='An identifier to be linked with the data value obtained from user. '
                    'It has to be unique per form.'
    )
    description: str = Schema(..., description='The displayed text.')
    header: str = Schema(None, description='The header of the form item')
    footer: str = Schema(None, description='The footer of the form item')

    @classmethod
    def from_tag(cls, section: SectionTag) -> FormItemContent:
        header = None
        footer = None

        content_types_map = {
            InputTagType.date: FormItemContentType.date,
            InputTagType.datetime: FormItemContentType.datetime,
            InputTagType.text: FormItemContentType.string
        }

        for child in section.children:
            if isinstance(child, InputTag):
                type = child.attrs.type
                break
        else:
            raise ONEmSDKException(
                'When <section> plays the role of a form item content, '
                'it must contain a <input/>'
            )

        if isinstance(section.children[0], HeaderTag):
            header = section.children[0].render()
        if isinstance(section.children[-1], FooterTag):
            footer = section.children[-1].render()

        return FormItemContent(
            type=content_types_map[type],
            name=section.attrs.name,
            description=section.render(exclude_header=True, exclude_footer=True),
            header=header or section.attrs.header,
            footer=footer or section.attrs.footer,
        )


class FormItemMenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class FormItemMenuItem(BaseModel):
    """
    An item in a form's menu
    """
    type: FormItemMenuItemType = Schema(
        ...,
        description='The type of a menu item inside a form'
    )
    description: str = Schema(..., description='The displayed text.')
    value: str = Schema(
        None,
        description='If type=option, value is used to identify the option chosen by the user'
    )

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]
                 ) -> Union[FormItemMenuItem, None]:

        type = FormItemMenuItemType.content
        value = None

        if isinstance(tag, str):
            description = tag
        else:
            description = tag.render()

        if not description:
            return None

        if isinstance(tag, LiTag) and tag.attrs.value:
            type = FormItemMenuItemType.option
            value = tag.attrs.value

        return FormItemMenuItem(type=type, value=value, description=description)


class FormItemMenu(BaseModel):
    """
    Item in a form's body used to ask the user to select an option from a list
    """
    type: str = Schema(
        'form-menu',
        description='The type of a FormItemMenu is always form-menu',
        const=True
    )
    body: List[FormItemMenuItem] = Schema(
        ...,
        description='A sequence of menu items containing options and/or option separators'
    )
    name: str = Schema(
        ...,
        description='An identifier to be linked with the data value obtained from user. '
                    'It has to be unique per form.'
    )
    header: str = Schema(None, description='The form menu header')
    footer: str = Schema(None, description='The form menu footer')

    @classmethod
    def from_tag(cls, section_tag: SectionTag) -> FormItemMenu:
        body: List[FormItemMenuItem] = []
        header = None
        footer = None

        for child in section_tag.children:
            if isinstance(child, UlTag):
                body.extend([FormItemMenuItem.from_tag(li) for li in child.children])
            elif isinstance(child, HeaderTag):
                header = child.render()
            elif isinstance(child, FooterTag):
                footer = child.render()
            else:
                body.append(FormItemMenuItem.from_tag(child))

        return FormItemMenu(
            body=list(filter(None, body)),
            name=section_tag.attrs.name,
            header=header or section_tag.attrs.header,
            footer=footer or section_tag.attrs.footer,
        )


class FormMeta(BaseModel):
    """
    Configuration fields for a Form
    """
    completion_status_show: bool = Schema(
        None,
        title='Show completion status',
        description='Whether to display the completions status'
    )
    completion_status_in_header: bool = Schema(
        None,
        title='Show completion status in header',
        description='Whether to display the completion status in header'
    )
    confirmation_needed: bool = Schema(
        None,
        title='Confirmation needed',
        description='Whether to add an additional item at the end of the form for confirmation'
    )


class Form(BaseModel):
    """
    A top level component used to acquire information from user
    """
    type: str = Schema('form', description='The type of a form is always form',
                       const=True)
    body: List[Union[FormItemContent, FormItemMenu]] = Schema(
        ...,
        description='Sequence of components used to acquire the pieces of data needed from user'
    )
    method: str = Schema('POST', description='The HTTP method used to send the form data')
    path: str = Schema(..., description='The path used to send the form data')
    header: str = Schema(
        None,
        description='The header of the form. It can be overwritten by each body component'
    )
    footer: str = Schema(
        None,
        description='The footer of the form. It can be overwritten by each body component'
    )
    meta: FormMeta = Schema(None, description='Contains configuration flags')

    @classmethod
    def from_tag(cls, form_tag: FormTag) -> Form:
        body = []
        for section in form_tag.children:
            for child in section.children:
                if isinstance(child, UlTag):
                    body.append(FormItemMenu.from_tag(section))
                    break
            else:
                body.append(FormItemContent.from_tag(section))

        assert len(body) == len(form_tag.children)

        form = Form(
            header=form_tag.attrs.header,
            footer=form_tag.attrs.footer,
            meta=FormMeta(
                completion_status_show=form_tag.attrs.completion_status_show,
                completion_status_in_header=form_tag.attrs.completion_status_in_header,
                confirmation_needed=form_tag.attrs.confirmation_needed
            ),
            method=form_tag.attrs.method,
            path=form_tag.attrs.action,
            body=body
        )
        return form


class MessageContentType(str, Enum):
    form = 'form'
    menu = 'menu'


class Response(BaseModel):
    """
    A JSON-serialized instance of Response must be sent as response to the ONEm platform. It can be built only from a top level object (Menu, Form).
    """
    content_type: MessageContentType = Schema(
        ...,
        title='Content type',
        description='The type of the content of the response'
    )
    content: Union[Form, Menu] = Schema(
        ...,
        description='The content of the response'
    )

    def __init__(self, content: Union[Menu, Form]):
        if isinstance(content, Menu):
            content_type = MessageContentType.menu
        elif isinstance(content, Form):
            content_type = MessageContentType.form
        else:
            raise ONEmSDKException(f'Cannot create response from {type(content)}')

        super(Response, self).__init__(content_type=content_type, content=content)

    @classmethod
    def from_tag(cls, tag: Union[FormTag, SectionTag]):
        if isinstance(tag, FormTag):
            return Response(content=Form.from_tag(tag))
        if isinstance(tag, SectionTag):
            return Response(content=Menu.from_tag(tag))
        raise ONEmSDKException(f'Cannot create response from {tag.Config.tag_name} tag')
