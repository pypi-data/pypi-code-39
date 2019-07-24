#!/usr/bin/python
# -*- coding: utf-8 -*-

# Cagou: desktop/mobile frontend for Salut à Toi XMPP client
# Copyright (C) 2016-2019 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from functools import partial
import mimetypes
import sys
from sat.core import log as logging
from sat.core.i18n import _
from sat.core import exceptions
from cagou.core.constants import Const as C
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import sp, dp
from kivy.clock import Clock
from kivy import properties
from sat_frontends.quick_frontend import quick_widgets
from sat_frontends.quick_frontend import quick_chat
from sat_frontends.tools import jid
from cagou.core import cagou_widget
from cagou.core import xmlui
from cagou.core.image import Image
from cagou.core.common import SymbolButton, JidButton
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from cagou import G
from cagou.core import menu

log = logging.getLogger(__name__)

PLUGIN_INFO = {
    "name": _(u"chat"),
    "main": "Chat",
    "description": _(u"instant messaging with one person or a group"),
    "icon_symbol": u"chat",
}

# FIXME: OTR specific code is legacy, and only used nowadays for lock color
# we can probably get rid of them.
OTR_STATE_UNTRUSTED = 'untrusted'
OTR_STATE_TRUSTED = 'trusted'
OTR_STATE_TRUST = (OTR_STATE_UNTRUSTED, OTR_STATE_TRUSTED)
OTR_STATE_UNENCRYPTED = 'unencrypted'
OTR_STATE_ENCRYPTED = 'encrypted'
OTR_STATE_ENCRYPTION = (OTR_STATE_UNENCRYPTED, OTR_STATE_ENCRYPTED)

SYMBOL_UNENCRYPTED = 'lock-open'
SYMBOL_ENCRYPTED = 'lock'
SYMBOL_ENCRYPTED_TRUSTED = 'lock-filled'
COLOR_UNENCRYPTED = (0.4, 0.4, 0.4, 1)
COLOR_ENCRYPTED = (0.4, 0.4, 0.4, 1)
COLOR_ENCRYPTED_TRUSTED = (0.29,0.87,0.0,1)


class MessAvatar(Image):
    pass


class MessageWidget(BoxLayout, quick_chat.MessageWidget):
    mess_data = properties.ObjectProperty()
    mess_xhtml = properties.ObjectProperty()
    mess_padding = (dp(5), dp(5))
    avatar = properties.ObjectProperty()
    delivery = properties.ObjectProperty()
    font_size = properties.NumericProperty(sp(12))

    def __init__(self, **kwargs):
        # self must be registered in widgets before kv is parsed
        kwargs['mess_data'].widgets.add(self)
        super(MessageWidget, self).__init__(**kwargs)
        avatar_path = self.mess_data.avatar
        if avatar_path is not None:
            self.avatar.source = avatar_path

    @property
    def chat(self):
        """return parent Chat instance"""
        return self.mess_data.parent

    def _get_message(self):
        """Return currently displayed message"""
        return self.mess_data.main_message

    def _set_message(self, message):
        if message == self.mess_data.message.get(u""):
            return False
        self.mess_data.message = {u"": message}
        return True

    message = properties.AliasProperty(_get_message, _set_message)

    @property
    def message_xhtml(self):
        """Return currently displayed message"""
        return self.mess_data.main_message_xhtml

    @property
    def info_type(self):
        return self.mess_data.info_type

    def widthAdjust(self):
        """this widget grows up with its children"""
        pass
        # parent = self.mess_xhtml.parent
        # padding_x = self.mess_padding[0]
        # text_width, text_height = self.mess_xhtml.texture_size
        # if text_width > parent.width:
        #     self.mess_xhtml.text_size = (parent.width - padding_x, None)
        #     self.text_max = text_width
        # elif self.mess_xhtml.text_size[0] is not None and text_width  < parent.width - padding_x:
        #     if text_width < self.text_max:
        #         self.mess_xhtml.text_size = (None, None)
        #     else:
        #         self.mess_xhtml.text_size = (parent.width  - padding_x, None)

    def update(self, update_dict):
        if 'avatar' in update_dict:
            self.avatar.source = update_dict['avatar']
        if 'status' in update_dict:
            status = update_dict['status']
            self.delivery.text =  u'\u2714' if status == 'delivered' else u''


