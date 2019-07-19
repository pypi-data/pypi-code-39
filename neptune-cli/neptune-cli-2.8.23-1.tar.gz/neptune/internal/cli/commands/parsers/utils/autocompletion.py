#
# Copyright (c) 2018, deepsense.io
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

from argcomplete import CompletionFinder


class OverridableSubActionsCompletionCompleter(CompletionFinder):
    """
    The default CompletionFinder doesn't respect the need to override
    completion behaviour for subparsers.

    This class allows to define a custom completer for a subparser:

        def complete(parser, cword_prefix):
            return ...
        self.argparse_parser.add_subparsers(...).completer = complete
    """
    def __init__(self, *args, **kwargs):
        super(OverridableSubActionsCompletionCompleter, self).__init__(*args, **kwargs)

    def _get_subparser_completions(self, parser, cword_prefix):
        if hasattr(parser, 'completer') and callable(parser.completer):
            all_completions = parser.completer(parser, cword_prefix)
            return [c for c in all_completions if c.startswith(cword_prefix)]

        return super(OverridableSubActionsCompletionCompleter, self)._get_subparser_completions(parser, cword_prefix)


autocomplete = OverridableSubActionsCompletionCompleter()
