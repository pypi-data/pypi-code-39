"""
Classes and utilities to manage IXN classical protocols objects.

@author yoram@ignissoft.com
"""

from collections import OrderedDict
from itertools import chain
from IPy import IP

from trafficgenerator.tgn_object import TgnL3

from ixnetwork.ixn_object import IxnObject
from ixnetwork.ixn_interface import filter_ints_based_on_vlan
from ixnetwork.ixn_traffic import TrafficEnd
from trafficgenerator.tgn_utils import is_ipv4


class IxnProtocol(IxnObject):
    """ Base class for IXN classical protocol objects (e.g. OSPF router, IGMP Querier, MLD Host
        etc.). """

    def __init__(self, **data):
        super(IxnProtocol, self).__init__(**data)
        self.ixn_ints = OrderedDict()

    @classmethod
    def get_protocols_with_int(cls, ixn_int):
        return list(p for p in cls.get_objects_of_class() if ixn_int in p.ixn_ints.values())

    @classmethod
    def get_protocols_with_port(cls, ixn_port, l3, vlan=None):
        ixn_ints = ixn_port.get_objects_with_object('interface', l3)
        if vlan is not None:
            ixn_ints = filter_ints_based_on_vlan(ixn_ints, vlan)
        return list(chain(*[cls.get_protocols_with_int(i) for i in ixn_ints]))


class IxnProtocolServer(IxnProtocol):
    """ Base class for IXN protocol server (e.g. IGMP Querier, MLD Host etc.). """

    def __init__(self, **data):
        super(IxnProtocolServer, self).__init__(**data)
        for int_ref in self.get_attribute('interfaces').split(' '):
            self.ixn_ints[int_ref] = self.root.get_object_by_ref(int_ref)

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return []


class IxnProtocolRouter(IxnProtocol):
    """ Base class for IXN router (e.g. OSPF router etc.). """

    interface_attribute = 'interfaces'

    def __init__(self, **data):
        data['objType'] = self.objType
        super(IxnProtocolRouter, self).__init__(**data)
        for ixn_router_int in self.get_children('interface'):
            int_ref = ixn_router_int.get_attribute(self.interface_attribute)
            self.ixn_ints[ixn_router_int] = self.root.get_object_by_ref(int_ref)

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return self.get_objects_by_type('routeRange')


# BGP router is represented differently than all other routers in the objects tree.
# Its interfaces are stored as protocol server rather than protocol router.
class IxnBgpRouter(IxnProtocolServer):
    """ Represents IXN BGP router. """

    def __init__(self, **data):
        super(IxnBgpRouter, self).__init__(**data)
        if IP(self.get_attribute('dutIpAddress')).version() == 4:
            self.__class__ = IxnBgpRouterIpV4
        else:
            self.__class__ = IxnBgpRouterIpV6

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return self.get_objects_by_type('routeRange')

    @classmethod
    def get_protocols_with_port(cls, ixn_port, l3, vlan=None):
        cls = IxnBgpRouterIpV4 if is_ipv4(l3) else IxnBgpRouterIpV6
        return super(IxnBgpRouter, cls).get_protocols_with_port(ixn_port, l3, vlan)


class IxnBgpRouterIpV4(IxnBgpRouter):
    pass


class IxnBgpRouterIpV6(IxnBgpRouter):
    pass


class IxnOspfRouter(IxnProtocolRouter):
    """ Represents IXN OSPF router. """

    objType = 'router'


class IxnOspfV3Router(IxnProtocolRouter):
    """ Represents IXN OSPFv3 router. """

    objType = 'router'


class IxnPimsmRouter(IxnProtocolRouter):
    """ Represents IXN PIM-SM router. """

    objType = 'router'

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return self.get_object_by_type('interface').get_objects_by_type('joinPrune')


class IxnIsisRouter(IxnProtocolRouter):
    """ Represents IXN ISIS router. """

    objType = 'router'
    interface_attribute = 'interfaceId'

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return self.get_objects_with_attribute('routeRange', 'type', l3)


class IxnLdpRouter(IxnProtocolRouter):
    """ Represents IXN LDP router. """

    objType = 'router'
    interface_attribute = 'protocolInterface'


class IxnRouteRange(IxnObject, TgnL3):
    """ Base class for IXN route ranges. """

    def ip(self):
        return self.networkNumber

    def num_ips(self):
        return self.numberOfRoutes


