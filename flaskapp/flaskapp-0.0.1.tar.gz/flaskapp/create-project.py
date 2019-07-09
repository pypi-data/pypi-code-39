flask_projector = __import__("flask-projector")
from pathlib import Path

def run(name, target_dir=None):
    if target_dir is None:
        target_dir = Path.cwd()
    project_dir = target_dir.joinpath(name) 

    if project_dir.exists():
        print("Already directory exists: '{:s}'".format(str(project_dir.resolve())))
        return

    project_dir.mkdir()
    try:

        print("Successed to make project dir: '{:s}'".format(str(project_dir.resolve())))
    except:
        project_dir.unlink()
    


if __name__ == '__main__':
