with open("snows_glistening.txt") as read:
    nums = [l.strip() for l in read.readlines()]

gamma = ""
epsilon = ""
for i in range(len(nums[0])):
    one_count = 0
    zero_count = 0
    for n in nums:
        if n[i] == "1":
            one_count += 1
        else:
            zero_count += 1
    if one_count > zero_count:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        gamma += "0"
        epsilon += "1"
print(f"wooo got 22nd place globally: {int(gamma, 2) * int(epsilon, 2)}")

oxy = nums.copy()
co2 = nums.copy()
for i in range(len(nums[0])):
    # these two segments are so similar but so different AAAAA
    if len(oxy) > 1:
        oxy_one_count = 0
        oxy_zero_count = 0
        for o in oxy:
            if o[i] == "1":
                oxy_one_count += 1
            else:
                oxy_zero_count += 1
        target = "1" if oxy_one_count >= oxy_zero_count else "0"
        oxy = [o for o in oxy if o[i] == target]

    if len(co2) > 1:
        co2_one_count = 0
        co2_zero_count = 0
        for o in co2:
            if o[i] == "1":
                co2_one_count += 1
            else:
                co2_zero_count += 1
        target = "0" if co2_one_count >= co2_zero_count else "1"
        co2 = [o for o in co2 if o[i] == target]
print(f"but i sucked on this part, 12 mins ahahaha: {int(oxy[0], 2) * int(co2[0], 2)}")
