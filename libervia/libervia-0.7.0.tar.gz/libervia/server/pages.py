#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011-2019 Jérôme Poisson <goffi@goffi.org>

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
from twisted.web import server
from twisted.web import resource as web_resource
from twisted.web import util as web_util
from twisted.internet import defer
from twisted.words.protocols.jabber import jid
from twisted.python import failure

from sat.core.i18n import _
from sat.core import exceptions
from sat.tools.common import date_utils
from sat.core.log import getLogger
from sat_frontends.bridge.bridge_frontend import BridgeException

from libervia.server.constants import Const as C
from libervia.server import session_iface
from libervia.server.utils import quote, SubPage
from libervia.server.classes import WebsocketMeta

import uuid
import os.path
import urllib
import time
import hashlib
import copy

log = getLogger(__name__)


class CacheBase(object):
    def __init__(self):
        self._created = time.time()
        self._last_access = self._created

    @property
    def created(self):
        return self._created

    @property
    def last_access(self):
        return self._last_access

    @last_access.setter
    def last_access(self, timestamp):
        self._last_access = timestamp


class CachePage(CacheBase):
    def __init__(self, rendered):
        super(CachePage, self).__init__()
        self._created = time.time()
        self._last_access = self._created
        self._rendered = rendered
        self._hash = hashlib.sha256(rendered).hexdigest()

    @property
    def rendered(self):
        return self._rendered

    @property
    def hash(self):
        return self._hash


class CacheURL(CacheBase):
    def __init__(self, request):
        super(CacheURL, self).__init__()
        try:
            self._data = copy.deepcopy(request.data)
        except AttributeError:
            self._data = {}
        self._template_data = copy.deepcopy(request.template_data)
        self._prepath = request.prepath[:]
        self._postpath = request.postpath[:]
        del self._template_data["csrf_token"]

    def use(self, request):
        self.last_access = time.time()
        request.data = copy.deepcopy(self._data)
        request.template_data.update(copy.deepcopy(self._template_data))
        request.prepath = self._prepath[:]
        request.postpath = self._postpath[:]


