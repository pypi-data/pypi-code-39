import pickle
import logging
log = logging.getLogger()

def save(self, obj):
    pickle.dump(obj, self.fs.open(self.path, "wb"))

def load(self):
    return pickle.load(self.fs.open(self.path, "rb"))