class Cube:
    def __init__(self, x: (int, int), y: (int, int), z: (int, int)) -> None:
        for i in [x, y, z]:
            assert len(i) == 2 and i[0] <= i[1], "invalid range you mongrel"
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def bounds(self) -> ((int, int), (int, int), (int, int)):
        return self.x, self.y, self.z

    @property
    def volume(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.y[1] - self.y[0] + 1)
            * (self.z[1] - self.z[0] + 1)
        )

    # got this from some guy i forgot on discord
    def overlaps(self, other: "Cube") -> bool:
        return not any(
            a[1] < b[0] or b[1] < a[0]
            for a, b in zip(self.bounds, other.bounds)
        )

    # got this unholy code from some guy named mustafa on discord
    def make_hole(self, other: "Cube") -> ["Cube"]:
        max_x1 = max(self.x[0], other.x[0])
        min_x2 = min(self.x[1], other.x[1])
        max_y1 = max(self.y[0], other.y[0])
        min_y2 = min(self.y[1], other.y[1])

        remaining = []
        if other.x[0] > self.x[0]:
            remaining.append(Cube(
                (self.x[0], other.x[0] - 1),
                (self.y[0], self.y[1]),
                (self.z[0], self.z[1])
            ))
        if other.y[0] > self.y[0]:
            remaining.append(Cube(
                (max_x1, min_x2),
                (self.y[0], other.y[0] - 1),
                (self.z[0], self.z[1])
            ))
        if other.z[0] > self.z[0]:
            remaining.append(Cube(
                (max_x1, min_x2),
                (max_y1, min_y2),
                (self.z[0], other.z[0] - 1)
            ))

        if other.x[1] < self.x[1]:
            remaining.append(Cube(
                (other.x[1] + 1, self.x[1]),
                (self.y[0], self.y[1]),
                (self.z[0], self.z[1])
            ))
        if other.y[1] < self.y[1]: 
            remaining.append(Cube(
                (max_x1, min_x2),
                (other.y[1] + 1, self.y[1]),
                (self.z[0], self.z[1])
            ))
        if other.z[1] < self.z[1]:
            remaining.append(Cube(
                (max_x1, min_x2),
                (max_y1, min_y2),
                (other.z[1] + 1, self.z[1])
            ))
        
        return remaining

    def __repr__(self) -> str:
        return str(self.bounds)


operations = []
with open("parson_brown.txt") as read:
    for l in read.readlines():
        a, b = l.strip().split()
        on = a == "on"
        b = b.split(",")
        b = [x.split("=") for x in b]
        for i in range(len(b)):
            b[i][1] = [int(y) for y in b[i][1].split("..")]
        operations.append([on, [x[1] for x in b]])

all_cubes = []
x = 1
for on, ranges in operations:
    cube = Cube(*ranges)
    new_cubes = []
    for pc in all_cubes:
        if not cube.overlaps(pc):
            new_cubes.append(pc)
            continue
        new_cubes.extend(pc.make_hole(cube))
    all_cubes = new_cubes
    if on:
        all_cubes.append(cube)

total = sum(c.volume for c in all_cubes)
print(f"bruh half of this code is copied from other people's: {total}")
