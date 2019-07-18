import json
import os

from loader import Loader

app_dir = "sample_app"
settings_dir = "sample_settings"
root = os.path.join(os.path.dirname(__file__), app_dir)

loader = Loader(root)
settings = loader.load_settings(settings_dir)
print("unsafe:", json.dumps(settings, indent=4))
print("safe:", json.dumps(settings.masked(), indent=4))
