"""CSC111 Project: University of Toronto Course Finder: Visualizing Graphs

Module Description:
===================
The module contains the code for visualizing graphs.
"""


from typing import Dict
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from future_graph import future
from data_formatting import get_courses_data
from prereq_graph import build_trace_graph

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
ROOT_COLOUR = 'rgb(89, 205, 105)'
OTHERS_COLOUR = 'rgb(105, 89, 205)'


def future_run(future_courses: Dict, course: str) -> None:
    """Return a visualization of the future graph of the given course."""
    graph = future(future_courses, course)
    draw_graph(graph)


def prereq_run(course: str) -> None:
    """Return a visualization of the prerequisites graph of the given course. """
    courses = get_courses_data()
    g = build_trace_graph(courses, course)
    draw_graph(g)


def draw_graph(graph: nx.Graph()) -> None:
    """Return a visual interactive representation of the input graph.
    """
    if nx.check_planarity(graph)[0]:
        # if graph is planar, use planar layout
        pos = getattr(nx, 'planar_layout')(graph)
    else:
        # kamada kawai layout
        df = pd.DataFrame(index=graph.nodes(), columns=graph.nodes())
        for row, data in nx.shortest_path_length(graph):
            for col, dist in data.items():
                df.loc[row, col] = dist
        df = df.fillna(df.max().max())
        pos = nx.kamada_kawai_layout(graph, dist=df.to_dict())

    # node coordinates
    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]
    # node values
    labels = list(node[1]['value'] for node in graph.nodes(data=True))
    # node colors
    colours = [ROOT_COLOUR if graph.nodes[k]['tag'] == 'original' else OTHERS_COLOUR
               for k in graph.nodes]
    # add nodes to diagram
    if len(labels) > 70:
        # if very high number of nodes, only show node markers
        mode = 'markers'
    else:
        # if low-ish number of nodes, display node value next to markers
        mode = 'markers+text'
    trace3 = go.Scatter(x=x_values,
                        y=y_values,
                        mode=mode,
                        name='nodes',
                        marker=dict(symbol='circle-dot',
                                    size=5,
                                    color=colours,
                                    line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                    ),
                        text=labels,
                        textposition='top right',
                        hovertemplate='%{text}',
                        hoverlabel={'namelength': 0}
                        )

    fig = go.Figure(data=[trace3])

    add_edges(graph, fig, pos)

    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def add_edges(graph: nx.DiGraph, fig: go.Figure, pos: dict) -> None:
    """Mutates fig to add all of graph's directed edges."""
    for edge in graph.edges:
        # choose color based on edge type
        color = 'red' if graph.get_edge_data(edge[0], edge[1])['edge_type'] == 'prereq' else 'blue'
        # add edge to diagram
        fig.add_annotation(
            x=pos[edge[1]][0],  # arrows' head
            y=pos[edge[1]][1],  # arrows' head
            ax=pos[edge[0]][0],  # arrows' tail
            ay=pos[edge[0]][1],  # arrows' tail
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            text='',  # if you want only the arrow
            showarrow=True,
            opacity=0.2,
            arrowhead=3,
            arrowsize=2,
            arrowwidth=1,
            arrowcolor=color
        )


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'plotly.graph_objects', 'future_graph', 'prereq_graph',
                          'data_formatting'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
