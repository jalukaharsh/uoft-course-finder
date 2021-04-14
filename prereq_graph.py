from typing import List
from data_formatting import Graph


def build_trace_graph(courses: Dict[str, Dict], course: str) -> Graph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    AST = courses[course]['AST']

    if AST == []:  # base case: no prereqs/coreqs
        graph = Graph()
        course_vertex = course_graph.get_vertex(course)
        graph.add_vertex(course_vertex)
        return graph
    else:
        for vertex in AST.get_all_vertices():
            if vertex.get_type() == 'course' and vertex != course:
                prereq_AST = build_prereq_graph(courses, vertex)
                merge_graphs(AST, prereq_AST)


def merge_graph(AST: Graph(), prereq_AST: Graph()) -> None:
    """Mutates AST so that all vertices and edges in prereq_AST are added to AST."""
    AST_vertices = AST.get_all_vertices()
    for vertex in prereq_AST.get_all_vertices():
        if vertex not in AST_vertices:
            AST.add_vertex(vertex)
        else:
            # duplicate vertex case
            for neighbour in vertex.neighbours:
                AST.add_edge(vertex, neighbour)
