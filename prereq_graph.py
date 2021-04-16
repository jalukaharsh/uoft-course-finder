"""Code to build the prerequisities graph. """

import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple, Dict
from data_formatting import get_courses_data


def build_trace_graph(courses: Dict[str, Dict], course: str) -> nx.DiGraph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    prereq_tree = courses[course]['prereq_tree']
    coreq_tree = courses[course]['coreq_tree']
    AST = nx.compose_all([tree for tree in [prereq_tree, coreq_tree, nx.DiGraph()]
                          if tree is not None])
    for vertex in AST.nodes(data=True):
        # recursive base case is when the only node in AST has course as its item
        if vertex[1]['type'] == 'course' and vertex[0] != course:
            prereq_AST = build_trace_graph(courses, vertex[0])
            AST = nx.compose(AST, prereq_AST)
    return AST


# def future_courses(courses, prereq: str) -> str:
#     """Returns """
#     future_courses = []
#     for v in courses:
#         if prereq in courses[v]['prerequisites']:
#             future_courses.append(v)
#     return str.join('\n', future_courses)
#
#
# def draw_trace_graph(G: nx.Graph(), courses: Dict[str, dict]) -> None:
#     """Draws the given trace graph. Adds an event listener for clicks nodes that displays
#     future courses."""
#     fig, ax = plt.subplots()
#     pos = nx.spring_layout(G)
#     nodes = nx.draw_networkx_nodes(G, pos=pos, ax=ax)
#     nx.draw_networkx_edges(G, pos=pos, ax=ax)
#
#     annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
#                         bbox=dict(boxstyle="round", fc="w"),
#                         arrowprops=dict(arrowstyle="->"))
#     annot.set_visible(False)
#
#     def update_annot(ind):
#         node = ind["ind"][0]
#         xy = pos[node]
#         annot.xy = xy
#         node_attr = {'node': node}
#         node_attr.update(G.nodes[node])
#         # add hover box stuff here
#         text = future_courses(courses, node)
#         annot.set_text(text)
#
#     def hover(event):
#         vis = annot.get_visible()
#         if event.inaxes == ax:
#             cont, ind = nodes.contains(event)
#             if cont:
#                 update_annot(ind)
#                 annot.set_visible(True)
#                 fig.canvas.draw_idle()
#             else:
#                 if vis:
#                     annot.set_visible(False)
#                     fig.canvas.draw_idle()
#
#     fig.canvas.mpl_connect("motion_notify_event", hover)
#     plt.show()


def prereq_run(course: str) -> None:
    """Return a visualization of the prerequisites graph of the given course. """
    courses = get_courses_data()
    g = build_trace_graph(courses, course)
    # print(g.nodes)
    from visualizing_graph import draw_graph_prereq
    draw_graph_prereq(g)


if __name__ == '__main__':
    prereq_run('CSC240H1')
