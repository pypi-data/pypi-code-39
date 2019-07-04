# -*- coding: utf-8 -*-
import os
import glob
import click
import polib
import subprocess
import sqlite3

from terminaltables import SingleTable
from googletrans import Translator

from ..main import odoo

from ..utils import manage_error
from ..parameters import DatabaseParameter, ModuleParameter


def echo_success():
    click.secho('Success!', fg='green', blink=True, bold=True)


@manage_error
def connect_db():
    click.echo('--> Connecting to local DB ', nl=False)
    home = os.path.expanduser("~")
    local_db = sqlite3.connect(home + '/eeodoo_translations.db')
    cr = local_db.cursor()
    create_table = """
        CREATE TABLE IF NOT EXISTS eeodoo_translations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT UNIQUE NOT NULL,
            translation TEXT NOT NULL,
            sync BOOLEAN DEFAULT(0)
        );
    """
    cr.execute(create_table)
    echo_success()
    return local_db, cr

@manage_error
def export_po(database, module, lang, po_path, display_mode):
    msg = '--> Exporting PO from %s ' %module
    click.echo(msg, nl=False)
    command = ['bin/start_openerp', '-d', database, '--i18n-export=' + po_path, '-l', lang, '--modules=' + module]
    pd = subprocess.Popen(command, stdout=display_mode, stderr=display_mode)
    rcode = pd.wait()
    if rcode:
        raise Exception(pd.stderr.read().decode())
    echo_success()


@manage_error
def translate_po(po_path, lang, cr, local_db, interactive):
    click.echo('--> Translating PO ', nl=False)
    inter = click.style('interactive >>>', bold=False, fg='green')
    if interactive:
        click.echo('')
    po = polib.pofile(po_path)
    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.kr',
    ])
    regs = [[click.style('Ref.', bold=True, fg='green'), click.style('Original', bold=True, fg='green'), click.style('Translated', bold=True, fg='green')]]
    for index, entry in enumerate(po):
        translation = entry.msgstr
        if entry.msgid == entry.msgstr:
            cr.execute("SELECT translation FROM eeodoo_translations WHERE origin='%s'" %entry.msgid)
            query_res = cr.fetchall()
            if query_res:
                translation = query_res[0][0]
            else:
                translation = translator.translate(entry.msgid, dest=lang).text
            cr.execute("REPLACE INTO eeodoo_translations (origin, translation) values ('%s', '%s')" %(entry.msgid, translation))
        if interactive:
            click.echo('')
            msg = inter + ' %s --> %s' %(entry.msgid, translation)
            click.echo(msg)
            pre_translation = translation
            translation = click.prompt(inter, default=pre_translation)
            if pre_translation != translation:
                cr.execute("REPLACE INTO eeodoo_translations (origin, translation) values ('%s', '%s')" %(entry.msgid, translation))
        entry.msgstr = translation
        regs.append((index+1, entry.msgid, entry.msgstr))

    if interactive:
        click.echo('')
    else:
        echo_success()
    table = SingleTable(regs)
    click.echo(table.table)

    trans_id = 1
    while trans_id:
        trans_id = click.prompt('Ammend Translation? Leave blank to omit', default='')
        try:
            if trans_id == '':
                trans_id = 0
            else:
                trans_id = int(trans_id)
        except Exception:
            trans_id = len(regs) + 1
        if trans_id in range(1, len(regs)):
            entry = po[trans_id - 1]
            click.echo('')
            msg = inter + ' %s --> %s' %(entry.msgid, entry.msgstr)
            click.echo(msg)
            pre_translation = entry.msgstr
            translation = click.prompt(inter, default=pre_translation)
            if pre_translation != translation:
                cr.execute("REPLACE INTO eeodoo_translations (origin, translation) values ('%s', '%s')" %(entry.msgid, translation))
            entry.msgstr = translation
            click.echo('')
    local_db.commit()
    local_db.close()
    po.save()

@manage_error
def move_po(module, po_path, force_move, display_mode):
    if not force_move:
        if not click.confirm('Do you want to move PO to i18n?'):
            click.echo('--> File temporaly stored in %s' %po_path)
            return
    click.echo('--> Moving PO to ' + module + '/i18n ', nl=False)
    module_path = os.path.abspath(glob.glob('*/' + module)[0]) + '/i18n'
    command = ['mkdir', '-p', module_path]
    md = subprocess.Popen(command, stdout=display_mode, stderr=display_mode)
    rcode = md.wait()
    if rcode:
        raise Exception(md.stderr.read().decode())
    command = ['mv', po_path, module_path+'/.']
    mv = subprocess.Popen(command, stdout=display_mode, stderr=display_mode)
    rcode = mv.wait()
    if rcode:
        raise Exception(mv.stderr.read().decode())
    echo_success()

@odoo.command()
@click.argument('database', type=DatabaseParameter())
@click.argument('module', type=ModuleParameter())
@click.option('-l', '--lang',
              help="Lang Code", default='es_AR')
@click.option('-f', '--force-move',
              help="Force move to i18n", default=False, is_flag=True)
@click.option('-i', '--interactive',
              help="Interactive Mode", default=False, is_flag=True)
def translate_module(database, module, lang, force_move, interactive):
    """
    Export po file, translate it automaticaly and copy to i18n path.
    """
    display_mode = subprocess.PIPE

    po_path = '/tmp/' + lang + '.po'

    # Connect to local DB
    local_db, cr = connect_db()

    # Export PO
    export_po(database, module, lang, po_path, display_mode)

    # Translate PO
    translate_po(po_path, lang, cr, local_db, interactive)

    # Move PO to i18n
    move_po(module, po_path, force_move, display_mode)

    click.echo('Goodbye!')
