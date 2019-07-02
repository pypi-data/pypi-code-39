import os

from op_askpass.configuration import get_configuration_directory
from op_askpass.one_password.client import OPClient


def main() -> None:
    item_name = os.environ["OP_ASKPASS_ITEM_NAME"]
    op_client = OPClient(executable_path=get_configuration_directory() / "op")
    print(op_client.get_password(item_name=item_name))
