import json
def parse_args(args):
    return dict(map(lambda x: x.split(":"), args))


def parse_datasets(datasets):
    parsed_datasets = []
    for dataset in datasets:
        commit = None
        dataset_slug = dataset
        if ":" in dataset:
            dataset_slug, commit = dataset.split(":")
        parsed_datasets += [{"slug": dataset_slug, "commit": commit}]
    return parsed_datasets



def print_object(o):
    print(json.dumps(o, sort_keys=True, indent=4))