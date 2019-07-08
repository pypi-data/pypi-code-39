"""
    A simple runbook which does nothing but returns the list of
    VM resources
"""
from googleapiclient import discovery as gcp_client


def remediate(credentials, resource_details, context):
    """ Entry point """
    context.log('Starting runbook')

    project_id = resource_details['project_id']
    try:
        client = gcp_client.build('compute', 'v1', credentials=credentials)

        context.log('Getting list of instances')
        vms = client.instances().list(project=project_id, zone='us-central1-a').execute()
        context.log('Getting list of instances - successful')

        context.body = {'total_number_of_instance': len(vms['items'])}

    except (Exception, TypeError) as runbook_error:
        context.generate_error(
            'Error encountered when running runbook remediate_sample',
            body=str(runbook_error)
        )
