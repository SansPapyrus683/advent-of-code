def is_repeat(string: str, chunk: int) -> bool:
    if len(string) % chunk != 0:
        return False
    
    size = len(string) // chunk
    target = string[:size]
    for i in range(size, len(string), size):
        if string[i:i+size] != target:
            return False
    return True


ranges = [tuple(int(i) for i in r.split("-")) for r in input().split(",")]

p1_invalid = 0
p2_invalid = 0
for start, end in ranges:
    for i in range(start, end + 1):
        str_i = str(i)
        p1_invalid += i * is_repeat(str_i, 2)
        # not sure if there's a faster way to eval this...
        p2_invalid += i * any(is_repeat(str_i, j) for j in range(2, len(str_i) + 1))

print(f"HAHAHAHA I FORGOT I HAD A CHUNKS METHOD: {p1_invalid}")
print(f"MY P2 TIME COULDA BEEN SO MUCH BETTER: {p2_invalid}")
