"""Code for GUI. """

import tkinter as tk
from tkinter import ttk
from visualizing_graph import future_run
from data_formatting import get_courses_data

courses = get_courses_data()


def retrieve() -> None:
    """Ran whenever 'Search' button is clicked on the main screen. """
    newroot = tk.Tk()
    newroot.geometry("300x100")

    newframe = tk.Frame(newroot)
    newframe.pack()

    if course_input.get() in courses:
        prereq_button = tk.Button(newframe, text="Prerequisite Graph")  # TODO: Add command
        prereq_button.pack(side=tk.LEFT, padx=5, pady=20)

        future_button = tk.Button(newframe, text="Future Graph", command=lambda: future_run(course_input.get()))
        future_button.pack(padx=5, pady=20)
    else:
        show_error = tk.Label(newframe, text='Sorry, no such course exists in the database. '
                                            'Please type the course code exactly as it would appear '
                                            'on the academic calendar.', wraplength=250,
                              justify=tk.CENTER, pady=20)
        show_error.pack()


root = tk.Tk()
root.geometry("600x450")

frame = tk.Frame(root)
frame.pack()

var = tk.StringVar()
var.set("Course code:")

label = tk.Label(frame, textvariable=var, pady=5)
label.pack()

course_input = tk.Entry(frame, width=20)
course_input.pack(padx=5, pady=5)

Button = tk.Button(frame, text="Search", command=retrieve)
Button.pack(padx=5, pady=5)

root.mainloop()
