# Copyright (c) 2014 Thales Services SAS
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import random

from neutron_lib import context as neutron_ctx
from neutron_lib.plugins.ml2 import api
from neutron_lib.plugins import utils as p_utils
from neutron_lib.utils import helpers
from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_log import log

from neutron.common import exceptions as exc
from neutron.db import api as db_api
from neutron.objects import base as base_obj


LOG = log.getLogger(__name__)

IDPOOL_SELECT_SIZE = 100


class BaseTypeDriver(api.ML2TypeDriver):
    """BaseTypeDriver for functions common to Segment and flat."""

    def __init__(self):
        try:
            self.physnet_mtus = helpers.parse_mappings(
                cfg.CONF.ml2.physical_network_mtus, unique_values=False
            )
        except Exception as e:
            LOG.error("Failed to parse physical_network_mtus: %s", e)
            self.physnet_mtus = []

    def get_mtu(self, physical_network=None):
        return p_utils.get_deployment_physnet_mtu()


class SegmentTypeDriver(BaseTypeDriver):
    """SegmentTypeDriver for segment allocation.

    Provide methods helping to perform segment allocation fully or partially
    specified.
    """

    def __init__(self, model):
        super(SegmentTypeDriver, self).__init__()
        if issubclass(model, base_obj.NeutronDbObject):
            self.model = model.db_model
        else:
            self.model = model
        self.primary_keys = set(dict(self.model.__table__.columns))
        self.primary_keys.remove("allocated")

    # TODO(ataraday): get rid of this method when old TypeDriver won't be used
    def _get_session(self, arg):
        if isinstance(arg, neutron_ctx.Context):
            return arg.session, db_api.context_manager.writer.using(arg)
        return arg, arg.session.begin(subtransactions=True)

    def allocate_fully_specified_segment(self, context, **raw_segment):
        """Allocate segment fully specified by raw_segment.

        If segment exists, then try to allocate it and return db object
        If segment does not exists, then try to create it and return db object
        If allocation/creation failed, then return None
        """

        network_type = self.get_type()
        session, ctx_manager = self._get_session(context)

        try:
            with ctx_manager:
                alloc = (
                    session.query(self.model).filter_by(**raw_segment).
                    first())
                if alloc:
                    if alloc.allocated:
                        # Segment already allocated
                        return
                    else:
                        # Segment not allocated
                        LOG.debug("%(type)s segment %(segment)s allocate "
                                  "started ",
                                  {"type": network_type,
                                   "segment": raw_segment})
                        count = (session.query(self.model).
                                 filter_by(allocated=False, **raw_segment).
                                 update({"allocated": True}))
                        if count:
                            LOG.debug("%(type)s segment %(segment)s allocate "
                                      "done ",
                                  {"type": network_type,
                                   "segment": raw_segment})
                            return alloc

                        # Segment allocated or deleted since select
                        LOG.debug("%(type)s segment %(segment)s allocate "
                                  "failed: segment has been allocated or "
                                  "deleted",
                                  {"type": network_type,
                                   "segment": raw_segment})

                # Segment to create or already allocated
                LOG.debug("%(type)s segment %(segment)s create started",
                          {"type": network_type, "segment": raw_segment})
                alloc = self.model(allocated=True, **raw_segment)
                alloc.save(session)
                LOG.debug("%(type)s segment %(segment)s create done",
                          {"type": network_type, "segment": raw_segment})

        except db_exc.DBDuplicateEntry:
            # Segment already allocated (insert failure)
            alloc = None
            LOG.debug("%(type)s segment %(segment)s create failed",
                      {"type": network_type, "segment": raw_segment})

        return alloc

    def allocate_partially_specified_segment(self, context, **filters):
        """Allocate model segment from pool partially specified by filters.

        Return allocated db object or None.
        """

        network_type = self.get_type()
        session, ctx_manager = self._get_session(context)
        with ctx_manager:
            select = (session.query(self.model).
                      filter_by(allocated=False, **filters))

            # Selected segment can be allocated before update by someone else,
            allocs = select.limit(IDPOOL_SELECT_SIZE).all()

            if not allocs:
                # No resource available
                return

            alloc = random.choice(allocs)
            raw_segment = dict((k, alloc[k]) for k in self.primary_keys)
            LOG.debug("%(type)s segment allocate from pool "
                      "started with %(segment)s ",
                      {"type": network_type,
                       "segment": raw_segment})
            count = (session.query(self.model).
                     filter_by(allocated=False, **raw_segment).
                     update({"allocated": True}))
            if count:
                LOG.debug("%(type)s segment allocate from pool "
                          "success with %(segment)s ",
                          {"type": network_type,
                           "segment": raw_segment})
                return alloc

            # Segment allocated since select
            LOG.debug("Allocate %(type)s segment from pool "
                      "failed with segment %(segment)s",
                      {"type": network_type,
                       "segment": raw_segment})
            # saving real exception in case we exceeded amount of attempts
            raise db_exc.RetryRequest(
                exc.NoNetworkFoundInMaximumAllowedAttempts())
