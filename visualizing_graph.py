"""CSC111 Project: University of Toronto Course Finder: Data Filtering

Module Description:
===================
The module contains the code for visualizing graphs.
"""
from typing import Dict
import networkx as nx
import plotly.graph_objects as go
from future_graph import future


LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
ROOT_COLOUR = 'rgb(89, 205, 105)'
OTHERS_COLOUR = 'rgb(105, 89, 205)'


def draw_graph(graph: nx.Graph(), layout: str = 'spring_layout') -> None:
    """Return a visual interactive representation of the input graph.
    """
    pos = getattr(nx, layout)(graph)

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]
    labels = list(graph.nodes)

    colours = [ROOT_COLOUR if graph.nodes[k]['tag'] == 'original' else OTHERS_COLOUR
               for k in graph.nodes]

    x_edges = []
    y_edges = []
    for edge in graph.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = go.Scatter(x=x_edges,
                        y=y_edges,
                        mode='lines',
                        name='edges',
                        line=dict(color=LINE_COLOUR, width=1),
                        hoverinfo='none',
                        )

    trace4 = go.Scatter(x=x_values,
                        y=y_values,
                        mode='markers',
                        name='nodes',
                        marker=dict(symbol='circle-dot',
                                    size=5,
                                    color=colours,
                                    line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                    ),
                        text=labels,
                        hovertemplate='%{text}',
                        hoverlabel={'namelength': 0}
                        )

    data1 = [trace3, trace4]
    fig = go.Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def draw_graph_prereq(graph: nx.Graph(), layout: str = 'spring_layout') -> None:
    """Return a visual interactive representation of the input graph.
    """
    pos = getattr(nx, layout)(graph)

    x_values = [pos[k][0] for k in graph.nodes]
    y_values = [pos[k][1] for k in graph.nodes]
    labels = list(graph.nodes)

    x_edges = []
    y_edges = []
    for edge in graph.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = go.Scatter(x=x_edges,
                        y=y_edges,
                        mode='lines',
                        name='edges',
                        line=dict(color=LINE_COLOUR, width=1),
                        hoverinfo='none',
                        )

    trace4 = go.Scatter(x=x_values,
                        y=y_values,
                        mode='markers',
                        name='nodes',
                        marker=dict(symbol='circle-dot',
                                    size=5,
                                    line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                    ),
                        text=labels,
                        hovertemplate='%{text}',
                        hoverlabel={'namelength': 0}
                        )

    data1 = [trace3, trace4]
    fig = go.Figure(data=data1)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    fig.show()


def future_run(courses: Dict, course: str) -> None:
    """Return a visualization of the future graph of the given course. """
    graph = future(courses, course)
    draw_graph(graph)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['networkx', 'plotly.graph_objects', 'future_graph'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
