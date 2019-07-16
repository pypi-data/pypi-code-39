# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["NvmeSubsystemControllerHost", "NvmeSubsystemControllerHostSchema"]
__pdoc__ = {
    "NvmeSubsystemControllerHostSchema.resource": False,
    "NvmeSubsystemControllerHost": False,
}


class NvmeSubsystemControllerHostSchema(ResourceSchema):
    """The fields of the NvmeSubsystemControllerHost object"""

    id = fields.Str()
    r""" The host identifier registered with the controller.


Example: b8546ca6097349e5b1558dc154fc073b """
    nqn = fields.Str()
    r""" The NVMe qualified name of the host.


Example: nqn.2014-08.org.nvmexpress:uuid:c2846cb1-89d2-4020-a3b0-71ce907b4eef """
    transport_address = fields.Str()
    r""" The transport address of the host.


Example: nn-0x20000090fae00806:pn-0x10000090fae00806 """

    @property
    def resource(self):
        return NvmeSubsystemControllerHost

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class NvmeSubsystemControllerHost(Resource):  # pylint: disable=missing-docstring

    _schema = NvmeSubsystemControllerHostSchema
