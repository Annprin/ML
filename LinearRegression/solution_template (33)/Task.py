import numpy as np


class Preprocessor:

    def __init__(self):
        pass

    def fit(self, X, Y=None):
        pass

    def transform(self, X):
        pass

    def fit_transform(self, X, Y=None):
        pass


class MyOneHotEncoder(Preprocessor):

    def __init__(self, dtype=np.float64):
        super(Preprocessor).__init__()
        self.dtype = dtype

    def fit(self, X, Y=None):
        """
        param X: training objects, pandas-dataframe, shape [n_objects, n_features]
        param Y: unused
        """
        self.unique_dict = [{el: [1 if idx == i else 0 for idx in range(len(X[column].unique().tolist()))] 
                                for i, el in enumerate(sorted(X[column].unique().tolist()))} for column in X.columns]

    def transform(self, X):
        """
        param X: objects to transform, pandas-dataframe, shape [n_objects, n_features]
        returns: transformed objects, numpy-array, shape [n_objects, |f1| + |f2| + ...]
        """
        X = X.to_numpy()
        result = []
        for i in X:
            new_row = []
            for j, el in enumerate(i):
                new_row += self.unique_dict[j][el]
            result.append(new_row)

        return np.array(result)

    def fit_transform(self, X, Y=None):
        self.fit(X)
        return self.transform(X)

    def get_params(self, deep=True):
        return {"dtype": self.dtype}


class SimpleCounterEncoder:

    def __init__(self, dtype=np.float64):
        self.dtype = dtype

    def fit(self, X, Y):
        """
        param X: training objects, pandas-dataframe, shape [n_objects, n_features]
        param Y: target for training objects, pandas-series, shape [n_objects,]
        """
        self.unique_dict = [{el: [(Y[X[column] == el]).sum()/(X[column][X[column] == el]).count(), 
                                  (X[column][X[column] == el]).count() / X.shape[0]] 
                                for el in X[column].unique().tolist()} for column in X.columns]

    def transform(self, X, a=1e-5, b=1e-5):
        """
        param X: objects to transform, pandas-dataframe, shape [n_objects, n_features]
        param a: constant for counters, float
        param b: constant for counters, float
        returns: transformed objects, numpy-array, shape [n_objects, 3 * n_features]
        """
        X = X.to_numpy()
        result = []
        for i in X:
            new_row = []
            for j, el in enumerate(i):
                new_row += self.unique_dict[j][el]
                new_row += [(self.unique_dict[j][el][0] + a) / (self.unique_dict[j][el][1] + b)]
            result.append(new_row)

        return np.array(result)

    def fit_transform(self, X, Y, a=1e-5, b=1e-5):
        self.fit(X, Y)
        return self.transform(X, a, b)

    def get_params(self, deep=True):
        return {"dtype": self.dtype}


def group_k_fold(size, n_splits=3, seed=1):
    idx = np.arange(size)
    np.random.seed(seed)
    idx = np.random.permutation(idx)
    n_ = size // n_splits
    for i in range(n_splits - 1):
        yield idx[i * n_: (i + 1) * n_], np.hstack((idx[:i * n_], idx[(i + 1) * n_:]))
    yield idx[(n_splits - 1) * n_:], idx[:(n_splits - 1) * n_]


class FoldCounters:

    def __init__(self, n_folds=3, dtype=np.float64):
        self.dtype = dtype
        self.n_folds = n_folds

    def fit(self, X, Y, seed=1):
        """
        param X: training objects, pandas-dataframe, shape [n_objects, n_features]
        param Y: target for training objects, pandas-series, shape [n_objects,]
        param seed: random seed, int
        """
        self.stat = []
        indxs = list(group_k_fold(len(X), self.n_folds, seed))
        for test, train in indxs:
            train_X = X.iloc[train]
            train_Y = Y.iloc[train]
            unique_dict = [{el: [(train_Y[train_X[column] == el]).sum()/(train_X[column][X[column] == el]).count(), 
                                  (train_X[column][train_X[column] == el]).count() / train_X.shape[0]] 
                                for el in train_X[column].unique().tolist()} for column in train_X.columns]
            self.stat.append((test, unique_dict))

    def transform(self, X, a=1e-5, b=1e-5):
        """
        param X: objects to transform, pandas-dataframe, shape [n_objects, n_features]
        param a: constant for counters, float
        param b: constant for counters, float
        returns: transformed objects, numpy-array, shape [n_objects, 3 * n_features]
        """
        X = X.to_numpy()
        result = []
        for ind, i in enumerate(X):
            new_row = []
            use_dict = {}
            for k, d in self.stat:
                if ind in k:
                    use_dict = d
            for j, el in enumerate(i):
                new_row += use_dict[j][el]
                new_row += [(use_dict[j][el][0] + a) / (use_dict[j][el][1] + b)]
            result.append(new_row)
        print(np.array(result))
        return np.array(result)

    def fit_transform(self, X, Y, a=1e-5, b=1e-5):
        self.fit(X, Y)
        return self.transform(X, a, b)


def weights(x, y):
    """
    param x: training set of one feature, numpy-array, shape [n_objects,]
    param y: target for training objects, numpy-array, shape [n_objects,]
    returns: optimal weights, numpy-array, shape [|x unique values|,]
    """
    decode = {val: [1 if idx == i else 0 for idx in range(len(np.unique(x)))] for i, val in enumerate(sorted(np.unique(x)))}
    x_ohe = np.array([decode[i] for i in x])
    w = np.zeros(x_ohe.shape[1])
    max_iter = 1000
    learning_rate = 0.01
    tol = 1e-9
    for _ in range(max_iter):
        p = x_ohe @ w
        p = np.clip(p, 1e-15, 1 - 1e-15)
        grad = x_ohe.T @ (p - y)
        w_new = w - learning_rate * grad
        if np.linalg.norm(w_new - w) < tol:
            break
        w = w_new

    return w