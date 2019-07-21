import tempfile

PIPELINE_BASE = "%s/fxquants-pipelines" % tempfile.gettempdir()
PIPELINE_MOUNT_TARGET = "/opt/fxquants/pipeline"
PROJECTS_FOLDER = "projects"
PIPELINE_YML_NAME = "fxq-pipeline.yml"
LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
JSON_HEADERS = {'content-type': 'application/json'}
URI_LIST_HEADERS = {'content-type': 'text/uri-list'}
ANALYTICS_SERVICE_ID = 'analytics-8200'
