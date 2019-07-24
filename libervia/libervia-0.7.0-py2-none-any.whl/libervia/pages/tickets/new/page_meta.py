#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from libervia.server.constants import Const as C
from twisted.internet import defer
from sat.tools.common import template_xmlui
from sat.core.log import getLogger

log = getLogger(__name__)
"""ticket handling pages"""

name = u"tickets_new"
access = C.PAGES_ACCESS_PROFILE
template = u"ticket/create.html"


@defer.inlineCallbacks
def prepare_render(self, request):
    data = self.getRData(request)
    template_data = request.template_data
    service, node = data.get(u"service", u""), data.get(u"node", u"")
    profile = self.getProfile(request)
    schema = yield self.host.bridgeCall("ticketsSchemaGet", service.full(), node, profile)
    data["schema"] = schema
    # following fields are handled in backend
    ignore = (
        "author",
        "author_jid",
        "author_email",
        "created",
        "updated",
        "comments_uri",
        "status",
        "milestone",
        "priority",
    )
    xmlui_obj = template_xmlui.create(self.host, schema, ignore=ignore)
    try:
        # small trick to get a one line text input instead of the big textarea
        xmlui_obj.widgets[u"labels"].type = u"string"
    except KeyError:
        pass

    # same as for tickets_edit, we have to convert for now
    wid = xmlui_obj.widgets[u'body']
    if wid.type == u"xhtmlbox":
        wid.type = u"textbox"
        wid.value =  yield self.host.bridgeCall(
            u"syntaxConvert", wid.value, C.SYNTAX_XHTML, u"markdown",
            False, profile)
    template_data[u"new_ticket_xmlui"] = xmlui_obj


@defer.inlineCallbacks
def on_data_post(self, request):
    data = self.getRData(request)
    service = data["service"]
    node = data["node"]
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


    yield self.host.bridgeCall(
        "ticketSet", service.full(), node, posted_data, u"", u"", u"", profile
    )
    # we don't want to redirect to creation page on success, but to tickets list
    data["post_redirect_page"] = (
        self.getPageByName(u"tickets"),
        service.full(),
        node or u"@",
    )
