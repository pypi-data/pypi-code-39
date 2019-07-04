# -*- coding: utf-8 -*-

import click
from terminaltables import SingleTable

from ..main import odoo

from ..parameters import DatabaseParameter, ModelParameter
from ..utils import with_cr

def _get_odoo_version(cr):
    version_query = """
    SELECT latest_version FROM ir_module_module WHERE name='base'
    """
    cr.execute(version_query)
    full_version = cr.fetchone()[0]
    version_as_int = int(full_version.split('.')[0])
    return version_as_int


@odoo.command()
@click.argument('database', type=DatabaseParameter())
@click.option('-f', '--filter', 'filter_',
              help="Show only groups matching pattern.")
@with_cr
def groups(database, filter_, cr=False):
    """
    Human explain of fields available in <model>
    """
    if not cr:
        click.echo("\nError: Could not connect to database %s" % database)
        return

    try:
        odoo_version = _get_odoo_version(cr)
    except BaseException as err:
        click.echo(err)
        msg = "\nError: Could not recognize the database as an Odoo DB"
        click.echo(msg)

    query = "SELECT md.name AS xml_id, (COALESCE(mc.name || ' / ', '') || rg.name) AS name FROM res_groups rg LEFT JOIN ir_model_data md ON md.res_id=rg.id LEFT JOIN ir_module_category mc ON mc.id = rg.category_id WHERE md.model='res.groups'"

    if filter_:
        query += " AND (COALESCE(mc.name || ' / ', '') || rg.name) ~* '%s'" %filter_

    cr.execute(query)

    regs = cr.fetchall()
    header = [(click.style(col.name, bold=True, fg='green'))
              for col in cr.description]
    regs.insert(0, header)
    table = SingleTable(regs)
    click.echo(table.table)
