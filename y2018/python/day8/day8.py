def parse_tree(tree: list[int]) -> tuple[int, dict[int, int]]:
    total_metadata = 0
    at = 0
    values = {}
    node_at = 0

    def actually_parse_tree() -> int:
        nonlocal total_metadata, at, values, node_at

        child_num, meta_num = tree[at], tree[at + 1]
        at += 2

        children = []
        node = node_at
        values[node] = 0
        node_at += 1
        for _ in range(child_num):
            children.append(actually_parse_tree())

        for _ in range(meta_num):
            total_metadata += tree[at]
            if not children:
                values[node] += tree[at]
            elif 0 < tree[at] <= len(children):
                values[node] += values[children[tree[at] - 1]]
            at += 1
        return node

    actually_parse_tree()
    return total_metadata, values


nodes = [int(i) for i in open('day8.txt').readline().split()]
metadata, node_vals = parse_tree(nodes)
print(f"metadata sum: {metadata}")
print(f"value of root: {node_vals[0]}")
