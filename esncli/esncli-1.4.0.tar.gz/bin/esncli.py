#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

from __future__ import unicode_literals

import os
import sys
import locale
import codecs
import requests
import json

from argtoolbox import DefaultCommand as DDefaultCommand
from argtoolbox import BasicProgram
# pylint: disable-msg=W0611
# from argtoolbox import SimpleSection
from argtoolbox import Element

from requests.auth import HTTPBasicAuth
from requests_toolbelt.adapters import host_header_ssl
from httplib import HTTPConnection


# if you want to debug argcomplete completion,
# you just need to export _ARC_DEBUG=True

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)


class DefaultCommand(DDefaultCommand):

    MSG_UPDATING = "Updating unknown module."
    MSG_UPDATED = "Unknown module updated."
    MSG_ERROR_UPDATE = "Can not update unknown module"

    def __init__(self, *args, **kwargs):
        super(DefaultCommand, self).__init__(*args, **kwargs)
        self.login = None
        self.password = None
        self.base_url = None
        self.no_verify = False
        self.default_endpoint = '/api/configurations?scope=platform'
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Accept": "application/json;charset=utf-8"
        }

    def __call__(self, args):
        super(DefaultCommand, self).__call__(args)
        self.login = args.login
        self.password = args.password
        self.base_url = args.url
        self.no_verify = args.no_verify
        if args.host:
            self.headers['Host'] = args.host
        self.session = requests.Session()
        self.session.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
        if args.debug >= 2:
            HTTPConnection.debuglevel = 1

    def update(self, endpoint, data, legends=None):
        self.log.info(self.MSG_UPDATING)
        if legends:
            for msg in legends:
                self.log.info(msg)
        self.log.debug("data : %s", json.dumps(data, sort_keys=True, indent=2))
        r = self.session.put(self.base_url + endpoint,
                             data=json.dumps(data),
                             headers=self.headers,
                             auth=HTTPBasicAuth(self.login, self.password),
                             verify=not self.no_verify)
        if r.status_code in [200, 204]:
            self.log.debug("status_code : %s", r.status_code)
            self.log.info(self.MSG_UPDATED)
            return True
        self.log.error("Error : %s : %s", r.status_code, r.text)
        if 'Content-Type' in r.headers:
            content_type = r.headers['Content-Type'].split(';')[0]
            if content_type == 'application/json':
                self.log.debug("data : %s", r.json())
                self.log.debug(
                    "data : %s",
                    json.dumps(r.json(), sort_keys=True, indent=2))
        self.log.error(self.MSG_ERROR_UPDATE)
        return False

    def get_my_domain_id(self):
        r = self.session.get(self.base_url + '/api/user',
                             headers=self.headers,
                             auth=HTTPBasicAuth(self.login, self.password),
                             verify=not self.no_verify)
        if r.status_code != 200:
            self.log.error("Can not get user's domain.")
            return False

        return r.json()['domains'][0]['domain_id']

    def create_ldap_connection(self, domain_id, domain_admin_login, domain_admin_password, ldap_parameters):
        endpoint = '/api/configurations?scope=domain&domain_id=' + domain_id
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "ldap",
                    "value": [
                        {
                            "configuration": {
                                "mapping": {
                                    "firstname": "givenName",
                                    "lastname": "sn",
                                    "job_title": "title",
                                    "main_phone": "mobile"
                                },
                                "adminDn": ldap_parameters['bind_dn'],
                                "adminPassword": ldap_parameters['bind_password'],
                                "url": ldap_parameters['uri'],
                                "searchBase": ldap_parameters['search_base'],
                                "searchFilter": ldap_parameters['search_filter']
                            },
                            "usage": {
                                "auth": ldap_parameters['usage_auth'],
                                "search": ldap_parameters['usage_search'],
                                "autoProvisioning": ldap_parameters['usage_provisioning']
                            },
                            "name": ldap_parameters['name']
                        }
                    ]
                }
            ]
        }]

        r = self.session.put(self.base_url + endpoint,
            data=json.dumps(data),
            headers=self.headers,
            auth=HTTPBasicAuth(domain_admin_login, domain_admin_password),
            verify=not self.no_verify)

        if r.status_code in [200, 204]:
            self.log.debug("status_code : %s", r.status_code)
            self.log.info("LDAP connection parameters configured")
            return True

        self.log.error("Error : %s : %s", r.status_code, r.text)
        return False

