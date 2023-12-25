import networkx as nx

with open("the_snowman.txt") as read:
    components = nx.Graph()
    for w in read.readlines():
        name, other = w.split(":")
        name = name.strip()
        for ow in other.split():
            components.add_edge(name, ow, capacity=1)

to_cut = nx.minimum_edge_cut(components)
for w1, w2 in to_cut:
    components.remove_edge(w1, w2)

group1, group2 = nx.connected_components(components)
sz_prod = len(group1) * len(group2)
print(f"crap i can never seem to finish the songs: {sz_prod}")
