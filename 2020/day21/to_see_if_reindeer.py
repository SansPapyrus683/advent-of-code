food = []
num_at = 0
all_allergens = set()
all_ingredients = set()
with open('really_can_fly.txt') as read:
    for line in read.readlines():
        line = line.strip()
        ingredients = [i.strip() for i in line[:line.find('(')].split()]
        allergens = [i.strip() for i in line[line.find('(') + 1:-1].replace('contains', '').split(',')]
        for a in allergens:
            all_allergens.add(a)
        for i in ingredients:
            all_ingredients.add(i)
        food.append([ingredients, allergens])

toxins = set()
poss_list = {}
for a in all_allergens:
    shared = all_ingredients.copy()
    for f in food:
        if a in f[1]:
            shared = shared.intersection(f[0])
    toxins = toxins.union(shared)
    poss_list[a] = shared

safe_count = 0
for f in food:
    for i in f[0]:
        if i not in toxins:
            safe_count += 1
print("good god what kind of a language is this: %i" % safe_count)

canonical = {a: '' for a in all_allergens}
while not all(canonical.values()):
    for a, i in poss_list.items():
        if len(i) == 1:
            canonical[a] = i.pop()
            for other in poss_list.values():
                if canonical[a] in other:
                    other.remove(canonical[a])
print("and why does the protag have so many allergies lol: %s" % ','.join(canonical[a] for a in sorted(all_allergens)))
