import networkx as nx


class AstGraph(object):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.count_binop = 0
        self.count_body = 0

    def add_children(self, parent, children, label=''):
        for child in children:
            self.graph.add_edge(parent, child, label=label)

    def visit(self, node):
        visit_method_name = ('visit_' + node.__class__.__name__).lower()
        visitor = getattr(self, visit_method_name)
        return visitor(node)

    def visit_module(self, node):
        self.graph.add_node(node, shape='box', label='Module', fillcolor='maroon', style='filled', width=2)
        self.add_children(node, self.visit(node.body[0]))
        return [node]

    def visit_constant(self, node):
        self.graph.add_node(node, shape='box', label=f'Constant {node.value}',
                            fillcolor='aqua', style='filled', width=2)
        return [node]

    def visit_name(self, node):
        self.graph.add_node(node, shape='box', label=f'Name {node.id}', fillcolor='green', style='filled', width=2)
        return [node]

    def visit_expr(self, node):
        return self.visit(node.value)

    def visit_arguments(self, node):
        self.graph.add_node(node, shape='box', label='arguments', fillcolor='purple', style='filled', width=2)
        for arg in node.args:
            self.add_children(node, self.visit(arg))
        return [node]

    def visit_arg(self, node):
        self.graph.add_node(node, shape='box', label=f'Arg {node.arg}', fillcolor='lightblue', style='filled', width=2)
        return [node]

    def visit_for(self, node):
        self.graph.add_node(node, shape='box', label='For', fillcolor='pink', style='filled', width=2)
        self.add_children(node, self.visit(node.target), label='variable')
        self.add_children(node, self.visit(node.iter), label='iteration')
        self.count_body += 1
        self.graph.add_node('body' + str(self.count_body), shape='box', label='body', fillcolor='cyan',
                            style='filled', width=2)
        self.add_children(node, ['body' + str(self.count_body)])
        for body in node.body:
            self.add_children('body' + str(self.count_body), self.visit(body))
        return [node]

    def visit_binop(self, node):
        self.graph.add_node(node, shape='box', label='BinOp', fillcolor='teal', style='filled', width=2)
        self.add_children(node, self.visit(node.left), label='left')
        self.count_binop += 1
        self.graph.add_node(str(node.op) + str(self.count_binop), shape='box', label=f'{type(node.op).__name__}',
                            fillcolor='purple', style='filled')
        self.add_children(node, [str(node.op) + str(self.count_binop)], label='operation')
        self.add_children(node, self.visit(node.right), label='right')
        return [node]

    def visit_assign(self, node):
        self.graph.add_node(node, shape='box', label='Assign', fillcolor='gray', style='filled', width=2)
        for target in node.targets:
            self.add_children(node, self.visit(target))
        self.add_children(node, self.visit(node.value))
        return [node]

    def visit_return(self, node):
        self.graph.add_node(node, shape='box', label='Return', fillcolor='brown', style='filled', width=2)
        self.add_children(node, self.visit(node.value))
        return [node]

    def visit_functiondef(self, node):
        self.graph.add_node(node, shape='box', label=f'Function {node.name}',
                            fillcolor='blue', style='filled', width=2)
        self.add_children(node, self.visit(node.args))
        for body in node.body:
            self.add_children(node, self.visit(body))
        return [node]

    def visit_list(self, node):
        self.graph.add_node(node, shape='box', label='List', fillcolor='pink', style='filled', width=2)
        for elt in node.elts:
            self.add_children(node, self.visit(elt))
        return [node]

    def visit_subscript(self, node):
        self.graph.add_node(node, shape='box', label='Subscript', fillcolor='salmon', style='filled', width=2)
        self.add_children(node, self.visit(node.value), label='value')
        self.add_children(node, self.visit(node.slice), label='slice')
        return [node]

    def visit_call(self, node):
        self.graph.add_node(node, shape='box', label='Call', fillcolor='orange', style='filled', width=2)
        self.add_children(node, self.visit(node.func))
        for arg_node in node.args:
            self.add_children(node, self.visit(arg_node))
        return [node]

    def visit_index(self, node):
        return self.visit(node.value)
