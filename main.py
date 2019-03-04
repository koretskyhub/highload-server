import argparse
from multiprocessing import Process
import socket

import constants
import config
from worker import Worker


def get_arguments_namespace():
    parser = argparse.ArgumentParser(description = 'Web-server for highload tp course')
    parser.add_argument('--config-file', type = str, help = 'file to load parameters for run server')
    parser.add_argument('--host', type = str, default = 'localhost', help = 'address to bind server socket')
    parser.add_argument('--port', type = int, default = 80, help = 'port to bind server socket')
    parser.add_argument('--cpu_limit', type = int, default = 1, help = 'number of workers to run by server')
    parser.add_argument('--document_root', type =  str, help = 'absolute path to serve files from')

    return parser.parse_args()


def main():
    ns = get_arguments_namespace()

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
    sock.listen(constants.QUEUE_SIZE)
    sock.setblocking(False)
    
    print('Server listening at:', params['host'], 'port', params['port'])
    print('serving files from:', params['document_root'])
    print('workers number is:', params['cpu_limit'])

    try:
        for _ in range(params['cpu_limit']):
            worker = Process(target = Worker, args=(sock, params['document_root']))
            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        for worker in workers:
            worker.terminate()
            
        print('Server terminated')


if __name__ == '__main__':
    main()
