model_saver_mapping = {}


def registry_model_saver_class(data_source_scheme, corpus_processor_class):
    model_saver_mapping[data_source_scheme] = corpus_processor_class


def get_model_saver_class(config):
    return model_saver_mapping[config.get('model_saver_scheme', 'raw')]


def get_model_saver(config):
    model_saver_class = get_model_saver_class(config)
    return model_saver_class(config)


from ioflow.model_saver.raw_model_saver import RawModelSaver
registry_model_saver_class('raw', RawModelSaver)

from ioflow.model_saver.http_based_model_saver import HttpBasedModelSaver
registry_model_saver_class('http', HttpBasedModelSaver)
