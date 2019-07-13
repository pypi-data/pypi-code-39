from flask import Flask, jsonify, request
from parc_checker_core import parc_checker_core
import json

app = Flask(__name__)

@app.route('/parc/checker/api/v1/actions', methods=["GET"])
def get_actions():
    action_items = [(act.name, act.value) for act in list(parc_checker_core.get_actions())]
    actions = [{'name': action_item[0], 'value': action_item[1]} for action_item in action_items]
    return jsonify({"actions": actions})

@app.route('/parc/checker/api/v1/documentTypes', methods=["GET"])
def get_document_types():
    return jsonify({"documentTypes" : [doc_type for doc_type in parc_checker_core.get_document_types()]})

@app.route('/parc/checker/api/v1/check', methods=["POST"])
def check():
    content = request.json
    response = parc_checker_core.check(content["document_type"], parc_checker_core.Action(content["action"]), json.loads(content["request"]), "{}")
    return jsonify({"results:": response})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
