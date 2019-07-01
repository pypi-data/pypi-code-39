# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron_lib.api.definitions import project_id as apidef
from neutron_lib.api import extensions as api_extensions

from neutron.api import extensions


class Project_id(api_extensions.APIExtensionDescriptor):
    """Extension that indicates that project_id is enabled.

    This extension indicates that the Keystone V3 'project_id' field
    is supported in the API.
    """

    api_definition = apidef

    extensions.register_custom_supported_check(
        apidef.ALIAS, lambda: True, plugin_agnostic=True
    )
