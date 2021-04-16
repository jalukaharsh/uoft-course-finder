"""CSC111 Project: University of Toronto Course Finder: GUI

Module Description:
====================
The module contains the class PrereqTree, which is used to parse Prerequisite strings.
"""
from __future__ import annotations
import re


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

        split_str = combine_parentheses(split_str)

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


def combine_parentheses(split_str: list[str]) -> list[str]:
    """Takes a tokenized prereq string and combines each parenthetical
    into a single string (which is later recursed on)
    """
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

    return split_str