class SendButton(SymbolButton):
    message_input_box = properties.ObjectProperty()


class MessageInputBox(BoxLayout):
    message_input = properties.ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MessageInputBox, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.post_init, 0)

    def post_init(self, *args):
        if sys.platform == 'android':
            self.add_widget(SendButton(message_input_box=self), 0)

    def send_text(self):
        self.message_input.send_text()


class MessageInputWidget(TextInput):

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        # We don't send text when shift is pressed to be able to add line feeds
        # (i.e. multi-lines messages). We don't send on Android either as the
        # send button appears on this platform.
        if (keycode[-1] == "enter"
            and "shift" not in modifiers
            and sys.platform != 'android'):
            self.send_text()
        else:
            return super(MessageInputWidget, self).keyboard_on_key_down(
                window, keycode, text, modifiers)

    def send_text(self):
        self.dispatch('on_text_validate')


class MessagesWidget(GridLayout):
    pass


class TransferButton(SymbolButton):
    chat = properties.ObjectProperty()

    def on_release(self, *args):
        menu.TransferMenu(callback=self.chat.onTransferOK).show(self)


class ExtraMenu(DropDown):
    chat = properties.ObjectProperty()

    def on_select(self, menu):
        if menu == 'bookmark':
            G.host.bridge.menuLaunch(C.MENU_GLOBAL, (u"groups", u"bookmarks"),
                                     {}, C.NO_SECURITY_LIMIT, self.chat.profile,
                                     callback=partial(
                                        G.host.actionManager, profile=self.chat.profile),
                                     errback=G.host.errback)
        else:
            raise exceptions.InternalError(u"Unknown menu: {}".format(menu))


class ExtraButton(SymbolButton):
    chat = properties.ObjectProperty()


class EncryptionMainButton(SymbolButton):

    def __init__(self, chat, **kwargs):
        """
        @param chat(Chat): Chat instance
        """
        self.chat = chat
        self.encryption_menu = EncryptionMenu(chat)
        super(EncryptionMainButton, self).__init__(**kwargs)
        self.bind(on_release=self.encryption_menu.open)

    def selectAlgo(self, name):
        """Mark an encryption algorithm as selected.

        This will also deselect all other button
        @param name(unicode, None): encryption plugin name
            None for plain text
        """
        buttons = self.encryption_menu.container.children
        buttons[-1].selected = name is None
        for button in buttons[:-1]:
            button.selected = button.text == name

    def getColor(self):
        if self.chat.otr_state_encryption == OTR_STATE_UNENCRYPTED:
            return  (0.4, 0.4, 0.4, 1)
        elif self.chat.otr_state_trust == OTR_STATE_TRUSTED:
            return (0.29,0.87,0.0,1)
        else:
            return  (0.4, 0.4, 0.4, 1)

    def getSymbol(self):
        if self.chat.otr_state_encryption == OTR_STATE_UNENCRYPTED:
            return 'lock-open'
        elif self.chat.otr_state_trust == OTR_STATE_TRUSTED:
            return 'lock-filled'
        else:
            return 'lock'


class TrustManagementButton(SymbolButton):
    pass


class EncryptionButton(BoxLayout):
    selected = properties.BooleanProperty(False)
    text = properties.StringProperty()
    trust_button = properties.BooleanProperty(False)
    best_width = properties.NumericProperty(0)

    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        self.register_event_type('on_trust_release')
        super(EncryptionButton, self).__init__(**kwargs)
        if self.trust_button:
            self.add_widget(TrustManagementButton())

    def on_release(self):
        pass

    def on_trust_release(self):
        pass


