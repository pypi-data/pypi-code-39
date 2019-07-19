# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from future.builtins import object

from neptune.internal.common import NeptuneException


class ValidationError(NeptuneException):

    def __init__(self, message, critical=False):
        super(ValidationError, self).__init__(message)
        self.critical = critical


class JobValidationRule(object):

    def __init__(self, critical):
        self.critical = critical

    def validate(self, job, args):
        pass


class JobValidationRules(JobValidationRule):

    def __init__(self, *rules):
        super(JobValidationRules, self).__init__(critical=False)
        self.rules = rules

    def validate(self, job, args):
        for rule in self.rules:
            rule.validate(job, args)


class JobIsInState(JobValidationRule):

    def __init__(self, expectedState, critical):
        super(JobIsInState, self).__init__(critical=critical)
        self.expectedState = expectedState

    def validate(self, job, args):
        if job.state != self.expectedState:
            raise ValidationError(
                u"Job {} has state: '{}' instead of expected: '{}'".format(
                    job.id, job.state, self.expectedState),
                critical=self.critical)
