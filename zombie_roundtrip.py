#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 2025

@author: ruixu
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =====================================================
# Import packages
# =====================================================
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import math

# =====================================================
# Define locations (nodes) and coordinates
# =====================================================
locations = {
    "Bunker": (0, 100),
    "Grocers1": (200, 600),
    "Pharmacy": (450, 600),
    "Hospital": (550, 400),
    "Grocery2": (950, 400),
    "GasStation": (450, 200),
    "A": (0,0),
    "B": (0,200),
    "C": (200, 0),
    "D": (200, 200),
    "E": (200, 400),
    "F": (200, 500),
    "G": (200, 700),
    "H": (450, 0),
    "I": (450, 400),
    "J": (450, 500),
    "K": (450, 700),
    "L": (650, 0),
    "M": (650, 400),
    "N": (650, 600),
    "O": (650, 700),
    "P": (950, 600)
}

# =====================================================
# Define edges (roads)
# =====================================================
edges = [
    ("Bunker", "A"), ("Bunker", "B"),
    ("A", "C"), ("B", "D"), ("C", "D"), ("C", "H"),
    ("D", "E"), ("E", "I"), ("E", "F"), ("F", "J"),
    ("F", "Grocers1"), ("Grocers1", "G"), ("G", "K"),
    ("K", "O"), ("K","Pharmacy"), ("Pharmacy", "N"),
    ("Pharmacy", "J"), ("J", "I"), ("Hospital", "M"),
    ("I", "Hospital"), ("I", "GasStation"),
    ("GasStation", "H"), ("H", "L"), ("L", "M"),
    ("M", "Grocery2"), ("Grocery2", "P"),
    ("P", "N"), ("N", "M"), ("N", "O")
]

# =====================================================
# Build graph
# =====================================================
G = nx.Graph()
for node, pos in locations.items():
    G.add_node(node, pos=pos)
G.add_edges_from(edges)

# Assign Manhattan distance as edge weight
pos = nx.get_node_attributes(G, 'pos')
for u, v in G.edges():
    G[u][v]['weight'] = abs(pos[u][0] - pos[v][0]) + abs(pos[u][1] - pos[v][1])

# =====================================================
# Visualize map
# =====================================================
plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_size=480, node_color="#AEDFF7", font_size=8, font_weight="bold")
plt.title("Map of the Town")
plt.axis("equal")
plt.show()

# =====================================================
# Shortest Path Solver (Round Trip)
# =====================================================
required_fixed = ["Pharmacy", "Hospital", "GasStation"]
grocers = ["Grocers1", "Grocery2"]
start = "Bunker"

# Precompute shortest paths
sp_len = dict(nx.all_pairs_dijkstra_path_length(G, weight="weight"))
sp_path = dict(nx.all_pairs_dijkstra_path(G, weight="weight"))

def best_path_for_choice(chosen_grocer):
    """
    Evaluate all permutations of required stops including chosen grocery,
    and return to the Bunker (round trip).
    """
    terminals = [start] + required_fixed + [chosen_grocer]
    best = {"order": None, "dist": math.inf, "full_path": None}
    
    for perm in itertools.permutations([t for t in terminals if t != start]):
        order = (start,) + perm + (start,)  # return to Bunker
        dist = sum(sp_len[order[i]][order[i+1]] for i in range(len(order)-1))
        
        if dist < best["dist"]:
            full = []
            for i in range(len(order)-1):
                seg = sp_path[order[i]][order[i+1]]
                if i == 0:
                    full.extend(seg)
                else:
                    full.extend(seg[1:])
            best = {"order": order, "dist": dist, "full_path": full}
    
    return best

# =====================================================
# Evaluate both grocery options
# =====================================================
best_overall = None
chosen_grocer = None

for g in grocers:
    candidate = best_path_for_choice(g)
    if best_overall is None or candidate["dist"] < best_overall["dist"]:
        best_overall = candidate
        chosen_grocer = g

# =====================================================
# Print results
# =====================================================
print("===================================================")
print("Zombie Apocalypse Optimal Route (Round Trip)")
print("===================================================")
print(f"Chosen Grocery: {chosen_grocer}")
print(f"Visit Order: {' -> '.join(best_overall['order'])}")
print(f"Total Manhattan Distance (Round Trip): {best_overall['dist']}")
print("\nStreet-by-Street Path:")
print(" -> ".join(best_overall["full_path"]))
print("===================================================")

# =====================================================
# Visualize Optimal Route
# =====================================================
plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_size=480, node_color="#CFE8FF", font_size=8, font_weight="bold")
path_edges = list(zip(best_overall["full_path"][:-1], best_overall["full_path"][1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")
terminal_nodes = set(best_overall["order"])
node_colors = ["#FFD166" if n in terminal_nodes else "#CFE8FF" for n in G.nodes()]
nx.draw_networkx_nodes(G, pos, nodelist=list(G.nodes()), node_color=node_colors, node_size=520)
plt.title("Optimal Round Trip Route Highlighted on the Map")
plt.axis("equal")
plt.show()
