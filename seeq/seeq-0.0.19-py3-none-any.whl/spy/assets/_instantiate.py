import pandas as pd

from .. import _common


def instantiate(model_module, metadata):
    return pd.DataFrame(_instantiate(model_module, metadata))


def _instantiate(model_module, metadata):
    results = list()
    unique_assets = metadata[['Path', 'Asset', 'Template']].drop_duplicates().dropna()
    for index, row in unique_assets.iterrows():
        if not _common.present(row, 'Template') or not _common.present(row, 'Asset') or not _common.present(row, 'Path'):
            continue

        template = getattr(model_module, row['Template'].replace(' ', '_'))
        instance = template({
            'Name': row['Asset'],
            'Asset': row['Asset'],
            'Path': row['Path']
        })

        instance_metadata = metadata[(metadata['Asset'] == row['Asset']) & (metadata['Path'] == row['Path'])]

        results.extend(instance.build(instance_metadata))

    return results
