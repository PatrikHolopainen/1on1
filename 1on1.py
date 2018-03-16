import networkx as nx
import matplotlib.pyplot as plt
import marshal
import hashlib
import math
import timeit

network = nx.DiGraph() #Create a directed graph

network.add_edges_from( #Add edges
    [
    ('1','2'),('1','3'),
    ('2','1'),('2','3'),
    ('3','1'),('3','2'),
    ('4','5'),('4','6'),
    ('5','4'),('5','6'),
    ('6','4'),('6','5'),
    ]
)

"""
createCompleteDi(nodes,remove)
Creates a complete network from given nodes and removes the given edges

INPUT
nodes: list of nodes (int)
remove: list of tuples of nodes (inte)
OUTPUT:
the created network (networkx.digraph)
"""
def createCompleteDi(nodes,remove=[]):
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

Uses a dictionary to store already calculated subgraphs in order to reduce runtime.

INPUT:
net: network (networkx.digraph)
OUTPUT:
amount of possible divisions (int)
"""
def solveGraph(net):
    nodes = net.nodes()
    netlen = len(net)
    solved = {}
    successors = {}
    for x in nodes:
        successors[x] = net.successors(x)

    def createCycles(start,availableNodes):
        def inner(node,available,chain):
            if(node == start):
                return solveSubGraph([n for n in available if n != node])
            elif(node not in available):
                return 0
            else:
                temp = 0
                for x in successors[node]:
                    chain1 = chain
                    chain1.append(x)
                    temp += inner(x,[n for n in available if n != node],chain1)
                return (temp)
        summedShit = 0
        for x in successors[start]:
            summedShit += inner(x,availableNodes,[x])
        return summedShit

    def marsh(r):
        m = marshal.dumps(r)
        return hashlib.md5(m).hexdigest()

    def solveSubGraph(availableNodes):
        n = len(availableNodes)
        if n == 0:
            return 1
        elif n == 1:
            return 0
        if marsh(availableNodes) in solved:
            return (solved[marsh(availableNodes)])
        else:
            startingNode = availableNodes[0]
            solved[marsh(availableNodes)] = createCycles(startingNode,availableNodes)

            return (solved[marsh(availableNodes)])

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
        if(k == 1):
            return 1
        else:
            return((k)*subtract(k-1)-(-1)**k)
    return(math.factorial(n)-subtract(n))

def takeTime():
    network = nx.gnp_random_graph(9,1,directed=True)
    print(solveGraph(network))

if __name__ == '__main__':
    print(timeit.timeit("takeTime()", setup="from __main__ import timeshit", number=1))
