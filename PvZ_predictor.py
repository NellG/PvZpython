# script to predict how many games to level up in PvZ
# as a function of win probability

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def diamond(lvl, win):
    loss = 1-win
    zero = loss * (lvl[0] + lvl[1])
    one = loss * lvl[2] + win * lvl[0]
    two = loss * lvl[3] + win * lvl[1]
    three = loss * lvl[4] + win * lvl[2]
    four = win * lvl[3]
    five = win * lvl[4]

    return [zero, one, two, three, four, five]


cutoff = 0.0001
max = 50
win = np.linspace(0, 1, 101)
expected = []

for p in win:
    probability = []
    game_list = []
    game = 1
    left = 1
    levels = [1, 0, 0, 0 , 0, 0]

    while left > cutoff:
        levels = diamond(levels, p)
        probability.append(levels[5])
        game_list.append(game)
        game += 1
        left = (1-sum(probability))*game

        if game > max*10:
            left = 0
            probability.append(1-sum(probability))
            game_list.append(game)

    expected.append(round(sum(np.array(probability)*np.array(game_list)), 3))

fix, ax = plt.subplots()
ax.plot(win, expected)
ax.set(xlabel = 'Probability of win', ylabel = 'Expected rounds to level up', title = 'Prediction for Diamond League')
plt.xlim(0,1)
plt.ylim(0, 50)
ax.grid()
plt.show()
