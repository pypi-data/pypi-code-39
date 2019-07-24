import suanpan
from suanpan.app import app
from suanpan.app.arguments import Folder, Npy
from tensorflow import keras


@app.input(Npy(key="inputData1", alias="trainImages"))
@app.input(Npy(key="inputData2", alias="trainLabels"))
@app.input(Npy(key="inputData3", alias="testImages"))
@app.input(Npy(key="inputData4", alias="testLabels"))
@app.output(Folder(key="outputData1", alias="model"))
def getData(context):
    args = context.args

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    model.fit(args.trainImages, args.trainLabels, epochs=10)
    loss, acc = model.evaluate(args.testImages, args.testLabels)
    print('\nTest accuracy:', acc)


if __name__ == "__main__":
    suanpan.run(app)
