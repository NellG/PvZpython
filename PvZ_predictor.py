# script to predict how many games to level up in PvZ
# as a function of win probability

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def diamondbetter(lvlin, win):
    loss = 1-win
    lvlout = np.zeros((2,6))
    downs = np.array([[1,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0]])
    ups = np.array([[1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0]])
    lvlout[0,:4] = loss*np.dot(downs, (lvlin[0,:]+lvlin[1,:]))
    lvlout[1,1:] = win*np.dot(ups, (lvlin[0,:]+lvlin[1,:]))
    return lvlout

def diamond(lvl, win):
    loss = 1-win
    zero = loss * (lvl[0] + lvl[1])
    one = loss * lvl[2] + win * lvl[0]
    two = loss * lvl[3] + win * lvl[1]
    three = loss * lvl[4] + win * lvl[2]
    four = win * lvl[3]
    five = win * lvl[4]

    return [zero, one, two, three, four, five]

def ex_games(cutoff, max, win, league):
    expected = []

    for p in win:
        probability = []
        game_list = []
        game = 1
        left = 1
        levels = np.zeros((2,6))
        levels[1,0] = 1

        while left > cutoff:
            levels = league(levels, p)
            probability.append(levels[1,5])
            game_list.append(game)
            game += 1
            left = (1-sum(probability))*game

            if game > max*10:
                left = 0
                probability.append(1-sum(probability))
                game_list.append(game)

        expected.append(round(sum(np.array(probability)*np.array(game_list)), 3))

    return np.array(expected)

cutoff = 0.0001
max = 50
win = np.linspace(0, 1, 101)

ex_diamond = ex_games(cutoff, max, win, diamondbetter)
offset = ex_diamond-20

fix, ax = plt.subplots()
ax.plot(win, ex_diamond, color = 'red', label = 'Diamond League')
ax.plot(win, offset, color = 'blue', label = 'Offset')
ax.set(xlabel = 'Probability of win', ylabel = 'Expected rounds to level up', title = 'Prediction for Each League')
plt.xlim(0,1)
plt.ylim(0, 50)
ax.grid()
ax.legend()
plt.show()