class WhoAmICommand(DefaultCommand):

    def __call__(self, args):
        super(WhoAmICommand, self).__call__(args)
        r = self.session.get(self.base_url + '/api/user',
                             headers=self.headers,
                             auth=HTTPBasicAuth(self.login, self.password),
                             verify=not self.no_verify)
        if r.status_code != 200:
            self.log.error("Can not get user's profile.")
            return False
        data = r.json()
        del data['avatars']
        del data['configurations']
        self.log.info("data : %s", json.dumps(data, sort_keys=True, indent=2))
        return True


class PasswordCommand(DefaultCommand):
    """Password command"""

    def __call__(self, args):
        super(PasswordCommand, self).__call__(args)

        endpointUrl = args.url + '/api/user'
        oldPassword = os.environ.get('ESN_PLATFORMADMIN_DEFAULT_PASSWORD', 'secret')
        newPassword = args.new_password

        self.log.info(
            "Checking authentication with account : %s",
            args.login)
        self.log.info("Checking authentication with old password ...")
        r = self.session.get(endpointUrl,
                             auth=HTTPBasicAuth(args.login, oldPassword),
                             headers=self.headers,
                             verify=not args.no_verify)
        self.log.debug("status_code : %s", r.status_code)
        if r.status_code == 200:
            self.log.info("Old password ok.")
            return self.change_password(args, oldPassword, newPassword)
        else:
            self.log.info("Checking authentication with supplied password ...")
            r = self.session.get(endpointUrl,
                                 headers=self.headers,
                                 auth=HTTPBasicAuth(args.login, newPassword),
                                 verify=not args.no_verify)
            self.log.debug("status_code : %s", r.status_code)
            if r.status_code == 200:
                self.log.info("Supplied password ok (not changing it).")
                return True
            else:
                self.log.error("Error : %s : %s", r.status_code, r.text)
                if 'Content-Type' in r.headers:
                    content_type = r.headers['Content-Type'].split(';')[0]
                    if content_type == 'application/json':
                        self.log.debug("data : %s", r.json())
                        self.log.debug(
                            "data : %s",
                            json.dumps(r.json(), sort_keys=True, indent=2))
        self.log.error("Can not update admin password.")
        return False

    def change_password(self, args, oldPassword, newPassword):
        endpointUrl = args.url + '/api/passwordreset/changepassword'
        data = {
            "oldpassword": oldPassword,
            "newpassword": newPassword
        }
        self.log.info("Update password for account : %s ...", args.login)
        self.log.debug("data : %s", data)
        r = self.session.put(endpointUrl,
                             data=json.dumps(data),
                             headers=self.headers,
                             auth=HTTPBasicAuth(args.login, oldPassword),
                             verify=not args.no_verify)
        self.log.debug("status_code : %s", r.status_code)
        if r.status_code == 200:
            self.log.info("Password updated.")
            return True
        else:
            self.log.error("Error : %s : %s", r.status_code, r.text)
            if 'Content-Type' in r.headers:
                content_type = r.headers['Content-Type'].split(';')[0]
                if content_type == 'application/json':
                    self.log.debug("res : %s", r.json())
                    self.log.debug(
                        "res : %s",
                        json.dumps(r.json(), sort_keys=True, indent=2))
            return False


class CoreLoginCommand(DefaultCommand):
    """Core login command"""

    MSG_UPDATING = "Updating core/login module."
    MSG_UPDATED = "core/login module updated."
    MSG_ERROR_UPDATE = "Can not update core/login module"

    def __call__(self, args):
        super(CoreLoginCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "login",
                    "value": {
                        "resetpassword": args.allow_reset_password,
                        "failure": {
                            "size": args.nb_retry,
                        }
                    }
                }
            ]
        }]
        legends = [
            "Do not allow users to update their passwords ...",
            "Enable members visibility ..."
        ]
        return self.update(self.default_endpoint, data, legends)


