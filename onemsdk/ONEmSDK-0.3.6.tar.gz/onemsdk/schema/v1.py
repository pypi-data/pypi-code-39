from __future__ import annotations

from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel

from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import FormTag, SectionTag, LiTag, PTag, BrTag, UlTag, ResponseType


class MenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class MenuItem(BaseModel):
    type: MenuItemType
    description: str
    method: Optional[str]
    path: Optional[str]

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]) -> MenuItem:
        if isinstance(tag, str):
            menu_item = MenuItem(
                type=MenuItemType.content,
                description=tag,
                method=None,
                path=None
            )
            return menu_item

        tag_data = tag.data()

        if tag_data['href']:
            menu_item = MenuItem(
                type=MenuItemType.option,
                description=tag_data['text'],
                method=tag_data['method'],
                path=tag_data['href']
            )
        else:
            menu_item = MenuItem(
                type=MenuItemType.content,
                description=tag_data['text'],
                method=None,
                path=None
            )
        return menu_item


class Menu(BaseModel):
    type = 'menu'
    header: Optional[str]
    footer: Optional[str]
    body: List[MenuItem]

    @classmethod
    def from_tag(cls, section_tag: SectionTag) -> Menu:
        body = []
        for child in section_tag.children:
            if isinstance(child, UlTag):
                body.extend([MenuItem.from_tag(li) for li in child.children])
            else:
                body.append(MenuItem.from_tag(child))

        menu = Menu(
            header=section_tag.attrs.header,
            footer=section_tag.attrs.footer,
            body=body
        )
        return menu


class FormItemContentType(str, Enum):
    string = 'string'
    date = 'date'
    datetime = 'datetime'


class FormItemContent(BaseModel):
    type: FormItemContentType
    name: str
    description: str
    header: Optional[str]
    footer: Optional[str]

    @classmethod
    def from_tag(cls, section: SectionTag) -> FormItemContent:
        content_types_map = {
            ResponseType.date: FormItemContentType.date,
            ResponseType.datetime: FormItemContentType.datetime,
            ResponseType.text: FormItemContentType.string,
        }
        content = FormItemContent(
            type=content_types_map[section.attrs.expected_response.type],
            name=section.attrs.name,
            description=section.render(),
            header=section.attrs.header,
            footer=section.attrs.footer,
        )
        return content


class FormItemMenuItemType(str, Enum):
    option = 'option'
    content = 'content'


class FormItemMenuItem(BaseModel):
    type: FormItemMenuItemType
    value: Optional[str]
    description: str

    @classmethod
    def from_tag(cls, tag: Union[LiTag, PTag, BrTag, str]) -> FormItemMenuItem:
        if isinstance(tag, str):
            return FormItemMenuItem(
                type=FormItemMenuItemType.content,
                value=None,
                description=tag
            )

        tag_data = tag.data()

        if isinstance(tag, LiTag):
            if not tag_data['value']:
                item_type = FormItemMenuItemType.content
            else:
                item_type = FormItemMenuItemType.option

            menu_item = FormItemMenuItem(
                type=item_type,
                value=tag_data['value'],
                description=tag_data['text']
            )
        else:
            menu_item = FormItemMenuItem(
                type=FormItemMenuItemType.content,
                value=None,
                description=tag_data['text']
            )
        return menu_item


class FormItemMenu(Menu):
    type = 'form-menu'
    body: List[FormItemMenuItem]

    @classmethod
    def from_tag(cls, section_tag: SectionTag) -> FormItemMenu:
        body: List[FormItemMenuItem] = []
        for child in section_tag.children:
            if isinstance(child, UlTag):
                body.extend([FormItemMenuItem.from_tag(li) for li in child.children])
            else:
                body.append(FormItemMenuItem.from_tag(child))

        menu = FormItemMenu(
            header=section_tag.attrs.header,
            footer=section_tag.attrs.footer,
            body=body
        )
        return menu


class FormMeta(BaseModel):
    completion_status_show: bool = True
    completion_status_in_header: bool = True
    confirmation_needed: bool = True


class Form(BaseModel):
    type = 'form'
    header: Optional[str]
    footer: Optional[str]
    meta: Optional[FormMeta]
    method: str = 'POST'
    path: str
    body: List[Union[FormItemContent, FormItemMenu]]

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
            path=form_tag.attrs.path,
            body=body
        )
        return form


class MessageContentType(str, Enum):
    form = 'form'
    menu = 'menu'


class Response(BaseModel):
    corr_id: Optional[str]
    content_type: MessageContentType
    content: Union[Form, Menu]

    def __init__(self, **data):
        if isinstance(data['content'], Menu):
            content_type = MessageContentType.menu
        else:
            content_type = MessageContentType.form

        data['content_type'] = content_type

        super(Response, self).__init__(**data)

    @classmethod
    def from_tag(cls, tag: Union[FormTag, SectionTag], message_id: Optional[str] = None):
        if isinstance(tag, FormTag):
            return Response(
                message_id=message_id,
                content_type=MessageContentType.form,
                content=Form.from_tag(tag)
            )
        if isinstance(tag, SectionTag):
            return Response(
                message_id=message_id,
                content_type=MessageContentType.menu,
                content=Menu.from_tag(tag)
            )
        raise ONEmSDKException(f'Cannot create response from {tag.Config.tag_name} tag')
