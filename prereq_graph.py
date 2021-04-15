import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple
from .data_formatting import PrereqTree


def convert_tree(tree: PrereqTree) -> Tuple[nx.Graph(), str]:
    g = nx.Graph()
    if tree.subtrees == []:
        g.add_node(tree.item, attr_dict={'type': 'course'})
    else:
        for subtree in tree.subtrees:
            converted_subtree, subtree_root = convert_tree(subtree)
            g = nx.compose(g, converted_subtree)
            # add edge from root of g to root of subtree
            edge_type = 'connective' if subtree_root in {'or', 'and'} else 'course'
            g.add_edge(tree.item, subtree_root, edge_type)
    return g, tree.item


def build_trace_graph(courses: Dict[str, Dict], course: str) -> Graph():
    """Returns the prereq/coreq trace subgraph of the given course."""
    prereq_tree = courses[course]['prereq_tree']
    coreq_tree = courses[course]['coreq_tree']
    AST = nx.compose(convert_tree(prereq_tree), convert_tree(coreq_tree))

    for vertex in list(AST.nodes):
        # recursive base case is when the only node in AST has course as its item
        if AST.data(vertex)['type'] == 'course' and vertex != course:
            prereq_AST = build_trace_graph(courses, vertex)
            AST = compose(AST, prereq_AST)
    return AST


def future_courses(courses, prereq: str) -> str:
    """Returns """
    future_courses = []
    for v in courses:
        if prereq in courses[v]['prerequisites']:
            future_courses.append(v)
    return str.join('\n', future_courses)


def draw_trace_graph(G: nx.Graph()) -> None:
    """Draws the given trace graph. Adds an event listener for clicks nodes that displays
    future courses."""
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos=pos, ax=ax)
    nx.draw_networkx_edges(G, pos=pos, ax=ax)

    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        node = ind["ind"][0]
        xy = pos[node]
        annot.xy = xy
        node_attr = {'node': node}
        node_attr.update(G.nodes[node])
        # add hover box stuff here
        text = future_courses(node)
        annot.set_text(text)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = nodes.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()
