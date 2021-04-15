"""
CSC111 Project: University of Toronto: Data Filtering

Module Description:
====================
The module contains the code that will filter the courses based on courses taken in the past,
breadth, department and level.
"""

from typing import Dict, Optional


def breadth(br: str, courses: Dict) -> Dict:
    """Return a list of course titles of all the courses that satisfy the br breadth requirement.
    """
    if br == 'Pick a breadth category' or br == '':
        return courses
    new_courses = {}
    for course in courses:
        if courses[course]['arts_and_science_breadth'] is not None and \
                br in courses[course]['arts_and_science_breadth']:
            new_courses[course] = courses[course]
    return new_courses


def level(lev: str, courses: Dict) -> Dict:
    """Return a list of course titles of all the courses that are at the lvl level."""
    if lev == 'Pick a level' or lev == '':
        return courses
    new_courses = {}
    for course in courses:
        if course[3] == str(lev):
            new_courses[course] = courses[course]
    return new_courses


def department(dept: str, courses: Dict) -> Dict:
    """Return a list of course titles of all the courses that are from dept department. """
    if dept == 'Pick a department' or dept == '':
        return courses
    new_courses = {}
    for course in courses:
        if courses[course]['department'] != dept:
            new_courses[course] = courses[course]
    return new_courses


def filter_courses(courses: Dict, lvl: str, dept: str, br: str) -> Dict:
    """Return a dictionary that has all the courses filtered by the specified level, department
    and/or breadth requirement.
    """
    course1 = breadth(br, courses)
    course2 = level(lvl, course1)
    course3 = department(dept, course2)
    return course3