class CoreFeaturesCommand(DefaultCommand):
    """Core features command"""

    MSG_UPDATING = "Updating core/features module."
    MSG_UPDATED = "core/features module updated."
    MSG_ERROR_UPDATE = "Can not update core/features module"

    def __call__(self, args):
        super(CoreFeaturesCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "features",
                    "value": {
                        "application-menu:invitation": False,
                        "control-center:invitation": False,
                        "application-menu:members": False,
                        "control-center:members": True,
                        "application-menu:communities": True,
                        "control-center:password": False,
                        "application-menu:jobqueue": False,
                        "control-center:appstore": False,
                        "application-menu:appstore": False,
                        "header:user-notification": True,
                        "header:fullscreen": True
                    }
                }
            ]
        }]
        return self.update(self.default_endpoint, data)

class CoreModulesCommand(DefaultCommand):
    """Core Modules activation command"""

    MSG_UPDATING = "Updating core/modules list."
    MSG_UPDATED = "core/modules list updated."
    MSG_ERROR_UPDATE = "Can not update core/modules list"

    def __call__(self, args):
        super(CoreModulesCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "modules",
                    "value": [
                        { "id": "linagora.esn.chat", "enabled": not args.disable_chat },
                        { "id": "linagora.esn.community", "enabled": not args.disable_community },
                        { "id": "linagora.esn.linshare", "enabled": not args.disable_linshare },
                        { "id": "linagora.esn.calendar", "enabled": True },
                        { "id":"linagora.esn.unifiedinbox", "enabled": True },
                        { "id":"linagora.esn.contact", "enabled": True}
                    ]
                }
            ]
        }]
        return self.update(self.default_endpoint, data)



class CoreDavServerCommand(DefaultCommand):
    """Dav command"""

    MSG_UPDATING = "Updating core/dav module."
    MSG_UPDATED = "core/dav module updated."
    MSG_ERROR_UPDATE = "Can not update core/dav module"

    def __call__(self, args):
        super(CoreDavServerCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "davserver",
                    "value": {
                        "backend": {
                            "url": args.backend_url
                        },
                        "frontend": {
                            "url": args.frontend_url
                        }
                    }
                }
            ]
        }]
        legends = [
            "Updating dav backend url ...",
            "Updating dav frontend url ..."
        ]
        return self.update(self.default_endpoint, data, legends)


