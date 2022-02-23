import copy
import os

import numpy as np


class Matrix:

    def __init__(self, data=None):
        if data is not None:
            for i in range(0, len(data) - 1):
                if len(data[i]) != len(data[i + 1]):
                    raise ValueError("Data should be rectangle matrix")
            self._data = copy.deepcopy(data)
        else:
            raise ValueError("Data should be not None")

    def rows(self):
        return len(self._data)

    def cols(self):
        return len(self._data[0])

    def __add__(self, other):
        if self.rows() != other.rows() or self.cols() != other.cols():
            raise Exception("Invalid argument")
        res = Matrix([[0] * self.cols() for _ in range(self.rows())])
        for i in range(self.rows()):
            for j in range(self.cols()):
                res._data[i][j] = self._data[i][j] + other._data[i][j]
        return res

    def __mul__(self, other):
        if self.rows() != other.rows() or self.cols() != other.cols():
            raise Exception("Invalid argument")
        res = Matrix([[0] * self.cols() for _ in range(self.rows())])
        for i in range(self.rows()):
            for j in range(self.cols()):
                res._data[i][j] = self._data[i][j] * other._data[i][j]
        return res

    def __matmul__(self, other):
        if self.cols() != other.rows():
            raise Exception("Invalid argument")
        res = Matrix([[0] * self.cols() for _ in range(self.rows())])
        for i in range(self.rows()):
            for j in range(other.cols()):
                for k in range(self.cols()):
                    res._data[i][j] += self._data[i][k] * other._data[k][j]
        return res

    def __str__(self):
        s = ""
        for r in self._data:
            for c in r:
                s += str(c)
                s += ' '
            s += '\n'
        return s

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.__str__())


if __name__ == '__main__':
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    if not os.path.exists("artifacts/easy"):
        os.mkdir("artifacts/easy")
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))
    (matrix1 + matrix2).save("artifacts/easy/matrix+.txt")
    (matrix1 * matrix2).save("artifacts/easy/matrix*.txt")
    (matrix1 @ matrix2).save("artifacts/easy/matrix@.txt")