#!/usr/bin/env python

import json
from flask import Flask, jsonify, request
from .model.model import Model
from .validator import Validator


model = Model()
validator = Validator( model.input_validation )

# init Flask app
app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=['POST'])
def predict():
    requestData = json.loads(request.data)

    predictions = []
    for row in requestData["dataset"]:
        if not validator.validate( row ):
            return jsonify({
                "status": "error",
                "message": "input data does not match the schema! \n"
                            + "Received data " + row + "\n"
                            + "Model schema " + model.input_validation
            })

        predictions.append( row )

    # returning result to the client
    return jsonify({"status": "ok", "dataset": predictions})

if __name__ == "__main__":
    # starting the web server on port 5000
    app.run(debug=False, host='0.0.0.0')