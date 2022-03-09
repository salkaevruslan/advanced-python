import concurrent.futures
import datetime
import multiprocessing
import os
import math
import sys
import timeit

from matplotlib import pyplot as plt


def integrate(f, a, b, *, n_jobs=1, n_iter=1000):
    print(f"Beginning default integration with n_jobs={n_jobs} time:{datetime.datetime.now()}")
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    print(f"Ended default integration with n_jobs={n_jobs} time:{datetime.datetime.now()}")
    return acc


def integration_step_thread(x):
    return x[1](x[3] + x[0] * x[2]) * x[2]


def integrate_thread(f, a, b, *, n_jobs=1, n_iter=1000):
    print(f"Beginning integration using threads with n_jobs={n_jobs} time:{datetime.datetime.now()}")
    res = 0
    step = (b - a) / n_iter
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = executor.map(integration_step_thread, map(lambda i: (i, f, step, a), range(n_iter)))
    for f in futures:
        res += f
    print(f"Ended integration using threads with n_jobs={n_jobs} time:{datetime.datetime.now()}")
    return res


def integration_step_process(x):
    return x[1](x[3] + x[0] * x[2]) * x[2]


def integrate_process(f, a, b, *, n_jobs=1, n_iter=1000):
    print(f"Beginning integration using processes with n_jobs={n_jobs} time:{datetime.datetime.now()}")
    res = 0
    step = (b - a) / n_iter
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = executor.map(integration_step_thread, map(lambda i: (i, f, step, a), range(n_iter)))
    for f in futures:
        res += f
    print(f"Ended integration using processes with n_jobs={n_jobs} time:{datetime.datetime.now()}")
    return res


if __name__ == "__main__":
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    sys.stdout = open("artifacts/medium-logs.txt", 'w')
    process_times = []
    threads_times = []
    default_times = []
    for i in range(multiprocessing.cpu_count() * 2):
        process_times.append(
            timeit.timeit(lambda: integrate_process(math.cos, 0, math.pi / 2, n_jobs=i + 1), number=1))
        threads_times.append(
            timeit.timeit(lambda: integrate_thread(math.cos, 0, math.pi / 2, n_jobs=i + 1), number=1))
        default_times.append(
            timeit.timeit(lambda: integrate(math.cos, 0, math.pi / 2, n_jobs=i + 1), number=1))
    sys.stdout.close()
    x = list(map(lambda i: i + 1, range(multiprocessing.cpu_count() * 2)))
    plt.plot(x, process_times, label="Processes")
    plt.plot(x, threads_times, label="Threads")
    plt.plot(x, default_times, label="Default")
    plt.legend()
    plt.xlabel("Jobs")
    plt.ylabel("Time(sec)")
    plt.savefig("artifacts/medium-plot.png")
