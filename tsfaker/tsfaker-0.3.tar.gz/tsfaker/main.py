import click

from tsfaker.generator.table import TableGenerator
from tsfaker.io.io_arguments import process_input_output_arguments
from tsfaker.io.resources import process_resources, add_schema_to_resources
from tsfaker.io.schema import read_schema, iter_schemas_to_generate


@click.command(help="Generate a csv from table-schema descriptor(s), "
                    "given as a local folder path, local files paths, remote url or on stdin ('-').")
@click.argument('schema_descriptors', type=str, nargs=-1)
@click.option('--output-files', '-o', default='-', type=str, multiple=True,
              help="Output files paths (same number as SCHEMAS_DESCRIPTORS) or stdout ('-' default), "
                   "or existing local folder path if SCHEMAS_DESCRIPTORS are given as a local folder path.")
@click.option('--resources', '-r', type=str, multiple=True,
              help="CSV paths or directory containing CSV, to read foreign keys values.")
@click.option('--nrows', '-n', default=10, type=int, help='Number of rows to generate (default=10).')
@click.option('--pretty', is_flag=True, help='Get a console-friendly tabular output, instead of csv.')
@click.option('--dry-run', is_flag=True, help='Write logs but do not generate data.')
@click.option('--overwrite', is_flag=True, help='Overwrite existing output files.')
@click.option('--ignore-foreign-keys', is_flag=True, help='Ignore foreign keys relationships.')
def cli(schema_descriptors, output_files, resources, nrows, pretty, dry_run, overwrite, ignore_foreign_keys):
    input_descriptors, output_files = process_input_output_arguments(schema_descriptors, output_files)

    schemas = [read_schema(descriptor, output_file, ignore_foreign_keys) for descriptor, output_file in
               zip(input_descriptors, output_files)]

    resource_name_to_path_or_schema = process_resources(resources)
    add_schema_to_resources(resource_name_to_path_or_schema, schemas)

    for schema in iter_schemas_to_generate(resource_name_to_path_or_schema):
        table_generator = TableGenerator(schema, nrows, resource_name_to_path_or_schema)
        table_generator.generate_output_csv(dry_run, pretty, overwrite)


if __name__ == '__main__':
    cli()
