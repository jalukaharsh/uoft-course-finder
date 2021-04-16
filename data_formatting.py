"""CSC111 Project: University of Toronto Course Finder: Data Formatting

Module Description:
====================
The module contains the function that processes the raw data file into list of courses, with each
course represented as a dictionary.
"""

from __future__ import annotations
from typing import Tuple, Dict
import json
import networkx as nx
from PrereqTree_class import PrereqTree


def get_courses_data() -> dict:
    """Return a dictionary of course data from the courses.json file. Two new key-value pairs are
    added; 'prereq_tree' and 'coreq_tree'. The value for each key is a tree generated based on the
    string of prerequisites and corequisites respectively.
    """
    json_data = open('courses.json')
    data = json.load(json_data)
    data_dict = {}
    for course in data:
        if 'prerequisites' not in course or course['prerequisites'] is None:
            course['prereq_tree'] = None
        else:
            add_tree(course, 'pre')

        if 'corequisites' not in course or course['corequisites'] is None:
            course['coreq_tree'] = None
        else:
            add_tree(course, 'co')

        data_dict[course['code']] = course
    return data_dict


def add_tree(course: Dict, type: str) -> None:
    """Mutates course to insert a prerequisite/corequisite tree (depending on type).

    Preconditions
        - type in {'co', 'pre'}
    """
    code = course['code']
    # if a course appears in its own req list then remove it.
    course[type + 'requisites'] = course[type + 'requisites'].replace(code, '')
    tree = PrereqTree(course[type + 'requisites'])

    # add requisite tree to course dict
    course[type + 'req_tree'], root, connective_count = convert_tree(tree, type + 'req', code)
    # add course to graph
    course[type + 'req_tree'].add_node(code, type='course', value=code)
    # add edge from course to req tree root
    if root != '':
        course[type + 'req_tree'].add_edge(code, root, edge_type=type + 'req')


def convert_tree(tree: PrereqTree, tree_type: str,
                 course: str, connective_count=0) -> Tuple[nx.DiGraph, str, int]:
    """Returns as a tuple the given PrereqTree as a networkx graph along with the tree's root and
    the total number of connectives counted so far.
    Connective_count counts the number of connectives encountered so far, so that we can label all
    connectives uniquely.
    Preconditions
        - tree_type in {'prereq', 'coreq'}
    """
    g = nx.DiGraph()
    if tree.subtrees == []:
        # base case: leaf node, which always represents a course
        if tree.item == '':
            return g, '', connective_count
        g.add_node(tree.item, type='course', value=tree.item)
        return g, tree.item, connective_count
    else:
        # create a copy to avoid mutation
        connective_count_2 = connective_count

        # add root of tree to g
        tree_root_label = f'{tree.item}_{course}_{connective_count_2}'
        g.add_node(tree_root_label, type='connective', value=tree.item)
        connective_count_2 += 1

        # convert & add subtrees to g
        for subtree in tree.subtrees:
            # helper
            connective_count_2 = add_subtree(g, subtree, tree_type, course,
                                             connective_count_2, tree_root_label)

        return g, tree_root_label, connective_count_2


def add_subtree(g: nx.DiGraph, subtree: PrereqTree, tree_type: str, course: str,
                connective_count: int, tree_root_label: str) -> int:
    """Converts the given subtree to nx.DiGraph object and composes it into g (g is mutated).
    Returns the updated value of connective_count i.e. the number of connectives encountered
    so far.
    Preconditions
        - tree_type in {'prereq', 'coreq'}
    """
    # counts the number of connectives encountered so far in order to label any upcoming connectives
    connective_count_2 = connective_count

    # convert this subtree to nx.DiGraph object. This is the recursive step in convert_graph.
    converted_subtree, subtree_root, connective_count_2 = \
        convert_tree(subtree, tree_type, course, connective_count_2)

    if subtree_root == '':
        return connective_count

    # add nodes from converted_subtree to g
    for node in converted_subtree.nodes(data=True):
        if node[0] in {'or', 'and'}:
            # if node is an unlabeled connective
            g.add_node(f'{node[0]}_{course}_{connective_count_2}', type='connective', value=node[0])
            connective_count_2 += 1
        else:
            # if node is a labeled connective or a course (all courses have already been labeled
            # in the base case of convert_tree)
            g.add_node(node[0], type=node[1]['type'], value=node[1]['value'])
            if node[1]['type'] == 'connective':
                connective_count_2 += 1

    # add edge from tree root to this subtree's root
    g.add_edge(tree_root_label, subtree_root, edge_type=tree_type)
    # add edges from converted_subtree to g
    g.add_edges_from(converted_subtree.edges, edge_type=tree_type)

    return connective_count_2


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['re', 'json', 'networkx'],
        'allowed-io': ['get_courses_data'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
