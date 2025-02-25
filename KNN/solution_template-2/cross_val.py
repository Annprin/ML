import numpy as np
import typing
from collections import defaultdict


def kfold_split(num_objects: int,
                num_folds: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """Split [0, 1, ..., num_objects - 1] into equal num_folds folds
       (last fold can be longer) and returns num_folds train-val
       pairs of indexes.

    Parameters:
    num_objects: number of objects in train set
    num_folds: number of folds for cross-validation split

    Returns:
    list of length num_folds, where i-th element of list
    contains tuple of 2 numpy arrays, he 1st numpy array
    contains all indexes without i-th fold while the 2nd
    one contains i-th fold
    """
    len_folds = num_objects // num_folds
    ans = []
    for i in range(num_folds - 1):
        ans.append((np.array([j for j in range(i * len_folds)] + [j for j in range((i + 1) * len_folds, num_objects)]), 
                    np.array([j for j in range(i * len_folds, (i + 1) * len_folds)])))
    ans.append((np.array([j for j in range((num_folds - 1) * len_folds)]), 
                    np.array([j for j in range((num_folds - 1) * len_folds, num_objects)])))
    return ans

def knn_cv_score(X: np.ndarray, y: np.ndarray, parameters: dict[str, list],
                 score_function: callable,
                 folds: list[tuple[np.ndarray, np.ndarray]],
                 knn_class: object) -> dict[str, float]:
    """Takes train data, counts cross-validation score over
    grid of parameters (all possible parameters combinations)

    Parameters:
    X: train set
    y: train labels
    parameters: dict with keys from
        {n_neighbors, metrics, weights, normalizers}, values of type list,
        parameters['normalizers'] contains tuples (normalizer, normalizer_name)
        see parameters example in your jupyter notebook

    score_function: function with input (y_true, y_predict)
        which outputs score metric
    folds: output of kfold_split
    knn_class: class of knn model to fit

    Returns:
    dict: key - tuple of (normalizer_name, n_neighbors, metric, weight),
    value - mean score over all folds
    """
    ans = {}
    for n in parameters['n_neighbors']:
        for metric in parameters['metrics']:
            for weight in parameters['weights']:
                for normalizer, normalizer_name in parameters['normalizers']:
                    score = []
                    for train_ind, val_ind in folds:
                        train = X[train_ind]
                        y_train = y[train_ind]
                        val = X[val_ind]
                        y_val = y[val_ind]
                        if normalizer:
                            normalizer.fit(train)
                            train = normalizer.transform(train)
                            val = normalizer.transform(val)
                        knn = knn_class(n_neighbors=n, metric=metric, weights=weight)
                        knn.fit(train, y_train)
                        y_pred = knn.predict(val)
                        score.append(score_function(y_val, y_pred))
                    ans[(normalizer_name, n, metric, weight)] = np.mean(np.array(score))
    print(ans)
    return ans