class EncryptionMenu(DropDown):
    # best with to display all algorithms buttons + trust buttons
    best_width = properties.NumericProperty(0)

    def __init__(self, chat, **kwargs):
        """
        @param chat(Chat): Chat instance
        """
        self.chat = chat
        super(EncryptionMenu, self).__init__(**kwargs)
        btn = EncryptionButton(
            text=_(u"unencrypted (plain text)"),
            on_release=self.unencrypted,
            selected=True,
            bold=False,
            )
        self.add_widget(btn)
        for plugin in G.host.encryption_plugins:
            btn = EncryptionButton(
                text=plugin[u'name'],
                on_release=partial(self.startEncryption, plugin=plugin),
                on_trust_release=partial(self.getTrustUI, plugin=plugin),
                trust_button=True,
                )
            self.add_widget(btn)
            log.info("added encryption: {}".format(plugin['name']))

    def messageEncryptionStopCb(self):
        log.info(_(u"Session with {destinee} is now in plain text").format(
            destinee = self.chat.target))

    def messageEncryptionStopEb(self, failure_):
        msg = _(u"Error while stopping encryption with {destinee}: {reason}").format(
            destinee = self.chat.target,
            reason = failure_)
        log.warning(msg)
        G.host.addNote(_(u"encryption problem"), msg, C.XMLUI_DATA_LVL_ERROR)

    def unencrypted(self, button):
        self.dismiss()
        G.host.bridge.messageEncryptionStop(
            unicode(self.chat.target),
            self.chat.profile,
            callback=self.messageEncryptionStopCb,
            errback=self.messageEncryptionStopEb)

    def messageEncryptionStartCb(self, plugin):
        log.info(_(u"Session with {destinee} is now encrypted with {encr_name}").format(
            destinee = self.chat.target,
            encr_name = plugin['name']))

    def messageEncryptionStartEb(self, failure_):
        msg = _(u"Session can't be encrypted with {destinee}: {reason}").format(
            destinee = self.chat.target,
            reason = failure_)
        log.warning(msg)
        G.host.addNote(_(u"encryption problem"), msg, C.XMLUI_DATA_LVL_ERROR)

    def startEncryption(self, button, plugin):
        """Request encryption with given plugin for this session

        @param button(EncryptionButton): button which has been pressed
        @param plugin(dict): plugin data
        """
        self.dismiss()
        G.host.bridge.messageEncryptionStart(
            unicode(self.chat.target),
            plugin['namespace'],
            True,
            self.chat.profile,
            callback=partial(self.messageEncryptionStartCb, plugin=plugin),
            errback=self.messageEncryptionStartEb)

    def encryptionTrustUIGetCb(self, xmlui_raw):
        xml_ui = xmlui.create(
            G.host, xmlui_raw, profile=self.chat.profile)
        xml_ui.show()

    def encryptionTrustUIGetEb(self, failure_):
        msg = _(u"Trust manager interface can't be retrieved: {reason}").format(
            reason = failure_)
        log.warning(msg)
        G.host.addNote(_(u"encryption trust management problem"), msg,
                       C.XMLUI_DATA_LVL_ERROR)

    def getTrustUI(self, button, plugin):
        """Request and display trust management UI

        @param button(EncryptionButton): button which has been pressed
        @param plugin(dict): plugin data
        """
        self.dismiss()
        G.host.bridge.encryptionTrustUIGet(
            unicode(self.chat.target),
            plugin['namespace'],
            self.chat.profile,
            callback=self.encryptionTrustUIGetCb,
            errback=self.encryptionTrustUIGetEb)

    def otr_start(self):
        self.dismiss()
        G.host.launchMenu(
            C.MENU_SINGLE,
            (u"otr", u"start/refresh"),
            {u'jid': unicode(self.chat.target)},
            None,
            C.NO_SECURITY_LIMIT,
            self.chat.profile
            )

    def otr_end(self):
        self.dismiss()
        G.host.launchMenu(
            C.MENU_SINGLE,
            (u"otr", u"end session"),
            {u'jid': unicode(self.chat.target)},
            None,
            C.NO_SECURITY_LIMIT,
            self.chat.profile
            )

    def otr_authenticate(self):
        self.dismiss()
        G.host.launchMenu(
            C.MENU_SINGLE,
            (u"otr", u"authenticate"),
            {u'jid': unicode(self.chat.target)},
            None,
            C.NO_SECURITY_LIMIT,
            self.chat.profile
            )


