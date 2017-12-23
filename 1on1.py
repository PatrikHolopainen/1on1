import networkx as nx
import matplotlib.pyplot as plt
import marshal
import hashlib
import math

network = nx.DiGraph()

network.add_edges_from(
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
people = [
    "Anna",
    "Olli",
    "Pekka",
    "Outi",
    "Vesa",
    "Amy",
    "IÄ",
    "Ukki",
    "Laura",
    "Maria",]
notOkay = [
    ("Pekka","Outi"),
    ("Outi","Pekka"),
    ("Vesa","Amy"),
    ("Amy","Vesa"),
    ("IÄ","Ukki"),
    ("Ukki","IÄ"),
    ("Laura","Maria"),
    ("Maria","Laura"),
]
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

def solveGraph(net):
    nodes = net.nodes()
    netlen = len(net)
    solved = {}
    successors = {}
    for x in nodes:
        successors[x] = net.successors(x)

    def marsh(r):
        m = marshal.dumps(r)
        return hashlib.md5(m).hexdigest()

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

    def solveSubGraph(availableNodes):
        #print(len(solved))
        n = len(availableNodes)
        if n == 0:
            return 1
        elif n == 1:
            return 0
        if marsh(availableNodes) in solved:
            return (solved[marsh(availableNodes)])
        else:
            startingNode = availableNodes[0]
            #solved[marsh(availableNodes)] = 1 Test purposes
            solved[marsh(availableNodes)] = createCycles(startingNode,availableNodes)

            return (solved[marsh(availableNodes)])

    return solveSubGraph(nodes)




def drawNet(net):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    nx.draw_circular(net,with_labels=True)
    plt.show()

def timeshit():
    network = nx.gnp_random_graph(10,1,directed=True)
    networks = []
    for i in range(1,10):
        networks.append(nx.gnp_random_graph(i,1,directed=True))
    for x in networks:
        print(solveGraph(x))

def calculatePossibilities(n): #Calculates the amount of possible ways to do the draw from a complete network of size n.
    def subtract(k):
        if(k == 1):
            return 1
        else:
            return((k)*subtract(k-1)-(-1)**k)
    return(math.factorial(n)-subtract(n))

if __name__ == '__main__':
    import timeit
    #print(timeit.timeit("timeshit()", setup="from __main__ import timeshit", number=1))
    print(calculatePossibilities(100))
