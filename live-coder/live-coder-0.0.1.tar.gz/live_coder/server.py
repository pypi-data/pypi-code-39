from flask import Flask, request, jsonify, abort
app = Flask(__name__)

from ._find_tests import find_test_classes
from ._add_prints import add_prints_from_file_paths, delete_print_files
from ._project_files_finder import ProjectFilesFinder
from ._print_to_vars import print_to_vars
from ._run_test import run_test

found_test_file_ids = []


def _format_path(path):
    if path[-1] != '/':
        path += '/'
    return path

def _format_test_id(test_id):
    test_class_id = '.'.join(test_id.split('.')[:-1])
    return test_class_id, test_id

def _update_found_tests(tests):
    global found_test_file_ids
    found_test_file_ids = []
    for test in tests:
        found_test_file_ids.append(
            test['id'][:test['id'].rfind('.')]
        )

def _get_test_classes(root):
    'throws ImportError'
    test_classes = find_test_classes(found_test_file_ids, root, request.json['tests_relative_path'])
    tests = [test_class.serialize() for test_class in test_classes]
    _update_found_tests(tests)
    return tests


@app.route("/new_project", methods=['POST'])
def new_project():
    '''
        Given a project root path and tests directory path and return a list of test classes with methods.
    '''
    if not request.json:
        abort(400)
    root = _format_path(request.json['root_path'])
    try:
        return jsonify(_get_test_classes(root))
    except ImportError:
        return jsonify({
            'error': 'ImportError'
        })


def _test_values(project_root, test_method_id):
    print_code_output, test_output = run_test(project_root, test_method_id)
    return print_to_vars(print_code_output), test_output

@app.route("/live_values", methods=['POST'])
def get_live_values():
    '''
        Given a project root path and test id return live values for the test.
    '''
    if not request.json:
        abort(400)
    root = _format_path(request.json['root_path'])
    test_class_id, test_method_id = _format_test_id(request.json['test_id'])
    if 'unittest.loader._FailedTest.' in test_class_id:
        return jsonify({'error': 'Extension is sending a failed test id.'})
    
    file_paths = ProjectFilesFinder(root, [test_class_id]).run()
    written_file_paths = add_prints_from_file_paths(root, file_paths)
    live_values, test_output = _test_values(root, test_method_id)
    delete_print_files(written_file_paths)

    try:
        test_classes = _get_test_classes(root)
    except ImportError:
        return jsonify({
            'error': 'ImportError'
        })

    return jsonify({'live_values': live_values, 'test_output': test_output, 'test_classes': test_classes})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
