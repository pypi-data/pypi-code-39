# coding=utf8
from django.core.management.base import BaseCommand

from django.template.engine import Engine


class Command(BaseCommand):
    help = 'Create a standalone script. '

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--func_name')
        parser.add_argument('--output')

    def handle(self, *args, **options):
        filename = options['filename']
        settings_module_name = options['settings']
        func_name = options.get('func_name', 'main')
        output = options.get('output', 'new_script')
        engine = Engine.get_default()
        tpl = engine.get_template('scripts/single_script.py.tpl')
        with open(output, 'w') as f:
            f.write(tpl.render({'function_name': func_name, 'settings_module_name': settings_module_name}))

        self.stdout.write(self.style.SUCCESS('File {} created Successfully"'.format(filename)))
