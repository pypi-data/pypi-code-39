#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from libervia.server.constants import Const as C
from twisted.internet import defer
from sat.core.i18n import _
from sat.core.log import getLogger

log = getLogger(__name__)

name = u"photos"
access = C.PAGES_ACCESS_PROFILE
template = u"photo/discover.html"


@defer.inlineCallbacks
def prepare_render(self, request):
    profile = self.getProfile(request)
    template_data = request.template_data
    namespace = self.host.ns_map["fis"]
    if profile is not None:
        try:
            interests = yield self.host.bridgeCall(
                "interestsList", "", "", namespace, profile)
        except Exception:
            log.warning(_(u"Can't get interests list for {profile}").format(
                profile=profile))
        else:
            # we only want photo albums
            filtered_interests = []
            for interest in interests:
                if interest.get(u'subtype') != u'photos':
                    continue
                path = interest.get(u'path', u'')
                path_args = [p for p in path.split(u'/') if p]
                interest["url"] = self.getSubPageURL(
                    request,
                    u"photos_album",
                    interest[u'service'],
                    *path_args
                )
                filtered_interests.append(interest)

            template_data[u'interests'] = filtered_interests


@defer.inlineCallbacks
def on_data_post(self, request):
    jid_ = self.getPostedData(request, u"jid")
    url = self.getPageByName(u"photos_album").getURL(jid_)
    self.HTTPRedirect(request, url)
