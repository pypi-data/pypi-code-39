#!/usr/bin/env python2
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

"""common advanced widgets, which can be reused everywhere."""

from sat.core.i18n import _
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from cagou.core.menu import TouchMenuItemBehaviour
from kivy import properties
from kivy.metrics import dp
from cagou import G
from sat.core import log as logging

log = logging.getLogger(__name__)


class Identities(object):

    def __init__(self, entity_ids):
        identities = {}
        for cat, type_, name in entity_ids:
            identities.setdefault(cat, {}).setdefault(type_, []).append(name)
        client = identities.get('client', {})
        if 'pc' in client:
            self.type = 'desktop'
        elif 'phone' in client:
            self.type = 'phone'
        elif 'web' in client:
            self.type = 'web'
        elif 'console' in client:
            self.type = 'console'
        else:
            self.type = 'desktop'

        self.identities = identities

    @property
    def name(self):
        return self.identities.values()[0].values()[0][0]


class ItemWidget(TouchMenuItemBehaviour, BoxLayout):
    name = properties.StringProperty()
    base_width = properties.NumericProperty(dp(100))


class DeviceWidget(ItemWidget):

    def __init__(self, main_wid, entity_jid, identities, **kw):
        self.entity_jid = entity_jid
        self.identities = identities
        own_jid = next(G.host.profiles.itervalues()).whoami
        self.own_device = entity_jid.bare == own_jid
        if self.own_device:
            name = self.identities.name
        elif self.entity_jid.node:
            name = self.entity_jid.node
        elif self.entity_jid == own_jid.domain:
            name = _(u"your server")
        else:
            name = entity_jid

        super(DeviceWidget, self).__init__(name=name, main_wid=main_wid, **kw)

    @property
    def profile(self):
        return self.main_wid.profile

    def getSymbol(self):
        if self.identities.type == 'desktop':
            return 'desktop'
        elif self.identities.type == 'phone':
            return 'mobile'
        elif self.identities.type == 'web':
            return 'globe'
        elif self.identities.type == 'console':
            return 'terminal'
        else:
            return 'desktop'

    def do_item_action(self, touch):
        pass


class CategorySeparator(Label):
    pass
