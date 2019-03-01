import argparse

def get_arguments_namespace():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config-file', type = str)
    parser.add_argument('--host', type = str, default = 'localhost')
    parser.add_argument('--port', type = int, default = 80)
    parser.add_argument('--cpu_limit', type = int, default = 1)
    parser.add_argument('--document_root', type =  str)

    return parser.parse_args()
