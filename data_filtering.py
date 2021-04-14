"""
CSC111 Project: University of Toronto: Data Filtering

Module Description:
====================
The module contains the code that will filter the courses based on courses taken in the past,
breadth, department and level.
"""

from typing import List, Dict
course_dict = {}  # the dictionary of courses


def course_info(course_code: str) -> Dict:
    """Return all the course details of a given course."""
    return course_dict[course_code]


def breadth(br: int) -> List:
    """Return a list of course titles of all the courses that satisfy the br breadth requirement.
    """
    lst = []
    for course in course_dict:
        if str(br) in course_dict[course]['arts_and_science_breadth']:
            lst.append(course)
    return lst


def level(lev: int) -> List:
    """Return a list of course titles of all the courses that are at the lvl level."""
    lst = []
    for course in course_dict:
        if course[4] == str(lev):
            lst.append(course)
    return lst


def department(dept: str) -> List:
    """Return a list of course titles of all the courses that are from dept department. """
    lst = []
    for course in course_dict:
        if course_dict[course]['department'] == dept:
            lst.append(course)
    return lst
