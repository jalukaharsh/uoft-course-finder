"""Code to build the prerequisities graph. """


from typing import Dict
import networkx as nx


def build_trace_graph(courses: Dict[str, Dict], course: str) -> nx.DiGraph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    prereq_tree = courses[course]['prereq_tree']
    coreq_tree = courses[course]['coreq_tree']
    ast = nx.compose_all([tree for tree in [prereq_tree, coreq_tree, nx.DiGraph()]
                          if tree is not None])
    for vertex in ast.nodes(data=True):
        # recursive base case is when the only node in AST has course as its item
        if vertex[1]['type'] == 'course' and vertex[0] != course:
            prereq_ast = build_trace_graph(courses, vertex[0])
            ast = nx.compose(ast, prereq_ast)

    for item in ast.nodes:
        if item == course:
            ast.nodes[item]['tag'] = 'original'
        else:
            ast.nodes[item]['tag'] = 'no'
    return ast


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
