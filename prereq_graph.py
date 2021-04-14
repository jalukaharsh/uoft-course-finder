from typing import List
from data_formatting import Graph


def build_prereq_graph(course_graph: Graph(), course: str) -> Graph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    v1 = course_graph.get_vertex(course)
    prereq_graphs = []

    for neighbour in v1:
        edge_type = v1.get_edge_type(neighbour)
        if edge_type in {'prereq', 'coreq'}:
            prereq_graphs.append(build_prereq_graph(course_graph, neighbour.name))
    merge_graphs(prereq_graphs)


def merge_graphs(graphs: List[Graph()]) -> Graph():
    return
