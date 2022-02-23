import os

import numpy as np


class ToStrMixin:
    def __str__(self):
        new_line = '\n'
        return f'[{new_line.join(map(lambda x: "[" + " ".join(map(str, x)) + "]", self._data))}]'


class ToFileMixin:
    def save(self, path):
        with open(path, 'w') as file:
            file.write(self.__str__())


class GetSetMixin:
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = np.asarray(data)


class Matrix(np.lib.mixins.NDArrayOperatorsMixin, ToFileMixin, ToStrMixin, GetSetMixin):
    def __init__(self, data):
        self._data = np.asarray(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x.data if isinstance(x, Matrix) else x
                       for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


if __name__ == '__main__':
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    if not os.path.exists("artifacts/medium"):
        os.mkdir("artifacts/medium")
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))
    (matrix1 + matrix2).save("artifacts/medium/matrix+.txt")
    (matrix1 * matrix2).save("artifacts/medium/matrix*.txt")
    (matrix1 @ matrix2).save("artifacts/medium/matrix@.txt")
