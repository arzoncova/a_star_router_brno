# a_star_router_brno
A* router for finding an optimal path between two localities in Brno based on a profile preference. 

## / Motivation /
## The main goal of this project is to implement the A* algorithm to find an optimal path between
## two localities in Brno. While finding the optimal path, the program takes into account the user's
## preference of the route profile (flat, hilly, mountain).
##
## The current network is made of 16 nodes and serves intentionally as a proof of concept. Its goal is to
## verify graph symmetry and correctness of the A* algorithm. 
## It is not supposed to fulfill the role of real navigation at street level.


## / How it works /
## The road network is modeled as an undirected graph represented as a dictionary, where each key 
## represents a node. The list of each node defines its directly connected neighbours.
## Nodes are placed in a 2D Cartesian system with its origin at locality Prýgl [0, 0]. Distances
## do not correspond to reality and are just approximations. (1 unit in map is 100 metres in reality).
## The third element of each node is its elevation in meters above sea level.
##
## Correctness of the A* algorithm:
## To guarantee the optimality and completeness of A*, its heuristic function has to be admissible
## and consistent.
##
## - Admissibility:
## The heuristic function is set as the sum of the Euclidean distance from the current node to the goal 
## and a penalization of minimum guaranteed elevation gain, weighted by the user's ride profile.
## Because Euclidean distance is always the shortest path and the heuristic does not use negative 
## elevation difference, h(n) <= h*(n) is ensured. 
##
## - Consistency:
## Both Euclidean distance and elevation gained satisfy the triangle inequality (any node on path between 
## start and goal can only add distance or elevation gained), ensuring h(n) <= edge_cost(n, m) + h(m).
##

## not done yet: ##
##  The program also calculates an estimate of speed, overall work, and overall time of the ride, 
## based on the user's physiological parameters and elevation gained.
## Once the optimal route is found, the program calculates:
## - recommended power in watts based on the rider's weight and training zone.
## - estimated overall time of the ride and average speed.
## - overall work done in kJ.
