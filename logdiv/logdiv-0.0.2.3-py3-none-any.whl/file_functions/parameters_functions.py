# All these could be joined in a single function

def retrieve_weblog_columns(parameters):
    columns_dict = parameters['weblog_format']
    return columns_dict;

def retrieve_pages_columns(parameters):
    pages_dict = parameters['pages_data_format']
    return pages_dict;

def retrieve_topics(parameters):
    return [s.strip() for s in parameters['classifications_to_use']['topics_to_use'].split(',')];

def retrieve_categories(parameters):
    return [s.strip() for s in parameters['classifications_to_use']['categories_to_use'].split(',')];

def retrieve_session_features(parameters):
    return [s.strip() for s in parameters['session_data']['features'].split(',')];

def retrieve_main_page_id(parameters):
    return [s.strip() for s in parameters['classifications_to_use']['main_page_id'].split(',')];

def retrieve_session_features_transformed(parameters):
    return [s.strip() for s in parameters['session_data']['features_transformed'].split(',')];

def retrieve_session_features_log_transformed(parameters):
    return [s.strip() for s in parameters['session_data']['features_log_transformed'].split(',')];