class Chat(quick_chat.QuickChat, cagou_widget.CagouWidget):
    message_input = properties.ObjectProperty()
    messages_widget = properties.ObjectProperty()

    def __init__(self, host, target, type_=C.CHAT_ONE2ONE, nick=None, occupants=None,
                 subject=None, profiles=None):
        quick_chat.QuickChat.__init__(
            self, host, target, type_, nick, occupants, subject, profiles=profiles)
        self.otr_state_encryption = OTR_STATE_UNENCRYPTED
        self.otr_state_trust = OTR_STATE_UNTRUSTED
        # completion attributes
        self._hi_comp_data = None
        self._hi_comp_last = None
        self._hi_comp_dropdown = DropDown()
        self._hi_comp_allowed = True
        cagou_widget.CagouWidget.__init__(self)
        transfer_btn = TransferButton(chat=self)
        self.headerInputAddExtra(transfer_btn)
        if type_ == C.CHAT_ONE2ONE:
            self.encryption_btn = EncryptionMainButton(self)
            self.headerInputAddExtra(self.encryption_btn)
        self.extra_menu = ExtraMenu(chat=self)
        extra_btn = ExtraButton(chat=self)
        self.headerInputAddExtra(extra_btn)
        self.header_input.hint_text = u"{}".format(target)
        self.postInit()

    def __unicode__(self):
        return u"Chat({})".format(self.target)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __repr__(self):
        return self.__str__()

    @classmethod
    def factory(cls, plugin_info, target, profiles):
        profiles = list(profiles)
        if len(profiles) > 1:
            raise NotImplementedError(u"Multi-profiles is not available yet for chat")
        if target is None:
            target = G.host.profiles[profiles[0]].whoami
        return G.host.widgets.getOrCreateWidget(cls, target, on_new_widget=None,
                                                on_existing_widget=G.host.getOrClone,
                                                profiles=profiles)

    @property
    def message_widgets_rev(self):
        return self.messages_widget.children

    ## header ##

    def changeWidget(self, jid_):
        """change current widget for a new one with given jid

        @param jid_(jid.JID): jid of the widget to create
        """
        plugin_info = G.host.getPluginInfo(main=Chat)
        factory = plugin_info['factory']
        G.host.switchWidget(self, factory(plugin_info, jid_, profiles=[self.profile]))
        self.header_input.text = ''

    def onHeaderInput(self):
        text = self.header_input.text.strip()
        try:
            if text.count(u'@') != 1 or text.count(u' '):
                raise ValueError
            jid_ = jid.JID(text)
        except ValueError:
            log.info(u"entered text is not a jid")
            return

        def discoCb(disco):
            # TODO: check if plugin XEP-0045 is activated
            if "conference" in [i[0] for i in disco[1]]:
                G.host.bridge.mucJoin(unicode(jid_), "", "", self.profile,
                                      callback=self._mucJoinCb, errback=self._mucJoinEb)
            else:
                self.changeWidget(jid_)

        def discoEb(failure):
            log.warning(u"Disco failure, ignore this text: {}".format(failure))

        G.host.bridge.discoInfos(jid_.domain, self.profile, callback=discoCb,
                                 errback=discoEb)

    def onHeaderInputCompleted(self, input_wid, completed_text):
        self._hi_comp_allowed = False
        input_wid.text = completed_text
        self._hi_comp_allowed = True
        self._hi_comp_dropdown.dismiss()
        self.onHeaderInput()

    def onHeaderInputComplete(self, wid, text):
        if not self._hi_comp_allowed:
            return
        text = text.lstrip()
        if not text:
            self._hi_comp_data = None
            self._hi_comp_last = None
            self._hi_comp_dropdown.dismiss()
            return

        profile = list(self.profiles)[0]

        if self._hi_comp_data is None:
            # first completion, we build the initial list
            comp_data = self._hi_comp_data = []
            self._hi_comp_last = ''
            for jid_, jid_data in G.host.contact_lists[profile].all_iter:
                comp_data.append((jid_, jid_data))
            comp_data.sort(key=lambda datum: datum[0])
        else:
            comp_data = self._hi_comp_data

        # XXX: dropdown is rebuilt each time backspace is pressed or if the text is changed,
        #      it works OK, but some optimisation may be done here
        dropdown = self._hi_comp_dropdown

        if not text.startswith(self._hi_comp_last) or not self._hi_comp_last:
            # text has changed or backspace has been pressed, we restart
            dropdown.clear_widgets()

            for jid_, jid_data in comp_data:
                nick = jid_data.get(u'nick', u'')
                if text in jid_.bare or text in nick.lower():
                    btn = JidButton(
                        jid = jid_.bare,
                        profile = profile,
                        size_hint = (0.5, None),
                        nick = nick,
                        on_release=lambda __, txt=jid_.bare: self.onHeaderInputCompleted(wid, txt)
                        )
                    dropdown.add_widget(btn)
        else:
            # more chars, we continue completion by removing unwanted widgets
            to_remove = []
            for c in dropdown.children[0].children:
                if text not in c.jid and text not in (c.nick or ''):
                    to_remove.append(c)
            for c in to_remove:
                dropdown.remove_widget(c)
        if dropdown.attach_to is None:
            dropdown.open(wid)
        self._hi_comp_last = text

    def messageDataConverter(self, idx, mess_id):
        return {"mess_data": self.messages[mess_id]}

    def _onHistoryPrinted(self):
        """Refresh or scroll down the focus after the history is printed"""
        # self.adapter.data = self.messages
        for mess_data in self.messages.itervalues():
            self.appendMessage(mess_data)
        super(Chat, self)._onHistoryPrinted()

    def createMessage(self, message):
        self.appendMessage(message)

    def appendMessage(self, mess_data):
        """Append a message Widget to the history

        @param mess_data(quick_chat.Message): message data
        """
        if self.handleUserMoved(mess_data):
            return
        self.messages_widget.add_widget(MessageWidget(mess_data=mess_data))
        self.notify(mess_data)

    def _get_notif_msg(self, mess_data):
        return _(u"{nick}: {message}").format(
            nick=mess_data.nick,
            message=mess_data.main_message)

    def notify(self, mess_data):
        """Notify user when suitable

        For one2one chat, notification will happen when window has not focus
        or when one2one chat is not visible. A note is also there when widget
        is not visible.
        For group chat, note will be added on mention, with a desktop notification if
        window has not focus.
        """
        visible_clones = [w for w in G.host.getVisibleList(self.__class__)
                          if w.target == self.target]
        if len(visible_clones) > 1 and visible_clones.index(self) > 0:
            # to avoid multiple notifications in case of multiple cloned widgets
            # we only handle first clone
            return
        is_visible = bool(visible_clones)
        if self.type == C.CHAT_ONE2ONE:
            if (not Window.focus or not is_visible) and not mess_data.history:
                notif_msg = self._get_notif_msg(mess_data)
                G.host.desktop_notif(
                    notif_msg,
                    title=_(u"private message"))
                if not is_visible:
                    G.host.addNote(
                        _(u"private message"),
                        notif_msg,
                        symbol = u"chat",
                        action = {
                            "action": u'chat',
                            "target": self.target,
                            "profiles": self.profiles}
                        )
        else:
            if mess_data.mention and not mess_data.history:
                notif_msg = self._get_notif_msg(mess_data)
                G.host.addNote(
                    _(u"mention"),
                    notif_msg,
                    symbol = u"chat",
                    action = {
                        "action": u'chat',
                        "target": self.target,
                        "profiles": self.profiles}
                    )
                if not Window.focus:
                    G.host.desktop_notif(
                        notif_msg,
                        title=_(u"mention ({room_jid})").format(
                            room_jid=self.target)
                        )

    def onSend(self, input_widget):
        G.host.messageSend(
            self.target,
            {'': input_widget.text}, # TODO: handle language
            mess_type = (C.MESS_TYPE_GROUPCHAT
                if self.type == C.CHAT_GROUP else C.MESS_TYPE_CHAT), # TODO: put this in QuickChat
            profile_key=self.profile
            )
        input_widget.text = ''

    def fileTransferEb(self, err_msg, cleaning_cb, profile):
        if cleaning_cb is not None:
            cleaning_cb()
        msg = _(u"can't transfer file: {reason}").format(reason=err_msg)
        log.warning(msg)
        G.host.addNote(_(u"File transfer error"),
                       msg,
                       level=C.XMLUI_DATA_LVL_WARNING)

    def fileTransferCb(self, metadata, cleaning_cb, profile):
        log.debug("file transfered: {}".format(metadata))
        extra = {}

        # FIXME: Q&D way of getting file type, upload plugins shouls give it
        mime_type = mimetypes.guess_type(metadata['url'])[0]
        if mime_type is not None:
            if mime_type.split(u'/')[0] == 'image':
                # we generate url ourselves, so this formatting is safe
                extra['xhtml'] = u"<img src='{url}' />".format(**metadata)

        G.host.messageSend(
            self.target,
            {'': metadata['url']},
            mess_type = (C.MESS_TYPE_GROUPCHAT
                if self.type == C.CHAT_GROUP else C.MESS_TYPE_CHAT),
            extra = extra,
            profile_key=profile
            )

    def onTransferOK(self, file_path, cleaning_cb, transfer_type):
        if transfer_type == C.TRANSFER_UPLOAD:

            G.host.bridge.fileUpload(
                file_path,
                "",
                "",
                {"ignore_tls_errors": C.boolConst(not G.host.tls_validation)},
                self.profile,
                callback = partial(
                    G.host.actionManager,
                    progress_cb = partial(self.fileTransferCb, cleaning_cb=cleaning_cb),
                    progress_eb = partial(self.fileTransferEb, cleaning_cb=cleaning_cb),
                    profile = self.profile,
                    ),
                errback = partial(G.host.errback,
                                  message=_(u"can't upload file: {msg}"))
            )
        elif transfer_type == C.TRANSFER_SEND:
            if self.type == C.CHAT_GROUP:
                log.warning(u"P2P transfer is not possible for group chat")
                # TODO: show an error dialog to user, or better hide the send button for
                #       MUC
            else:
                jid_ = self.target
                if not jid_.resource:
                    jid_ = G.host.contact_lists[self.profile].getFullJid(jid_)
                G.host.bridge.fileSend(unicode(jid_), file_path, "", "", {},
                                       profile=self.profile)
                # TODO: notification of sending/failing
        else:
            raise log.error(u"transfer of type {} are not handled".format(transfer_type))

    def messageEncryptionStarted(self, plugin_data):
        quick_chat.QuickChat.messageEncryptionStarted(self, plugin_data)
        self.encryption_btn.symbol = SYMBOL_ENCRYPTED
        self.encryption_btn.color = COLOR_ENCRYPTED
        self.encryption_btn.selectAlgo(plugin_data[u'name'])

    def messageEncryptionStopped(self, plugin_data):
        quick_chat.QuickChat.messageEncryptionStopped(self, plugin_data)
        self.encryption_btn.symbol = SYMBOL_UNENCRYPTED
        self.encryption_btn.color = COLOR_UNENCRYPTED
        self.encryption_btn.selectAlgo(None)

    def _mucJoinCb(self, joined_data):
        joined, room_jid_s, occupants, user_nick, subject, profile = joined_data
        self.host.mucRoomJoinedHandler(*joined_data[1:])
        jid_ = jid.JID(room_jid_s)
        self.changeWidget(jid_)

    def _mucJoinEb(self, failure):
        log.warning(u"Can't join room: {}".format(failure))

    def onOTRState(self, state, dest_jid, profile):
        assert profile in self.profiles
        if state in OTR_STATE_ENCRYPTION:
            self.otr_state_encryption = state
        elif state in OTR_STATE_TRUST:
            self.otr_state_trust = state
        else:
            log.error(_(u"Unknown OTR state received: {}".format(state)))
            return
        self.encryption_btn.symbol = self.encryption_btn.getSymbol()
        self.encryption_btn.color = self.encryption_btn.getColor()

    def onVisible(self):
        if not self.sync:
            self.resync()

    def onDelete(self):
        # we always keep one widget, so it's available when swiping
        # TODO: delete all widgets when chat is closed
        nb_instances = sum(1 for _ in self.host.widgets.getWidgetInstances(self))
        if nb_instances > 1:
            return super(Chat, self).onDelete()
        else:
            return False


PLUGIN_INFO["factory"] = Chat.factory
quick_widgets.register(quick_chat.QuickChat, Chat)
