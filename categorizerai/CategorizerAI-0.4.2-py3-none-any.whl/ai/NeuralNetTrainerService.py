from winterboot.Autowired import Autowired
from winterboot.Service import Service


config = Autowired('config')

@Service
class NeuralNetTrainerService:

    def trainNeuralNet(self, trainValues, trainResults, model):
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        hist = model.fit(trainValues, trainResults, batch_size=config().BATCH_SIZE, epochs=config().EPOCHS, verbose=2)
        accuracy = hist.history.get('acc')[-1]
        return accuracy
