import random


def get_random_coords(n):
    num = random.choice([x for x in range(1, 5)]) + n
    sp_x = random.sample([x for x in range(-300, -60)], num)
    sp_y = random.sample([y for y in range(230, 400)], num)
    sp_ans = []
    for i in range(num):
        sp_ans.append([sp_x[i], sp_y[i]])
    return sp_ans