class LiberviaPage(web_resource.Resource):
    isLeaf = True  #  we handle subpages ourself
    signals_handlers = {}
    cache = {}
    #  Set of tuples (service/node/sub_id) of nodes subscribed for caching
    # sub_id can be empty string if not handled by service
    cache_pubsub_sub = set()

    def __init__(
        self, host, vhost_root, root_dir, url, name=None, redirect=None, access=None,
        dynamic=False, parse_url=None, prepare_render=None, render=None, template=None,
        on_data_post=None, on_data=None, on_signal=None, url_cache=False,
        replace_on_conflict=False
        ):
        """Initiate LiberviaPage instance

        LiberviaPages are the main resources of Libervia, using easy to set python files
        The non mandatory arguments are the variables found in page_meta.py
        @param host(Libervia): the running instance of Libervia
        @param vhost_root(web_resource.Resource): root resource of the virtual host which
            handle this page.
        @param root_dir(unicode): aboslute file path of the page
        @param url(unicode): relative URL to the page
            this URL may not be valid, as pages may require path arguments
        @param name(unicode, None): if not None, a unique name to identify the page
            can then be used for e.g. redirection
            "/" is not allowed in names (as it can be used to construct URL paths)
        @param redirect(unicode, None): if not None, this page will be redirected.
            A redirected parameter is used as in self.pageRedirect.
            parse_url will not be skipped
            using this redirect parameter is called "full redirection"
            using self.pageRedirect is called "partial redirection" (because some
            rendering method can still be used, e.g. parse_url)
        @param access(unicode, None): permission needed to access the page
            None means public access.
            Pages inherit from parent pages: e.g. if a "settings" page is restricted
            to admins, and if "settings/blog" is public, it still can only be accessed by
            admins. See C.PAGES_ACCESS_* for details
        @param dynamic(bool): if True, activate websocket for bidirectional communication
        @param parse_url(callable, None): if set it will be called to handle the URL path
            after this method, the page will be rendered if noting is left in path
            (request.postpath) else a the request will be transmitted to a subpage
        @param prepare_render(callable, None): if set, will be used to prepare the
            rendering. That often means gathering data using the bridge
        @param render(callable, None): if not template is set, this method will be
            called and what it returns will be rendered.
            This method is mutually exclusive with template and must return a unicode
            string.
        @param template(unicode, None): path to the template to render.
            This method is mutually exclusive with render
        @param on_data_post(callable, None): method to call when data is posted
            None if data post is not handled
            on_data_post can return a string with following value:
                - C.POST_NO_CONFIRM: confirm flag will not be set
            on_data_post can raise following exceptions:
                - exceptions.DataError: value is incorrect, message will be displayed
                    as a notification
        @param on_data(callable, None): method to call when dynamic data is sent
            this method is used with Libervia's websocket mechanism
        @param on_signal(callable, None): method to call when a registered signal is
            received. This method is used with Libervia's websocket mechanism
        @param url_cache(boolean): if set, result of parse_url is cached (per profile).
            Useful when costly calls (e.g. network) are done while parsing URL.
        @param replace_on_conflict(boolean): if True, don't raise ConflictError if a
            page of this name already exists, but replace it
        """

        web_resource.Resource.__init__(self)
        self.host = host
        self.vhost_root = vhost_root
        self.root_dir = root_dir
        self.url = url
        self.name = name
        if name is not None:
            if (name in self.named_pages
                and not (replace_on_conflict and self.named_pages[name].url == url)):
                raise exceptions.ConflictError(
                    _(u'a Libervia page named "{}" already exists'.format(name)))
            if u"/" in name:
                raise ValueError(_(u'"/" is not allowed in page names'))
            if not name:
                raise ValueError(_(u"a page name can't be empty"))
            self.named_pages[name] = self
        if access is None:
            access = C.PAGES_ACCESS_PUBLIC
        if access not in (
            C.PAGES_ACCESS_PUBLIC,
            C.PAGES_ACCESS_PROFILE,
            C.PAGES_ACCESS_NONE,
        ):
            raise NotImplementedError(
                _(u"{} access is not implemented yet").format(access)
            )
        self.access = access
        self.dynamic = dynamic
        if redirect is not None:
            # only page access and name make sense in case of full redirection
            # so we check that rendering methods/values are not set
            if not all(
                lambda x: x is not None
                for x in (parse_url, prepare_render, render, template)
            ):
                raise ValueError(
                    _(u"you can't use full page redirection with other rendering"
                      u"method, check self.pageRedirect if you need to use them"))
            self.redirect = redirect
        else:
            self.redirect = None
        self.parse_url = parse_url
        self.prepare_render = prepare_render
        self.template = template
        self.render_method = render
        self.on_data_post = on_data_post
        self.on_data = on_data
        self.on_signal = on_signal
        self.url_cache = url_cache
        if access == C.PAGES_ACCESS_NONE:
            # none pages just return a 404, no further check is needed
            return
        if template is not None and render is not None:
            log.error(_(u"render and template methods can't be used at the same time"))
        if parse_url is not None and not callable(parse_url):
            log.error(_(u"parse_url must be a callable"))

        # if not None, next rendering will be cached
        #  it must then contain a list of the the keys to use (without the page instance)
        # e.g. [C.SERVICE_PROFILE, "pubsub", server@example.tld, pubsub_node]
        self._do_cache = None

    def __unicode__(self):
        return u"LiberviaPage {name} at {url} (vhost: {vhost_root})".format(
            name=self.name or u"<anonymous>", url=self.url, vhost_root=self.vhost_root)

    def __str__(self):
        return self.__unicode__().encode("utf-8")


    @property
    def named_pages(self):
        return self.vhost_root.named_pages

    @property
    def uri_callbacks(self):
        return self.vhost_root.uri_callbacks

    @property
    def pages_redirects(self):
        return self.vhost_root.pages_redirects

    @property
    def cached_urls(self):
        return self.vhost_root.cached_urls

    @property
    def main_menu(self):
        return self.vhost_root.main_menu

    @staticmethod
    def createPage(host, meta_path, vhost_root, url_elts, replace_on_conflict=False):
        """Create a LiberviaPage instance

        @param meta_path(unicode): path to the page_meta.py file
        @param vhost_root(resource.Resource): root resource of the virtual host
        @param url_elts(list[unicode]): list of path element from root site to this page
        @param replace_on_conflict(bool): same as for [LiberviaPage]
        @return (tuple[dict, LiberviaPage]): tuple with:
            - page_data: dict containing data of the page
            - libervia_page: created resource
        """
        dir_path = os.path.dirname(meta_path)
        page_data = {"__name__": u".".join([u"page"] + url_elts)}
        # we don't want to force the presence of __init__.py
        # so we use execfile instead of import.
        # TODO: when moved to Python 3, __init__.py is not mandatory anymore
        #       so we can switch to import
        execfile(meta_path, page_data)
        return page_data, LiberviaPage(
            host=host,
            vhost_root=vhost_root,
            root_dir=dir_path,
            url=u"/" + u"/".join(url_elts),
            name=page_data.get(u"name"),
            redirect=page_data.get(u"redirect"),
            access=page_data.get(u"access"),
            dynamic=page_data.get(u"dynamic", False),
            parse_url=page_data.get(u"parse_url"),
            prepare_render=page_data.get(u"prepare_render"),
            render=page_data.get(u"render"),
            template=page_data.get(u"template"),
            on_data_post=page_data.get(u"on_data_post"),
            on_data=page_data.get(u"on_data"),
            on_signal=page_data.get(u"on_signal"),
            url_cache=page_data.get(u"url_cache", False),
            replace_on_conflict=replace_on_conflict
        )

    @classmethod
    def importPages(cls, host, vhost_root, root_path=None, _parent=None, _path=None,
        _extra_pages=False):
        """Recursively import Libervia pages

        @param host(Libervia): Libervia instance
        @param vhost_root(LiberviaRootResource): root of this VirtualHost
        @param root_path(unicode, None): use this root path instead of vhost_root's one
            Used to add default site pages to external sites
        @param _parent(Resource, None): _parent page. Do not set yourself, this is for
            internal use only
        @param _path(list(unicode), None): current path. Do not set yourself, this is for
            internal use only
        @param _extra_pages(boolean): set to True when extra pages are used (i.e.
            root_path is set). Do not set yourself, this is for internal use only
        """
        if _path is None:
            _path = []
        if _parent is None:
            if root_path is None:
                root_dir = os.path.join(vhost_root.site_path, C.PAGES_DIR)
            else:
                root_dir = os.path.join(root_path, C.PAGES_DIR)
                _extra_pages = True
            _parent = vhost_root
        else:
            root_dir = _parent.root_dir
        for d in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, d)
            if not os.path.isdir(dir_path):
                continue
            if _extra_pages and d in _parent.children:
                log.debug(_(u"[{host_name}] {path} is already present, ignoring it")
                    .format(host_name=vhost_root.host_name, path=u'/'.join(_path+[d])))
                continue
            meta_path = os.path.join(dir_path, C.PAGES_META_FILE)
            if os.path.isfile(meta_path):
                new_path = _path + [d]
                try:
                    page_data, resource = cls.createPage(host, meta_path, vhost_root, new_path)
                except exceptions.ConflictError as e:
                    if _extra_pages:
                        # extra pages are discarded if there is already an existing page
                        continue
                    else:
                        raise e
                _parent.putChild(d, resource)
                log_msg = (u"[{host_name}] Added /{path} page".format(
                    host_name=vhost_root.host_name,
                    path=u"[…]/".join(new_path)))
                if _extra_pages:
                    log.debug(log_msg)
                else:
                    log.info(log_msg)
                if "uri_handlers" in page_data:
                    if not isinstance(page_data, dict):
                        log.error(_(u"uri_handlers must be a dict"))
                    else:
                        for uri_tuple, cb_name in page_data["uri_handlers"].iteritems():
                            if len(uri_tuple) != 2 or not isinstance(cb_name, basestring):
                                log.error(_(u"invalid uri_tuple"))
                                continue
                            if not _extra_pages:
                                log.info(_(u"setting {}/{} URIs handler")
                                         .format(*uri_tuple))
                            try:
                                cb = page_data[cb_name]
                            except KeyError:
                                log.error(_(u"missing {name} method to handle {1}/{2}")
                                          .format(name=cb_name, *uri_tuple))
                                continue
                            else:
                                resource.registerURI(uri_tuple, cb)

                LiberviaPage.importPages(
                    host, vhost_root, _parent=resource, _path=new_path,
                    _extra_pages=_extra_pages)

    @classmethod
    def onFileChange(cls, host, file_path, flags, site_root, site_path):
        """Method triggered by file_watcher when something is changed in files

        This method is used in dev mode to reload pages when needed
        @param file_path(filepath.FilePath): path of the file which triggered the event
        @param flags[list[unicode]): human readable flags of the event (from
            internet.inotify)
        @param site_root(LiberviaRootResource): root of the site
        @param site_path(unicode): absolute path of the site
        """
        if flags == ['create']:
            return
        path = file_path.path.decode('utf-8')
        base_name = os.path.basename(path)
        if base_name != u"page_meta.py":
            # we only handle libervia pages
            return

        log.debug(u"{flags} event(s) received for {file_path}".format(
            flags=u", ".join(flags), file_path=file_path))

        dir_path = os.path.dirname(path)
        if not dir_path.startswith(site_path):
            raise exceptions.InternalError(u"watched file should start with site path")

        path_elts = [p for p in dir_path[len(site_path):].split('/') if p]
        if not path_elts:
            return

        if path_elts[0] == C.PAGES_DIR:
            # a page has been modified
            del path_elts[0]
            if not path_elts:
                # we need at least one element to parse
                return
            # we retrieve page by starting from site root and finding each path element
            parent = page = site_root
            new_page = False
            for idx, child_name in enumerate(path_elts):
                try:
                    try:
                        page = page.original.children[child_name]
                    except AttributeError:
                        page = page.children[child_name]
                except KeyError:
                    if idx != len(path_elts)-1:
                        # a page has been created in a subdir when one or more
                        # page_meta.py are missing on the way
                        log.warning(_(u"Can't create a page at {path}, missing parents")
                                    .format(path=path))
                        return
                    new_page = True
                else:
                    if idx<len(path_elts)-1:
                        parent = page.original

            try:
                # we (re)create a page with the new/modified code
                __, resource = cls.createPage(host, path, site_root, path_elts,
                                              replace_on_conflict=True)
                if not new_page:
                    try:
                        resource.children = page.original.children
                    except AttributeError:
                        # FIXME: this .original handling madness is due to EncodingResourceWrapper
                        #        EncodingResourceWrapper should probably be removed
                        resource.children = page.children
            except Exception as e:
                log.warning(_(u"Can't create page: {reason}").format(reason=e))
            else:
                url_elt = path_elts[-1]
                if not new_page:
                    # the page was already existing, we remove it
                    del parent.children[url_elt]
                # we can now add the new page
                parent.putChild(url_elt, resource)
                if new_page:
                    log.info(_(u"{page} created").format(page=resource))
                else:
                    log.info(_(u"{page} reloaded").format(page=resource))

    def registerURI(self, uri_tuple, get_uri_cb):
        """Register a URI handler

        @param uri_tuple(tuple[unicode, unicode]): type or URIs handler
            type/subtype as returned by tools/common/parseXMPPUri
            or type/None to handle all subtypes
        @param get_uri_cb(callable): method which take uri_data dict as only argument
            and return absolute path with correct arguments or None if the page
            can't handle this URL
        """
        if uri_tuple in self.uri_callbacks:
            log.info(_(u"{}/{} URIs are already handled, replacing by the new handler")
                .format( *uri_tuple))
        self.uri_callbacks[uri_tuple] = (self, get_uri_cb)

    def getSignalId(self, request):
        """Retrieve signal_id for a request

        signal_id is used for dynamic page, to associate a initial request with a
        signal handler. For WebsocketRequest, signal_id attribute is used (which must
        be orginal request's id)
        For server.Request it's id(request)
        """
        return getattr(request, 'signal_id', id(request))

    def registerSignal(self, request, signal, check_profile=True):
        r"""register a signal handler

        the page must be dynamic
        when signal is received, self.on_signal will be called with:
            - request
            - signal name
            - signal arguments
        signal handler will be removed when connection with dynamic page will be lost
        @param signal(unicode): name of the signal
            last arg of signal must be profile, as it will be checked to filter signals
        @param check_profile(bool): if True, signal profile (which MUST be last arg)
            will be checked against session profile.
            /!\ if False, profile will not be checked/filtered, be sure to know what you
                are doing if you unset this option /!\
        """
        # FIXME: add a timeout; if socket is not opened before it, signal handler
        #        must be removed
        if not self.dynamic:
            log.error(_(u"You can't register signal if page is not dynamic"))
            return
        signal_id = self.getSignalId(request)
        LiberviaPage.signals_handlers.setdefault(signal, {})[signal_id] = [
            self,
            request,
            check_profile,
        ]
        request._signals_registered.append(signal)

    def getConfig(self, key, default=None, value_type=None):
        return self.host.getConfig(self.vhost_root, key=key, default=default,
                                   value_type=value_type)

    def getBuildPath(self, session_data):
        return session_data.cache_dir + self.vhost.site_name

    def getPageByName(self, name):
        return self.vhost_root.getPageByName(name)

    def getPagePathFromURI(self, uri):
        return self.vhost_root.getPagePathFromURI(uri)

    def getPageRedirectURL(self, request, page_name=u"login", url=None):
        """generate URL for a page with redirect_url parameter set

        mainly used for login page with redirection to current page
        @param request(server.Request): current HTTP request
        @param page_name(unicode): name of the page to go
        @param url(None, unicode): url to redirect to
            None to use request path (i.e. current page)
        @return (unicode): URL to use
        """
        return u"{root_url}?redirect_url={redirect_url}".format(
            root_url=self.getPageByName(page_name).url,
            redirect_url=urllib.quote_plus(request.uri)
            if url is None
            else url.encode("utf-8"),
        )

    def getURL(self, *args):
        """retrieve URL of the page set arguments

        *args(list[unicode]): argument to add to the URL as path elements
            empty or None arguments will be ignored
        """
        url_args = [quote(a) for a in args if a]

        if self.name is not None and self.name in self.pages_redirects:
            #  we check for redirection
            redirect_data = self.pages_redirects[self.name]
            args_hash = tuple(args)
            for limit in xrange(len(args) + 1):
                current_hash = args_hash[:limit]
                if current_hash in redirect_data:
                    url_base = redirect_data[current_hash]
                    remaining = args[limit:]
                    remaining_url = "/".join(remaining)
                    return os.path.join("/", url_base, remaining_url)

        return os.path.join(self.url, *url_args)

    def getCurrentURL(self, request):
        """retrieve URL used to access this page

        @return(unicode): current URL
        """
        # we get url in the following way (splitting request.path instead of using
        # request.prepath) because request.prepath may have been modified by
        # redirection (if redirection args have been specified), while path reflect
        # the real request

        # we ignore empty path elements (i.e. double '/' or '/' at the end)
        path_elts = [p for p in request.path.split("/") if p]

        if request.postpath:
            if not request.postpath[-1]:
                #  we remove trailing slash
                request.postpath = request.postpath[:-1]
            if request.postpath:
                #  getSubPageURL must return subpage from the point where
                # the it is called, so we have to remove remanining
                # path elements
                path_elts = path_elts[: -len(request.postpath)]

        return u"/" + "/".join(path_elts).decode("utf-8")

    def getParamURL(self, request, **kwargs):
        """use URL of current request but modify the parameters in query part

        **kwargs(dict[str, unicode]): argument to use as query parameters
        @return (unicode): constructed URL
        """
        current_url = self.getCurrentURL(request)
        if kwargs:
            encoded = urllib.urlencode(
                {k: v.encode("utf-8") for k, v in kwargs.iteritems()}
            ).decode("utf-8")
            current_url = current_url + u"?" + encoded
        return current_url

    def getSubPageByName(self, subpage_name, parent=None):
        """retrieve a subpage and its path using its name

        @param subpage_name(unicode): name of the sub page
            it must be a direct children of parent page
        @param parent(LiberviaPage, None): parent page
            None to use current page
        @return (tuple[str, LiberviaPage]): page subpath and instance
        @raise exceptions.NotFound: no page has been found
        """
        if parent is None:
            parent = self
        for path, child in parent.children.iteritems():
            try:
                child_name = child.name
            except AttributeError:
                #  LiberviaPages have a name, but maybe this is an other Resource
                continue
            if child_name == subpage_name:
                return path, child
        raise exceptions.NotFound(_(u"requested sub page has not been found"))

    def getSubPageURL(self, request, page_name, *args):
        """retrieve a page in direct children and build its URL according to request

        request's current path is used as base (at current parsing point,
        i.e. it's more prepath than path).
        Requested page is checked in children and an absolute URL is then built
        by the resulting combination.
        This method is useful to construct absolute URLs for children instead of
        using relative path, which may not work in subpages, and are linked to the
        names of directories (i.e. relative URL will break if subdirectory is renamed
        while getSubPageURL won't as long as page_name is consistent).
        Also, request.path is used, keeping real path used by user,
        and potential redirections.
        @param request(server.Request): current HTTP request
        @param page_name(unicode): name of the page to retrieve
            it must be a direct children of current page
        @param *args(list[unicode]): arguments to add as path elements
            if an arg is None, it will be ignored
        @return (unicode): absolute URL to the sub page
        """
        current_url = self.getCurrentURL(request)
        path, child = self.getSubPageByName(page_name)
        return os.path.join(
            u"/", current_url, path, *[quote(a) for a in args if a is not None]
        )

    def getURLByNames(self, named_path):
        """Retrieve URL from pages names and arguments

        @param named_path(list[tuple[unicode, list[unicode]]]): path to the page as a list
            of tuples of 2 items:
                - first item is page name
                - second item is list of path arguments of this page
        @return (unicode): URL to the requested page with given path arguments
        @raise exceptions.NotFound: one of the page was not found
        """
        current_page = None
        path = []
        for page_name, page_args in named_path:
            if current_page is None:
                current_page = self.getPageByName(page_name)
                path.append(current_page.getURL(*page_args))
            else:
                sub_path, current_page = self.getSubPageByName(
                    page_name, parent=current_page
                )
                path.append(sub_path)
                if page_args:
                    path.extend([quote(a) for a in page_args])
        return self.host.checkRedirection(self.vhost_root, u"/".join(path))

    def getURLByPath(self, *args):
        """Generate URL by path

        this method as a similar effect as getURLByNames, but it is more readable
        by using SubPage to get pages instead of using tuples
        @param *args: path element:
            - if unicode, will be used as argument
            - if util.SubPage instance, must be the name of a subpage
        @return (unicode): generated path
        """
        args = list(args)
        if not args:
            raise ValueError("You must specify path elements")
        # root page is the one needed to construct the base of the URL
        # if first arg is not a SubPage instance, we use current page
        if not isinstance(args[0], SubPage):
            root = self
        else:
            root = self.getPageByName(args.pop(0))
        # we keep track of current page to check subpage
        current_page = root
        url_elts = []
        arguments = []
        while True:
            while args and not isinstance(args[0], SubPage):
                arguments.append(quote(args.pop(0)))
            if not url_elts:
                url_elts.append(root.getURL(*arguments))
            else:
                url_elts.extend(arguments)
            if not args:
                break
            else:
                path, current_page = current_page.getSubPageByName(args.pop(0))
                arguments = [path]
        return self.host.checkRedirection(self.vhost_root, u"/".join(url_elts))

    def getChildWithDefault(self, path, request):
        # we handle children ourselves
        raise exceptions.InternalError(
            u"this method should not be used with LiberviaPage"
        )

    def nextPath(self, request):
        """get next URL path segment, and update request accordingly

        will move first segment of postpath in prepath
        @param request(server.Request): current HTTP request
        @return (unicode): unquoted segment
        @raise IndexError: there is no segment left
        """
        pathElement = request.postpath.pop(0)
        request.prepath.append(pathElement)
        return urllib.unquote(pathElement).decode("utf-8")

    def _filterPathValue(self, value, handler, name, request):
        """Modify a path value according to handler (see [getPathArgs])"""
        if handler in (u"@", u"@jid") and value == u"@":
            value = None

        if handler in (u"", u"@"):
            if value is None:
                return u""
        elif handler in (u"jid", u"@jid"):
            if value:
                try:
                    return jid.JID(value)
                except RuntimeError:
                    log.warning(_(u"invalid jid argument: {value}").format(value=value))
                    self.pageError(request, C.HTTP_BAD_REQUEST)
            else:
                return u""
        else:
            return handler(self, value, name, request)

        return value

    def getPathArgs(self, request, names, min_args=0, **kwargs):
        """get several path arguments at once

        Arguments will be put in request data.
        Missing arguments will have None value
        @param names(list[unicode]): list of arguments to get
        @param min_args(int): if less than min_args are found, PageError is used with
            C.HTTP_BAD_REQUEST
            Use 0 to ignore
        @param **kwargs: special value or optional callback to use for arguments
            names of the arguments must correspond to those in names
            special values may be:
                - '': use empty string instead of None when no value is specified
                - '@': if value of argument is empty or '@', empty string will be used
                - 'jid': value must be converted to jid.JID if it exists, else empty
                    string is used
                - '@jid': if value of arguments is empty or '@', empty string will be
                    used, else it will be converted to jid
        """
        data = self.getRData(request)

        for idx, name in enumerate(names):
            if name[0] == u"*":
                value = data[name[1:]] = []
                while True:
                    try:
                        value.append(self.nextPath(request))
                    except IndexError:
                        idx -= 1
                        break
                    else:
                        idx += 1
            else:
                try:
                    value = data[name] = self.nextPath(request)
                except IndexError:
                    data[name] = None
                    idx -= 1
                    break

        values_count = idx + 1
        if values_count < min_args:
            log.warning(_(u"Missing arguments in URL (got {count}, expected at least "
                          u"{min_args})").format(count=values_count, min_args=min_args))
            self.pageError(request, C.HTTP_BAD_REQUEST)

        for name in names[values_count:]:
            data[name] = None

        for name, handler in kwargs.iteritems():
            if name[0] == "*":
                data[name] = [
                    self._filterPathValue(v, handler, name, request) for v in data[name]
                ]
            else:
                data[name] = self._filterPathValue(data[name], handler, name, request)

    ## Pagination/Filtering ##

    def getPubsubExtra(self, request, page_max=10, params=None, extra=None,
        order_by=C.ORDER_BY_CREATION):
        """Set extra dict to retrieve PubSub items corresponding to URL parameters

        Following parameters are used:
            - after: set rsm_after with ID of item
            - before: set rsm_before with ID of item
        @param request(server.Request): current HTTP request
        @param page_max(int): required number of items per page
        @param params(None, dict[unicode, list[unicode]]): params as returned by
            self.getAllPostedData.
            None to parse URL automatically
        @param extra(None, dict): extra dict to use, or None to use a new one
        @param order_by(unicode, None): key to order by
            None to not specify order
        @return (dict): fill extra data
        """
        if params is None:
            params = self.getAllPostedData(request, multiple=False)
        if extra is None:
            extra = {}
        else:
            assert not {u"rsm_max", u"rsm_after", u"rsm_before",
                        C.KEY_ORDER_BY}.intersection(extra.keys())
        extra[u"rsm_max"] = unicode(page_max)
        if order_by is not None:
            extra[C.KEY_ORDER_BY] = order_by
        if u'after' in params:
            extra[u'rsm_after'] = params[u'after']
        elif u'before' in params:
            extra[u'rsm_before'] = params[u'before']
        return extra

    def setPagination(self, request, pubsub_data):
        """Add  to template_data if suitable

        "previous_page_url" and "next_page_url" will be added using respectively
        "before" and "after" URL parameters
        @param request(server.Request): current HTTP request
        @param pubsub_data(dict): pubsub metadata parsed with
            data_objects.parsePubSubMetadata
        """
        template_data = request.template_data
        try:
            last_id = pubsub_data[u"rsm_last"]
        except KeyError:
            # no pagination available
            return

        if pubsub_data.get("rsm_index", 1) > 0:
            # We only show previous button if it's not the first page already.
            # If we have no index, we default to display the button anyway
            # as we can't know if we are on the first page or not.
            first_id = pubsub_data[u"rsm_first"]
            template_data['previous_page_url'] = self.getParamURL(request,
                                                                  before=first_id)
        if not pubsub_data[u"complete"]:
            # we also show the page next button if complete is None because we
            # can't know where we are in the feed in this case.
            template_data['next_page_url'] = self.getParamURL(request, after=last_id)


    ## Cache handling ##

    def _setCacheHeaders(self, request, cache):
        """Set ETag and Last-Modified HTTP headers, used for caching"""
        request.setHeader("ETag", cache.hash)
        last_modified = self.host.getHTTPDate(cache.created)
        request.setHeader("Last-Modified", last_modified)

    def _checkCacheHeaders(self, request, cache):
        """Check if a cache condition is set on the request

        if condition is valid, C.HTTP_NOT_MODIFIED is returned
        """
        etag_match = request.getHeader("If-None-Match")
        if etag_match is not None:
            if cache.hash == etag_match:
                self.pageError(request, C.HTTP_NOT_MODIFIED, no_body=True)
        else:
            modified_match = request.getHeader("If-Modified-Since")
            if modified_match is not None:
                modified = date_utils.date_parse(modified_match)
                if modified >= int(cache.created):
                    self.pageError(request, C.HTTP_NOT_MODIFIED, no_body=True)

    def checkCacheSubscribeCb(self, sub_id, service, node):
        self.cache_pubsub_sub.add((service, node, sub_id))

    def checkCacheSubscribeEb(self, failure_, service, node):
        log.warning(_(u"Can't subscribe to node: {msg}").format(msg=failure_))
        # FIXME: cache must be marked as unusable here

    def psNodeWatchAddEb(self, failure_, service, node):
        log.warning(_(u"Can't add node watched: {msg}").format(msg=failure_))

    def checkCache(self, request, cache_type, **kwargs):
        """check if a page is in cache and return cached version if suitable

        this method may perform extra operation to handle cache (e.g. subscribing to a
        pubsub node)
        @param request(server.Request): current HTTP request
        @param cache_type(int): on of C.CACHE_* const.
        @param **kwargs: args according to cache_type:
            C.CACHE_PUBSUB:
                service: pubsub service
                node: pubsub node
                short: short name of feature (needed if node is empty to find namespace)

        """
        if request.postpath:
            #  we are not on the final page, no need to go further
            return

        profile = self.getProfile(request) or C.SERVICE_PROFILE

        if cache_type == C.CACHE_PUBSUB:
            service, node = kwargs["service"], kwargs["node"]
            if not node:
                try:
                    short = kwargs["short"]
                    node = self.host.ns_map[short]
                except KeyError:
                    log.warning(_(u'Can\'t use cache for empty node without namespace '
                                  u'set, please ensure to set "short" and that it is '
                                  u'registered'))
                    return
            if profile != C.SERVICE_PROFILE:
                #  only service profile is cache for now
                return
            session_data = self.host.getSessionData(request, session_iface.ISATSession)
            locale = session_data.locale
            if locale == C.DEFAULT_LOCALE:
                # no need to duplicate cache here
                locale = None
            try:
                cache = (self.cache[profile][cache_type][service][node]
                         [self.vhost_root][request.uri][locale][self])
            except KeyError:
                # no cache yet, let's subscribe to the pubsub node
                d1 = self.host.bridgeCall(
                    "psSubscribe", service.full(), node, {}, profile
                )
                d1.addCallback(self.checkCacheSubscribeCb, service, node)
                d1.addErrback(self.checkCacheSubscribeEb, service, node)
                d2 = self.host.bridgeCall("psNodeWatchAdd", service.full(), node, profile)
                d2.addErrback(self.psNodeWatchAddEb, service, node)
                self._do_cache = [self, profile, cache_type, service, node,
                                  self.vhost_root, request.uri, locale]
                #  we don't return the Deferreds as it is not needed to wait for
                # the subscription to continue with page rendering
                return

        else:
            raise exceptions.InternalError(u"Unknown cache_type")
        log.debug(u"using cache for {page}".format(page=self))
        cache.last_access = time.time()
        self._setCacheHeaders(request, cache)
        self._checkCacheHeaders(request, cache)
        request.write(cache.rendered)
        request.finish()
        raise failure.Failure(exceptions.CancelError(u"cache is used"))

    def _cacheURL(self, __, request, profile):
        self.cached_urls.setdefault(profile, {})[request.uri] = CacheURL(request)

    @classmethod
    def onNodeEvent(cls, host, service, node, event_type, items, profile):
        """Invalidate cache for all pages linked to this node"""
        try:
            cache = cls.cache[profile][C.CACHE_PUBSUB][jid.JID(service)][node]
        except KeyError:
            log.info(_(
                u"Removing subscription for {service}/{node}: "
                u"the page is not cached").format(service=service, node=node))
            d1 = host.bridgeCall("psUnsubscribe", service, node, profile)
            d1.addErrback(
                lambda failure_: log.warning(
                    _(u"Can't unsubscribe from {service}/{node}: {msg}").format(
                        service=service, node=node, msg=failure_)))
            d2 = host.bridgeCall("psNodeWatchAdd", service, node, profile)
            # TODO: check why the page is not in cache, remove subscription?
            d2.addErrback(
                lambda failure_: log.warning(
                    _(u"Can't remove watch for {service}/{node}: {msg}").format(
                        service=service, node=node, msg=failure_)))
        else:
            cache.clear()

    @classmethod
    def onSignal(cls, host, signal, *args):
        """Generic method which receive registered signals

        if a callback is registered for this signal, call it
        @param host: Libervia instance
        @param signal(unicode): name of the signal
        @param *args: args of the signals
        """
        for page, request, check_profile in cls.signals_handlers.get(
            signal, {}
        ).itervalues():
            if check_profile:
                signal_profile = args[-1]
                request_profile = page.getProfile(request)
                if not request_profile:
                    # if you want to use signal without session, unset check_profile
                    # (be sure to know what you are doing)
                    log.error(_(u"no session started, signal can't be checked"))
                    continue
                if signal_profile != request_profile:
                    #  we ignore the signal, it's not for our profile
                    continue
            if request._signals_cache is not None:
                # socket is not yet opened, we cache the signal
                request._signals_cache.append((request, signal, args))
                log.debug(
                    u"signal [{signal}] cached: {args}".format(signal=signal, args=args)
                )
            else:
                page.on_signal(page, request, signal, *args)

    def onSocketOpen(self, request):
        """Called for dynamic pages when socket has just been opened

        we send all cached signals
        """
        assert request._signals_cache is not None
        # we need to replace corresponding original requests by this websocket request
        # in signals_handlers
        signal_id = request.signal_id
        for signal_handlers_map in self.__class__.signals_handlers.itervalues():
            if signal_id in signal_handlers_map:
                signal_handlers_map[signal_id][1] = request

        cache = request._signals_cache
        request._signals_cache = None
        for request, signal, args in cache:
            self.on_signal(self, request, signal, *args)

    def onSocketClose(self, request):
        """Called for dynamic pages when socket has just been closed

        we remove signal handler
        """
        for signal in request._signals_registered:
            signal_id = self.getSignalId(request)
            try:
                del LiberviaPage.signals_handlers[signal][signal_id]
            except KeyError:
                log.error(_(u"Can't find signal handler for [{signal}], this should not "
                            u"happen").format(signal=signal))
            else:
                log.debug(_(u"Removed signal handler"))

    def delegateToResource(self, request, resource):
        """continue workflow with Twisted Resource"""
        buf = resource.render(request)
        if buf == server.NOT_DONE_YET:
            pass
        else:
            request.write(buf)
            request.finish()
        raise failure.Failure(exceptions.CancelError(u"resource delegation"))

    def HTTPRedirect(self, request, url):
        """redirect to an URL using HTTP redirection

        @param request(server.Request): current HTTP request
        @param url(unicode): url to redirect to
        """
        web_util.redirectTo(url.encode("utf-8"), request)
        request.finish()
        raise failure.Failure(exceptions.CancelError(u"HTTP redirection is used"))

    def redirectOrContinue(self, request, redirect_arg=u"redirect_url"):
        """helper method to redirect a page to an url given as arg

        if the arg is not present, the page will continue normal workflow
        @param request(server.Request): current HTTP request
        @param redirect_arg(unicode): argument to use to get redirection URL
        @interrupt: redirect the page to requested URL
        @interrupt pageError(C.HTTP_BAD_REQUEST): empty or non local URL is used
        """
        try:
            url = request.args["redirect_url"][0]
        except (KeyError, IndexError):
            pass
        else:
            #  a redirection is requested
            if not url or url[0] != u"/":
                # we only want local urls
                self.pageError(request, C.HTTP_BAD_REQUEST)
            else:
                self.HTTPRedirect(request, url)

    def pageRedirect(self, page_path, request, skip_parse_url=True, path_args=None):
        """redirect a page to a named page

        the workflow will continue with the workflow of the named page,
        skipping named page's parse_url method if it exist.
        If you want to do a HTTP redirection, use HTTPRedirect
        @param page_path(unicode): path to page (elements are separated by "/"):
            if path starts with a "/":
                path is a full path starting from root
            else:
                - first element is name as registered in name variable
                - following element are subpages path
            e.g.: "blog" redirect to page named "blog"
                  "blog/atom.xml" redirect to atom.xml subpage of "blog"
                  "/common/blog/atom.xml" redirect to the page at the given full path
        @param request(server.Request): current HTTP request
        @param skip_parse_url(bool): if True, parse_url method on redirect page will be
            skipped
        @param path_args(list[unicode], None): path arguments to use in redirected page
        @raise KeyError: there is no known page with this name
        """
        # FIXME: render non LiberviaPage resources
        path = page_path.rstrip(u"/").split(u"/")
        if not path[0]:
            redirect_page = self.vhost_root
        else:
            redirect_page = self.named_pages[path[0]]

        for subpage in path[1:]:
            if redirect_page is self.vhost_root:
                redirect_page = redirect_page.children[subpage]
            else:
                redirect_page = redirect_page.original.children[subpage]

        if path_args is not None:
            args = [quote(a) for a in path_args]
            request.postpath = args + request.postpath

        if self._do_cache:
            # if cache is needed, it will be handled by final page
            redirect_page._do_cache = self._do_cache
            self._do_cache = None

        redirect_page.renderPage(request, skip_parse_url=skip_parse_url)
        raise failure.Failure(exceptions.CancelError(u"page redirection is used"))

    def pageError(self, request, code=C.HTTP_NOT_FOUND, no_body=False):
        """generate an error page and terminate the request

        @param request(server.Request): HTTP request
        @param core(int): error code to use
        @param no_body: don't write body if True
        """
        if self._do_cache is not None:
            # we don't want to cache error pages
            self._do_cache = None
        request.setResponseCode(code)
        if no_body:
            request.finish()
        else:
            template = u"error/" + unicode(code) + ".html"
            template_data = request.template_data
            session_data = self.host.getSessionData(request, session_iface.ISATSession)
            if session_data.locale is not None:
                template_data[u'locale'] = session_data.locale
            if self.vhost_root.site_name:
                template_data[u'site'] = self.vhost_root.site_name

            rendered = self.host.renderer.render(
                template,
                error_code=code,
                **template_data
            )

            self.writeData(rendered, request)
        raise failure.Failure(exceptions.CancelError(u"error page is used"))

    def writeData(self, data, request):
        """write data to transport and finish the request"""
        if data is None:
            self.pageError(request)
        data_encoded = data.encode("utf-8")

        if self._do_cache is not None:
            redirected_page = self._do_cache.pop(0)
            cache = reduce(lambda d, k: d.setdefault(k, {}), self._do_cache, self.cache)
            page_cache = cache[redirected_page] = CachePage(data_encoded)
            self._setCacheHeaders(request, page_cache)
            log.debug(_(u"{page} put in cache for [{profile}]")
                .format( page=self, profile=self._do_cache[0]))
            self._do_cache = None
            self._checkCacheHeaders(request, page_cache)

        try:
            request.write(data_encoded)
        except AttributeError:
            log.warning(_(u"Can't write page, the request has probably been cancelled "
                          u"(browser tab closed or reloaded)"))
            return
        request.finish()

    def _subpagesHandler(self, __, request):
        """render subpage if suitable

        this method checks if there is still an unmanaged part of the path
        and check if it corresponds to a subpage. If so, it render the subpage
        else it render a NoResource.
        If there is no unmanaged part of the segment, current page workflow is pursued
        """
        if request.postpath:
            subpage = self.nextPath(request)
            try:
                child = self.children[subpage]
            except KeyError:
                self.pageError(request)
            else:
                child.render(request)
                raise failure.Failure(exceptions.CancelError(u"subpage page is used"))

    def _prepare_dynamic(self, __, request):
        # we need to activate dynamic page
        # we set data for template, and create/register token
        socket_token = unicode(uuid.uuid4())
        socket_url = self.host.getWebsocketURL(request)
        socket_debug = C.boolConst(self.host.debug)
        request.template_data["websocket"] = WebsocketMeta(
            socket_url, socket_token, socket_debug
        )
        # we will keep track of handlers to remove
        request._signals_registered = []
        # we will cache registered signals until socket is opened
        request._signals_cache = []
        self.host.registerWSToken(socket_token, self, request)

    def _prepare_render(self, __, request):
        return defer.maybeDeferred(self.prepare_render, self, request)

    def _render_method(self, __, request):
        return defer.maybeDeferred(self.render_method, self, request)

    def _render_template(self, __, request):
        template_data = request.template_data

        # if confirm variable is set in case of successfuly data post
        session_data = self.host.getSessionData(request, session_iface.ISATSession)
        if session_data.popPageFlag(self, C.FLAG_CONFIRM):
            template_data[u"confirm"] = True
        notifs = session_data.popPageNotifications(self)
        if notifs:
            template_data[u"notifications"] = notifs
        if session_data.locale is not None:
            template_data[u'locale'] = session_data.locale
        if self.vhost_root.site_name:
            template_data[u'site'] = self.vhost_root.site_name

        return self.host.renderer.render(
            self.template,
            page_url=self.getURL(),
            media_path=u"/" + C.MEDIA_DIR,
            cache_path=session_data.cache_dir,
            build_path=u"/" + C.BUILD_DIR + u"/",
            main_menu=self.main_menu,
            **template_data)

    def _renderEb(self, failure_, request):
        """don't raise error on CancelError"""
        failure_.trap(exceptions.CancelError)

    def _internalError(self, failure_, request):
        """called if an error is not catched"""
        if failure_.check(BridgeException) and failure_.value.condition == u'not-allowed':
            log.warning(u"not allowed exception catched")
            self.pageError(request, C.HTTP_FORBIDDEN)
        log.error(_(u"Uncatched error for HTTP request on {url}: {msg}")
            .format( url=request.URLPath(), msg=failure_))
        self.pageError(request, C.HTTP_INTERNAL_ERROR)

    def _on_data_post_error(self, failure_, request):
        failure_.trap(exceptions.DataError)
        # something is wrong with the posted data, we re-display the page with a
        # warning notification
        session_data = self.host.getSessionData(request, session_iface.ISATSession)
        session_data.setPageNotification(self, failure_.value.message, C.LVL_WARNING)
        request.setResponseCode(C.HTTP_SEE_OTHER)
        request.setHeader("location", request.uri)
        request.finish()
        raise failure.Failure(exceptions.CancelError(u"Post/Redirect/Get is used"))

    def _on_data_post_redirect(self, ret, request):
        """called when page's on_data_post has been done successfuly

        This will do a Post/Redirect/Get pattern.
        this method redirect to the same page or to request.data['post_redirect_page']
        post_redirect_page can be either a page or a tuple with page as first item, then
        a list of unicode arguments to append to the url.
        if post_redirect_page is not used, initial request.uri (i.e. the same page as
        where the data have been posted) will be used for redirection.
        HTTP status code "See Other" (303) is used as it is the recommanded code in
        this case.
        @param ret(None, unicode, iterable): on_data_post return value
            see LiberviaPage.__init__ on_data_post docstring
        """
        if ret is None:
            ret = ()
        elif isinstance(ret, basestring):
            ret = (ret,)
        else:
            ret = tuple(ret)
            raise NotImplementedError(
                _(u"iterable in on_data_post return value is not used yet")
            )
        session_data = self.host.getSessionData(request, session_iface.ISATSession)
        request_data = self.getRData(request)
        if "post_redirect_page" in request_data:
            redirect_page_data = request_data["post_redirect_page"]
            if isinstance(redirect_page_data, tuple):
                redirect_page = redirect_page_data[0]
                redirect_page_args = redirect_page_data[1:]
                redirect_uri = redirect_page.getURL(*redirect_page_args)
            else:
                redirect_page = redirect_page_data
                redirect_uri = redirect_page.url
        else:
            redirect_page = self
            redirect_uri = request.uri

        if not C.POST_NO_CONFIRM in ret:
            session_data.setPageFlag(redirect_page, C.FLAG_CONFIRM)
        request.setResponseCode(C.HTTP_SEE_OTHER)
        request.setHeader("location", redirect_uri)
        request.finish()
        raise failure.Failure(exceptions.CancelError(u"Post/Redirect/Get is used"))

    def _on_data_post(self, __, request):
        csrf_token = self.host.getSessionData(
            request, session_iface.ISATSession
        ).csrf_token
        try:
            given_csrf = self.getPostedData(request, u"csrf_token")
        except KeyError:
            given_csrf = None
        if given_csrf is None or given_csrf != csrf_token:
            log.warning(
                _(u"invalid CSRF token, hack attempt? URL: {url}, IP: {ip}").format(
                    url=request.uri, ip=request.getClientIP()
                )
            )
            self.pageError(request, C.HTTP_FORBIDDEN)
        d = defer.maybeDeferred(self.on_data_post, self, request)
        d.addCallback(self._on_data_post_redirect, request)
        d.addErrback(self._on_data_post_error, request)
        return d

    def getPostedData(self, request, keys, multiple=False, raise_on_missing=True):
        """Get data from a POST request or from URL's query part and decode it

        @param request(server.Request): request linked to the session
        @param keys(unicode, iterable[unicode]): name of the value(s) to get
            unicode to get one value
            iterable to get more than one
        @param multiple(bool): True if multiple values are possible/expected
            if False, the first value is returned
        @param raise_on_missing(bool): raise KeyError on missing key if True
            else use None for missing values
        @return (iterator[unicode], list[iterator[unicode], unicode, list[unicode]):
            values received for this(these) key(s)
        @raise KeyError: one specific key has been requested, and it is missing
        """
        #  FIXME: request.args is already unquoting the value, it seems we are doing
        #         double unquote
        if isinstance(keys, basestring):
            keys = [keys]
            get_first = True
        else:
            get_first = False

        ret = []
        for key in keys:
            gen = (urllib.unquote(v).decode("utf-8") for v in request.args.get(key, []))
            if multiple:
                ret.append(gen)
            else:
                try:
                    ret.append(next(gen))
                except StopIteration:
                    if raise_on_missing:
                        raise KeyError(key)
                    else:
                        ret.append(None)

        return ret[0] if get_first else ret

    def getAllPostedData(self, request, except_=(), multiple=True):
        """get all posted data

        @param request(server.Request): request linked to the session
        @param except_(iterable[unicode]): key of values to ignore
            csrf_token will always be ignored
        @param multiple(bool): if False, only the first values are returned
        @return (dict[unicode, list[unicode]]): post values
        """
        except_ = tuple(except_) + (u"csrf_token",)
        ret = {}
        for key, values in request.args.iteritems():
            key = urllib.unquote(key).decode("utf-8")
            if key in except_:
                continue
            if not multiple:
                ret[key] = urllib.unquote(values[0]).decode("utf-8")
            else:
                ret[key] = [urllib.unquote(v).decode("utf-8") for v in values]
        return ret

    def getProfile(self, request):
        """helper method to easily get current profile

        @return (unicode, None): current profile
            None if no profile session is started
        """
        sat_session = self.host.getSessionData(request, session_iface.ISATSession)
        return sat_session.profile

    def getRData(self, request):
        """helper method to get request data dict

        this dictionnary if for the request only, it is not saved in session
        It is mainly used to pass data between pages/methods called during request
        workflow
        @return (dict): request data
        """
        try:
            return request.data
        except AttributeError:
            request.data = {}
            return request.data

    def _checkAccess(self, data, request):
        """Check access according to self.access

        if access is not granted, show a HTTP_FORBIDDEN pageError and stop request,
        else return data (so it can be inserted in deferred chain
        """
        if self.access == C.PAGES_ACCESS_PUBLIC:
            pass
        elif self.access == C.PAGES_ACCESS_PROFILE:
            profile = self.getProfile(request)
            if not profile:
                # no session started
                if not self.host.options["allow_registration"]:
                    # registration not allowed, access is not granted
                    self.pageError(request, C.HTTP_FORBIDDEN)
                else:
                    # registration allowed, we redirect to login page
                    login_url = self.getPageRedirectURL(request)
                    self.HTTPRedirect(request, login_url)

        return data

    def setBestLocale(self, request):
        """Guess the best locale when it is not specified explicitly by user

        This method will check "accept-language" header, and set locale to first
        matching value with available translations.
        """
        accept_language = request.getHeader("accept-language")
        if not accept_language:
            return
        accepted = {a.strip() for a in accept_language.split(',')}
        available = [unicode(l) for l in self.host.renderer.translations]
        for lang in accepted:
            lang = lang.split(';')[0].strip().lower()
            if not lang:
                continue
            for a in available:
                if a.lower().startswith(lang):
                    session_data = self.host.getSessionData(request,
                                                            session_iface.ISATSession)
                    session_data.locale = a
                    return

    def renderPartial(self, request, template, template_data):
        """Render a template to be inserted in dynamic page

        this is NOT the normal page rendering method, it is used only to update
        dynamic pages
        @param template(unicode): path of the template to render
        @param template_data(dict): template_data to use
        """
        if not self.dynamic:
            raise exceptions.InternalError(
                _(u"renderPartial must only be used with dynamic pages")
            )
        session_data = self.host.getSessionData(request, session_iface.ISATSession)
        if session_data.locale is not None:
            template_data[u'locale'] = session_data.locale
        if self.vhost_root.site_name:
            template_data[u'site'] = self.vhost_root.site_name

        return self.host.renderer.render(
            template,
            page_url=self.getURL(),
            media_path=u"/" + C.MEDIA_DIR,
            cache_path=session_data.cache_dir,
            build_path=u"/" + C.BUILD_DIR + u"/",
            main_menu=self.main_menu,
            **template_data
        )

    def renderAndUpdate(
        self, request, template, selectors, template_data_update, update_type="append"
    ):
        """Helper method to render a partial page element and update the page

        this is NOT the normal page rendering method, it is used only to update
        dynamic pages
        @param request(server.Request): current HTTP request
        @param template: same as for [renderPartial]
        @param selectors: CSS selectors to use
        @param template_data_update: template data to use
            template data cached in request will be copied then updated
            with this data
        @parap update_type(unicode): one of:
            append: append rendered element to selected element
        """
        template_data = request.template_data.copy()
        template_data.update(template_data_update)
        html = self.renderPartial(request, template, template_data)
        try:
            request.sendData(
                u"dom", selectors=selectors, update_type=update_type, html=html)
        except Exception as e:
            log.error(u"Can't renderAndUpdate, html was: {html}".format(html=html))
            raise e

    def renderPage(self, request, skip_parse_url=False):
        """Main method to handle the workflow of a LiberviaPage"""

        # template_data are the variables passed to template
        if not hasattr(request, "template_data"):
            session_data = self.host.getSessionData(request, session_iface.ISATSession)
            csrf_token = session_data.csrf_token
            request.template_data = {
                u"profile": session_data.profile,
                u"csrf_token": csrf_token,
            }

            # XXX: here is the code which need to be executed once
            #      at the beginning of the request hanling
            if request.postpath and not request.postpath[-1]:
                # we don't differenciate URLs finishing with '/' or not
                del request.postpath[-1]

            # i18n
            if C.KEY_LANG in request.args:
                try:
                    locale = request.args.pop(C.KEY_LANG)[0]
                except IndexError:
                    log.warning(u"empty lang received")
                else:
                    if u"/" in locale:
                        # "/" is refused because locale may sometime be used to access
                        # path, if localised documents are available for instance
                        log.warning(_(u'illegal char found in locale ("/"), hack '
                                      u'attempt? locale={locale}').format(locale=locale))
                        locale = None
                    session_data.locale = locale

            # if locale is not specified, we try to find one requested by browser
            if session_data.locale is None:
                self.setBestLocale(request)

        d = defer.Deferred()
        d.addCallback(self._checkAccess, request)

        if self.redirect is not None:
            d.addCallback(
                lambda __: self.pageRedirect(
                    self.redirect, request, skip_parse_url=False
                )
            )

        if self.parse_url is not None and not skip_parse_url:
            if self.url_cache:
                profile = self.getProfile(request)
                try:
                    cache_url = self.cached_urls[profile][request.uri]
                except KeyError:
                    # no cache for this URI yet
                    #  we do normal URL parsing, and then the cache
                    d.addCallback(self.parse_url, request)
                    d.addCallback(self._cacheURL, request, profile)
                else:
                    log.debug(_(u"using URI cache for {page}").format(page=self))
                    cache_url.use(request)
            else:
                d.addCallback(self.parse_url, request)

        d.addCallback(self._subpagesHandler, request)

        if request.method not in (C.HTTP_METHOD_GET, C.HTTP_METHOD_POST):
            # only HTTP GET and POST are handled so far
            d.addCallback(lambda __: self.pageError(request, C.HTTP_BAD_REQUEST))

        if request.method == C.HTTP_METHOD_POST:
            if self.on_data_post is None:
                # if we don't have on_data_post, the page was not expecting POST
                # so we return an error
                d.addCallback(lambda __: self.pageError(request, C.HTTP_BAD_REQUEST))
            else:
                d.addCallback(self._on_data_post, request)
            # by default, POST follow normal behaviour after on_data_post is called
            # this can be changed by a redirection or other method call in on_data_post

        if self.dynamic:
            d.addCallback(self._prepare_dynamic, request)

        if self.prepare_render:
            d.addCallback(self._prepare_render, request)

        if self.template:
            d.addCallback(self._render_template, request)
        elif self.render_method:
            d.addCallback(self._render_method, request)

        d.addCallback(self.writeData, request)
        d.addErrback(self._renderEb, request)
        d.addErrback(self._internalError, request)
        d.callback(self)
        return server.NOT_DONE_YET

    def render_GET(self, request):
        return self.renderPage(request)

    def render_POST(self, request):
        return self.renderPage(request)
