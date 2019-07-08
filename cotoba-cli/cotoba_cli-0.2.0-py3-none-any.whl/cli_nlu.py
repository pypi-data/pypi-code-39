import os
import click
import sys

from cotoba_cli.cognito import get_cognito_authorization
from cotoba_cli import config
from cotoba_cli import nlu


@click.group(help='nlu')
@click.option('--endpoint-url', type=str, help='Endpoint URL', default=None)
@click.pass_context
def cli_nlu(context, endpoint_url):
    if not context.obj:
        context.obj = {}
    if not endpoint_url:
        if os.environ.get('COTOBA_ENDPOINT_URL'):
            endpoint_url = os.environ.get('COTOBA_ENDPOINT_URL')
        elif config.load()['default'].get('endpoint-url'):
            endpoint_url = config.load()['default'].get('endpoint-url')
        else:
            sys.stderr.write('endpoint-url is not set.\n')
            sys.exit(1)

    context.obj['endpoint_url'] = endpoint_url


@cli_nlu.command(help='Create and upload training data.')
@click.option('--data-name', 'data_name', type=str, required=True,
              help='Name.')
@click.option('--file', 'file_path', type=str, required=True,
              help='Path to training data file.')
@click.pass_context
def create_training_data(context, data_name, file_path):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_training_data(authorization, data_name, file_path,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update training data description.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data name to read.')
@click.option('--description', 'description', type=str, required=True,
              help='Description of updated content.')
@click.pass_context
def update_training_data(context, training_data_id, description):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_training_data(authorization,
                                   training_data_id,
                                   description,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete training data.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data name to read.')
@click.pass_context
def delete_training_data(context, training_data_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_training_data(authorization, training_data_id,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List training data.')
@click.pass_context
def list_training_data(context):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_training_data(authorization, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read training data.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data name to read.')
@click.pass_context
def read_training_data(context, training_data_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_training_data(authorization, training_data_id,
                                 endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List algorithm.')
@click.pass_context
def list_algorithm(context):
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_algorithm(endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read algorithm hyperparameters.')
@click.option('--algorithm-name', 'algorithm_name',
              type=str, required=True, help='Name.')
@click.pass_context
def read_algorithm_hyper_parameter(context, algorithm_name):
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_algorithm_hyper_parameter(algorithm_name,
                                             endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create and upload slot dictionary.')
@click.option('--data-name', 'data_name', type=str, required=True,
              help='Name.')
@click.option('--file', 'file_path', type=str, required=True,
              help='Path to slot dictionary file.')
@click.pass_context
def create_slot_dictionary(context, data_name, file_path):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_slot_dictionary(authorization, data_name, file_path,
                                     endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read slot dictionary.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=True,
              help='Slot dictionary name to read.')
@click.pass_context
def read_slot_dictionary(context, slot_dictionary_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_slot_dictionary(authorization, slot_dictionary_id,
                                   endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete slot dictionary.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=True,
              help='Slot dictionary name to delete.')
@click.pass_context
def delete_slot_dictionary(context, slot_dictionary_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_slot_dictionary(authorization, slot_dictionary_id,
                                     endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update slot dictionary description.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=True,
              help='Slot dictionary name to delete.')
@click.option('--description', 'description', type=str, required=True,
              help='Description of updated content.')
@click.pass_context
def update_slot_dictionary(context, slot_dictionary_id, description):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_slot_dictionary(authorization,
                                     slot_dictionary_id,
                                     description,
                                     endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List slot dictionary.')
@click.pass_context
def list_slot_dictionary(context):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_slot_dictionaries(authorization, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create model.')
@click.option('--training-data-id', 'training_data_id',
              type=str, required=True,
              help='Training data id.')
@click.option('--algorithm-name', 'algorithm_name',
              type=str, required=True,
              help='Algorithm name.')
@click.option('--job-name', 'job_name',
              type=str, required=True,
              help='Job name.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, required=False,
              help='Slot dictionary id.')
@click.option('--description', 'description',
              type=str, required=False,
              help='Description.')
@click.option('--hyper-parameters-file', 'file_path',
              type=str, required=False,
              help='Path to Hyper parameters file.')
@click.option('--hyper-parameters', 'hyper_parameters',
              type=str, required=False,
              help='Hyper parameters. Invalid when option '
                   '--hyper-parameters-file is specified.')
@click.option('--original-model-id', 'original_model_id',
              type=str, required=False,
              help='original model id for continuous learning.')
@click.pass_context
def create_model(context,
                 training_data_id,
                 algorithm_name,
                 slot_dictionary_id,
                 job_name,
                 description,
                 file_path,
                 hyper_parameters,
                 original_model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_model(authorization,
                           training_data_id,
                           algorithm_name,
                           slot_dictionary_id,
                           job_name,
                           description,
                           file_path,
                           hyper_parameters,
                           original_model_id,
                           endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update model description.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--description', 'description',
              type=str, required=True,
              help='Description of updated content.')
@click.pass_context
def update_model(context, model_id, description):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_model(authorization, model_id, description,
                           endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def read_model(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_model(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Delete model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def delete_model(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_model(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='List model.')
@click.pass_context
def list_model(context):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.list_models(authorization, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Create endpoint.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--slot-dictionary-id', 'slot_dictionary_id',
              type=str, help='slot dictionary id.')
@click.option('--min-capacity', 'min_capacity',
              type=int, help='min capacity for auto-scaling.',
              default=1)
@click.option('--max-capacity', 'max_capacity',
              type=int, help='max capacity for auto-scaling.',
              default=1)
@click.option('--initial-instance-count', 'initial_instance_count',
              type=int,
              help='initial instance count for creating endpoint.',
              default=1)
@click.pass_context
def create_endpoint(context, model_id, min_capacity, max_capacity,
                    initial_instance_count, slot_dictionary_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.create_endpoint(authorization, model_id,
                              min_capacity, max_capacity,
                              initial_instance_count,
                              slot_dictionary_id,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Update endpoint.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--min-capacity', 'min_capacity',
              type=int, help='min capacity for auto-scaling.',
              default=1)
@click.option('--max-capacity', 'max_capacity',
              type=int, help='max capacity for auto-scaling.',
              default=1)
@click.option('--desired-instance-count', 'desired_instance_count',
              type=int,
              help='desired instance count for updating endpoint.',
              required=True)
@click.pass_context
def update_endpoint(context, model_id, min_capacity, max_capacity,
                    desired_instance_count):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.update_endpoint(authorization, model_id,
                              min_capacity, max_capacity,
                              desired_instance_count,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read possitble intents of model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def read_intent(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_intent(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read possible slots of model.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def read_slot(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.read_slot(authorization, model_id, endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='delete endpoint.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.pass_context
def delete_endpoint(context, model_id):
    authorization = get_cognito_authorization()
    endpoint_url = context.obj['endpoint_url']
    res = nlu.delete_endpoint(authorization, model_id,
                              endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Inference by using endpoint.')
@click.option('--utterance', 'utterance',
              type=str, required=True,
              help='utterance.')
@click.option('--model-id', 'model_id',
              type=str, required=True,
              help='model id.')
@click.option('--api-key', 'api_key',
              type=str, default='',
              help='api key.')
@click.option('--slot-dic', 'slot_dic',
              type=str, default='',
              help='slot dic json.')
@click.pass_context
def inference(context, utterance, model_id, api_key, slot_dic):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.inference(authorization,
                        utterance,
                        model_id,
                        api_key=api_key,
                        slot_dic=slot_dic,
                        endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Get endpoint url.')
@click.option('--endpoint-id', 'endpoint_id',
              type=str, required=True,
              help='endpoint_id.')
@click.option('--api-key', 'api_key',
              type=str, default='',
              help='api_key.')
@click.pass_context
def get_endpoint_url(context, endpoint_id, api_key):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.get_endpoint_url(authorization,
                               endpoint_id,
                               api_key=api_key,
                               endpoint_url=endpoint_url)
    res.print()


@cli_nlu.command(help='Read remaining resources.')
@click.pass_context
def read_remaining_resources(context):
    endpoint_url = context.obj['endpoint_url']
    authorization = get_cognito_authorization()
    res = nlu.read_remaining_resources(authorization,
                                       endpoint_url=endpoint_url)
    res.print()
