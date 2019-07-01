import click
import json
import logging
import re
import requests
import subprocess

from role import Definition

SP_DEFAULT_NAME = "http://redlock"


@click.group()
@click.option('-l', '--log-level', envvar="AR_LOG_LEVEL", default="INFO")
def cli(log_level):
    """azuredlock performs basic tasks to help integrate and manage azure + redlock = azuredlock. It is built to be
    run from the Azure Cloud Shell which already has the necessary dependencies installed: Azure CLI and Azure
    Managed Identity. But, it can be run elsewhere if the azure cli is present. The script assumes the user is
    logged in to the azure cli and has the necessary privileges to create Azure AD Applications, Service Principles,
    Roles, Resource Groups and can assign these privileges too. The Azure CLI can be launched from the Azure Portal. """
    level = log_level.upper()
    if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise Exception('Bad log level')

    logging.getLogger().setLevel(level)
    logging.debug("DEBUG logging set")


@cli.command()
@click.option('-sp-name', '--service-principle-name', default=SP_DEFAULT_NAME, envvar="AR_SP_NAME",
              prompt="Service Principal Name",
              help='Azure AD Service Principle Name. Azure AD will turn it into a valid URL.')
@click.option('-rl-url', '--redlock-url',
              envvar="AR_RL_URL", prompt='RedLock URL', help='''RedLock Application URL. Maps from deployment location.
                                                             Examples:
                                                             https://app.redlock.io/ -> https://api.redlock.io
                                                             https://app2.redlock.io/ -> https://api2.redlock.io/
                                                             https://api.eu.redlock.io/ ->
                                                             https://api.eu.redlock.io/''',
              default="https://api.redlock.io/")
@click.option('-g', '--redlock-group', envvar="AR_RL_GROUP", prompt='RedLock account group name',
              help="RedLock Account Group Name", default="Default Account Group")
@click.option('-u', '--redlock-user', envvar="AR_RL_USER", prompt='RedLock username',
              help="RedLock Username with Admin Privileges. Typically email address.")
@click.option('-p', '--redlock-password', envvar="AR_RL_PWD", prompt='RedLock password', hide_input=True,
              confirmation_prompt=True, help="RedLock Password")
@click.option('-rd', '--reader-data-role', is_flag=True, help="Include this flag to install Azure Reader & Data Role at"
                                                              " the Subscription Level. Very permissive. ")
@click.option('-j', '--json-output', is_flag=True, help="Include this flag to output json suitable for other tools like"
                                                        "jq")
@click.option('-d', '--accept-defaults', envvar="AR_ACCEPT_DEFAULTS", is_flag=True,
              help="Automatically accept defaults", default=False)
def onboard(service_principle_name, redlock_url, redlock_group, redlock_user, redlock_password, accept_defaults,
            reader_data_role, json_output):
    """Creates the required Azure AD objects to integrate an Azure Subscription with RedLock. Then it posts them to
    RedLock. It will ask for required info or it reads environment variables:

    \b
    AR_LOG_LEVEL=<set the verbosity of logging>
    AR_SP_NAME=<Azure Service Principal Name>
    AR_RL_URL=<RedLock App URL>
    AR_RL_USER=<RedLock Username>
    AR_RL_PWD=<RedLock Password>
    AR_ACCEPT_DEFAULTS=<Quiet if RedLock Account Already exists. >

    """
    builder = {
        'params': {'service_principle_name': service_principle_name, 'redlock_url': redlock_url,
                   'redlock_group': redlock_group, 'redlock_user': redlock_user,
                   'redlock_password': redlock_password},
        'redlock': {'headers': {'Content-Type': 'application/json', 'Accept': 'application/json'}},
        'sp': {}}

    _get_account(builder)
    if _check_account_exists(builder) and not accept_defaults:
        click.confirm('RedLock Cloud Account ID {} already exists. Continue?'.format(builder['account']['id']),
                      default=True, abort=True)
    _create_sp_reader(builder)
    _get_sp(builder, service_principle_name)
    _get_account_group_id(builder)
    if not _check_account_exists(builder):
        _create_redlock_account(builder)
    else:
        _update_redlock_account(builder)

    if reader_data_role:
        _assign_rd_role_sub(builder)

    if json_output:
        click.echo(json.dumps(builder, indent=2))
    else:
        click.echo("DONE")