class CoreEmailCommand(DefaultCommand):
    """Dav command"""

    MSG_UPDATING = "Updating core/email module."
    MSG_UPDATED = "core/email module updated."
    MSG_ERROR_UPDATE = "Can not update core/email module"

    def __call__(self, args):
        super(CoreEmailCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "mail",
                    "value":
                    {
                        "mail": {
                            "noreply": args.no_reply_email,
                            "feedback": args.feedback_email
                        },
                        "transport": {
                            "config": {
                                "host": args.server_host,
                                "secure": False,
                                "tls": {
                                    "rejectUnauthorized": False
                                },
                                "port": int(args.server_port)
                            }
                        }
                    }
                }
            ]
        }]
        legends = [
            "Updating feedback email ...",
            "Updating no-reply email ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class CoreWebCommand(DefaultCommand):
    """Dav command"""

    MSG_UPDATING = "Updating core/web module."
    MSG_UPDATED = "core/web module updated."
    MSG_ERROR_UPDATE = "Can not update core/web module"

    def __call__(self, args):
        super(CoreWebCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "web",
                    "value": {
                        "base_url": args.frontend_url
                    }
                }
            ]
        }]
        legends = [
            "Updating esn frontend url ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class InboxCommand(DefaultCommand):
    """Dav command"""

    MSG_UPDATING = "Updating inbox module."
    MSG_UPDATED = "inbox module updated."
    MSG_ERROR_UPDATE = "Can not update inbox module"

    def __call__(self, args):
        super(InboxCommand, self).__call__(args)
        data = [{
            "name": "linagora.esn.unifiedinbox",
            "configurations": [
                {
                    "name": "api",
                    "value": args.frontend_url + "/jmap"
                },
                {
                    "name": "composer.attachments",
                    "value": True
                },
                {
                    "name": "downloadUrl",
                    "value": args.frontend_url + "/download/{blobId}/{name}"
                },
                {
                    "name": "drafts",
                    "value": True
                },
                {
                    "name": "isJmapSendingEnabled",
                    "value": True
                },
                {
                    "name": "isSaveDraftBeforeSendingEnabled",
                    "value": False
                },
                {
                    "name": "maxSizeUpload",
                    "value": 20971520
                },
                {
                    "name": "swipeRightAction",
                    "value": "markAsRead"
                },
                {
                    "name": "uploadUrl",
                    "value": args.frontend_url + "/upload"
                },
                {
                    "name": "view",
                    "value": "messages"
                }
            ]
        }]
        legends = [
            "Updating inbox frontend url ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class ContactCommand(DefaultCommand):
    """Dav command"""

    MSG_UPDATING = "Updating contact module."
    MSG_UPDATED = "contact module updated."
    MSG_ERROR_UPDATE = "Can not update contact module"

    def __call__(self, args):
        super(ContactCommand, self).__call__(args)
        data = [{
            "name": "linagora.esn.contact",
            "configurations": [
                {
                    "name": "features",
                    "value": {
                        "isSharingAddressbookEnabled": True,
                        "isVirtualUserAddressbookEnabled": True,
                        "isVirtualFollowingAddressbookEnabled": False
                    }
                }
            ]
        }]
        legends = [
            "Updating contact features ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class CalendarCommand(DefaultCommand):
    """Calendar command"""

    MSG_UPDATING = "Updating calendar module."
    MSG_UPDATED = "calendar module updated."
    MSG_ERROR_UPDATE = "Can not update calendar module"

    def __call__(self, args):
        super(CalendarCommand, self).__call__(args)
        data = [{
            "name": "linagora.esn.calendar",
            "configurations": [
                {
                    "name": "features",
                    "value": {
                        "isSharingCalendarEnabled": args.enable_sharing_calendar
                    }
                }
            ]
        }]
        legends = [
            "Updating calendar features ...",
            "Updating sharing calendar feature ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class LemonLDAPCommand(DefaultCommand):
    """LemonLDAP command"""

    MSG_UPDATING = "Updating lemonldap module."
    MSG_UPDATED = "lemonldap module updated."
    MSG_ERROR_UPDATE = "Can not update lemonldap module"

    def __call__(self, args):
        super(LemonLDAPCommand, self).__call__(args)
        data = [{
            "name": "linagora.esn.lemonldap",
            "configurations": [
                {
                    "name": "mapping",
                    "value": {
                        "ll-auth-user": "AUTH-USER",
                        "ll-auth-domain": "AUTH-DOMAIN",
                        "firstname": "AUTH-FIRST-NAME",
                        "lastname": "AUTH-LAST-NAME"
                    }
                },
                {
                    "name": "logoutUrl",
                    "value": args.logout_url
                }
            ]
        }]
        legends = [
            "Updating lemonldap parameters ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class JamesCommand(DefaultCommand):
    """James command"""

    MSG_UPDATING = "Updating james module."
    MSG_UPDATED = "james module updated."
    MSG_ERROR_UPDATE = "Can not update james module"

    def __call__(self, args):
        super(JamesCommand, self).__call__(args)
        data = [{
            "name": "linagora.esn.james",
            "configurations": [
                {
                    "name": "webadminApiFrontend",
                    "value": args.frontend_url
                },
                {
                    "name": "webadminApiBackend",
                    "value": args.backend_url
                }
            ]
        }]
        legends = [
            "Updating james parameters ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class LinShareCommand(DefaultCommand):
    """LinShare command"""

    MSG_UPDATING = "Updating linshare module."
    MSG_UPDATED = "linshare module updated."
    MSG_ERROR_UPDATE = "Can not update linshare module"

    def __call__(self, args):
        super(LinShareCommand, self).__call__(args)
        data = [{
            "name": "linagora.esn.linshare",
            "configurations": [
                {
                    "name": "apiBasePathBackend",
                    "value": args.backend_url
                },
                {
                    "name": "apiBasePathFrontend",
                    "value": args.frontend_api_url
                },
                {
                    "name": "instanceURL",
                    "value": args.frontend_url
                }
            ]
        }]
        legends = [
            "Updating linshare parameters ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class GeneralCommand(DefaultCommand):
    """General command"""

    MSG_UPDATING = "Updating core/general module."
    MSG_UPDATED = "core/general module updated."
    MSG_ERROR_UPDATE = "Can not update core/general module"

    def __call__(self, args):
        super(GeneralCommand, self).__call__(args)
        data = [{
            "name": "core",
            "configurations": [
                {
                    "name": "businessHours",
                    "value": [
                        {
                            "daysOfWeek": [1, 2, 3, 4, 5],
                            "start": "09:00",
                            "end": "18:00"
                        }
                    ]
                },
                {
                    "name": "datetime",
                    "value": {
                        "timeZone": "GMT",
                        "use24hourFormat": args.time_format_24
                    }
                }
            ]
        }]
        legends = [
            "Updating core/general parameters ...",
        ]
        return self.update(self.default_endpoint, data, legends)


class LDAPCommand(DefaultCommand):
    """LDAP command"""

    MSG_UPDATING = "Updating core/ldap module."
    MSG_UPDATED = "core/ldap module updated."
    MSG_ERROR_UPDATE = "Can not update core/ldap module"

    def __call__(self, args):
        super(LDAPCommand, self).__call__(args)
        domain_id = self.get_my_domain_id()

        if not domain_id:
            return False

        ldap_parameters = {
            "name": args.name,
            "bind_dn": args.bind_dn,
            "bind_password": args.bind_password,
            "uri": args.uri,
            "search_base": args.search_base,
            "search_filter": args.search_filter,
            "usage_auth": args.usage_auth,
            "usage_search": args.usage_search,
            "usage_provisioning": args.usage_provisioning
        }

        return self.create_ldap_connection(domain_id, self.login, self.password, ldap_parameters)


class AutoconfCommand(DefaultCommand):
    """Autoconf command"""

    MSG_UPDATING = "Updating core/autoconf module."
    MSG_UPDATED = "core/autoconf module updated."
    MSG_ERROR_UPDATE = "Can not update core/autoconf module"

    def __call__(self, args):
        super(AutoconfCommand, self).__call__(args)
        r = self.session.get(self.base_url + '/api/user',
                             headers=self.headers,
                             auth=HTTPBasicAuth(self.login, self.password),
                             verify=not self.no_verify)
        if r.status_code != 200:
            self.log.error("Can not get user'domain.")
            return False
        domain_id = r.json()['domains'][0]['domain_id']
        self.log.debug("domain_id : %s", domain_id)
        endpoint = '/admin/api/autoconf?domain_id=' + domain_id
        data = {
            "imap":{
                "hostName": args.imap_host,
                "port": args.imap_port,
                "socketType":"2"
            },
            "smtp":{
                "description": "SMTP",
                "hostname": args.smtp_host,
                "port": args.smtp_port,
                "socketType":"2"
            }
        }
        self.log.debug("data : %s", json.dumps(data, sort_keys=True, indent=2))
        legends = [
            "Updating core/autoconf parameters ...",
        ]
        return self.update(endpoint, data, legends)

class CreateDomainCommand(DefaultCommand):
    """Create domain command"""

    MSG_UPDATING = "Creating domain..."
    MSG_UPDATED = "Domain created."
    MSG_ERROR_UPDATE = "Could not create domain."

    def allow_users_to_setup_forwardings(self, domain_id, admin_login, admin_password):
        endpoint = '/unifiedinbox/api/inbox/forwardings/configurations?scope=domain&domain_id=' + domain_id
        data = {"forwarding": True,"isLocalCopyEnabled": True}

        r = self.session.put(self.base_url + endpoint,
            data=json.dumps(data),
            headers=self.headers,
            auth=HTTPBasicAuth(admin_login, admin_password),
            verify=not self.no_verify)

        if r.status_code in [200, 204]:
            self.log.debug("status_code : %s", r.status_code)
            self.log.info("Inbox forwardings enabled.")
            return True

        self.log.error("Error setting up inbox forwarding: %s : %s", r.status_code, r.text)
        return False

    def get_domain_ldap_connection(self, domain_id, admin_login, admin_password):
        endpoint = '/api/configurations?scope=domain&domain_id=' + domain_id
        data = [{
            "name": "core",
            "keys": ["ldap"]
        }]
        r = self.session.post(self.base_url + endpoint,
            data=json.dumps(data),
            headers=self.headers,
            auth=HTTPBasicAuth(admin_login, admin_password),
            verify=not self.no_verify)

        if r.status_code != 200:
            self.log.error("Can't retrieve ldap connection parameters.")
            return {}

        data = r.json()[0]['configurations'][0]['value'][0]
        ldap_parameters = {
            "name": data['name'],
            "bind_dn": data['configuration']['adminDn'],
            "bind_password": data['configuration']['adminPassword'],
            "uri": data['configuration']['url'],
            "search_base": data['configuration']['searchBase'],
            "search_filter": data['configuration']['searchFilter'],
            "usage_auth": data['usage']['auth'],
            "usage_search": data['usage']['search'],
            "usage_provisioning": data['usage']['autoProvisioning']
        }

        return ldap_parameters

    def create_related_ldap_connection(self, new_domain_id, new_admin_email, new_admin_password, ldap_search_base, domain_name):
        # Get reference LDAP parameters
        reference_domain_id = self.get_my_domain_id()
        ldap_parameters = self.get_domain_ldap_connection(reference_domain_id, self.login, self.password)

        if not ldap_parameters:
            return False

        ldap_parameters['search_base'] = ldap_search_base
        ldap_parameters['name'] = ldap_parameters['name'] + " - " + domain_name

        return self.create_ldap_connection(new_domain_id, new_admin_email, new_admin_password, ldap_parameters)

    def __call__(self, args):
        super(CreateDomainCommand, self).__call__(args)
        r = self.session.get(self.base_url + '/api/domains?name=' + args.domain_name,
            headers=self.headers,
            auth=HTTPBasicAuth(self.login, self.password),
            verify=not self.no_verify)

        if r.status_code != 200:
            self.log.error("Cannot check if domain already exists: %s : %s", r.status_code, r.text)
            return False

        if r.json():
            self.log.error("Domain already exists.")
            return False

        r = self.session.get(self.base_url + '/api/availability?resourceType=email&resourceId=' + args.new_admin_email,
            headers=self.headers,
            auth=HTTPBasicAuth(self.login, self.password),
            verify=not self.no_verify)

        if r.status_code != 200:
            self.log.error("Cannot check if admin email address is available.")
            return False

        if not r.json()['available']:
            self.log.error("Admin email address is already taken.")
            return False

        data = {
            "name": args.domain_name,
            "company_name": args.domain_name,
            "administrator": {
                "email": args.new_admin_email,
                "password": args.new_admin_password
            }
        }

        r = self.session.post(self.base_url + '/api/domains',
            headers=self.headers,
            data=json.dumps(data),
            auth=HTTPBasicAuth(self.login, self.password),
            verify=not self.no_verify)

        if r.status_code != 201:
            self.log.error("Error creating domain: %s : %s", r.status_code, r.text)
            return False

        self.log.debug("status_code : %s", r.status_code)
        self.log.info(self.MSG_UPDATED)

        new_domain_id = r.json()['id']

        # Configure the new domain
        result = self.create_related_ldap_connection(new_domain_id, args.new_admin_email, args.new_admin_password, args.ldap_search_base, args.domain_name)

        if not result:
            return False

        return self.allow_users_to_setup_forwardings(new_domain_id, args.new_admin_email, args.new_admin_password)


class EsnCLI(BasicProgram):
    """Main program."""

    def add_config_options(self):
        super(EsnCLI, self).add_config_options()

        default = self.config.get_default_section()
        default.add_element(Element(
            "login",
            default=os.environ.get('ESN_CLI_LOGIN', None),
            required=True,
            desc="Email of an administrator. You can set an env variable ESN_CLI_LOGIN instead of this parameter."))

        default.add_element(Element(
            "password",
            default=os.environ.get('ESN_CLI_PASSWORD', None),
            required=True,
            desc="Password of the administrator. You can set an env variable ESN_CLI_PASSWORD instead of this parameter."))

        default.add_element(Element(
            "url",
            default=os.environ.get('ESN_CLI_URL', None),
            required=True,
            desc="Base url of esn like https://192.168.1.1. You can set an env variable ESN_CLI_URL instead of this parameter."))

        default.add_element(Element(
            "host",
            default=os.environ.get('ESN_CLI_HOST', None),
            desc="""Vhost name to override IP if needed.
            ex 'op-admin.openpaas.org'. You can set an env variable ESN_CLI_HOST instead of this parameter."""))

    def add_commands(self):
        super(EsnCLI, self).add_commands()
        self.parser.add_argument(
            "-l", "--login",
            action="store",
            **self.config.default.login.get_arg_parse_arguments())
        self.parser.add_argument(
            "-p", "--password",
            **self.config.default.password.get_arg_parse_arguments())
        self.parser.add_argument(
            "--url",
            **self.config.default.url.get_arg_parse_arguments())
        self.parser.add_argument(
            "--host",
            **self.config.default.host.get_arg_parse_arguments())

        self.parser.add_argument("--no-verify", action="store_true",
                                 default=False,
                                 help="Do not verify SSL certificate")

        subparsers = self.parser.add_subparsers()

        parser = subparsers.add_parser(
            'password',
            help="Description of password")
        parser.add_argument("-n", "--new-password",
                            required=True,
                            help="new admin password.")

        parser.set_defaults(__func__=PasswordCommand(self.config))

        # core-login
        parser = subparsers.add_parser(
            'core-login',
            help="Description of core-login")
        parser.add_argument(
            "-r", "--nb_retry", default=6, type=int,
            help="""Threshold before locking account after to many
            authentication failure. Default: 6""")
        parser.add_argument(
            "-a", "--allow-reset-password", default=False,
            action="store_true",
            help="Do not allow users to reset their password with ESN")
        parser.set_defaults(__func__=CoreLoginCommand(self.config))

        # core-features
        parser = subparsers.add_parser(
            'core-features',
            help="Description of core-features")
        parser.set_defaults(__func__=CoreFeaturesCommand(self.config))

        # core-modules
        parser = subparsers.add_parser(
            'core-modules',
            help="Description of core-modules")
        parser.add_argument(
            "--disable-linshare", default=False,
            action="store_true",
            help="Enable the LinShare module. Default: %(default)s")
        parser.add_argument(
            "--disable-community", default=False,
            action="store_true",
            help="Enable the Community module. Default: %(default)s")
        parser.add_argument(
            "--disable-chat", default=False,
            action="store_true",
            help="Enable the Chat module. Default: %(default)s")
        parser.set_defaults(__func__=CoreModulesCommand(self.config))

        # core-dav
        parser = subparsers.add_parser(
            'core-dav',
            help="Description of core-dav")
        parser.add_argument(
            "-b", "--backend-url", default="http://sabre:80",
            help="Default value for sabre backend url. Default: %(default)s")
        parser.add_argument(
            "-f", "--frontend-url", required=True,
            help="Sabre frontend url. ex: https://dav.openpaas.org")
        parser.set_defaults(__func__=CoreDavServerCommand(self.config))

        # core-email
        parser = subparsers.add_parser(
            'core-email',
            help="Description of core-email")
        parser.add_argument(
            "--no-reply-email", required=True,
            help="")
        parser.add_argument(
            "--feedback-email", required=True,
            help="")
        parser.add_argument(
            "--server-host", default="james",
            help="")
        parser.add_argument(
            "--server-port", default="25",
            help="")

        parser.set_defaults(__func__=CoreEmailCommand(self.config))

        # core-web
        parser = subparsers.add_parser(
            'core-web',
            help="Description of core-web")
        parser.add_argument(
            "-f", "--frontend-url", required=True,
            help="ESN frontend url. ex: https://openpaas.openpaas.org")
        parser.set_defaults(__func__=CoreWebCommand(self.config))

        # inbox
        parser = subparsers.add_parser(
            'inbox',
            help="Description of inbox")
        parser.add_argument(
            "-f", "--frontend-url", required=True,
            help="""Default url for jmap frontend.
            ex: https://jmap.openpaas.org""")
        parser.set_defaults(__func__=InboxCommand(self.config))

        # contact
        parser = subparsers.add_parser(
            'contact',
            help="Description of contact")
        parser.set_defaults(__func__=ContactCommand(self.config))

        # calendar
        parser = subparsers.add_parser(
            'calendar',
            help="Description of calendar")
        parser.add_argument(
            "--enable-sharing-calendar", default=False,
            action="store_true",
            help="""Allow users to reset their password
            with ESN (Default: %(default)s)""")
        parser.set_defaults(__func__=CalendarCommand(self.config))

        # lemonldap
        parser = subparsers.add_parser(
            'lemonldap',
            help="Description of lemonldap")
        parser.add_argument(
            "-u", "--logout-url", required=True,
            help="""Default logout url for esn.
            ex: https://auth.openpaas.org/?logout=1""")
        parser.set_defaults(__func__=LemonLDAPCommand(self.config))

        # james
        parser = subparsers.add_parser(
            'james',
            help="Description of james")
        parser.add_argument(
            "-b", "--backend-url", default="http://james-admin:8000",
            help="Default value for james backend url. Default: %(default)s")
        parser.add_argument(
            "-f", "--frontend-url", required=True,
            help="""Default value for james frontend url.
            ex: https://james-admin.openpaas.org""")
        parser.set_defaults(__func__=JamesCommand(self.config))

        # linshare
        parser = subparsers.add_parser(
            'linshare',
            help="Description of linshare")
        parser.add_argument(
            "-b", "--backend-url",
            default="http://linshare-backend:8080/linshare/webservice/rest",
            help="""Default value for linshare backend url.
            Default: %(default)s""")
        parser.add_argument(
            "-f", "--frontend-url", required=True,
            help="""Default value for linshare frontend.
            ex: https://linshare.openpaas.org""")
        parser.add_argument(
            "-a", "--frontend-api-url", required=True,
            help="""Default value of linshare api used by the browser.
            ex: https://linshare-external.openpaas.org/linshare/webservice/rest""")
        parser.set_defaults(__func__=LinShareCommand(self.config))

        # general
        parser = subparsers.add_parser(
            'general',
            help="Description of general")
        parser.add_argument(
            "--time-format-24", default=False,
            action="store_true",
            help="Display time format in french (Default: %(default)s)")
        parser.set_defaults(__func__=GeneralCommand(self.config))

        # core-ldap
        parser = subparsers.add_parser(
            'core-ldap',
            help="Description of core-ldap")
        parser.add_argument("--uri", required=True, help="ldap://...")
        parser.add_argument("--name", required=True, help="LDAP public name")
        parser.add_argument("--bind-dn", required=True, help="")
        parser.add_argument("--bind-password", required=True, help="")
        parser.add_argument("--search-base", required=True, help="")
        parser.add_argument("--search-filter",
                            default='(mail={{username}})',
                            help="Default value: %(default)s")
        parser.add_argument("--usage-auth",
                            action="store_true", default=False,
                            help="Enable LDAP for authentication.")
        parser.add_argument("--usage-provisioning",
                            action="store_true", default=False,
                            help="Enable LDAP for provisioning.")
        parser.add_argument("--usage-search",
                            action="store_true", default=False,
                            help="Enable LDAP for search.")
        parser.set_defaults(__func__=LDAPCommand(self.config))

        # autoconf
        parser = subparsers.add_parser(
            'autoconf',
            help="Description of autoconf")
        parser.add_argument("--smtp-host", required=True, help="")
        parser.add_argument("--smtp-port", type=int,
                            default=143, help="")
        parser.add_argument("--imap-host", required=True, help="")
        parser.add_argument("--imap-port", type=int,
                            default=587, help="")
        parser.set_defaults(__func__=AutoconfCommand(self.config))

        parser = subparsers.add_parser(
            'whoami',
            help="Description of autoconf")
        parser.set_defaults(__func__=WhoAmICommand(self.config))

        # Create domain
        parser = subparsers.add_parser(
            'domain-create',
            help="Create a domain in ESN")
        parser.add_argument(
            "--name", dest= "domain_name",
            required=True,
            help="Name of the domain to create, e.g. mydomain.open-paas.org.")
        parser.add_argument(
            "--new-admin-email",
            required=True,
            help="Email address of the 1st admin of the domain, e.g. admin@mydomain.open-paas.org.")
        parser.add_argument(
            "--new-admin-password",
            default=os.environ.get('ESN_NEW_ADMIN_PASSWORD', None),
            required=True,
            help="Password of the 1st admin of the domain. You can set an env variable ESN_NEW_ADMIN_PASSWORD instead of this parameter.")
        parser.add_argument(
            "--ldap-search-base",
            required=True,
            help="Branch of the LDAP to look for users of this domain. e.g. ou=mydomain.com,ou=users,dc=openpaas,dc=org")
        parser.set_defaults(__func__=CreateDomainCommand(self.config))

PROG = EsnCLI(
    "esncli",
    desc="Description of program init.esn.config.py.")
if __name__ == "__main__":
    PROG()
