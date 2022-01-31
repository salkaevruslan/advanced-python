import ast

import networkx as nx

from graph import AstGraph


def read_file(path):
    with open(path) as file:
        return file.read()


if __name__ == '__main__':
    code = read_file("fib.py")
    tree = ast.parse(code)
    graph = AstGraph()
    graph.visit(tree)
    G = graph.graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    p = nx.drawing.nx_pydot.to_pydot(G)
    p.write_png('artifacts/fib.png')
