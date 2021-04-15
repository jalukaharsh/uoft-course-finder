"""Generate the future graphs."""

import networkx as nx
from typing import Dict


def future(courses: Dict[str, Dict], course: str) -> nx.Graph():
    """Return a graph containing all the future courses that this course can lead to. """
    future_graph = nx.DiGraph()
    future_graph.add_node(course, tag='original')
    add_children(courses, course, future_graph)
    return future_graph


def add_children(courses: Dict[str, Dict], course: str, graph: nx.Graph()) -> None:
    """Mutate the given graph object to add all the courses that course is a prerequisite for. """
    for item in courses:
        if courses[item]['prerequisites'] is not None and course in courses[item]['prerequisites']:
            graph.add_node(item, tag='no')
            graph.add_edge(course, item)
            try:
                add_children(courses, item, graph)
            except RecursionError:
                pass


def future_one_level(courses: Dict[str, Dict], course: str) -> nx.Graph():
    """Return a graph containing only the courses that the input course directly leads to.
    """
    future_graph = nx.Graph()
    future_graph.add_node(course, tag='original')
    for item in courses:
        if courses[item]['prerequisites'] is not None and course in courses[item]['prerequisites']:
            future_graph.add_node(item, tag='no')
            future_graph.add_edge(course, item)
    return future_graph


def future_one_level_mutate(courses: Dict[str, Dict], course: str, future_graph: nx.Graph()) -> None:
    """Mutate a graph to add only the courses that the input course directly leads to.

    Preconditions:
        - course is in the graph
    """
    for item in courses:
        if courses[item]['prerequisites'] is not None and course in courses[item]['prerequisites']:
            future_graph.add_node(item, tag='no')
            future_graph.add_edge(course, item)
