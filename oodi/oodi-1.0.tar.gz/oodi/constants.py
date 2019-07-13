
import os
import sys

if sys.platform == 'darwin':
    CONFIG_PATH = os.path.expanduser('~/Library/Application Support/Oodi')
else:
    CONFIG_PATH = os.path.expanduser('~/.config/Oodi')

DEFAULT_CONFIG_PATH = os.path.join(CONFIG_PATH, 'config.yaml')
