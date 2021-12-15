import networkx as nx
import numpy as np

def _parse(rawdata):
    weights = np.array([[int(x) for x in line] for line in rawdata.splitlines()])
    graph = nx.grid_2d_graph(*weights.shape)
    return graph, weights

def part_1(graph, weights):
    r"""
    >>> part_1(*_parse('''\
    ... 1163751742
    ... 1381373672
    ... 2136511328
    ... 3694931569
    ... 7463417111
    ... 1319128137
    ... 1359912421
    ... 3125421639
    ... 1293138521
    ... 2311944581
    ... '''))
    40
    """
 
    shape = weights.shape
    path = nx.algorithms.dijkstra_path(graph, (0,0), (shape[0]-1,shape[1]-1), weight=lambda exit,enter,_: weights[enter])
    return sum(weights[n] for n in path[1:])

def part_2(graph, weights):
    r"""
    >>> part_2(*_parse('''\
    ... 1163751742
    ... 1381373672
    ... 2136511328
    ... 3694931569
    ... 7463417111
    ... 1319128137
    ... 1359912421
    ... 3125421639
    ... 1293138521
    ... 2311944581
    ... '''))
    315
    """
    weights = np.hstack([(weights + i)%9 for i in range(5)])
    weights = np.vstack([(weights + i)%9 for i in range(5)])
    weights[weights == 0] = 9
    shape = weights.shape
    graph = nx.grid_2d_graph(*shape)

    path = nx.algorithms.dijkstra_path(graph, (0,0), (shape[0]-1,shape[1]-1), weight=lambda exit,enter,_: weights[enter])
    return sum(weights[n] for n in path[1:])
