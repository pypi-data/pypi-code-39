import argparse

from django.core.management.base import BaseCommand, CommandError

from django_datahooks import registry


class Command(BaseCommand):
    help = "Generate data"

    def add_arguments(self, parser):
        parser.formatter_class = argparse.RawDescriptionHelpFormatter

        subparsers = parser.add_subparsers(
            metavar="provider", dest="provider", help="Provider"
        )
        provider_parser = argparse.ArgumentParser(add_help=False)

        for name, cls in registry.providers.items():
            provider_parser = subparsers.add_parser(
                name, parents=[provider_parser], add_help=False
            )
            provider = cls()
            provider.add_arguments(provider_parser)

    def handle(self, **options):
        provider = options.get("provider")
        if not provider:
            raise CommandError("No data provider found with given name")

        provider_cls = registry.providers[provider]
        provider = provider_cls()
        provider.run(**options)
