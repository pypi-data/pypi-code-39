# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_mne Project, see:
# https://gitlab.com/obob/obob_mne
#
#    obob_mne is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    obob_mne is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with obob_subjectdb. If not, see <http://www.gnu.org/licenses/>.

import mne


def filter_event_id(event_id, conditions):
    """Filter mne-python style event_ids.

    Parameters
    ----------
    event_id : dict
        The event_id
    conditions : str or list or tuple
        The conditions to keep

    Returns
    -------
    The filtered event_id

    """
    conditions = [conditions] if not isinstance(conditions,
                                                (list, tuple)) else conditions
    good_event_keys = mne.epochs._hid_match(event_id, conditions)

    new_event_id = {key: value for key, value in event_id.items() if
                    key in good_event_keys}
    return new_event_id
