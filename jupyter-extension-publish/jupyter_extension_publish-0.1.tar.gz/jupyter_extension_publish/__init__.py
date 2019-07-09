def _jupyter_server_extension_paths():
    return [{
        "module": "jupyter_extension_publish"
    }]

# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        src="static",
        # directory in the `nbextension/` namespace
        dest="jupyter_extension_publish",
        # _also_ in the `nbextension/` namespace
        require="jupyter_extension_publish/index")]

def load_jupyter_server_extension(nbapp):
    from notebook.utils import url_path_join
    from .handlers import TestHandler, PublishS3Handler
    from .config import PublishSettings

    config = PublishSettings(
        # add access to NotebookApp config, too
        parent=nbapp,
        # for convenient access to frontend settings
        config_manager=nbapp.config_manager,
    ).config['PublishSettings']

    url = nbapp.web_app.settings['base_url']
    params = dict(
            nbapp=nbapp,
            access_key=config['s3_access_key_id'],
            secret_key=config['s3_secret_access_key'],
            endpoint_url=config['s3_endpoint_url'],
            region_name=config['s3_region_name'],
            bucket=config['s3_bucket']
            )
    nbapp.web_app.add_handlers(
        r'.*',  # match any host
        [
            (url_path_join(url, '/hello'), TestHandler),
            (url_path_join(url, '/publish_notebook'), PublishS3Handler, params),
        ]
    )
    nbapp.log.info("jupyter_extention_publish enabled!")
