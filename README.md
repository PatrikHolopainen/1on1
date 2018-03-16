# 1on1
1on1 is a small Python project that uses the Networx library
## Problem
Given a directed no-self-looping network, how many ways are there to divide it so,
that every node has a an in- and out-degree of exactly 1?
## Motivation
This project started from a Secret Santa family tradition:
The grown-ups of a family decided that it would be too much effort to buy
presents to all other grown-ups, so they started a game that would reduce the
amount of presents bought.
### Rules of the game
1) For every participant another random participant is chosen.
2) Each participant buys a single present to their target.
3) Each participant can be a targt only once, thus everyone gets and gives exactly
one present
4) A participant can't buy a present to himself, or their husband/wife/partner
(as they are likely going to buy presents for each other anyway)
## How to Use
The network to be solved is used in the function takeTime()  
n: amount of nodes (positive int)  
p: degree distribution (float from range [0,1])  
If you want to generate a random network with n nodes and p degree distribution (1 == complete network),
use the method nx.gnp_random_graph(n,p,directed=True).  
You can also create a network by using the given createCompleteDi function by giving a list of nodes
AND a list of not allowed edges.    

To solve the network use solveGraph on the network of choice. (Runtime exceeds trivial time when  n>10)  
To calculate all possible solutions for a COMPLETE network of size n use function calculatePossibilities(n). (Analytical solution)  

You can run 1on1.py from a command line.
