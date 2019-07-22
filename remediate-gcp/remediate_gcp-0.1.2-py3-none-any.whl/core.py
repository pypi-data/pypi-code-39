"""
    Runbook wrapper for GCP remediation
"""
import traceback
from importlib import import_module
from google.oauth2 import service_account
from google.auth import compute_engine
from . import utils

class Client:
    """ client wrapper for executing runbook """
    def __init__(self, service_account_json=None):
        self.runbook_return = utils.RunbookReturn()

        # Get credentials from service account JSON key
        if service_account_json is not None:
            try:
                self.credentials = service_account.Credentials.from_service_account_info(
                    service_account_json, scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
            except Exception:
                raise Exception("Invalid Service Account JSON.")
        # Get credentials from Compute
        else:
            try:
                self.credentials = compute_engine.Credentials()
            except Exception:
                raise Exception("Cannot obtain credentials from default service account.")

    def run(self, runbook_id, resource_details):
        """ Execute the runbook """
        self.runbook_return.resource = resource_details

        try:
            self.runbook_return.log(f'Grabbing runbook {runbook_id}')
            runbook = import_module('remediate_gcp.runbook.' + runbook_id)
        except ImportError:
            self.runbook_return.generate_error(f'Runbook {runbook_id} does not exists')
            return self.runbook_return

        try:
            runbook.remediate(self.credentials, resource_details, self.runbook_return)
            if self.runbook_return.error is None:
                self.runbook_return.status = 'ok'

        except Exception:
            self.runbook_return.generate_error(
                f'Unhandled Error encountered when running runbook {runbook_id}',
                body=traceback.format_exc()
                )

        self.runbook_return.log(f'Runbook {runbook_id} completed')
        return self.runbook_return
