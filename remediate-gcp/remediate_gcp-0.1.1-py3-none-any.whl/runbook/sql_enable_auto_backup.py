"""
    Enable automated backup of SQL instances
    Required parameters:
        - project_id
        - name
    Required permissions:
        - cloudsql.instances.update

    Notes:
        - SQL admin API needs to be enabled!
          https://console.developers.google.com/apis/library/sqladmin.googleapis.com?project=<project-name>
        - Start time in UTC. GCP sets 4 hrs window from backup time,
          but backup may run longer
"""
from googleapiclient import discovery as gcp_client


def remediate(credentials, resource_details, context):
    """ Entry point """
    start_backup_time = "07:00"  #UTC
    context.log('Starting runbook')

    context.log('Getting required parameters')

    try:
        project = resource_details['project_id']
        instance = resource_details['name']
    except KeyError:
        context.generate_error('[name] and/or [project_id] not found on resource details')
        return

    try:
        client = gcp_client.build('sqladmin', 'v1beta4', credentials=credentials)
        body = {
            "settings" : {
                "backupConfiguration": {
                    "binaryLogEnabled": True,
                    "enabled": True,
                    "kind": "sql#backupConfiguration",
                    "startTime": start_backup_time
                }
            }
        }

        context.log(f'Enabling automated backup on instance {instance}')
        res = client.instances().patch(project=project, instance=instance, body=body).execute()
        context.log('Operation completed')

        context.body = res

    except (Exception, TypeError) as runbook_error:
        context.generate_error(
            'Error encountered when running runbook to enable SQL instance automated backup',
            body=str(runbook_error)
        )
