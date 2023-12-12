from dfs_and_stuff import min_cost

depth = 4
costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
initial = [
    None, None,
    tuple("CDDA"), None,
    tuple("DBCD"), None,
    tuple("BABA"), None,
    tuple("BCAC"),
    None, None
]

print(f"at least p2 was ez after coding p1: {min_cost(initial, costs, depth)}")
