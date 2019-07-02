import argparse
import json
import os
import sys
from io import StringIO

from lspy.src import pg_logger
from lspy.src.bot import run, route, static_file, request

sys.argv[0] = __file__
pwd = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(pwd, "./assets"))
os.chdir(pwd)


@route('/web_exec_<name:re:.+>.py')
@route('/LIVE_exec_<name:re:.+>.py')
@route('/viz_interaction.py')
@route('/syntax_err_survey.py')
@route('/runtime_err_survey.py')
@route('/eureka_survey.py')
@route('/error_log.py')
def dummy_ok(name=None):
    return 'OK'


@route('/')
def home():
    return static_file("index.html", root="./assets")


@route('/<filepath:path>')
def index(filepath):
    return static_file(filepath, root="./assets")


@route('/LIVE_exec_py3.py')
def get_py_exec():
    out_s = StringIO()

    def json_finalizer(input_code, output_trace):
        ret = dict(code=input_code, trace=output_trace)
        json_output = json.dumps(ret, indent=None)
        out_s.write(json_output)

    options = json.loads(request.query.options_json)

    pg_logger.exec_script_str_local(request.query.user_script,
                                    request.query.raw_input_json,
                                    options['cumulative_mode'],
                                    options['heap_primitives'],
                                    json_finalizer)

    return out_s.getvalue()


def main():
    parser = argparse.ArgumentParser(description='网页中演示 Python 运行步骤')

    parser.add_argument('-p', '--port', dest="port", type=int, default=8899, help="端口号")

    args = parser.parse_args()
    run(host='127.0.0.1', port=args.port)
