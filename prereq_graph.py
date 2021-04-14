import networkx as nx
from typing import List
from data_formatting import Graph


def build_trace_graph(courses: Dict[str, Dict], course: str) -> Graph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    AST = courses[course]['AST']
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
