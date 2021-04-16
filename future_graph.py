"""CSC111 Project: University of Toronto Course Finder: Data Formatting

Module Description:
====================
The module contains the functions that generate the 'future graphs' for a given course.
"""

from typing import Dict
import networkx as nx


def future(courses: Dict[str, Dict], course: str) -> nx.Graph():
    """Return a graph containing all the future courses that this course can lead to. """
    future_graph = nx.Graph()
    future_graph.add_node(course, tag='original')
    add_children(courses, course, future_graph)
    return future_graph


def add_children(courses: Dict[str, Dict], course: str, graph: nx.Graph()) -> None:
    """Mutate the given graph object to add all the courses that course is a prerequisite for. """
    for item in courses:
        if courses[item]['prerequisites'] is not None and course in courses[item]['prerequisites']:
            graph.add_node(item, tag='no')
            graph.add_edge(course, item)
            add_children(courses, item, graph)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
