import numpy as np
from typing import Tuple


def sum_non_neg_diag(X: np.ndarray) -> int:
    """
    Вернуть  сумму неотрицательных элементов на диагонали прямоугольной матрицы X. 
    Если неотрицательных элементов на диагонали нет, то вернуть -1
    """
    d = np.diag(X)
    s = d[np.where(d >= 0)]
    return -1 if len(s) == 0 else np.sum(s)


def are_multisets_equal(x: np.ndarray, y: np.ndarray) -> bool:
    """
    Проверить, задают ли два вектора одно и то же мультимножество.
    """
    x = np.sort(x)
    y = np.sort(y)
    return np.all((x == y) == True)


def max_prod_mod_3(x: np.ndarray) -> int:
    """
    Вернуть максимальное прозведение соседних элементов в массиве x, 
    таких что хотя бы один множитель в произведении делится на 3.
    Если таких произведений нет, то вернуть -1.
    """
    res = x[:-1] * x[1:]
    mask = res % 3 == 0
    return np.max(res[mask]) if len(res[mask]) > 0 else -1


def convert_image(image: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """
    Сложить каналы изображения с указанными весами.
    """
    X = image.reshape(len(image) * len(image[0]), len(image[0][0]))
    return np.sum(X * weights, axis=1).reshape(len(image), len(image[0]))


def rle_scalar(x: np.ndarray, y: np.ndarray) -> int:
    """
    Найти скалярное произведение между векторами x и y, заданными в формате RLE.
    В случае несовпадения длин векторов вернуть -1.
    """
    new_x = np.repeat(x[:, 0], x[:, 1])
    new_y = np.repeat(y[:, 0], y[:, 1])
    if new_x.size != new_y.size:
        return -1
    return np.sum(new_x * new_y)


def cosine_distance(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    Вычислить матрицу косинусных расстояний между объектами X и Y.
    В случае равенства хотя бы одно из двух векторов 0, косинусное расстояние считать равным 1.
    """
    abs_X = np.sum(X ** 2, axis=1) ** 0.5
    abs_Y = np.sum(Y ** 2, axis=1) ** 0.5
    abs_XY = (abs_X.reshape(len(X), 1) * abs_Y)
    cos_matrix = X[:, np.newaxis] * Y
    res = np.divide(np.sum(cos_matrix, axis = 2), abs_XY, where=abs_XY != 0)
    res[abs_XY == 0] = 1
    return res
