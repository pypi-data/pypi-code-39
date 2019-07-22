import numpy as np
from keras.utils import Sequence


class BaseGenerator(Sequence):
    def __init__(self, X, y, batch_size, shuffle=True):
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return len(self.y) // self.batch_size

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.y))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def _get_data(self, indexes):
        return self.X[indexes], self.y[indexes]

    def __getitem__(self, index):
        idxs = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]
        return self._get_data(idxs)


class BaseGeneratorDF(BaseGenerator):
    def __init__(self, X, y, batch_size, shuffle=True):
        super().__init__(X, y, batch_size, shuffle)

    def _get_data(self, indexes):
        return self.X.iloc[indexes], self.y.iloc[indexes]


class SiameseGenerator(Sequence):
    def __init__(self, X, y, batch_size):
        self.X = X
        self.y = y
        self.label_set = list(set(self.y))
        self.batch_size = batch_size
        self.positive_indexes = self._get_positive_pairs()
        self.negative_indexes = self._get_negative_pairs()

    def _get_derangement(self, array):
        """ Get a random derangement of a list of indexes. """

        ders = [(x, np.random.choice(array[np.where(array != x)])) for x in array]
        return np.array(ders)

    def _get_positive_pairs(self):
        """ For each label build a derangement of the indexes. """

        first = True
        for label in np.random.permutation(self.label_set):
            same_idx = np.where(self.y == label)[0]
            der = self._get_derangement(same_idx)
            if not first:
                derangements = np.concatenate([derangements, der])
            else:
                first = False
                derangements = der
        return derangements

    def _get_negative_pairs(self):
        first = True
        for label in np.random.permutation(self.label_set):
            label_idx = np.where(self.y == label)[0]
            diff_idx = np.where(self.y != label)[0]
            replace = False
            if len(label_idx) > len(diff_idx):
                replace = True
            match = np.random.choice(diff_idx, size=len(label_idx), replace=replace)
            pairs = np.array(list(zip(label_idx, match)))
            if not first:
                all_pairs = np.concatenate([all_pairs, pairs])
            else:
                first = False
                all_pairs = pairs
        return all_pairs

    def __len__(self):
        ### TODO check : should be len(pos) == len(y)
        assert len(self.positive_indexes) == len(self.y)
        return len(self.positive_indexes) // self.batch_size

    def on_epoch_end(self):
        self.positive_indexes = self._get_positive_pairs()
        self.negative_indexes = self._get_negative_pairs()
        np.random.shuffle(self.positive_indexes)
        np.random.shuffle(self.negative_indexes)
        assert len(self.positive_indexes == self.negative_indexes)

    def __getitem__(self, index):
        start = self.batch_size * index
        positive_matches = self.X[self.positive_indexes[start : start + self.batch_size]]
        negative_matches = self.X[self.negative_indexes[start : start + self.batch_size]]
        samples = np.concatenate([positive_matches, negative_matches])
        labels = np.append(np.ones(len(positive_matches)), np.zeros(len(negative_matches)))
        assert len(samples) == len(labels)
        return samples, labels


class SiameseGeneratorDF(SiameseGenerator):
    def __init__(self, X, y, batch_size, columns):
        super().__init__(X=X, y=y, batch_size=batch_size)
        self.columns = columns

    def _get_siamese_input_dict(self, left, right):
        di = {}
        for cat in self.columns:
            di[cat + '_left'] = np.array(left[cat])
            di[cat + '_right'] = np.array(right[cat])
        return di

    def __getitem__(self, index):
        start = self.batch_size * index

        left_side_idxs = np.concatenate(
            [
                self.positive_indexes[start : start + self.batch_size, 0],
                self.negative_indexes[start : start + self.batch_size, 0],
            ]
        )
        right_side_idxs = np.concatenate(
            [
                self.positive_indexes[start : start + self.batch_size, 1],
                self.negative_indexes[start : start + self.batch_size, 1],
            ]
        )

        pairs = self._get_siamese_input_dict(
            left=self.X.iloc[left_side_idxs], right=self.X.iloc[right_side_idxs]
        )

        labels = np.append(np.ones(self.batch_size), np.zeros(self.batch_size))

        assert len(pairs[list(pairs.keys())[0]]) == len(labels)
        return pairs, labels
