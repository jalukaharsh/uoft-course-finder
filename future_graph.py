"""Generate the future graphs."""

import networkx as nx
from typing import Dict


def future(courses: Dict[str, Dict], course: str) -> nx.Graph():
    """Return a graph containing all the future courses that this course can lead to. """
    future_graph = nx.Graph()
    future_graph.add_node(course)
    add_children(courses, course, future_graph)
    return future_graph


def add_children(courses: Dict[str, Dict], course: str, graph: nx.Graph()) -> None:
    """Mutate the given graph object to add all the courses that course is a prerequisite for. """
    for item in courses:
        if course in courses[item]['prerequisites']:
            graph.add_node(item)
            graph.add_edge(item, course)
            add_children(courses, item, graph)
