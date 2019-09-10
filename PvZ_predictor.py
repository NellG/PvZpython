# script to predict how many games to level up in PvZ
# as a function of win probability

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Function to iterate through p-win steps
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

# Functions to calculate expected rounds to level up in each league for a given
# probability of winning

def wood(lvlin, win):
    loss = 1-win
    lvlout = np.zeros((2,6))
    downs = np.array([[1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,0]])
    ups = np.array([[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,1,1,0]])
    lvlout[0,:] = loss*np.dot(downs, (lvlin[0,:]+lvlin[1,:]))
    lvlout[1,:] = win*np.dot(ups, (lvlin[0,:]+lvlin[1,:]))
    return lvlout

def bronze(lvlin, win):
    loss = 1-win
    lvlout = np.zeros((2,6))
    downs = np.array([[1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,0]])
    upsl = np.array([[0,0,0,0,0,0], [0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,1,0]])
    upsw = np.array([[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,1,1,0]])
    lvlout[0,:] = loss*np.dot(downs, (lvlin[0,:]+lvlin[1,:]))
    lvlout[1,:] = win*np.dot(upsl, lvlin[0,:]) + win*np.dot(upsw, lvlin[1,:])
    return lvlout

def gold(lvlin, win):
    loss = 1-win
    lvlout = np.zeros((2,6))
    downs = np.array([[1,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,0], [0,0,0,0,0,0]])
    upsl = np.array([[0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0]])
    upsw = np.array([[0,0,0,0,0,0], [0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,1,0]])
    lvlout[0,:] = loss*np.dot(downs, (lvlin[0,:]+lvlin[1,:]))
    lvlout[1,:] = win*np.dot(upsl, lvlin[0,:]) + win*np.dot(upsw, lvlin[1,:])
    return lvlout

def diamond(lvlin, win):
    loss = 1-win
    lvlout = np.zeros((2,6))
    downs = np.array([[1,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,0], [0,0,0,0,0,0]])
    ups = np.array([[0,0,0,0,0,0], [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0]])
    lvlout[0,:] = loss*np.dot(downs, (lvlin[0,:]+lvlin[1,:]))
    lvlout[1,:] = win*np.dot(ups, (lvlin[0,:]+lvlin[1,:]))
    return lvlout

# Main code

# Set precision of expectation estimate
cutoff = 0.0001
max = 50
win = np.linspace(0, 1, 101)

# Calculate expected games for each league
ex_diamond = ex_games(cutoff, max, win, diamond)
ex_wood = ex_games(cutoff, max, win, wood)
ex_bronze = ex_games(cutoff, max, win, bronze)
ex_gold = ex_games(cutoff, max, win, gold)

# Plot expectations
fix, ax = plt.subplots()
ax.plot(win, ex_wood, color = 'saddlebrown', label = 'Wood League')
ax.plot(win, ex_bronze, color = 'goldenrod', label = 'Bronze/Silver League')
ax.plot(win, ex_gold, color = 'gold', label = 'Gold League')
ax.plot(win, ex_diamond, color = 'skyblue', label = 'Diamond/Taco League')
ax.set(xlabel = 'Probability of win', ylabel = 'Expected rounds to level up', title = 'Prediction for Each League')
plt.xlim(0,1)
plt.ylim(0, 50)
ax.grid()
ax.legend()
plt.show()
