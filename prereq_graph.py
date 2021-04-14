import networkx as nx
from typing import List, Tuple
from .data_formatting import PrereqTree


def convert_tree(tree: PrereqTree) -> Tuple[nx.Graph(), str]:
    g = nx.Graph()
    if tree.subtrees == []:
        g.add_node(tree.item, attr_dict={'type': 'course'})
    else:
        for subtree in tree.subtrees:
            converted_subtree, subtree_root = convert_prereq_tree(subtree)
            g = nx.compose(g, converted_subtree)
            # add edge from root of g to root of subtree
            edge_type = 'connective' if subtree_root in {'or', 'and'} else 'course'
            g.add_edge(tree.item, subtree_root, edge_type)
    return g, tree.item


def build_trace_graph(courses: Dict[str, Dict], course: str) -> Graph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    prereq_tree = courses[course]['prereq_tree']
    coreq_tree = courses[course]['coreq_tree']
    AST = nx.compose(convert_tree(prereq_tree), convert_tree(coreq_tree))

    for vertex in list(AST.nodes):
        # recursive base case is when the only node in AST has course as its item
        if AST.data(vertex)['type'] == 'course' and vertex != course:
            prereq_AST = build_prereq_graph(courses, vertex)
            AST = compose(AST, prereq_AST)
    return AST


# def merge_graph(AST: Graph(), prereq_AST: Graph()) -> None:
#     """Mutates AST so that all vertices and edges in prereq_AST are added to AST."""
#     AST_vertices = AST.get_all_vertices()
#     for vertex in prereq_AST.get_all_vertices():
#         if vertex not in AST_vertices:
#             AST.add_vertex(vertex)
#         else:
#             # duplicate vertex case
#             for neighbour in vertex.neighbours:
#                 AST.add_edge(vertex, neighbour)

def draw_trace_graph(courses: Dict[str, Dict], course: str) -> None:
    graph = build_trace_graph(courses, course)
    nx.draw_networkx(graph)
