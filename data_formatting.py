"""CSC111 Project: University of Toronto Course Finder: Data Formatting
Module Description:
====================
The module contains the function that processes the raw data file into list of courses, with each
course represented as a dictionary.
"""


from __future__ import annotations
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
            # if a course appears in its own prereq list then remove it
            course['prerequisites'] = course['prerequisites'].replace(course['code'], '') 
            prereq_tree = PrereqTree(course['prerequisites'])
            course['prereq_tree'], root = convert_tree(prereq_tree, 'prereq')
            course['prereq_tree'].add_node(course['code'])
            course['prereq_tree'].add_edge(course['code'], root)

        if 'corequisites' not in course or course['corequisites'] is None:
            course['coreq_tree'] = None
        else:
            course['corequisites'] = course['corequisites'].replace(course['code'], '')
            coreq_tree = PrereqTree(course['corequisites'])
            course['coreq_tree'], root = convert_tree(coreq_tree, 'coreq')
            course['coreq_tree'].add_node(course['code'])
            course['coreq_tree'].add_edge(course['code'], root)

        data_dict[course['code']] = course
    return data_dict


def convert_tree(tree: PrereqTree, tree_type: str) -> Tuple[nx.Graph, str]:
    """Returns as a tuple the given PrereqTree as a networkx graph along with the tree's root."""
    g = nx.Graph()
    if tree.subtrees == []:
        g.add_node(tree.item, attr_dict={'type': 'course'})
    else:
        for subtree in tree.subtrees:
            converted_subtree, subtree_root = convert_tree(subtree, tree_type)
            g = nx.compose(g, converted_subtree)
            # add edge from root of g to root of subtree
            g.add_edge(tree.item, subtree_root, edge_type=tree_type)
    return g, tree.item


class PrereqTree:
    """A tree dataclass representing prerequisites and corequisites.

     All courses which are not offered by UTSG are deliberately removed. If a string contains two
     course codes without a (, ), ',', / between them (only english) then '/' is assumed.

    Instance Attributes:
        - item: the type of the tree. It can be 'or' or 'and' or a string of the form
            /[A-Z]{3}[0-9]{3}[H,Y]1/ (in which case it is a root and subtrees is empty)
        - subtrees: The vertices that are adjacent to this vertex. This

    Representation Invariants:
        - self.item == 'and' or self.item == 'or' or
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
            self.item = 'and'
            self.subtrees = []
            for el in ors:
                self.subtrees.append(PrereqTree('/'.join(el)))
