""" """
from enum import IntEnum

import conductor

NETWORK_ASSET_URL = conductor.NETWORK_ASSET_URL() + '/airfinder/'

SYMBLE_SETTINGS = {
    "symbleHeartbeat_reported": 60,
    "locationUpdateRate_reported": 11,
    "scansPerFix_reported": 4,
    "networkLostTimeout_reported": 600,
    "refLostTimeout": 600,
    "networkScanInterval_reported": 180,
    "networkToken": "4f50454e"
}

BACKHAUL_SETTINGS = {
    "noApHeartbeatInterval": 86400,
    "noRpHeartbeatInterval": 86400,
    "noApLocationUpdateRate": 21600,
    "noRpLocationUpdateRate": 21600,
    "maxWifis": 10,
    "maxCellIds": 0,
    "locationUpdateOrder": {
        "gpsLocationOrder": 1,
        "wifiLocationOrder": 2,
        "cellLocationOrder": 3
    }
}

ACCEL_SETTINGS = {
    "Enable": 1,
    "MovementDuration": 3,
    "Threshold": 80,
    "shockThreshold": 160
}

CACHING_SETTINGS = {
    "cachedMessagesEnable": 0,
    "noRpMessagesCached": 0
}

GPS_SETTINGS = {
    "gpsPowerMode": 0,
    "gpsTimeout": 180
}

HELP_MODE_SETTINGS = {
    "helpModeUpdateRate": 60
}

SITE_USER_PERMISSIONS = {
    "Admin": False,
    "Status": True,
    "AddTags": True,
    "EditDeleteTags": True,
    "EditDeleteGroupsCategories": False
}


class AirfinderBase(conductor.ConductorSubject):
    """
    The class that all Airfinder classes are Based off.

    All Airfinder classes are Conductor Subjects, but will
    additionally always contain metadata, enabled field, and
    a human-readable name.
    """
    @property
    def enabled(self):
        return bool(self._data.get('enabled'))

    @property
    def metadata(self):
        return self._data.get('assetInfo').get('metadata').get('props')

    @property
    def name(self):
        return self._data.get('value')

    def __repr__(self):
        return '{} {} ({})'.format(self.__class__.__name__, self.subject_id, self.name)


class EventCount(conductor.EventCount):
    event_type = 'airfinderLocation'


