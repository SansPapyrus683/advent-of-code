import re

Path = tuple[str, ...]

P1_SIZE_REQ = 100000
TOTAL_SIZE = 70000000
FREE_SPACE_REQ = 30000000


def dir_size(dir_: Path, tree: dict[Path, list[tuple[str, str]]]) -> int:
    total_size = 0
    for f in tree[dir_]:
        total_size += dir_size(dir_ + (f[1],), tree) if f[0] == "dir" else int(f[0])
    return total_size


prompt = "$"
cd_fmt = fr"\{prompt} cd (.+)"
ls_fmt = fr"\{prompt} ls"
structure = {}
curr_folder = []
curr_path = ["/"]
with open("taken_flight.txt") as read:
    for l in read.readlines()[1:]:  # exclude the initial cd
        if re.match(cd_fmt, l) is not None:
            if curr_path and tuple(curr_path) not in structure:
                structure[tuple(curr_path)] = curr_folder
                curr_folder = []

            new = re.findall(cd_fmt, l)[0]
            if new == "..":
                curr_path.pop()
            else:
                curr_path.append(new)
        elif re.match(ls_fmt, l) is not None:
            continue
        else:
            attr1, attr2 = l.split()
            curr_folder.append((attr1, attr2))

if curr_path and tuple(curr_path) not in structure:
    structure[tuple(curr_path)] = curr_folder

p1_total_size = 0
p2_min_size = float('inf')
p2_req_size = FREE_SPACE_REQ - (TOTAL_SIZE - dir_size(("/",), structure))
for path in structure:
    size = dir_size(path, structure)
    if size <= P1_SIZE_REQ:
        p1_total_size += size
    if size >= p2_req_size:
        p2_min_size = min(p2_min_size, size)

print(f"i'm scared: {p1_total_size}")
print(f"i got top 20 for this day both times: {p2_min_size}")
