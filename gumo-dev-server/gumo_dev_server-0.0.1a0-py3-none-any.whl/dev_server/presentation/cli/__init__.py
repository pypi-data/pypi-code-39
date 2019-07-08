import os
import sys
import subprocess
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def gumo_dev_server():
    from gumo.core.infrastructure import MockAppEngineEnvironment

    if len(sys.argv) == 1:
        print("Usage: gumo-dev-server <path-to-app.yaml>")
        exit(1)

    app_yaml = sys.argv[1]
    if not os.path.exists(app_yaml):
        print(f'File: {app_yaml} does not found.')
        exit(1)

    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml)

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
    cli = os.path.dirname(__file__)
    presentation = os.path.dirname(cli)
    dev_server = os.path.dirname(presentation)
    gumo = os.path.dirname(dev_server)
    sys.path.insert(0, os.path.dirname(gumo))
    gumo_dev_server()