class User(conductor.ConductorAccount):
    """
    This class provides methods for interacting with Airfinder through Conductor for any
    particular account.

    This is the starting point for everything else in this module. Initialize with your
    username and password. If the password is omitted the initializer will prompt for one.
    Optionally provide the account name that you're trying to access (if you don't provide
    the account, the constructor will try to figure out which account is linked to your username).
    """
    subject_name = "User"

    def _get_registered_af_asset(self, subject_name, subject_id):
        """ Base function for getting a registered asset from the Network Asset API. """
        return self._get_registered_asset("airfinder/" + subject_name, subject_id)

    def _get_registered_af_assets(self, asset_name):
        """ Base function for getting list of registered assets from the Network Asset API. """
        return self._get_registered_assets("airfinder/" + asset_name)

    def get_sites(self):
        """ Get all the sites this user has access to. """
        return [Site(self.session, x.get('id'), _data=x)
                for x in self._get_registered_af_assets('sites')]

    def get_site(self, site_id):
        """ Get a specific site. """
        x = self._get_registered_af_asset('site', site_id)
        return Site(self.session, x.get('id'), _data=x)

    def create_site(self, name):
        """" Create a site with the given name. """
        url = ''.join([NETWORK_ASSET_URL, 'sites'])
        data = {
            "configType": "Site",
            "configValue": name,
            "properties": {}
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        x = resp.json()
        return Site(self.session, x.get('id'), _data=x)

    def delete_site(self, site):
        """ Delete a specific site. """
        url = ''.join([NETWORK_ASSET_URL, 'site'])
        param = {'siteId': site}
        resp = self.session.delete(url, params=param)
        resp.raise_for_status()
        return resp.json()

    def create_site_user(self, email, site, site_user_permissions=None):
        """ Create a Site User. """
        if site_user_permissions is None:
            site_user_permissions = SITE_USER_PERMISSIONS

        url = ''.join([NETWORK_ASSET_URL, 'users'])
        data = {
            "sites": [str(site)],
            "email": email,
            "permissions": site_user_permissions
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        x = resp.json()
        return SiteUser(self.session, x['id'], _data=x)


class SiteUser(AirfinderBase):
    """
    This class is used to manage other Airfinder SiteUsers,
    given the User has Admin-level permissions.
    """
    subject_name = 'SiteUser'

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    @property
    def can_add_tags(self):
        """ Can the SiteUser add tags? """
        return bool(self.metadata.get('AddTags'))

    @property
    def is_admin(self):
        """ Is the SiteUser an Admin? """
        return bool(self.metadata.get('Admin'))

    @property
    def can_edit_delete_groups_categories(self):
        """ Can the SiteUser Edit/Delete Groups and Categories? """
        return bool(self.metadata.get('EditDeleteGroupsCategories'))

    @property
    def can_edit_delete_tags(self):
        """ Can the SiteUser Edit/Delete tags? """
        return bool(self.metadata.get('EditDeleteTags'))

    @property
    def email(self):
        """ The SiteUser's email address. """
        return self.metadata.get('email')

    @property
    def user_id(self):
        return self.metadata.get('userId')

    @property
    def status(self):
        return bool(self.metadata.get('Status'))

    @property
    def site(self):
        return Site(self.session, self.metadata.get('siteId'))

    def forgot_password(self):
        """ Sends the site user an email to reset their password. """
        url = ''.join([NETWORK_ASSET_URL, 'users/forgotPassword'])
        params = {'email': self.email}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def resend_email(self):
        """ Resends the site user an email to reset their password. """
        url = ''.join([NETWORK_ASSET_URL, 'users/resend'])
        params = {'email': self.email}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


class Site(AirfinderBase):
    """ Represents an Airfinder Site. """
    subject_name = 'Site'

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    @property
    def owner_account_id(self):
        return self.metadata.get('accountId')

    def _get_registered_asset_by_site(self, subject_name, subject_id):
        """ Gets a registered asset by site-id. """
        url = ''.join([NETWORK_ASSET_URL, '{}/{}'.format(subject_name, subject_id)])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def _get_registered_assets_by_site(self, asset_name):
        """ Gets all the registered assets by site-id. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def rename(self, name):
        """ Rename an existing site. """
        # TODO
        url = ''.join([NETWORK_ASSET_URL, 'sites'])
        param = {'siteId': self.subject_id}
        updates = {
            "name": name,
        }
        resp = self.session.put(url, params=param, json=updates)
        resp.raise_for_status()
        _data = resp.json()

    def get_site_users(self):
        """ Gets all the site-users, in the site. """
        return [SiteUser(self.session, x.get('id'), _data=x) for x in
                self._get_registered_assets_by_site('users')]

    def get_site_user(self, site_user_id):
        """ Gets a site-user in a site. """
        x = self._get_registered_asset_by_site('user', site_user_id)
        return SiteUser(self.session, x.get('id'), _data=x)

    def get_areas(self):
        """ Gets all the areas for a site. """
        return [Area(self.session, x.get('id'), self, _data=x) for x in
                self._get_registered_assets_by_site('areas')]

    def create_area(self, name):
        """ Create an area as a part of this Site. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def delete_area(self, area_id):
        """ Delete an area. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_area(self, area_id):
        """ Gets an area in a site. """
        x = self._get_registered_asset_by_site('area', area_id)
        return Area(self.session, x.get('id'), self, _data=x)

    def get_workflows(self):
        """ Gets all the workflows for the Site. """
        return self._get_registered_assets_by_site('workflows')

    def get_workflow(self, workflow_id):
        """" Gets a workflow for the Site. """
        return self._get_registered_asset_by_site('workflow', workflow_id)

    def remove_locations(self, locations):
        """ Remove locations from a Site. """
        # TODO: test
        url = ''.join([NETWORK_ASSET_URL, 'tags'])
        data = {
            "nodeAddresses": [locations],
            "siteId": self.subject_id
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_tags(self):
        """ Gets all the tags in a site. """
        return self._get_registered_assets_by_site('tags')

    def get_tag(self, mac_id):
        """ Gets a tag in the site. """
        return self._get_registered_asset_by_site('tag', mac_id)

    def add_tag(self, mac_id, field1="", field2="", category=None, description=""):
        """ Adds a tag in the site. """
        url = ''.join([NETWORK_ASSET_URL, 'tags'])
        params = {
            "accountId": self.metadata.get('accountId'),
            "macAddress": mac_id,
            "siteId": self.subject_id,
            "description": description,
            "categoryId": category,
            "groups": [""],
            "field1": field1,
            "field2": field2,
            "properties": "object",
            "homeLocation": "",
            "adjacentLocations": [""],
            "trackTagAge": ""
        }
        resp = self.session.post(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def bulk_add_tags(self, file_name):
        """ Bulk-add tags to an airfinder site. """
        raise NotImplemented

    def remove_tag(self, mac_id):
        """ Remove a tag to an airfinder site. """
        url = ''.join([NETWORK_ASSET_URL, 'tags'])
        params = {
            "nodeAddress": mac_id,
            "accountId": self.metadata.get('accountId'),
            "siteId": self.subject_id
        }
        resp = self.session.post(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def bulk_add_locations(self, file_name):
        """ Bulk-add locations to a site. """
        raise NotImplemented

    def get_groups(self):
        """ Get all the groups in a site. """
        return self._get_registered_assets_by_site('groups')

    def get_group(self, group_id):
        """ Get a group from a site. """
        return self._get_registered_asset_by_site('group', group_id)

    def get_categories(self):
        """ Get all the categories in a site."""
        return self._get_registered_assets_by_site('categories')

    def get_category(self, category_id):
        """ Get a category in a site. """
        return self._get_registered_asset_by_site('category', category_id)

    def get_asset_group(self):
        """ Get the Site as an Asset Group. """
        x = _get_registered_asset_by_site('assetGroup')
        return AssetGroup(self.session, x['id'], _data=x)


class Area(AirfinderBase):
    """ Represents an Airfinder Area inside of an Airfinder Site. """
    subject_name = 'Area'

    def __init__(self, session, subject_id, parent_site, _data=None):
        super().__init__(session, subject_id, _data)
        self.parent_site = parent_site

    def _get_registered_asset_by_area(self, subject_name, subject_id):
        """ Base function for getting a registered asset from the Network Asset API. """
        url = ''.join([NETWORK_ASSET_URL, '{}/{}'.format(subject_name, subject_id)])
        params = {'siteId': self.parent_site.subject_id, 'areaId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def _get_registered_assets_by_area(self, asset_name):
        """ Base function for getting list of registered assets from the Network Asset API. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.parent_site.subject_id, 'areaId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    @property
    def area_location(self):
        """ The issuance ID is the subject ID from the ConductorSubject base class. """
        return self.metadata.get('areaLocation')

    def get_parent_site(self):
        """ Get the Site that the area is within. """
        return self.parent_site

    def get_area_location(self):
        """ Get the location of the area; Outdoor will return coordinates, Indoor will return a mapping. """
        if 'Outdoor' == self.area_location:
            return self.metadata.get('points')
        elif 'Indoor' == self.area_location:
            return self.metadata.get('indoorMapping')

    def get_zones(self):
        """ Get all the Zones within the Area. """
        return [Zone(self.session, x.get('id'), self, _data=x) for x in
                self._get_registered_assets_by_area('zones')]

    def get_zone(self, zone_id):
        """ Get a Zone within the Area. """
        x = self._get_registered_asset_by_area('zone', zone_id)
        return Zone(self.session, x.get('id'), self, _data=x)

    def create_zone(self, name):
        """ Add a zone to the Area. """
        url = ''.join([NETWORK_ASSET_URL, 'zones'])
        params = {
            "siteId": self.parent_site.subject_id,
            "configType": "Zone",
            "configValue": name,
            "properties": "object",
        }
        resp = self.session.post(url, params=params)
        resp.raise_for_status()
        x = resp.json()
        return Zone(self.session, x.get('id'), self, _data=x)

    # TODO: Move this to zone.
    def delete_zone(self, zone_id):
        """ Remove a Zone from an Area. """
        url = ''.join([NETWORK_ASSET_URL, 'zones'])
        params = {"zoneId": zone_id}
        resp = self.session.delete(url, params=params)
        resp.raise_for_status()
        return resp.json()


class Zone(AirfinderBase):
    """ An Airfinder Zone within an Airfinder Area. """
    subject_name = 'Zone'

    def __init__(self, session, subject_id, parent_area, _data=None):
        super().__init__(session, subject_id, _data)
        self.parent_area = parent_area

    def _get_registered_asset_by_zone(self, subject_name, subject_id):
        """ Base function for getting a registered asset from the Network Asset API. """
        url = ''.join([NETWORK_ASSET_URL, '{}/{}'.format(subject_name, subject_id)])
        params = {
            'siteId': self.parent_area.parent_site.subject_id,
            'areaId': self.parent_area.subject_id,
            'zoneId': self.subject_id
        }
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def _get_registered_assets_by_zone(self, asset_name):
        """ Base function for getting list of registered assets from the Network Asset API. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {
            'siteId': self.parent_area.parent_site.subject_id,
            'areaId': self.parent_area.subject_id,
            'zoneId': self.subject_id
        }
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_locations(self):
        """ Get all the locations in a site. """
        return [Location(self.session, x.get('assetInfo').get('metadata').get('props').get('macAddress'), _data=x) for x in
                self._get_registered_assets_by_zone('locations')]

    def get_location(self, mac_id):
        """ Gets a location, in a site. """
        x = self._get_registered_asset_by_zone('location', mac_id)
        return Location(self.session, mac_id, _data=x)

    def add_location(self, mac_id, name):
        """ Adds a location to a site. """
        url = ''.join([NETWORK_ASSET_URL, 'locations'])
        params = {
            "accountId": 0,
            "macAddress": mac_id,
            'siteId': self.parent_area.parent_site.subject_id,
            'areaId': self.parent_area.subject_id,
            'zoneId': self.subject_id,
            "name": name,
            "properties": "object",
            "proxyLocations": [
                ""
            ]
        }
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        x = resp.json()
        return Location(self.session, x.get('id'), _data=x)

    def remove_location(self, mac_id):
        """ Remove a location from a site. """
        raise NotImplemented


class Tag(conductor.Module, AirfinderBase):
    """docstring for Tag"""

    def update_configuration(self, symble_conf=None, accel_conf=None, help_conf=None):
        """ TODO """
        raise NotImplemented

    def get_location(self):
        """ """
        raise NotImplemented


class Location(Tag):
    """ Represents an Airfinder Location. """
    subject_name = 'Location'

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    @property
    def node_address(self):
        return self._data.get('nodeAddress')

    @property
    def mac_address(self):
        return self.metadata.get('macAddress')

    @property
    def initial_detection_time(self):
        return conductor.parse_time(self._data.get('initialDetectionTime'))

    @property
    def registration_detection_time(self):
        return conductor.parse_time(self._data.get('registrationTime'))

    @property
    def last_provisioned_time(self):
        return conductor.parse_time(self.metadata.get('lastProvisionedTime'))

    @property
    def initial_provisioned_time(self):
        return conductor.parse_time(self.metadata.get('initialProvisionedTime'))

    @property
    def name(self):
        return self._data.get('nodeName')

    @property
    def site(self):
        return Site(self.session, self.metadata.get('siteId'))

    @property
    def area(self):
        return Area(self.session, self.site, self.metadata.get('areaId'))

    @property
    def zone(self):
        return Zone(self.session, self.area, self.metadata.get('zoneId'))

    @property
    def battery_status(self):
        return bool(self.metadata.get('batteryStatus'))

    @property
    def is_lost(self):
        return self.metadata.get('isLost')


class Supertag(Tag):
    """ """

    class DownlinkMessageType(IntEnum):
        DOWNLINK_CONFIGURATION = 0x01
        TEST_MODE_EN = 0x02
        HELP_MSG_RXED = 0x03

    DL_f = "{msg_type:02x}{msg_spec:02x}{data}".format
    DL_CONF_V1_f = "{change_msk:04x}{heartbeat_int:08x}{no_ap_heartbeat_int:08x}" \
                   "{no_rp_heartbeat_int:08x}{loc_update_rate:08x}{no_ap_loc_update_rate:08x}" \
                   "{no_rp_loc_update_rate:08x}{scan_per_fix:02x}{wifi_ap:02x}{cell_id:02x}" \
                   "{loc_update_order:02x}{net_lost_timeout:04x}{ref_lost_timeout:04x}" \
                   "{net_scan_int:04x}".format
    DL_CONF_V2_f = "{change_msk:08x}{heartbeat_int:08x}{no_ap_heartbeat_int:08x}" \
                   "{no_rp_heartbeat_int:08x}{loc_update_rate:08x}{no_ap_loc_update_rate:08x}" \
                   "{no_rp_loc_update_rate:08x}{help_mode_update_rate:08x}{scan_per_fix:02x}" \
                   "{wifi_ap:02x}{cell_id:02x}{loc_update_order:02x}{accel_en:02x}" \
                   "{accel_mvm_dur:04x}{accel_thresh:04x}{shock_thresh:04x}{msg_cache_en:02x}" \
                   "{msg_cache_num:02x}{gps_pwr_mode:02x}{gps_timeout:04x}{net_lost_timeout:04x}" \
                   "{ref_lost_timeout:04x}{net_scan_int:04x}{net_tok:08x}".format

    def update_configuration(self, symble_conf=None, accel_conf=None, help_conf=None, backhaul_conf=None,
                             caching_conf=None, gps_conf=None, gateway_addr=None, acked=True, time_to_live_s=60.0,
                             port=0, priority=10):
        """ TODO """
        if not symble_conf:
            symble_conf = SYMBLE_SETTINGS
        if not accel_conf:
            accel_conf = ACCEL_SETTINGS
        if not help_conf:
            help_conf = HELP_MODE_SETTINGS
        if not backhaul_conf:
            backhaul_conf = BACKHAUL_SETTINGS
        if not caching_conf:
            caching_conf = CACHING_SETTINGS
        if not gps_conf:
            gps_conf = GPS_SETTINGS

        #    "locationUpdateOrder"
        #        "gpsLocationOrder": 1,
        #        "wifiLocationOrder": 2,
        #        "cellLocationOrder": 3

        self.send_message(
            self.DL_f(msg_type=self.DownlinkMessageType.DOWNLINK_CONFIGURATION,
                      msg_spec=0x02,  # TODO
                      data=
                      self.DL_CONF_V2_f(
                          change_msk=0,
                          heartbeat_int=symble_conf[''],
                          no_ap_heartbeat_int=backhaul_conf['noApHeartbeatInterval'],
                          no_rp_heartbeat_int=backhaul_conf['noRpHeartbeatInterval'],
                          loc_update_rate=symble_conf[''],
                          no_ap_loc_update_rate=backhaul_conf['noApLocationUpdateRate'],
                          no_rp_loc_update_rate=backhaul_conf['noRpLocationUpdateRate'],
                          help_mode_update_rate=backhaul_conf['helpModeUpdateRate'],
                          scan_per_fix=symble_conf[''],
                          wifi_ap=backhaul_conf['maxWifis'],
                          cell_id=backhaul_conf['maxCellIds'],
                          loc_update_order=backhaul_conf[''],
                          accel_en=accel_conf[''],
                          accel_mvm_dur=accel_conf[''],
                          accel_thresh=accel_conf[''],
                          shock_thresh=accel_conf[''],
                          msg_cache_en=caching_conf['cachedMessagesEnable'],
                          msg_cache_num=caching_conf['noRpMessagesCached'],
                          gps_pwr_mode=gps_conf['gpsPowerMode'],
                          gps_timeout=gps_conf['gpsTimeout'],
                          net_lost_timeout=symble_conf[''],
                          ref_lost_timeout=symble_conf[''],
                          net_scan_int=symble_conf[''],
                          net_tok=symble_conf['networkToken']) if True else \
                          self.DL_CONF_V1_f(
                              change_msk=0,
                              heartbeat_int=0,
                              no_ap_heartbeat_int=0,
                              no_rp_heartbeat_int=0,
                              loc_update_rate=0,
                              no_ap_loc_update_rate=0,
                              no_rp_loc_update_rate=0,
                              scan_per_fix=0,
                              wifi_ap=0,
                              cell_id=0,
                              loc_update_order=0,
                              net_lost_timeout=0,
                              ref_lost_timeout=0,
                              net_scan_int=0)),
            gateway_addr=gateway_addr,
            acked=acked,
            time_to_live_s=time_to_live_s,
            port=port,
            priority=priority)

    def notify_help_mode_rxed(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
                              port=0, priority=10):
        """ TODO """
        self.send_message(
            self.DL_f(
                msg_type=self.DownlinkMessageType.HELP_MSG_RXED,
                msg_spec=0x02,  # TODO
                data=0x4357),
            gateway_addr=gateway_addr,
            acked=acked,
            time_to_live_s=time_to_live_s,
            port=port,
            priority=priority)

    def activate_test_mode(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
                           port=0, priority=10):
        """ TODO """
        self.send_message(
            self.DL_f(
                msg_type=self.DownlinkMessageType.TEST_MODE_EN,
                msg_spec=0x02),
            gateway_addr=gateway_addr,
            acked=acked,
            time_to_live_s=time_to_live_s,
            port=port,
            priority=priority)


def mac_to_addr(mac):
    """ Converts a BLE MAC Address into a Conductor Endnode Address. """
    if len(mac) == 26: return mac
    if len(mac) == 17: mac = mac.replace(':', '')
    af_fmt = mac[:3] + '-' + mac[3:]
    return "$501$0-0-00{}".format(af_fmt)


def addr_to_mac(addr):
    """ Converts a BLE MAC Address into a Conductor Endnode Address. """
    mac_addr = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        addr[5] | 0xc0, addr[4], addr[3], addr[2], addr[1], addr[0])
