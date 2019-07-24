import os

from tensorflow import keras

import suanpan
from suanpan.app import app
from suanpan.app.arguments import Folder, Int, Npy
from suanpan.model import Model
from suanpan.utils import json


class KerasModel(Model):
    def load(self, path):
        self.model = keras.models.model_from_json(
            json.load(os.path.join(path, "model.json"))
        )
        self.model.load_weights(os.path.join(path, "model.h5"))
        return self.model

    def save(self, path):
        self.model.save_weights(os.path.join(path, "model.h5"), save_format="h5")
        json.dump(self.model.to_json(), os.path.join(path, "model.json"))
        return path

    def prepare(self):
        self.model = keras.Sequential(
            [
                keras.layers.Flatten(input_shape=(28, 28)),
                keras.layers.Dense(128, activation="relu"),
                keras.layers.Dense(10, activation="softmax"),
            ]
        )
        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        return self.model

    def train(self, X, y, epochs=10):
        self.model.fit(X, y, epochs=epochs)
        return self.model

    def evaluate(self, X, y):
        return self.model.evaluate(X, y)

    def predict(self, X):
        return self.model.predict(X)


@app.input(Npy(key="inputData1", alias="trainImages"))
@app.input(Npy(key="inputData2", alias="trainLabels"))
@app.input(Npy(key="inputData3", alias="testImages"))
@app.input(Npy(key="inputData4", alias="testLabels"))
@app.output(Folder(key="outputData1", alias="modelFolder"))
@app.param(Int(key="param1", alias="epochs"))
def getData(context):
    args = context.args

    model = KerasModel()
    model.prepare()
    model.train(args.trainImages, args.trainLabels, epochs=args.epochs)
    loss, acc = model.evaluate(args.testImages, args.testLabels)
    print("\nTest accuracy:", acc)

    model.save(args.modelFolder)
    return args.modelFolder


if __name__ == "__main__":
    suanpan.run(app)
