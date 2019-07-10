# Imports from python.
import os
import warnings


# Imports from Django.
from django.apps import apps
from django.core import serializers
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.utils import parse_apps_and_model_labels
from django.db import DEFAULT_DB_ALIAS
from django.db import router


# Imports from other dependencies.
from progress.bar import ChargingBar


# Imports from civic_utils.
from civic_utils.conf import settings
from civic_utils.management.helpers import ALLOWED_SERIALIZER_FORMATS
from civic_utils.management.helpers import DEFAULT_FIXTURE_ACL
from civic_utils.management.helpers import FORMAT_EXTENSION_MAP
from civic_utils.management.helpers import FORMAT_MIME_MAP
from civic_utils.management.helpers import TEMP_DIR
from civic_utils.models import CivicBaseModel
from civic_utils.utils.aws import get_bucket


S3_FIXTURE_BUCKET = settings.AWS_S3_BUCKET

S3_FIXTURE_ROOT_PATH = settings.FIXTURE_ROOT_PATH


class ProxyModelWarning(Warning):
    pass


def get_civic_models_for_app(app_config_obj):
    return [
        model for model in app_config_obj.get_models()
        if issubclass(model, CivicBaseModel)
    ]


class Command(BaseCommand):
    help = (
        "Export selected contents of the database as fixtures uploaded to S3. "
        "Fixtures will be stored in the user-specified format (using each "
        "model's default manager unless --all is specified)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label[.ModelName]', nargs='*',
            help=(
                'Restricts dumped data to the specified app_label or '
                'app_label.ModelName.'
            ),
        )
        parser.add_argument(
            '--format', default='json',
            help='Specifies the output serialization format for fixtures.',
        )
        parser.add_argument(
            '--indent', type=int,
            help=(
                'Specifies the indent level to use when '
                'pretty-printing output.'
            ),
        )
        parser.add_argument(
            '--database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a specific database to dump fixtures from. '
                 'Defaults to the "default" database.',
        )
        parser.add_argument(
            '-e', '--exclude', action='append', default=[],
            help=(
                'An app_label or app_label.ModelName to exclude '
                '(use multiple --exclude to exclude multiple apps/models).'
            ),
        )
        parser.add_argument(
            '-l', '--local', action='store_true', dest='store_locally',
            help='Store fixtures locally, rather than uploading them to S3.',
        )
        parser.add_argument(
            '-a', '--all', action='store_true', dest='use_base_manager',
            help=(
                "Use Django's base manager to dump all models stored in the "
                "database, including those that would otherwise be filtered "
                "or modified by a custom manager."
            ),
        )
        parser.add_argument(
            '-f', '--filename',
            default='export',
            dest='output_filename',
            help='Specifies file to which the output is written.'
        )

    #
    def handle(self, *app_labels, **options):
        format = options['format']
        indent = options['indent']
        using = options['database']
        excludes = options['exclude']
        show_traceback = options['traceback']
        store_locally = options['store_locally']
        use_base_manager = options['use_base_manager']
        output_filename = options['output_filename']

        excluded_models, excluded_apps = parse_apps_and_model_labels(excludes)

        if not app_labels:
            all_apps_with_models = [
                app_config for app_config in apps.get_app_configs()
                if app_config.models_module is not None
                and app_config not in excluded_apps
            ]

            # This would be an excellent candidate for assignment expressions
            # (introduced via PEP 572 in Python 3.8) once we've upgraded.
            app_list = dict(
                (app_config, get_civic_models_for_app(app_config))
                for app_config in all_apps_with_models
                if get_civic_models_for_app(app_config)
            )
        else:
            app_list = {}
            for label in app_labels:
                try:
                    app_label, model_label = label.split('.')
                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError as e:
                        raise CommandError(str(e))

                    if app_config.models_module is None:
                        continue
                    elif app_config in excluded_apps:
                        continue

                    try:
                        model = app_config.get_model(model_label)
                    except LookupError:
                        raise CommandError(
                            "Unknown model: %s.%s" % (app_label, model_label)
                        )

                    app_list_value = app_list.setdefault(app_config, [])

                    # We may have previously seen an "all-models" request for
                    # this app (no model qualifier was given). In this case
                    # there is no need adding specific models to the list.
                    if app_list_value is not None:
                        if all([
                            model not in app_list_value,
                            issubclass(model, CivicBaseModel)
                        ]):
                            app_list_value.append(model)

                except ValueError:
                    # This is just an app - no model qualifier
                    app_label = label
                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError as e:
                        raise CommandError(str(e))

                    if app_config.models_module is None:
                        continue
                    elif app_config in excluded_apps:
                        continue

                    app_list[app_config] = get_civic_models_for_app(app_config)

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in ALLOWED_SERIALIZER_FORMATS:
            try:
                serializers.get_serializer(format)
            except serializers.SerializerDoesNotExist:
                pass

            raise CommandError("Unknown serialization format: %s" % format)

        output_extension = FORMAT_EXTENSION_MAP[format]

        models_to_export = serializers.sort_dependencies(app_list.items())

        def get_objects(count_only=False):
            """
            Collate the objects to be serialized. If count_only is True, just
            count the number of objects to be serialized.
            """
            for model in models_to_export:
                if model in excluded_models:
                    continue
                if all([
                    model._meta.proxy,
                    model._meta.proxy_for_model not in models_to_export,
                ]):
                    warnings.warn(
                        "%s is a proxy model and won't be serialized." % model._meta.label,
                        category=ProxyModelWarning,
                    )
                if not model._meta.proxy and router.allow_migrate_model(using, model):
                    if use_base_manager:
                        objects = model._base_manager
                    else:
                        objects = model._default_manager

                    queryset = objects.using(using).order_by(model._meta.pk.name)

                    if count_only:
                        yield queryset.order_by().count()
                    else:
                        yield queryset

        model_counts = [count for count in get_objects(count_only=True)]

        self.stdout.write('')
        self.stdout.write(self.style.HTTP_SERVER_ERROR('Civic Data Exporter'))
        self.stdout.write('')
        self.stdout.write(f"• Temporary local directory: ./{TEMP_DIR}/")

        if store_locally:
            self.stdout.write(f"• No S3 exports (storing locally instead)")
        else:
            self.stdout.write(f"• S3 bucket: TK")
            self.stdout.write(f"• S3 path: TK")

        self.stdout.write('')
        self.stdout.write((
            "The following types and counts of models will be exported "
            f"({sum(model_counts)} total model instances):"
        ))
        self.stdout.write('')

        counts_by_model_klass = dict(zip(models_to_export, model_counts))

        export_destinations = {
            model_config._meta.db_table: os.path.join(
                model_config._meta.model_name,
                f"{output_filename}.{output_extension}"
            )
            for model_config, instance_count in counts_by_model_klass.items()
        }

        for model_config, instance_count in counts_by_model_klass.items():
            model_label = (
                f'{model_config._meta.app_label}'
                '.'
                f'{model_config._meta.object_name}'
            )
            model_file = export_destinations[model_config._meta.db_table]

            self.stdout.write('{}{}'.format(
                ' -  ',
                self.style.SQL_KEYWORD(f"{model_label}"),
            ))
            self.stdout.write((
                f"    [{instance_count} "
                f"instance{'s' if instance_count != 1 else ''}"
                f"{'; blank file only' if instance_count == 0 else ''}]"
            ))
            self.stdout.write('    ➡ (prefix){}'.format(
                self.style.MIGRATE_LABEL(f"/{model_file}"),
            ))
            self.stdout.write('')

        try:
            self.stdout.ending = None
            progress_output = None
            object_count = 0

            # If dumpdata is outputting to stdout, there is no way to display progress
            if all([
                output_filename,
                self.stdout.isatty(),
                options['verbosity'] > 0
            ]):
                progress_output = self.stdout
                object_count = sum(model_counts)
                # progress_bar = ProgressBar(progress_output, object_count)
                progress_bar = ChargingBar(
                    'Exporting model instances',
                    max=object_count if object_count > 0 else 1,
                    suffix=(
                        '%(percent)d%% '
                        '[%(finished_models)d / '
                        f'{len(models_to_export)} models done]'
                    ),
                    finished_models=0,
                )

            exported_files = []

            total_models_exported = 0

            for model_queryset in get_objects():
                raw_destination = export_destinations[
                    model_queryset.model._meta.db_table
                ]
                full_destination = os.path.join(TEMP_DIR, raw_destination)

                os.makedirs(os.path.dirname(full_destination), exist_ok=True)

                per_model_output_file = full_destination

                with open(full_destination, 'w') as model_output:
                    model_queryset.serialize(
                        stream=model_output,
                        indent=indent,
                        # progress_output=progress_output,
                        # object_count=object_count,
                        # use_natural_foreign_keys=use_natural_foreign_keys,
                        # use_natural_primary_keys=use_natural_primary_keys,
                    )

                models_added = model_queryset.order_by().count()
                # total_models_exported += models_added

                progress_bar.finished_models += 1

                progress_bar.next(n=models_added if models_added else 1)

                exported_files.append(raw_destination)

            progress_bar.finish()

            # try:
            #     serializers.serialize(
            #         # format, get_objects(), indent=indent,
            #         # stream=stream or self.stdout,
            #         # progress_output=progress_output,
            #         # object_count=object_count,
            #     )
            # finally:
            #     if stream:
            #         stream.close()
        except Exception as e:
            if show_traceback:
                raise
            raise CommandError("Unable to serialize database: %s" % e)

        self.stdout.write('\n')

        formatted_export_destination = f"'./{TEMP_DIR}/'"

        if not store_locally:
            formatted_export_destination = "<some S3>"

            for export_path in exported_files:
                full_export_path = os.path.join(TEMP_DIR, export_path)

                with open(full_export_path, 'r') as input_file:
                    bucket = get_bucket(S3_FIXTURE_BUCKET)
                    bucket.put_object(
                        ACL=DEFAULT_FIXTURE_ACL,
                        Body=input_file.read(),
                        ContentType=FORMAT_MIME_MAP[format],
                        Key=os.path.join(S3_FIXTURE_ROOT_PATH, export_path)
                    )

                print(os.path.join(S3_FIXTURE_ROOT_PATH, export_path))

        # TODO(ajv): Add progress bar.
        # TODO(ajv): Add correct S3 information.
        # TODO(ajv): Delete temporary-files dir.

        self.stdout.write(self.style.SUCCESS(
            f"Successfully exported {sum(model_counts)} model instances to "
            f"{formatted_export_destination}.\n\n"
        ))


# use_natural_foreign_keys
# use_natural_primary_keys
