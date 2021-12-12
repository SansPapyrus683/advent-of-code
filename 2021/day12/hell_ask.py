from collections import defaultdict

START = "start"
END = "end"


def path_num_p1(adj: {str: [str]}) -> int:
    all_paths = set()

    def get_all_paths(at: str, path: [str]):
        for n in adj[at]:
            if n == END:
                all_paths.add(tuple(path + [END]))
            elif n.isupper() or n.islower() and n not in path:
                path.append(n)
                get_all_paths(n, path)
                path.pop()

    get_all_paths(START, [START])
    return len(all_paths)


def path_num_p2(adj: {str: [str]}) -> int:
    all_paths = set()

    def get_all_paths(at: str, path: [str], vis_small_twice: bool):
        for n in adj[at]:
            if n == END:
                all_paths.add(tuple(path + [END]))
            elif n.isupper():
                path.append(n)
                get_all_paths(n, path, vis_small_twice)
                path.pop()
            elif n.islower():
                presence = path.count(n)
                if presence == 0:
                    path.append(n)
                    get_all_paths(n, path, vis_small_twice)
                    path.pop()
                elif presence == 1 and not vis_small_twice:
                    path.append(n)
                    get_all_paths(n, path, True)
                    path.pop()

    get_all_paths(START, [START], False)
    return len(all_paths)


neighbors = defaultdict(list)
with open("you_married.txt") as read:
    for i in read.readlines():
        s, e = i.strip().split('-')
        neighbors[s].append(e)
        neighbors[e].append(s)

for n_list in neighbors.values():
    # make it so we can't go back to the start
    if START in n_list:
        n_list.remove(START)

print(f"bruh why do we have to find all the paths: {path_num_p1(neighbors)}")
print(f"i will hate small caves for my entire life now: {path_num_p2(neighbors)}")
