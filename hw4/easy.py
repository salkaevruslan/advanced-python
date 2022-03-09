import os
import timeit
from multiprocessing import Process
from threading import Thread


N = 10000
runs = 10


def fibonacci(n):
    fib = [0] * n
    fib[1] = fib[0] = 1
    for i in range(2, n):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib


def sync():
    for _ in range(runs):
        fibonacci(N)


def threads():
    tds = []
    for _ in range(runs):
        tds.append(Thread(target=fibonacci, args=(N,)))
    for t in tds:
        t.start()
    for t in tds:
        t.join()


def multiprocess():
    processes = []
    for _ in range(runs):
        processes.append(Process(target=fibonacci, args=(N,)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()


if __name__ == "__main__":
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    with open("artifacts/easy.txt", 'w') as file:
        print(f"Sync: {timeit.timeit(sync, number=1)} sec", file=file)
        print(f"Thread: {timeit.timeit(threads, number=1)} sec", file=file)
        print(f"Process: {timeit.timeit(multiprocess, number=1)} sec", file=file)
