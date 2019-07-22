"""
    Disable Compute firewall rule
    Required parameters:
        - accountId     # project ID
        - name          # firewall rule name
    Required permissions:
        - compute.firewalls.update

    Notes:
        - Disabled alert will have the description prepended with (Disabled by autoremediation)
"""
from googleapiclient import discovery as gcp_client


def remediate(credentials, resource_details, context):
    """ Entry point """
    context.log('Starting runbook')

    try:
        project_id = resource_details['accountId']
        firewall_rule_name = resource_details['name']
    except KeyError:
        context.generate_error('firewall [name] and/or [accountId] not found on resource details')
        return

    context.log('Adding (Disabled by autoremediation) to description')
    if 'description' in resource_details:
        description = "(Disabled by autoremediation) " + resource_details['description']
    else:
        description = "(Disabled by autoremediation)"

    try:
        client = gcp_client.build('compute', 'v1', credentials=credentials)
        body = {
            'name': firewall_rule_name,
            'description': description,
            'disabled': True
        }

        context.log(f'Disabling firewall rule {firewall_rule_name}')
        res = client.firewalls().patch(project=project_id, firewall=firewall_rule_name, body=body).execute()

        context.body = res
        context.log('Operation completed')
    except Exception as runbook_error:
        context.generate_error(
            'Error encountered when running runbook to disable firewall rule',
            body=str(runbook_error)
        )
