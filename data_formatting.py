"""CSC111 Project: University of Toronto Course Finder: Data Formatting

Module Description:
====================
The module contains the function that processes the raw data file into list of courses, with each
course represented as a dictionary.
"""
from __future__ import annotations
import json
from typing import Any
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
        - kind matches this regex \\A(?:(?:[A-Z]{3}[0-9]{3}[H,Y]1)|(?:or)|(?:and))\\Z
    """
    kind: str
    subtrees: PrereqTree
    
    __init__(self, prereq_str: str) -> None:
    
    



class _CoursesVertex:
    """A vertex in a the CourseGraph representing a course
     
     Attributes:
        - item: A course code
        - prerequisites: A PrereqTree representing the prerequisites of the course
        - corequisites: A PrereqTree representing the corequisites of the course
    """
    item: Any
    prerequisites: PrereqTree
    corequisites: PrereqTree
