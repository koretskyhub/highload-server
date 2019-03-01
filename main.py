from multiprocessing import Process
import socket

import cli_args
import config
from worker import Worker

_QUEUE_SIZE = 8

def open_socket(host, port, queue_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(queue_size)
    sock.setblocking(False)

    return sock


def main():
    ns = cli_args.get_arguments_namespace()

    if ns.config_file is not None:
        conf = config.Config(ns.config_file)
        params = dict(conf.params)
    elif ns.document_root is not None:
        params = dict(vars(ns))
    else:
        raise ValueError('Not enough parameters to start server')

    workers = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((params['host'], params['port']))
    sock.listen(_QUEUE_SIZE)
    sock.setblocking(False)

    try:
        for _ in range(params['cpu_limit']):
            worker = Process(target = Worker, args=(sock, params['document_root']))
            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        for _, worker in enumerate(workers):
            worker.terminate()

if __name__ == '__main__':
    main()
