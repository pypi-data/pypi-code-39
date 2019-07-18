from bqmigratrr.commands.BigQuery import BigQuery
from google.api_core.exceptions import Conflict

import os
import logging


bqMigrator = BigQuery("massage-stg-85cc4")

def up(migration, name: str):
    try:
        logging.info("Attempting to run migration for {}".format(name))
        migration.up(bqMigrator)
        bqMigrator.insertMigrationRow(name)
    except Conflict:
        logging.warning(
            "There was a conflict, {} may have already been run. Skipping".format(name))
