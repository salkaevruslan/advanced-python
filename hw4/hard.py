import codecs
import datetime
import multiprocessing
import os
import sys
import time
from multiprocessing import Process
from threading import Thread


def A(q, conn_to_B):
    try:
        while True:
            s = q.get()
            conn_to_B.send(s.lower())
            time.sleep(5)
    except Exception:
        pass
    finally:
        conn_to_B.close()


def B(conn_to_main, conn_to_A):
    try:
        while True:
            s = conn_to_A.recv()
            conn_to_main.send(codecs.encode(s, 'rot13'))
    except Exception:
        pass
    finally:
        conn_to_main.close()


def messages_sender(q):
    for line in sys.stdin:
        print(f"Sent message: {line} at {datetime.datetime.now()}")
        q.put(line)
    q.close()


def message_receiver(parent_conn):
    try:
        while True:
            s = parent_conn.recv()
            print(f"Received message: {s} at {datetime.datetime.now()}")
    except Exception:
        pass


if __name__ == "__main__":
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    sys.stdout = open("artifacts/hard.txt", 'w')
    q = multiprocessing.Queue()
    parent_conn_B, child_conn_A = multiprocessing.Pipe()
    parent_conn_main, child_conn_B = multiprocessing.Pipe()
    process_a = Process(target=A, args=(q, child_conn_A,))
    process_b = Process(target=B, args=(child_conn_B, parent_conn_B,))
    sender = Thread(target=messages_sender, args=(q,))
    receiver = Thread(target=message_receiver, args=(parent_conn_main,), daemon=True)
    process_a.start()
    process_b.start()
    sender.start()
    receiver.start()
    sender.join()
    process_a.kill()
    process_b.kill()
    sys.stdout.close()
