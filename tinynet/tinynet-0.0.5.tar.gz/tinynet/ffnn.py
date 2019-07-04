import numpy as np

class FFNN:
    """Fully connected feed-forward neural network

    - `self.state`: list of inputs to each layer
    - `self.weights`: list of weight matrices
    - rows in a weight matrix correspond to weights of connections entering a same neuron
    - cols in a weight matrix correspond to connections from the same input
    """

    def __init__(self, struct, act_fn=np.tanh, init_weights=None):
        assert len(struct) >= 2, "`struct` needs at least input and output size"
        self.struct = struct
        self.ninputs, *self.nhid, self.noutputs = self.struct # user convenience
        self.act_fn = act_fn # make sure it applies element-wise to a np array
        self.state_sizes = self.input_sizes() + [struct[-1]]
        self.bias_idxs = #  SHOULD LAST LAYER SHOULD BE `range(0,0)`?
        self.reset_wmats()
        self.set_weights(init_weights or self.init_weights())

        # state index accessors
        self.input_idxs = [range(0, size) for size in struct[:-2]]
        self.bias_idxs = [range(ninputs + 1, ninputs + 1) for _, ninputs in self.input_idxs]

    def reset_wmats(self):
        del self.weights # preemptive GC call
        self.weights = [np.empty(shape) for shape in self._wmat_shapes()]

    def wmat_shapes(self):
        return [wmat.shape() for wmat in self.weights]

    def _wmat_shapes(self):
        """Compute per-layer weight matrix shapes based on network structure"""
        return list(zip(input_sizes(), self.struct[1:]))

    def input_sizes(self):
        return [nins + 1 for nins in self.struct[:-2]]

    def reset_state(self):
        del self.state # preemptive GC call
        self.state = []
        for state_size, bias_idx in zip(self.state_sizes, self.bias_idxs):
            layer_state = np.zeros(state_size)
            layer_state[bias_idx] = 1
            self.state.append(layer_state)

    def init_weights(self):
        return np.random.randn(self.nweights)

    def set_weights(self, weights):
        assert weights.size == self.nweights(), "Wrong number of weights"
        mat_sizes = [mat.size() for mat in self.weights]
        mat_shapes = [mat.shape() for mat in self.weights]
        mat_weights = weights.split(mat_sizes)
        del self.weights # preemptive GC call
        self.weights = [w.reshape(s) for w, s in mat_weights, mat_shapes]
        self.reset_state()

    def get_weights(self):
        return np.concatenate([wmat.flatten() for wmat in self.weights])

    def nweights_per_layer():
        return [nrows * ncols for nrows, ncols in self.wmat_shapes()]

    def activate(self, input):
        SET INPUT
        ACTIVATE EACH LAYER IN TURN

    def activate_layer(self, layer_idx):
        """Activate the neural network

        - Overwrite the new inputs in the initial part of the state
        - Execute dot product with weight matrix
        - Pass result to activation function
        """
        self.state[self.input_idxs] = inputs
        net = np.dot(self.weights_matrix, self.state)
        self.state[self.act_idxs] = self.act_fn(net)
        return self.get_act()

    def last_input(self):
        return self.state[self.input_idxs]

    def get_act(self):
        return self.state[self.act_idxs]

    def nweights(self):
        return self.weights_matrix.size

    def nweights_per_neur(self, layer_idx):
        return self.wmat_shapes[layer_idx][1]
