def contains(all_bags, start: str, end: str) -> bool:
    for _, sub_bag in all_bags[start]:
        if sub_bag == end or contains(all_bags, sub_bag, end):
            return True


def bag_number(all_bags, the_bag: str) -> int:
    total_num = 0
    for bagNum, subBag in all_bags[the_bag]:
        # we need the bagNum of the subbag and then bagNum of each of the sub-subbags, and so on
        total_num += bagNum + bagNum * bag_number(all_bags, subBag)
    return total_num


with open('seasons.txt') as read:
    bags = {}
    for line in read.readlines():
        line = line.strip().split(' contain ')

        # NOTE: the bags has to come before bag (or else you end up with a buncha random s chars)
        for extraneous in ['bags', 'bag', 'no other', '.']:
            line = [s.replace(extraneous, '').strip() for s in line]

        outside, inside = line  # just being a explicit here
        inside = [i.strip().split() for i in inside.split(',') if i.strip()]

        bags[outside] = [[int(b[0]), " ".join(b[1:])] for b in inside]

my_bag = "shiny gold"
containsMyBag = 0
for b in bags:
    if b != my_bag and contains(bags, b, my_bag):
        containsMyBag += 1
print(f"goddamn the string parsing for this problem was hell: {containsMyBag}")
print(f"but boy i have improved on my recursion skills in a year tho: {bag_number(bags, my_bag)}")
