class BITS:
    def __init__(self, transmission: str):
        self.transmission = "".join(bin(int(c, 16))[2:].zfill(4) for c in transmission)
        self.version_total = 0
        self.result = float("inf")

    @staticmethod
    def operation(values: list[int], op: int) -> int:
        if op == 0:
            return sum(values)
        elif op == 1:
            prod = 1
            for v in values:
                prod *= v
            return prod
        elif op == 2:
            return min(values)
        elif op == 3:
            return max(values)
        elif op == 5:
            assert len(values) == 2, "comp packets should have exactly 2 values"
            return int(values[0] > values[1])
        elif op == 6:
            assert len(values) == 2, "comp packets should have exactly 2 values"
            return int(values[0] < values[1])
        elif op == 7:
            assert len(values) == 2, "comp packets should have exactly 2 values"
            return int(values[0] == values[1])

    def parse(self) -> int:
        if self.result != float("inf"):
            return self.result

        # returns the result of the packet and the index at which the packet stopped
        def parse(packet: str) -> tuple[int, int]:
            version = int(packet[:3], 2)
            self.version_total += version
            type_id = int(packet[3:6], 2)

            if type_id == 4:
                final = ''
                at = 6
                while True:
                    final += packet[at + 1:at + 5]
                    if packet[at] == '0':  # hit a 0, let's just stop now
                        at += 5
                        break
                    at += 5
                return int(final, 2), at

            else:
                length_type_id = int(packet[6])
                if length_type_id == 0:
                    total_len = int(packet[7:7 + 15], 2)
                    other_packets = packet[7 + 15:7 + 15 + total_len]
                    vals = []
                    # keep on parsing packets until it stops
                    while other_packets:
                        v, end = parse(other_packets)
                        vals.append(v)
                        if end is None:
                            break
                        other_packets = other_packets[end:]
                    return self.operation(vals, type_id), 7 + 15 + total_len
                else:
                    sub_num = int(packet[7:7 + 11], 2)
                    test_packet = packet[7 + 11:]
                    vals = []
                    # yeah, just parse it a certain # of times
                    for _ in range(sub_num):
                        v, end = parse(test_packet)
                        vals.append(v)
                        test_packet = test_packet[end:]
                    return self.operation(vals, type_id), len(packet) - len(test_packet)

        self.result = parse(self.transmission)[0]
        return self.result


with open("well_conspire.txt") as read:
    string = read.readline().strip()

bits = BITS(string)
print(f"the result of the thing is this: {bits.parse()} (p2 ans)")
print(f"and the sum of the versions is {bits.version_total} (p1 ans)")
