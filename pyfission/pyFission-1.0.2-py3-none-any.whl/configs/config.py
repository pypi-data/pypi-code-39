from os.path import dirname, join, realpath
from pyfission.configs.schema_mapper import *


# Folders in project
dir_fission = dirname(dirname(realpath(__file__)))
dir_logs = join(dir_fission, 'logs')
dir_secrets = join(dir_fission, 'secrets_storage')
dir_storage = join(dir_fission, 'storage')
dir_sql = join(dir_fission, 'sql')

timestamp_now_formatting = '%Y-%m-%d %H:%M:%S'
chunksize = 100_000
bq_config = {'query': {'useQueryCache': True}}
