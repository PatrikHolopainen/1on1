import networkx as nx
import matplotlib.pyplot as plt
import math
import timeit

"""
createDi(nodes,remove)
Creates a complete network from given nodes and REMOVES the given edges

INPUT
nodes: list of nodes (int)
remove: list of tuples of nodes (inte)
OUTPUT:
the created network (networkx.digraph)
"""
def createDi(nodes,remove=[]):
    net = nx.DiGraph()
    for x in nodes:
        for y in nodes:
            if x != y:
                net.add_edge(x,y)
    for x in remove:
        net.remove_edge(x[0],x[1])
    return net


"""
solveGraph(net)
Given a valid network recursively goes through all possible ways of removing
links in a way that every node ends up with exactly one in and exactly one out
link, without self-links.

Uses a dictionary to store already calculated subgraphs in order to reduce
runtime.

Currently a pretty slow runtime

INPUT:
net: network (networkx.digraph)
OUTPUT:
amount of possible divisions (int)
"""

def solveGraph(net):

    nodes = list(net.nodes())
    n = len(net)
    #print("Length of net:",n)
    solvedGraphs = {}

    def solveSubGraph(nodes):
        """
        There are three cases that this function solves. When the amount of
        nodes == 0, the algorithm has come to a point where there are no nodes
        left to check.
        """

        if len(nodes) == 0:
            # This is not possible, since you can't give a present to yourself
            return 1

        elif len(nodes) == 1:
            # This means that everyone has been dealt a present, hooray!
            return 0

        else:
            # Create a unique key out of available nodes
            t = tuple(nodes) #TODO is sorted needed?

            # If t is a key of solved, return the value directly

            if t in solvedGraphs:
                #print("Found in solvedGraphs")
                return solvedGraphs[t]


            # If t is not a key
            else:
                solvedGraphs[t] = startCycle(nodes)
                return solvedGraphs[t]

    def startCycle(nodes):
        start_node = nodes[0]

        def inner(node,availableNodes,chain):
            successors = net.successors(node)
            if len(chain) > 0 and node == start_node:
                return solveSubGraph([n for n in availableNodes if n not in chain])

            return sum([inner(successor,[an for an in availableNodes if an != successor],chain+[successor]) for successor in successors if successor in availableNodes])

        return inner(start_node,nodes,[])

    return solveSubGraph(nodes)

"""
drawNet(net)
Draws the given network

INPUT:
net: network (networkx.digraph)
"""
def drawNet(net):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    nx.draw_circular(net,with_labels=True)
    plt.show()


"""
calculatePossibilities(n)
Calculates the amount of possible ways to do the draw from a complete network of size n.

INPUT:
n: amount of nodes (int)
OUTPUT:
amonut of possible divisions (int)
"""
def calculatePossibilities(n):
    def subtract(k):
        if k == 0:
            return 0
        elif k== 1:
            return 1
        else:
            return((k)*subtract(k-1)-(-1)**k)

    n_total = math.factorial(n)-subtract(n)

    return n_total


def takeTime():
    # Set n to change the amount of nodes in a network
    n = 10
    network = nx.gnp_random_graph(n,1,directed=True)
    algorithm = solveGraph(network)
    formula = calculatePossibilities(n)

    print("Algorithm matches formula when n = {:d}: {}".format(n,algorithm==formula))
    print("Algorithm: {:d}".format(algorithm))
    print("Formula:   {:d}".format(formula))




if __name__ == '__main__':
    print("Runtime:",timeit.timeit("takeTime()", setup="from __main__ import takeTime", number=1))


#print(calculatePossibilities(4))