@cli.command()
@click.option('-sp-name', '--service-principle-name', default=SP_DEFAULT_NAME, envvar="AR_SP_NAME",
              prompt="Service Principal Name",
              help='Azure AD Service Principle Name. Azure AD will turn it into a valid URL.')
@click.option('-rl-url', '--redlock-url',
              envvar="AR_RL_URL", prompt='RedLock URL', help='''RedLock Application URL. Maps from deployment location.
                                                             Examples:
                                                             https://app.redlock.io/ -> https://api.redlock.io
                                                             https://app2.redlock.io/ -> https://api2.redlock.io/
                                                             https://api.eu.redlock.io/ ->
                                                             https://api.eu.redlock.io/''',
              default="https://api.redlock.io/")
@click.option('-g', '--redlock-group', envvar="AR_RL_GROUP", prompt='RedLock account group name',
              help="RedLock Account Group Name", default="Default Account Group")
@click.option('-u', '--redlock-user', envvar="AR_RL_USER", prompt='RedLock username',
              help="RedLock Username with Admin Privileges. Typically email address.")
@click.option('-p', '--redlock-password', envvar="AR_RL_PWD", prompt='RedLock password', hide_input=True,
              confirmation_prompt=True, help="RedLock Password")
@click.option('-j', '--json-output', is_flag=True, help="Include this flag to output json suitable for other tools like"
                                                        "jq")
@click.option('-l', '--rg-location', envvar="AR_RG_LOC", prompt='Resource Group Region',
              help="Resource Group Region for Flow Log Storage Accounts", default="eastus2")
@click.option('-n', '--rg-name', envvar="AR_RG_NAME", prompt='Resource Group Name',
              help="Resource Group Name for Flow Log Storage Accounts", default="RedLockFlowLogsRG")
@click.option('-r', '--role-name', envvar='AR_ROLE_NAME', prompt='Azure Custom Role Name', default='RedLock',
              help="Custom Azure Role to Add RedLock Privileges to")
@click.option('-d', '--accept-defaults', envvar="AR_ACCEPT_DEFAULTS", is_flag=True,
              help="Automatically accept defaults", default=False)
def full_onboard(service_principle_name, redlock_url, redlock_group, redlock_user, redlock_password, accept_defaults,
                 rg_location, rg_name, role_name, json_output):
    """Creates the required Azure AD objects to integrate an Azure Subscription with RedLock. Then it posts them to
    RedLock. It will ask for required info or it reads environment variables:

    \b
    AR_LOG_LEVEL=<set the verbosity of logging>
    AR_SP_NAME=<Azure Service Principal Name>
    AR_RL_URL=<RedLock App URL>
    AR_RL_USER=<RedLock Username>
    AR_RL_PWD=<RedLock Password>
    AR_ROLE_NAME=<Azure AD role for custom RedLock Privileges>
    AR_RG_NAME=<Azure Resource Group Name for holding FlowLog Storage Accounts>
    AR_RG_LOC=<Location for Azure RG. Only the metadata, the storage accounts can be from multi regions>
    AR_ACCEPT_DEFAULTS=<Quiet if RedLock Account Already exists. >

    """
    builder = {
        'params': {'service_principle_name': service_principle_name, 'redlock_url': redlock_url,
                   'redlock_group': redlock_group, 'redlock_user': redlock_user,
                   'redlock_password': redlock_password},
        'redlock': {'headers': {'Content-Type': 'application/json', 'Accept': 'application/json'}},
        'sp': {}}

    _get_account(builder)
    if _check_account_exists(builder) and not accept_defaults:
        click.confirm('Cloud Account ID {} already exists. Continue?'.format(builder['account']['id']),
                      default=True, abort=True)
    _create_sp_reader(builder)
    _get_sp(builder, service_principle_name)
    _get_account_group_id(builder)
    if not _check_account_exists(builder):
        _create_redlock_account(builder)
    else:
        _update_redlock_account(builder)
    _ensure_provider()

    _create_rg(builder, rg_location, rg_name)
    _assign_rd_role_rg(builder)

    role_def = Definition(role_name, "Custom privileges for RedLock", builder['account']['id'])
    role_def.add_action("Microsoft.Network/networkWatchers/queryFlowLogStatus/action")
    if not _check_role_exist(role_def.name):
        _create_role(builder, role_def)
        _assign_role(builder)

    if json_output:
        click.echo(json.dumps(builder, indent=2))
    else:
        click.echo("DONE")


