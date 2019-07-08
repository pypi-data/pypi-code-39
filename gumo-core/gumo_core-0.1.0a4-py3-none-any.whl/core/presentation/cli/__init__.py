import os
import sys
import subprocess
import logging


def gumo_dev_server():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    from gumo.core.infrastructure import MockAppEngineEnvironment

    if len(sys.argv) == 0:
        print("Usage: gumo-dev-server <path-to-app.yaml>")
        exit(1)

    app_yaml = sys.argv[1]
    if not os.path.exists(app_yaml):
        print(f'File: {app_yaml} does not found.')
        exit(1)

    print('loading..')
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml)
    exit(0)

    entry_point = os.path.join(
        os.path.dirname(app_yaml),
        'main.py'
    )
    subprocess.run(
        args=['python', entry_point],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


if __name__ == '__main__':
    gumo_dev_server()
