import ffnn

class RNN(FFNN):
    """Fully connected recurrent neural network"""
    def __init__(self, *args, **kwargs):
        super(RNN, self).__init__(*args, **kwargs)
        # self.act_idxs = range(ninputs + 1, ninputs + 1 + nneurs)
        self.act_idxs = [range(nins, nins + nacts) for (_, ninputs), nacts in zip(self.input_idxs, self.struct[1])]

    def input_sizes(self):
        return [nins + 1 + nacts for nins, nacts in zip(self.struct[:-2], self.struct[1:])]

