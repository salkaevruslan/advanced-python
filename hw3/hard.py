import os

from easy import Matrix


class HashMixin:
    def __hash__(self):
        """Сумма элементов в матрице по модулю"""
        return sum(map(sum, self._data)) % (10 ** 9 + 7)


class MatrixWithHash(Matrix, HashMixin):
    _cache = {}

    @classmethod
    def invalidate_caches(cls):
        cls._cache = {}

    def __matmul__(self, other):
        if self.cols() != other.rows():
            raise Exception("Invalid argument")
        key = (hash(self), hash(other))
        if key not in MatrixWithHash._cache:
            res = MatrixWithHash([[0] * self.cols() for _ in range(self.rows())])
            for i in range(self.rows()):
                for j in range(other.cols()):
                    for k in range(self.cols()):
                        res._data[i][j] += self._data[i][k] * other._data[k][j]
            MatrixWithHash._cache[key] = res
        return MatrixWithHash._cache[key]


if __name__ == '__main__':
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    if not os.path.exists("artifacts/hard"):
        os.mkdir("artifacts/hard")
    A = MatrixWithHash([[1, 2], [3, 4]])
    B = MatrixWithHash([[1, 0], [0, 1]])
    C = MatrixWithHash([[3, 2], [1, 4]])
    D = MatrixWithHash([[1, 0], [0, 1]])

    AB = A @ B
    MatrixWithHash.invalidate_caches()
    CD = C @ D

    A.save("artifacts/hard/A.txt")
    B.save("artifacts/hard/B.txt")
    C.save("artifacts/hard/C.txt")
    D.save("artifacts/hard/D.txt")
    CD.save("artifacts/hard/CD.txt")
    AB.save("artifacts/hard/AB.txt")
    with open("artifacts/hard/hash.txt", 'w') as f:
        f.write(f'{hash(AB)}\n{hash(CD)}')