@cli.command()
def ensure_provider():
    """
    registers microsoft.insights provider. idempotent so anything else like checking first seems superfluous
    """
    _ensure_provider()


@cli.command()
@click.option('-rl-url', '--redlock-url',
              type=click.Choice(['https://api.redlock.io/', 'https://api2.redlock.io/', 'https://api.eu.redlock.io/']),
              envvar="AR_RL_URL", prompt='RedLock URL', help="RedLock Application URL")
@click.option('-u', '--redlock-user', envvar="AR_RL_USER", prompt='RedLock username',
              help="RedLock Username with Admin Privileges")
@click.option('-j', '--json-output', is_flag=True, help="Include this flag to output json suitable for other tools like"
                                                        "jq")
@click.option('-p', '--redlock-password', envvar="AR_RL_PWD", prompt='RedLock password', hide_input=True,
              confirmation_prompt=True, help="RedLock Password")
def show_account_group_names(redlock_url, redlock_user, redlock_password, json_output):
    """
    lists the RedLock Account Group Names that are currently setup
    """
    builder = {
        'params': {'redlock_url': redlock_url, 'redlock_user': redlock_user, 'redlock_password': redlock_password},
        'redlock': {'headers': {'Content-Type': 'application/json', 'Accept': 'application/json'}}}
    names = _get_account_group_names(builder)
    if not json_output:
        click.echo()
        click.echo("Account Group Names")
        click.echo("===================")
        for name in names:
            click.echo(name)
    else:
        click.echo(json.dumps(names))


@cli.command()
@click.option('-sp-name', '--service-principle-name', default=SP_DEFAULT_NAME, envvar="AR_SP_NAME",
              prompt="Service Principal Name", help="Azure AD Service Principle Name")
def show_info(service_principle_name):
    """show info about the account, tenant, subscription, etc..."""
    builder = {'sp': {}}
    _get_account(builder)
    _get_sp(builder, service_principle_name)
    click.echo(json.dumps(builder, indent=2))


@cli.command()
def zen():
    """motivations for some of the design choices"""
    click.echo_via_pager("""\

azuredlock
==========

An onboarding tool for Azure. There are multiple steps for wiring up the necessary objects and resources in order to
create a RedLock account that monitors an Azure Subscription. This tool wraps the Azure CLI and RedLock API to ease
the creation of a minimal yet opinionated set of these objects and resources.

It relies heavily on the Azure CLI to perform most of the work (by "shelling out"). Almost all of the logic here is in
making these cli calls, capturing the outputs, and then making the next ones. 

The dominant use case is for an Administrator type of person to install this in their Azure Cloud Shell and then execute
`azuredlock onboard`. Two of the main dependencies are met in this situation: 
1. The Azure CLI is installed
2. The user is already logged in (authentication occurred when the Administrator opened the Azure Portal)

While the above is certainly the dominant case, there may be other scenarios where an Administrator has the Azure CLI
already installed and this tool may be of use too. Beyond the 'onboard' sub command, other functions are surfaced
as sub commands too. These are mainly parts of the overall onboard process which can be executed independently.

One can certainly do all of this piecemeal and directly with the Azure CLI and RedLock API. In many instances that would
even be the suggestion.

Sub Commands
------------
onboard: performs the entire series of steps necessary to create Azure AD objects, public cloud resources and 
RedLock account definitions.  Some of the choices are opinionated and made with a "getting started" mindset.
Use this as a first step.
 
full-onboard: Performs the above plus creation of an Azure Resource Group and an Azure AD Custom Role. 
These are some skeleton pieces for FlowLog Storage Accounts integrations. 

ensure-provider: FlowLog monitoring requires a certain provider be enabled per subscription (a one time operation). This
does that. It is idempotent so it can be called many times without harm.

show-account-group-names: pulls the current list of RedLock Account Groups. Use this to see what the current options are
beyond the Default Account Group. This is just an ease of use thing.

show-info: pulls Account and ServicePrincipal info from Azure AD uses the SP name
    
    """)


