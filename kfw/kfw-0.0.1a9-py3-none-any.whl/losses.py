import keras.backend as K


def affinity_matrix_loss(y_true, y_pred):
    """
    suppose V is a N x D matrix, corresponding to y_pred,
    and Y is a N x C matrix, corresponding to y_true,
    this loss function calculate:
        np.sum(np.exp2(np.matmul(V, V.T) - np.matmul(Y, Y.T)))
    for some reason, N can be very large, however, C and D is quite small.
    considering the memory, the calculation can transform to:
       np.sum(np.exp2(np.matmul(V.T, V))) - 2*np.sum(np.exp2(np.matmul(V.T, Y)))
       + np.sum(np.exp2(np.matmul(Y.T, Y)))
    for more details, please see *deep clustering: discriminative embeddings for segmentation and separation*.
    this function is copied from https://github.com/jcsilva/deep-clustering/blob/master/nnet.py
    :param y_true:
    :param y_pred:
    :return:
    """
    def norm(tensor):
        square_tensor = K.square(tensor)
        frobenius_norm2 = K.sum(square_tensor, axis=(1, 2))
        return frobenius_norm2

    def dot(x, y):
        return K.batch_dot(x, y, axes=(2, 1))

    def T(x):
        return K.permute_dimensions(x, [0, 2, 1])
    # return norm(dot(T(V), V)) - norm(dot(T(V), Y)) * 2 + norm(dot(T(Y), Y))
    return K.sqrt(K.mean(
        norm(dot(T(y_pred), y_pred)) -
        norm(dot(T(y_pred), y_true)) * 2 +
        norm(dot(T(y_true), y_true))))
