"""CSC111 Project: University of Toronto Course Finder: Prerequisite Graph

Module Description:
====================
The module contains the functions that generate the 'prereq graphs' for a given course.
"""

from typing import Dict
import networkx as nx


def build_trace_graph(courses: Dict[str, Dict], course: str) -> nx.DiGraph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    prereq_tree = courses[course]['prereq_tree']
    coreq_tree = courses[course]['coreq_tree']
    # if both prereq_tree and coreq_tree are None, then graph is set to an empty graph
    graph = nx.compose_all([tree for tree in [prereq_tree, coreq_tree, nx.DiGraph()]
                            if tree is not None])

    for vertex in graph.nodes(data=True):
        # recursive base case is when the only node in graph has course as its item
        if vertex[1]['type'] == 'course' and vertex[0] != course and vertex[0] in courses:
            prereq_graph = build_trace_graph(courses, vertex[0])
            graph = nx.compose(graph, prereq_graph)

        # mark original searched course so it can be colored distinctively
        if vertex[0] == course:
            graph.nodes[vertex[0]]['tag'] = 'original'
        else:
            graph.nodes[vertex[0]]['tag'] = 'no'

    remove_redundant_connectives(graph)

    return graph


def remove_redundant_connectives(graph: nx.DiGraph) -> None:
    """Mutate graph to remove redundant connectives i.e. those that only lead to one course"""
    removable_nodes = []
    for vertex in list(graph.nodes):
        # for each successor of vertex
        for neighbour in list(graph.successors(vertex)):
            # if the neighbour is a redundant connective
            if graph.nodes[neighbour]['type'] == 'connective' and graph.out_degree(neighbour) == 0:
                removable_nodes.append(neighbour)
            if graph.nodes[neighbour]['type'] == 'connective' and graph.out_degree(neighbour) == 1:
                # by definition, neighbour only has one neighbour
                neighbour_neighbour = list(graph.successors(neighbour))[0]

                # create an edge (vertex, neighbour_neighbour), bypassing the redundant connective
                edge_type = graph.get_edge_data(vertex, neighbour)['edge_type']
                graph.add_edge(vertex, neighbour_neighbour, edge_type=edge_type)

                # add the redundant connective to the list of nodes to be removed
                removable_nodes.append(neighbour)
    graph.remove_nodes_from(removable_nodes)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
