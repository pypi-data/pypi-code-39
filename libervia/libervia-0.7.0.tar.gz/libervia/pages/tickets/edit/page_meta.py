#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from libervia.server.constants import Const as C
from sat.core.i18n import _
from twisted.internet import defer
from sat.tools.common import template_xmlui
from sat.tools.common import data_format
from sat.core.log import getLogger

log = getLogger(__name__)
"""ticket handling pages"""

name = u"tickets_edit"
access = C.PAGES_ACCESS_PROFILE
template = u"ticket/edit.html"


def parse_url(self, request):
    try:
        item_id = self.nextPath(request)
    except IndexError:
        log.warning(_(u"no ticket id specified"))
        self.pageError(request, C.HTTP_BAD_REQUEST)

    data = self.getRData(request)
    data[u"ticket_id"] = item_id


@defer.inlineCallbacks
def prepare_render(self, request):
    data = self.getRData(request)
    template_data = request.template_data
    service, node, ticket_id = (
        data.get(u"service", u""),
        data.get(u"node", u""),
        data[u"ticket_id"],
    )
    profile = self.getProfile(request)

    # we don't ignore "author" below to keep it when a ticket is edited
    # by node owner/admin and "consistent publisher" is activated
    ignore = (
        "publisher",
        "author",
        "author_jid",
        "author_email",
        "created",
        "updated",
        "comments_uri",
    )
    tickets = yield self.host.bridgeCall(
        "ticketsGet",
        service.full() if service else u"",
        node,
        C.NO_LIMIT,
        [ticket_id],
        "",
        {},
        profile,
    )
    ticket = [template_xmlui.create(self.host, x, ignore=ignore) for x in tickets[0]][0]

    try:
        # small trick to get a one line text input instead of the big textarea
        ticket.widgets[u"labels"].type = u"string"
        ticket.widgets[u"labels"].value = ticket.widgets[u"labels"].value.replace(
            u"\n", ", "
        )
    except KeyError:
        pass

    # for now we don't have XHTML editor, so we'll go with a TextBox and a convertion
    # to a text friendly syntax using markdown
    wid = ticket.widgets[u'body']
    if wid.type == u"xhtmlbox":
        wid.type = u"textbox"
        wid.value =  yield self.host.bridgeCall(
            u"syntaxConvert", wid.value, C.SYNTAX_XHTML, u"markdown",
            False, profile)

    template_data[u"new_ticket_xmlui"] = ticket


@defer.inlineCallbacks
def on_data_post(self, request):
    data = self.getRData(request)
    service = data["service"]
    node = data["node"]
    ticket_id = data["ticket_id"]
    posted_data = self.getAllPostedData(request)
    if not posted_data["title"] or not posted_data["body"]:
        self.pageError(request, C.HTTP_BAD_REQUEST)
    try:
        posted_data["labels"] = [l.strip() for l in posted_data["labels"][0].split(",")]
    except (KeyError, IndexError):
        pass
    profile = self.getProfile(request)

    # we convert back body to XHTML
    body = yield self.host.bridgeCall(
        u"syntaxConvert", posted_data[u'body'][0], u"markdown", C.SYNTAX_XHTML,
        False, profile)
    posted_data[u'body'] = [u'<div xmlns="{ns}">{body}</div>'.format(ns=C.NS_XHTML,
                                                                     body=body)]

    extra = {u'update': True}
    yield self.host.bridgeCall(
        "ticketSet", service.full(), node, posted_data, u"", ticket_id,
        data_format.serialise(extra), profile
    )
    # we don't want to redirect to edit page on success, but to tickets list
    data["post_redirect_page"] = (
        self.getPageByName(u"tickets"),
        service.full(),
        node or u"@",
    )
