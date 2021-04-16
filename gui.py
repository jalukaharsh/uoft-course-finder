"""CSC111 Project: University of Toronto Course Finder: GUI

Module Description:
====================
The module contains the code for the graphical user interface.
"""

import tkinter as tk
from visualizing_graph import future_run
from data_formatting import get_courses_data
# from prereq_graph import prereq_run
from tkinter import ttk
from data_filtering import filter_courses


def run_app() -> None:
    """Run the application. """
    courses = get_courses_data()
    departments = list({courses[course]['department'] for course in courses})
    departments.sort()
    levels = ['100-level', '200-level', '300-level', '400-level']
    breadths = ['(1) Creative and Cultural Representation',
                '(2) Thought, Belief and Behaviour',
                '(3) Society and its Institutions',
                '(4) Living Things and Their Environment',
                '(5) The Physical and Mathematical Universes']

    def retrieve() -> None:
        """Ran whenever 'Search' button is clicked on the main screen. """
        br = breadth_list.get()
        lvl = level_list.get()
        lvl = lvl[0]
        department = dept_filter.get()
        future_courses_dict = filter_courses(courses, lvl, department, br)

        newroot = tk.Tk()
        newroot.geometry("300x100")

        newframe = tk.Frame(newroot)
        newframe.pack()

        if course_input.get() in courses:
            prereq_button = tk.Button(newframe, text="Prerequisite Graph",
                                      # command=lambda: prereq_run(course_input.get())
                                      )
            prereq_button.pack(side=tk.LEFT, padx=5, pady=20)

            future_button = tk.Button(newframe, text="Future Graph",
                                      command=lambda: future_run(future_courses_dict,
                                                                 course_input.get()))
            future_button.pack(padx=5, pady=20)
        else:
            show_error = tk.Label(newframe, text='Sorry, no such course exists in the database. '
                                                 'Please type the course code exactly as it would '
                                                 'appear on the academic calendar.', wraplength=250,
                                  justify=tk.CENTER, pady=20)
            show_error.pack()

    root = tk.Tk()
    root.geometry("300x200")

    frame = tk.Frame(root)
    frame.pack()

    var = tk.StringVar()
    var.set("Course code:")

    label = tk.Label(frame, textvariable=var, pady=5)
    label.pack()

    course_input = tk.Entry(frame, width=20)
    course_input.pack(padx=5, pady=5)

    advanced = tk.StringVar()
    advanced.set("Advanced filters (for the future graph):")

    advanced_filters = tk.Label(frame, textvariable=advanced, pady=5)
    advanced_filters.pack()

    breadth_list = ttk.Combobox(frame, values=list(breadths), width=40)
    breadth_list.set('Pick a breadth category')
    breadth_list.pack()

    level_list = ttk.Combobox(frame, values=list(levels), width=40)
    level_list.set('Pick a level')
    level_list.pack()

    dept_filter = ttk.Combobox(frame, values=list(departments), width=40)
    dept_filter.set('Pick a department')
    dept_filter.pack()

    search_button = tk.Button(frame, text="Search", command=retrieve)
    search_button.pack(padx=5, pady=10)

    root.mainloop()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'data_formatting', 'data_filtering', 'visualizing_graph'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
