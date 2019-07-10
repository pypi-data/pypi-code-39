import yaml

cfg = None
if cfg is None:
    with open('./etc/config.yaml', 'r') as f:
        cfg = yaml.load(f)
