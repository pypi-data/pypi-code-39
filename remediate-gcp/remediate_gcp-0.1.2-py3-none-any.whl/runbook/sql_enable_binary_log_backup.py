"""
    Enable Binary log Backup
    Required parameters:
        - project_id
        - name
    Required permissions:
        - cloudsql.instances.update

    Notes:
        - SQL admin API needs to be enabled!
          https://console.developers.google.com/apis/library/sqladmin.googleapis.com?project=<project-name>
"""
from googleapiclient import discovery as gcp_client


def remediate(credentials, resource_details, context):
    """ Entry point """
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
                    "enabled": True
                }
            }
        }

        context.log(f'Enabling binaryLog backup on instance {instance}')
        res = client.instances().patch(project=project, instance=instance, body=body).execute()
        context.log('Operation completed')

        context.body = res

    except (Exception, TypeError) as runbook_error:
        context.generate_error(
            'Error encountered when running runbook to enable Cloud SQL binaryLog backup',
            body=str(runbook_error)
        )
