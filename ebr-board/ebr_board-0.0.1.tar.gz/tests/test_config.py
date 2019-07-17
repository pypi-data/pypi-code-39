from unittest.mock import patch, Mock
from urllib.parse import quote_plus
from copy import deepcopy

from ebr_board.config import VaultConfig


@patch("ebr_board.config.connections.create_connection")
@patch("ebr_board.config.VaultAnyConfig")
def test_config(mock_va, mock_connections):
    """
    Tests that the instantiation of a config.VaultConfig object results in the correct configuration.
    """
    sample_config = {
        "elastic": {
            "user": "elastic_user",
            "pwd": "elastic_password",
            "index": "elastic_index",
        }
    }

    local_sample_config = deepcopy(sample_config)
    mock_va.return_value.auth_from_file = Mock(return_value=True)
    mock_va.return_value.load = Mock(return_value=local_sample_config)

    config = VaultConfig("config.yaml", "vault.yaml", "vault_creds.yaml")

    # Validate calls to VaultAnyConfig instance
    mock_va.assert_called_once_with("vault.yaml")
    mock_va.return_value.auth_from_file.assert_called_once_with("vault_creds.yaml")
    mock_va.return_value.load.assert_called_once_with(
        "config.yaml", process_secret_files=False
    )

    # Validate elastic configuration
    elastic_config = deepcopy(sample_config["elastic"])
    auth_string = (
        quote_plus(elastic_config["user"]) + ":" + quote_plus(elastic_config["pwd"])
    )
    elastic_config.update({"http_auth": auth_string})
    del elastic_config["user"]
    del elastic_config["pwd"]
    mock_connections.assert_called_once_with(hosts=[elastic_config])
    assert config.ES_INDEX == elastic_config["index"]