class IxnBgpRouteRange(IxnRouteRange):
    """ Represents IXN BGP route range. """

    def __init__(self, **data):
        super(IxnRouteRange, self).__init__(**data)
        self.networkNumber = self.get_attribute('networkAddress')
        self.numberOfRoutes = int(self.get_attribute('numRoutes'))


class IxnOspfRouteRange(IxnRouteRange):
    """ Represents IXN OSPF route range. """

    def __init__(self, **data):
        super(IxnRouteRange, self).__init__(**data)
        self.networkNumber = self.get_attribute('networkNumber')
        self.numberOfRoutes = int(self.get_attribute('numberOfRoutes'))


class IxnOspfv3RouteRange(IxnRouteRange):
    """ Represents IXN OSPF route range. """

    def __init__(self, **data):
        super(IxnRouteRange, self).__init__(**data)
        self.numberOfRoutes = int(self.get_attribute('numberOfRoutes'))
        self.firstRoute = self.get_attribute('firstRoute')

    def ip(self):
        return self.firstRoute


class IxnPimsmSource(IxnRouteRange):
    """ Represents IXN BGP route range. """

    def __init__(self, **data):
        super(IxnRouteRange, self).__init__(**data)
        self.networkNumber = self.get_attribute('sourceAddress')
        self.numberOfRoutes = int(self.get_attribute('sourceCount'))


class IxnIsisRouteRange(IxnRouteRange):
    """ Represents IXN ISIS route range. """

    def __init__(self, **data):
        super(IxnRouteRange, self).__init__(**data)
        self.networkNumber = self.get_attribute('firstRoute')
        self.numberOfRoutes = int(self.get_attribute('numberOfRoutes'))


class IxnLdpRouteRange(IxnRouteRange):
    """ Represents IXN LDP route range. """

    def __init__(self, **data):
        super(IxnRouteRange, self).__init__(**data)
        self.networkNumber = self.get_attribute('firstNetwork')
        self.numberOfRoutes = int(self.get_attribute('numberOfRoutes'))


class IxnIgmpHost(IxnProtocolServer):
    """ Represents IXN IGMP host. """

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return self.get_objects_by_type('group')


class IxnIgmpQuerier(IxnProtocolServer):
    """ Represents IXN IGMP querier. """
    pass


class IxnStpBridge(IxnProtocolRouter):
    """ Represents IXN STP bridge. """

    objType = 'bridge'
    interface_attribute = 'interfaceId'


class IxnOpenFlowDevice(IxnProtocolRouter):
    """ Represents IXN OpenFlow device. """

    objType = 'device'
    interface_attribute = 'protocolInterfaces'


class IxnLacp(IxnObject):
    """ Represents IXN LACP object. """
    pass


class IxnRsvpNeighborPair(IxnProtocolServer):
    """ Represents RSVP Neighbor Pair. """

    def __init__(self, **data):
        super(IxnProtocolServer, self).__init__(**data)
        ourIp = self.get_attribute('ourIp')
        for ixn_int in self.get_ancestor_object_by_type('vport').get_interfaces().values():
            for ixn_ip in ixn_int.get_objects_by_type('ipv4', 'ipv6'):
                if ixn_ip.get_attribute('ip') == ourIp:
                    self.ixn_ints[self] = ixn_int
                    return

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        if end == TrafficEnd.source:
            return [ep for ep in self.get_objects_by_type('destinationRange') if
                    ep.get_attribute('behavior') == 'ingress']
        elif end == TrafficEnd.destination:
            return [ep for ep in self.get_objects_by_type('destinationRange') if
                    ep.get_attribute('behavior') == 'egress']
        else:
            return self.get_objects_by_type('destinationRange')


class IxnStaticIp(IxnProtocolServer, TgnL3):
    """ Represents Static IP. """

    def __init__(self, **data):
        super(IxnProtocolServer, self).__init__(**data)
        int_ref = self.get_attribute('protocolInterface')
        self.ixn_ints[self] = self.root.get_object_by_ref(int_ref)

    def get_endpoints(self, l3=None, end=TrafficEnd.both):
        return [self]

    def ip(self):
        return self.get_attribute('ipStart')

    def num_ips(self):
        return int(self.get_attribute('count'))

    @classmethod
    def get_protocols_with_port(cls, ixn_port, l3, vlan=None):
        static = ixn_port.get_child_static('protocols').get_child_static('static')
        return [ip for ip in static.get_objects_by_type('ip') if ip.get_attribute('ipType').lower() == l3]


class IxnBfdfRouter(IxnProtocolRouter):
    """ Represents IXN BFD router. """

    objType = 'router'
