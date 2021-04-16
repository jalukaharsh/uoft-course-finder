"""CSC111 Project: University of Toronto Course Finder: Data Formatting
Module Description:
====================
The module contains the function that processes the raw data file into list of courses, with each
course represented as a dictionary.
"""


from __future__ import annotations
from typing import Tuple
import json
import re
import networkx as nx


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
            code = course['code']
            # if a course appears in its own prereq list then remove it
            course['prerequisites'] = course['prerequisites'].replace(code, '')

            prereq_tree = PrereqTree(course['prerequisites'])
            course['prereq_tree'], root, connective_count =\
                convert_tree(prereq_tree, 'prereq', code)

            # add edge from course to prereq tree
            course['prereq_tree'].add_node(code, type='course', value='')
            if root != '':
                course['prereq_tree'].add_node(f'{root[:-1]}_{connective_count}',
                                               type='connective', value='')
                course['prereq_tree'].add_edge(code, root, edge_type='prereq')
                # remove any isolated leftover connectives
                isolates = list(nx.isolates(course['prereq_tree']))
                course['prereq_tree'].remove_nodes_from(isolates)

        if 'corequisites' not in course or course['corequisites'] is None:
            course['coreq_tree'] = None
        else:
            code = course['code']
            # if a course appears in its own coreq list then remove it.
            course['corequisites'] = course['corequisites'].replace(code, '')
            coreq_tree = PrereqTree(course['corequisites'])

            course['coreq_tree'], root, connective_count =\
                convert_tree(coreq_tree, 'coreq', code)

            # add edge from course to coreq tree
            course['coreq_tree'].add_node(code, type='course', value='')
            if root != '':
                course['coreq_tree'].add_node(f'{root[:-1]}_{connective_count}',
                                              type='connective', value='')
                course['coreq_tree'].add_edge(code, root, edge_type='coreq')
                # remove any isolated leftover connectives
                isolates = list(nx.isolates(course['coreq_tree']))
                course['coreq_tree'].remove_nodes_from(isolates)

        data_dict[course['code']] = course
    return data_dict


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
        g.add_node(tree.item, type='course', value='')
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


class PrereqTree:
    """A tree dataclass representing prerequisites and corequisites.

     All courses which are not offered by UTSG are deliberately removed. If a string contains two
     course codes without a (, ), ',', / between them (only english) then '/' is assumed.

    Instance Attributes:
        - item: the type of the tree. It can be 'or' or 'and' or a string of the form
            /[A-Z]{3}[0-9]{3}[H,Y]1/ (in which case it is a root and subtrees is empty)
        - subtrees: The vertices that are adjacent to this vertex. This

    Representation Invariants:
        - self.item == 'and' or self.item == 'or' or self.item = '' or
            re.fullmatch(r'[A-Z]{3}[0-9]{3}[H,Y]1', self.item) is not None
    """
    item: str
    subtrees: list[PrereqTree]

    def __init__(self, prereq_str: str) -> None:
        """
        prereq_str is a string representing prerequisite/corequisite strings.
        It should be in the format described in the academic calendar for course lists.
        """
        # remove all whitespace
        prereq_str = re.sub(r'\s+', '', prereq_str)
        # commas and semicolons and pluses all mean the same thing in course lists
        prereq_str = prereq_str.replace(';', ',')
        prereq_str = prereq_str.replace('+', ',')

        # deal base case of prereq_str being just a single course:
        if re.fullmatch(r'[A-Z]{3}[0-9]{3}[H,Y]1', prereq_str) is not None:
            self.item = prereq_str
            self.subtrees = []
            return

        # tokenize the prereq string into courses codes, commas, forward slashes and parentheses
        split_str = re.findall(r'(?:(?:[A-Z]{3}[0-9]{3}[H,Y]1)|[/,()])', prereq_str)

        # combine each parenthetical into a single string (which we will later recurse on)
        while '(' in split_str:
            first_paren = split_str.index('(')
            nest = 1
            length = 1
            while nest >= 1:
                if length + first_paren >= len(split_str):
                    # this should only occur if there are unmatched parentheses
                    split_str.append(')')

                substr = split_str[length + first_paren]
                length += 1
                if substr == '(':
                    nest += 1
                elif substr == ')':
                    nest -= 1

            # join the parenthesized string together (without the parentheses included)
            parenthesized_str = ''.join(split_str[first_paren + 1:first_paren + length - 1])

            if re.search(r'[A-Z]{3}[0-9]{3}[H,Y]1', parenthesized_str) is None:
                # if the parenthesized string includes no course codes then we remove it
                split_str = split_str[0: first_paren] + split_str[first_paren + length:]
            else:
                # otherwise insert it into split str, replacing the indices that were used by
                # its constituent parts
                split_str = split_str[0: first_paren] + [parenthesized_str] + \
                            split_str[first_paren + length:]

        while ')' in split_str:  # this should only happen if there is some ')' which is
            # not matching a ')'.
            index = split_str.index(')')
            split_str = split_str[:index] + split_str[index + 1:]

        ors = []  # list of each or(/) block.
        current = []
        for substr in split_str:
            if substr == ',':
                ors.append(current)
                current = []
            elif substr != '/':
                current.append(substr)

        if current != '':
            ors.append(current)

        if len(ors) == 1:
            if len(ors[0]) >= 1:
                self.item = 'or'
                self.subtrees = []
                for el in ors[0]:
                    self.subtrees.append(PrereqTree(el))
            else:
                self.subtrees = []
                self.item = ''
        else:
            self.item = 'and'
            self.subtrees = []
            for el in ors:
                self.subtrees.append(PrereqTree('/'.join(el)))
