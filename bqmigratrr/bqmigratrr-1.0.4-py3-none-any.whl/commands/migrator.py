from bqmigratrr.commands.BigQuery import BigQuery

import os

bqMigrator = BigQuery("massage-stg-85cc4")


def up(migration):
    migration.up(bqMigrator)
