'''
Copyright 2019 Jacques Supcik

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

-----------------------------------------------------------------------------
Purpose: Dataclass for activities
Filename: groople/activity.py
Created Date: 2019-03-31
Author: Jacques Supcik
-----------------------------------------------------------------------------
'''

import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Activity:
    """ Activity class """
    id: int
    name: str
    description: str
    category: int
    attributes: dict
    groups: list
    organizer_id: int = None
    orga_email_list: list = field(default_factory=list)
    orga_email_list_participants: list = field(default_factory=list)

    def sort_groups(self):
        """ Sort groups based on order attribute """
        self.groups.sort(key=lambda i: i.order)

    @staticmethod
    def aggregate_age(age_list):
        """ Aggregate ages """
        result = list()
        age_range = None
        for age in sorted([int(i) for i in age_list]):
            if age_range is None:
                age_range = [age, age]
            elif age != age_range[1] + 1:
                result.append(age_range)
                age_range = [age, age]
            else:
                age_range[1] = age

        result.append(age_range)
        return " + ".join([f"{i[0]}-{i[1]}" for i in result])

    def extract_emails(self):

        def splitlist(x):
            email_re = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if x is None:
                return []

            l = re.split(r'[\s;,]+', str(x))
            l = [i for i in l if len(i) > 0]
            res = set()
            for i in l:
                if re.match(email_re, i):
                    res.add(i.lower())
                else:
                    logger.warning("Invalid email : %s", i)

            return sorted(list(res))

        self.orga_email_list = splitlist(self.attributes.get("organizer_email", ""))
        self.orga_email_list_participants = splitlist(
            self.attributes.get("participants_list_to_email", ""))

    def sanitize(self):
        """ Sanitize data """
        for i in ['gender', 'all_pass']:
            if i in self.attributes:
                self.attributes[f'{i}_s'] = ", ".join(
                    sorted(self.attributes[i]))
        if 'age' in self.attributes:
            self.attributes['age_s'] = Activity.aggregate_age(
                self.attributes['age'])
        self.extract_emails()

    def __str__(self):
        return f'{self.name}'
