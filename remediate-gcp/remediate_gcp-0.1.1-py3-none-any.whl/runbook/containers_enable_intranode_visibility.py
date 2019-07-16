"""
    Enable GKE cluster's intranode visibility
    Required parameters:
        - name (cluster name)
        - location
        - project (project id) or selfLink
    Required permissions:
        - container.clusters.update

    Notes:
        - Using v1beta1 API version
"""
from googleapiclient import discovery as gcp_client


def remediate(credentials, resource_details, context):
    """ Entry point """
    context.log('Starting runbook')

    if 'name' in resource_details and 'location' in resource_details:
        cluster_name = resource_details['name']
        location = resource_details['location']
    else:
        context.generate_error('cluster name and location is unknown')
        return

    if 'project' in resource_details:
        project_name = resource_details['project']
    elif 'selfLink' in resource_details:
        project_name = resource_details['selfLink'].split("/projects/")[1].split("/zones/")[0]
    else:
        context.generate_error('project_name is unknown')
        return

    cluster_name = f'projects/{project_name}/locations/{location}/clusters/{cluster_name}'
    context.log(f'Enabling intranode visbility on {cluster_name} ...')

    body = {
        "update": {
            "desiredIntraNodeVisibilityConfig": {
                "enabled": True
            }
        }
    }

    try:
        client = gcp_client.build('container', 'v1beta1', credentials=credentials)
        response = client.projects().locations().clusters().update(
            name=cluster_name, body=body
            ).execute()

        context.body = response
        context.log(f'Intranode enabled successfully on {cluster_name}')
    except Exception as runbook_error:
        context.generate_error(
            'Error encountered when running runbook containers_enable_intranode_visibility',
            body=str(runbook_error)
        )
