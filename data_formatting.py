"""CSC111 Project: University of Toronto Course Finder: Data Formatting

Module Description:
====================
The module contains the function that processes the raw data file into list of courses, with each
course represented as a dictionary.
"""
from __future__ import annotations
import json
from typing import Any, Optional
import re


def get_courses_data() -> dict:
    """gets course data from file"""
    json_data = open('courses.json')
    data = json.load(json_data)
    data_dict = {}
    for course in data:
        data_dict[course['code']] = course

    return data_dict


class PrereqTree:
    """tree representing prequisites
    Instance Attributes:
        - kind: the type of the tree. It can be 'or' or 'and' or a string of the form
            /[A-Z]{3}[0-9]{3}[H,Y]1/ (in which case it is a root and subtrees is empty)
        - subtrees: The vertices that are adjacent to this vertex. This

    Representation Invariants:
        - item is 'and' or 'or' or of the form [A-Z]{3}[0-9]{3}[H,Y]1
    """
    item: str
    subtrees: Optional[list[PrereqTree]]

    def __init__(self, prereq_str: str) -> None:
        # remove all whitespace
        prereq_str = re.sub(r'\s+', prereq_str)
        prereq_str = prereq_str.replace(';', ',')

        # deal base case of prereq_str being just a single course:
        if re.fullmatch(r'[A-Z]{3}[0-9]{3}[H,Y]1', prereq_str) is not None:
            self.item = prereq_str
            self.subtrees = None
            return

        # tokenize the prereq string into the form of courses, commas,
        # forward slashes and parentheses
        split_str = re.findall(r'(?:(?:[A-Z]{3}[0-9]{3}[H,Y]1)|[/,\,, (, )])')

        # combine each parenthetical into a single string (which we will later recurse on)
        while '(' in split_str:
            first_paren = split_str.index('(')
            nest = 1
            length = 1
            while nest >= 1:
                i = length + first_paren
                char = split_str[i]
                if char == '(':
                    nest += 1
                elif char == ')':
                    nest -= 1

                length += 1
            
            # join the parenthesized string
            parenthesized_str = ''.join(split_str[first_paren:first_paren + length])
            
            if re.search(r'[A-Z]{3}[0-9]{3}[H,Y]1', parenthesized_str) is None:
                # if the parenthesized string includes no course codes then we remove it
                split_str = split_str[0: first_paren] + split_str[first_paren + length:]
            else:
                split_str = split_str[0: first_paren] + [parenthesized_str] + \
                            split_str[first_paren + length:]

        ors = []  # list of each or(/) block. if longer than one then
        current = []
        for i in range(0, len(split_str)):
            char = split_str[i]
            if char == ',':
                ors.append(current)
                current = []
            elif char != '/':
                current.append(char)

        if current != '':
            ors.append(current)

        if len(ors) == 1:
            self.item = 'or'
            self.subtrees = []
            for el in ors[0]
                self.subtrees.append(PrereqTree(el))
        else:
            self.item = 'and'
            self.subtrees = []
            for el in ors:
                self.subtrees.append(PrereqTree(el))
