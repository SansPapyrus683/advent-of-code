from dfs_and_stuff import min_cost

depth = 2
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
# for how this works go to that module, dfs_and_stuff
initial = [
    None, None,
    tuple("CA"), None,
    tuple("DD"), None,
    tuple("BA"), None,
    tuple("BC"),
    None, None
]

print(f"bro how did people solve this by hand: {min_cost(initial, costs, depth)}")
