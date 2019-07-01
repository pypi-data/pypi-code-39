# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
This is the appropriate place for any query that computes something about
subscribers, other than a location. For example percentage nocturnal calls,
total events or radius of gyration.

"""
from .call_days import CallDays
from .new_subscribers import NewSubscribers
from .modal_location import ModalLocation
from .first_location import FirstLocation
from .entropy import PeriodicEntropy, LocationEntropy, ContactEntropy
from .daily_location import daily_location
from .nocturnal_events import NocturnalEvents
from .location_visits import LocationVisits
from .day_trajectories import DayTrajectories
from .radius_of_gyration import RadiusOfGyration
from .displacement import Displacement
from .event_count import EventCount
from .event_count import EventCount
from .subscriber_degree import SubscriberDegree
from .subscriber_location_cluster import subscriber_location_cluster, HartiganCluster
from .most_frequent_location import MostFrequentLocation
from .last_location import LastLocation

from .unique_location_counts import UniqueLocationCounts
from .total_active_periods import TotalActivePeriodsSubscriber
from .contact_balance import ContactBalance
from .scores import EventScore
from .label_event_score import LabelEventScore
from .distance_counterparts import DistanceCounterparts

from .pareto_interactions import ParetoInteractions
from .contact_reciprocal import (
    ContactReciprocal,
    ProportionContactReciprocal,
    ProportionEventReciprocal,
)


from .subscriber_tacs import (
    SubscriberTAC,
    SubscriberTACs,
    SubscriberHandsets,
    SubscriberHandset,
    SubscriberPhoneType,
)

from .subscriber_call_durations import (
    SubscriberCallDurations,
    PairedSubscriberCallDurations,
    PerLocationSubscriberCallDurations,
    PairedPerLocationSubscriberCallDurations,
)

from .meaningful_locations import (
    MeaningfulLocations,
    MeaningfulLocationsAggregate,
    MeaningfulLocationsOD,
)

from .contact_reference_locations_stats import ContactReferenceLocationStats
from .interevent_period import IntereventPeriod
from .topup_amount import TopUpAmount
from .topup_balance import TopUpBalance
from .mds_volume import MDSVolume
from .event_type_proportion import ProportionEventType
from .per_contact_event_stats import PerContactEventStats
from .per_location_event_stats import PerLocationEventStats
from .handset_stats import HandsetStats

__all__ = [
    "RadiusOfGyration",
    "NocturnalEvents",
    "FirstLocation",
    "CallDays",
    "ModalLocation",
    "daily_location",
    "DayTrajectories",
    "LocationVisits",
    "NewSubscribers",
    "subscriber_location_cluster",
    "HartiganCluster",
    "UniqueLocationCounts",
    "SubscriberDegree",
    "TotalActivePeriodsSubscriber",
    "ContactBalance",
    "EventScore",
    "LabelEventScore",
    "SubscriberTACs",
    "SubscriberTAC",
    "SubscriberHandsets",
    "SubscriberHandset",
    "SubscriberPhoneType",
    "ParetoInteractions",
    "SubscriberCallDurations",
    "PairedSubscriberCallDurations",
    "PerLocationSubscriberCallDurations",
    "PairedPerLocationSubscriberCallDurations",
    "Displacement",
    "MostFrequentLocation",
    "LastLocation",
    "PeriodicEntropy",
    "LocationEntropy",
    "ContactEntropy",
    "EventCount",
    "PerLocationEventStats",
    "PerContactEventStats",
    "MeaningfulLocations",
    "MeaningfulLocationsAggregate",
    "MeaningfulLocationsOD",
    "ProportionEventType",
    "PeriodicEntropy",
    "LocationEntropy",
    "ContactEntropy",
    "DistanceCounterparts",
    "ContactReferenceLocationStats",
    "IntereventPeriod",
    "TopUpAmount",
    "TopUpBalance",
    "MDSVolume",
    "ContactReciprocal",
    "ProportionEventReciprocal",
    "ProportionContactReciprocal",
    "HandsetStats",
]
