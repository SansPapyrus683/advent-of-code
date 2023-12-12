P2_KEY = 811589153
P2_MIX_AMT = 10


def mix(arr: list[tuple[int, int]]) -> None:
    for i in range(len(arr)):
        for v, (j, delta) in enumerate(arr):
            if j == i:
                new_pos = (v + delta) % (len(arr) - 1)
                del arr[v]
                arr.insert(new_pos, (j, delta))
                break


def coord_sum(arr: list[tuple[int, int]]) -> int | None:
    for i in range(len(arr)):
        if arr[i][1] == 0:
            a = (i + 1000) % len(arr)
            b = (i + 2000) % len(arr)
            c = (i + 3000) % len(arr)
            return arr[a][1] + arr[b][1] + arr[c][1]
    return None


with open("could_be_holy.txt") as read:
    file = [(v, int(i)) for v, i in enumerate(read.readlines())]

p1_file = file.copy()
mix(p1_file)
print(f"god the indexing in this problem was so a**: {coord_sum(p1_file)}")

p2_file = [(v, i * P2_KEY) for v, i in file]
for _ in range(P2_MIX_AMT):
    mix(p2_file)
print(f"you were supposed to mod by the len - 1, not the len: {coord_sum(p2_file)}")
