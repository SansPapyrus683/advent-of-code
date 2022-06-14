# merry christmas, everyone!

MOD = 20201227
MUL_BY = 7

card = 11562782
door = 18108497

card_loop = 1
so_far = 1
while True:
    so_far = (so_far * MUL_BY) % MOD
    if so_far == card:
        break
    card_loop += 1

print(f"good god i hate this day with the burning passion of a million suns: {pow(door, card_loop, MOD)}")
