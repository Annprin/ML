from typing import List


def sum_non_neg_diag(X: List[List[int]]) -> int:
    """
    Вернуть  сумму неотрицательных элементов на диагонали прямоугольной матрицы X. 
    Если неотрицательных элементов на диагонали нет, то вернуть -1
    """ 
    sum = 0
    not_null = False
    minim = min(len(X), len(X[0]))
    for i in range(minim):
        if X[i][i] >= 0:
            sum += X[i][i]
            not_null = True
    return sum if not_null else -1


def are_multisets_equal(x: List[int], y: List[int]) -> bool:
    """
    Проверить, задают ли два вектора одно и то же мультимножество.
    """
    ans = True
    m = {}
    for i in x:
        if i in y:
            y.remove(i)
        else:
            ans = False
            break
    if y:
        ans = False
    return ans


def max_prod_mod_3(x: List[int]) -> int:
    """
    Вернуть максимальное прозведение соседних элементов в массиве x, 
    таких что хотя бы один множитель в произведении делится на 3.
    Если таких произведений нет, то вернуть -1.
    """
    pr = 0
    first = True
    for i in range(len(x))[:-1]:
        if x[i] * x[i + 1] % 3 == 0:
            if first:
                pr = x[i] * x[i + 1]
                first = False
            pr = max(x[i] * x[i + 1], pr)
    return pr if pr else -1



def convert_image(image: List[List[List[float]]], weights: List[float]) -> List[List[float]]:
    """
    Сложить каналы изображения с указанными весами.
    """
    sum = [[0 for _ in range(len(image[0]))] for _ in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            for k in range(len(image[0][0])):
                sum[i][j] += weights[k] * image[i][j][k]
    return sum

        


def rle_scalar(x: List[List[int]], y:  List[List[int]]) -> int:
    """
    Найти скалярное произведение между векторами x и y, заданными в формате RLE.
    В случае несовпадения длин векторов вернуть -1.
    """
    a = []
    for i in x:
        a += [i[0]] * i[1]
    b = []
    for i in y:
        b += [i[0]] * i[1]
    if len(a) != len(b):
        return -1
    sc = 0
    for i in range(len(a)):
        sc += a[i] * b[i]
    return sc

def mod_2(x):
    m_2 = 0
    for i in x:
        m_2 += i ** 2
    return m_2

def mul(x, y):
    sc = 0
    for i in range(len(x)):
        sc += x[i] * y[i]
    return sc / (mod_2(x) ** 0.5 * mod_2(y) ** 0.5)

def all_null(x):
    all = True
    for i in x:
        if i != 0:
            all = False
    return all

def cosine_distance(X: List[List[float]], Y: List[List[float]]) -> List[List[float]]:
    """
    Вычислить матрицу косинусных расстояний между объектами X и Y. 
    В случае равенства хотя бы одно из двух векторов 0, косинусное расстояние считать равным 1.
    """
    res = [[0 for _ in range(len(Y))] for _ in range(len(X))]
    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            res[i][j] = 1 if (all_null(x) or all_null(y)) else mul(x, y)
    if len(X) < 50:
        print(res)
    return res
