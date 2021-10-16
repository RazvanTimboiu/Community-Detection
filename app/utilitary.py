import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_adjacency_and_degrees(graph, zero_indexed=True):
    """
    Function to build adjacency matrix and degree vector from a list of nodes and edges.
    :param graph: object containing details about a graph (nodes, edges, etc.)
    :param zero_indexed: 'True' if nodes are indexed from zero, 'False' otherwise.
    :return: adjacency matrix and degree vector.
    """
    adjacency_matrix = [[0 for _ in graph.nodes] for _ in graph.nodes]
    degree_vector = [0 for _ in graph.nodes]

    if zero_indexed:
        for i, j in graph.edges:
            adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
            degree_vector[i] += 1
            degree_vector[j] += 1
    else:
        for i, j in graph.edges:
            adjacency_matrix[i - 1][j - 1] = adjacency_matrix[j - 1][i - 1] = 1
            degree_vector[i - 1] += 1
            degree_vector[j - 1] += 1

    return adjacency_matrix, degree_vector


def read_network_from_gml(file_path):
    """
    Utility function to read a network from a '.gml' file.
    :param file_path : path to '.gml'.
    :return: a dictionary containing details about the network (nodes, edges, adjacency matrix and degree vector)

    """
    graph = nx.read_gml(file_path, label='id')

    if 0 in graph.nodes():
        adjacency_matrix, degrees = get_adjacency_and_degrees(graph, zero_indexed=True)
    else:
        adjacency_matrix, degrees = get_adjacency_and_degrees(graph, zero_indexed=False)

    network = {'adjacency_matrix': adjacency_matrix,
               'degree_vector': degrees,
               'number_of_nodes': graph.number_of_nodes(),
               'number_of_edges': graph.number_of_edges()}

    return network


def normalize(values):
    """
    This function maps each element of a list to [0, n) where 'n' represents the number of unique values in that list.
    Ex : [93 5 5 13 13 6 13] where n = 4  -> [0 1 1 2 2 3 2]
    :param values : list of numbers
    :return: mappings list.
    """
    uniques = list(dict.fromkeys(values))
    mapping = [uniques.index(value) for value in values]
    return mapping


def colormap_builder(indices):
    """
    This function constructs a colormap for a network configuration.
    Nodes belonging to the same community will have the same color.
    :param indices: List of community labels for each node within the network.
    :return: list of colors corresponding to each node within the network.
    """
    colors = ['#66cdaa', '#00bfff', '#ffe4b5', '#da70d6', '#ff6347', '#d2b48c', '#9400d3', '#b6afaf', '#f0831d',
              '#8d7c9b', '#ffdead', '#f0ffff', '#ffc0cb', '#afeeee', '#008080', '#800000', '#9370db', '#ffffe0',
              '#008b8b', '#0000cd', '#ffe4c4', '#696969', '#cd5c5c', '#f4a460', '#dda0dd', '#bdb76b', '#a52a2a',
              '#4b0082', '#a9a9a9', '#f0e68c', '#add8e6', '#b0c4de', '#b0e0e6', '#ffebcd', '#e9967a', '#808000',
              '#00ffff', '#5f9ea0', '#6495ed', '#00008b', '#ff0000', '#fffacd', '#8b008b', '#ffb6c1', '#ff7f50',
              '#b22222', '#f5f5dc', '#800080', '#48d1cc', '#9966cc', '#d3d3d3', '#fff8dc', '#008000', '#ffd700',
              '#ff8c00', '#fffafa', '#000080', '#c0c0c0', '#87ceeb', '#ffa07a', '#ff00ff', '#d2691e', '#dcdcdc',
              '#a0522d', '#9932cc', '#0000ff', '#006400', '#6a5acd', '#ffffff']

    colormap = [colors[index] for index in indices]
    return colormap


def draw_configuration_layout(communities, network, layout, hold):
    """
    Function to visualise the community configuration in a network.
    :param communities : List of community labels for each node within the network.
    :param network : Network details (number of nodes / edges, adjacency matrix etc.)
    :param layout : Choice of layout between circular / spring.
    :param hold : 'True' if the plot holds for 5 seconds or 'False' if it closes after 1 second.
    :return: -
    """
    graph = nx.from_numpy_matrix(np.matrix(network["adjacency_matrix"]))

    labels = {}
    for node in graph.nodes():
        labels[node] = node + 1

    if layout == 1:
        pos = nx.circular_layout(graph)
    else:
        pos = nx.spring_layout(graph)

    colormap = colormap_builder(communities)

    plt.figure(figsize=(10, 10), facecolor='white')

    nx.draw_networkx_labels(graph, pos, labels, font_color='#000000')
    nx.draw_networkx_nodes(graph, pos, node_size=600, node_color=colormap, edgecolors='k')
    nx.draw_networkx_edges(graph, pos, alpha=0.3)

    if hold:
        try:
            plt.pause(5)
            plt.close()
        except:
            print("Drawing stopped")
    else:
        try:
            plt.pause(1)
            plt.close()
        except:
            print("Drawing stopped")


def modularity(genes, network):
    """
    This function computes the modularity for given gene configuration.
    :param genes : Community configuration
    :param network : Network configuration
    :return modularity value
    Reference : https://en.wikipedia.org/wiki/Modularity_(networks)
    """
    normalized = normalize(genes)
    no_nodes = network['number_of_nodes']
    adjacency = network['adjacency_matrix']
    degrees = network['degree_vector']
    no_edges = network['number_of_edges']

    m = 2 * no_edges
    q = 0.0
    for one in range(0, no_nodes):
        for two in range(0, no_nodes):
            if normalized[one] == normalized[two]:
                q += (adjacency[one][two] - degrees[one] * degrees[two] / m)
    return q / m


def save_network_configuration(filename, communities, network):
    """
    Function to save a network configuration as a drawing (.png)
    :param filename: Name of the file where to save.
    :param communities: Community configuration for a network.
    :param network: Object containing details about the network.
    :return:
    """
    graph = nx.from_numpy_matrix(np.matrix(network["adjacency_matrix"]))
    pos = nx.circular_layout(graph)

    labels = {}
    for node in graph.nodes():
        labels[node] = node

    colormap = colormap_builder(communities)

    plt.figure(figsize=(15, 15))

    nx.draw_networkx_labels(graph, pos, labels, font_color='#000000')
    nx.draw_networkx_nodes(graph, pos, node_size=600, node_color=colormap, edgecolors='k')
    nx.draw_networkx_edges(graph, pos, alpha=0.3)

    plt.savefig(filename)


def plot_evolution_over_time(value, label):
    """
    Function to plot a list of values with respect to time (1-n interval where 'n' represents the size of 'value')
    :param value: list of numerical values
    :param label: name that should represent what those values mean.
    :return:
    """
    plt.plot(value)
    plt.ylabel(label)
    plt.xlabel('Generation')
    plt.title('Evolution of ' + label)
    plt.show()
