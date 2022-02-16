import ast
import inspect
import os

import networkx as nx

from ast_generator.graph import AstGraph
from ast_generator.fib import get_fib


def read_file(path):
    with open(path) as file:
        return file.read()


def main():
    if not os.path.exists("artifacts"):
        os.mkdir("artifacts")
    code = inspect.getsource(get_fib)
    tree = ast.parse(code)
    graph = AstGraph()
    graph.visit(tree)
    G = graph.graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png('artifacts/fib.png')


if __name__ == '__main__':
    main()