def _call_az(sub_command):
    if type(sub_command) is list:
        sub_command.insert(0, "az")
    else:
        sub_command = "az " + sub_command
    logging.debug("call_az[sub_command]: {}".format(sub_command))
    completion = subprocess.run(sub_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    completion.check_returncode()
    return completion


def _check_role_exist(name):
    completion = _call_az("role definition list --custom-role-only true --name {}".format(name))
    if completion.stdout:
        role_def = json.loads(completion.stdout.decode("utf-8"))
        logging.debug(role_def)
        return True
    return False


def _create_role(builder, definition):
    completion = _call_az("role definition create --role-definition '{}'".format(definition.json))
    if completion.stdout:
        role_def = json.loads(completion.stdout.decode("utf-8"))
        logging.debug(role_def)
        builder['subscription_role'] = role_def


def _assign_role(builder):
    logging.debug(builder)
    completion = _call_az("role assignment create --assignee {} --role {}".format(builder['sp']['name'],
                                                                                  builder['subscription_role']['name']))
    role_assign = json.loads(completion.stdout.decode("utf-8"))
    logging.debug(role_assign)
    builder['role_assign'] = role_assign


def _assign_rd_role_sub(builder):
    n = builder['sp']['name']
    r = 'c12c1c16-33a1-487b-954d-41c89c60f349'  # Well known id for BuiltIn Reader and Data Role
    s = builder['account']['id']
    completion = _call_az("role assignment create --assignee {} --role {} --scope /subscriptions/{}".format(n, r, s))
    if completion.stdout:
        rd_role = json.loads(completion.stdout.decode("utf-8"))
        builder['rd_role'] = rd_role


def _assign_rd_role_rg(builder):
    n = builder['sp']['name']
    r = 'c12c1c16-33a1-487b-954d-41c89c60f349'  # Well known id for BuiltIn Reader and Data Role
    s = builder['flowlogs']['rg']['id']
    completion = _call_az("role assignment create --assignee {} --role {} --scope {}".format(n, r, s))
    if completion.stdout:
        rd_role = json.loads(completion.stdout.decode("utf-8"))
        builder['rd_role'] = rd_role


def _ensure_provider():
    _call_az("provider register -n microsoft.insights --wait")
    logging.debug("Registered microsoft.insights provider")


def _check_name(name):
    r = re.compile('^[-\\w._()]+$')
    if not r.fullmatch(name):
        raise NameError("Bad Resource Group name {}".format(name))


def _create_rg(builder, location, name):
    _check_name(name)
    completion = _call_az('group create --name "{}" --location {}'.format(name, location))
    if completion.stdout:
        rg = json.loads(completion.stdout.decode("utf-8"))
        builder['flowlogs'] = {'rg': {'id': rg['id'],
                                      'location': rg['location'],
                                      'name': rg['name']}}
        logging.debug('_create_rg[builder]:', builder)


def _get_account(builder):
    completion = _call_az("account show")
    if completion.stdout:
        account = json.loads(completion.stdout.decode("utf-8"))
        builder["account"] = account
        logging.debug('_get_account[builder]:', builder)


def _get_sp(builder, sp_name=SP_DEFAULT_NAME):
    if not sp_name.startswith("http"):
        fixed_up_sp_name = "http://" + sp_name
    else:
        fixed_up_sp_name = sp_name
    cmd = "ad sp show --id {}".format(fixed_up_sp_name)
    completion = _call_az(cmd)
    if completion.stdout:
        sp = json.loads(completion.stdout.decode("utf-8"))
        builder["sp"].update(sp)
        logging.debug('_get_sp[builder]:', builder)


def _create_sp_reader(builder):
    cmd = "ad sp create-for-rbac -n {} --role reader".format(builder['params']['service_principle_name'])
    completion = _call_az(cmd)
    if completion.stdout:
        builder["sp"].update(json.loads(completion.stdout.decode("utf-8")))
        logging.debug('_create_sp_reader[builder]:', builder)


def _create_redlock_account(builder):
    _get_token(builder)
    params = builder['params']
    r = requests.post(params['redlock_url'] + 'cloud/azure', headers=builder['redlock']['headers'], json={
        "cloudAccount": {
            "accountId": builder['account']['id'],
            "enabled": "true",
            "groupIds": [builder['redlock']['group_id']],
            "name": builder['account']['name']
        },
        "clientId": builder['sp']['appId'],
        "key": builder['sp']['password'],
        "monitorFlowLogs": "true",
        "tenantId": builder['sp']['tenant'],
        "servicePrincipalId": builder['sp']['objectId']
    })
    if r.status_code != requests.codes.ok:
        click.echo('Error posting to RedLock service [%d] - %s' % (r.status_code, r.text))


def _update_redlock_account(builder):
    _get_token(builder)
    params = builder['params']
    r = requests.put(params['redlock_url'] + 'cloud/azure/{}'.format(builder['account']['id']),
                     headers=builder['redlock']['headers'], json={
        "cloudAccount": {
            "accountId": builder['account']['id'],
            "enabled": "true",
            "groupIds": [builder['redlock']['group_id']],
            "name": builder['account']['name']
        },
        "clientId": builder['sp']['appId'],
        "key": builder['sp']['password'],
        "monitorFlowLogs": "true",
        "tenantId": builder['sp']['tenant'],
        "servicePrincipalId": builder['sp']['objectId']
    })
    if r.status_code != requests.codes.ok:
        click.echo('Error putting to RedLock service [%d] - %s' % (r.status_code, r.text))


def _get_token(builder):
    """
    Retrieve the token using the credentials if not already seen
    """
    if not builder['redlock'].get('token', False):

        params = builder['params']
        r = requests.post(params['redlock_url'] + 'login', headers=builder['redlock']['headers'], json={
            'customerName': '',
            'username': params['redlock_user'],
            'password': params['redlock_password']
        })

        if r.status_code != requests.codes.ok:
            click.echo('Error authenticating to RedLock service [%d] - %s' % (r.status_code, r.text))

        token = r.json()['token']

        logging.debug("redlock_token: %s", token)
        builder['redlock']['token'] = token
        builder['redlock']['headers']['x-redlock-auth'] = token


def _check_account_exists(builder):
    """
    Gets default account info (subscription id) and checks with RedLock to see if that account already has been added
    """
    # No key so go check
    if not builder['redlock'].get('exists', False):
        _get_account(builder)
        _get_token(builder)
        params = builder['params']
        r = requests.get(params['redlock_url'] + 'cloud/azure/{}'.format(builder['account']['id']),
                         headers=builder['redlock']['headers'])
        if r.status_code != requests.codes.ok:
            builder['redlock']['exists'] = False
            return False
        else:
            builder['redlock']['exists'] = True
            return True
    # Have already checked before and here is the same answer
    else:
        return builder['redlock']['exists']


def _get_account_group_names(builder):
    groups = _get_account_groups(builder)
    names = []
    for group in groups:
        names.append(group['name'])
    return names


def _get_account_group_id(builder):
    groups = _get_account_groups(builder)
    param_group_name = builder['params']['redlock_group']
    for group in groups:
        if group['name'] == param_group_name:
            builder['redlock']['group_id'] = group['id']
            return
    raise Exception("Account Group {} not found".format(param_group_name))


def _get_account_groups(builder):
    _get_token(builder)

    r = requests.get(builder['params']['redlock_url'] + 'cloud/group/name', headers=builder['redlock']['headers'])
    if r.status_code != requests.codes.ok:
        raise Exception("Cannot contact RedLock for Account Groups List")

    return r.json()
