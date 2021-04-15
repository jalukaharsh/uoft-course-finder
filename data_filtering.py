"""
CSC111 Project: University of Toronto: Data Filtering

Module Description:
====================
The module contains the code that will filter the courses based on courses taken in the past,
breadth, department and level.
"""


from typing import List, Dict, Optional


def breadth(br: Optional[int], courses: Dict) -> Dict:
    """Return a list of course titles of all the courses that satisfy the br breadth requirement.
    """
    if br is None:
        return courses
    for course in courses:
        if str(br) not in courses[course]['arts_and_science_breadth']:
            courses.pop(course)
    return courses


def level(lev: Optional[int], courses: Dict) -> Dict:
    """Return a list of course titles of all the courses that are at the lvl level."""
    if lev is None:
        return courses
    for course in courses:
        if course[4] != str(lev):
            courses.pop(course)
    return courses


def department(dept: Optional[str], courses: Dict) -> Dict:
    """Return a list of course titles of all the courses that are from dept department. """
    if dept is None:
        return courses
    for course in courses:
        if courses[course]['department'] != dept:
            courses.pop(course)
    return courses


def filter_courses(courses: Dict, lvl: Optional[int], dept: Optional[str],
                   br: Optional[int]) -> Dict:
    """Return a dictionary that has all the courses filtered by the specified level, department
    and/or breadth requirement.
    """
    dict2 = courses.copy()
    breadth(br, dict2)
    level(lvl, dict2)
    department(dept, dict2)
    return dict2
