import numpy as np
p = 0.7
w = 0.6

n = 2
t = 1000000

stop_locations = []
for c in range(10000):
    B = 10000
    for k in range(t):
        if B < 1:
            stop_locations.append(k)
            break
        bet = B/n
        if bet < 1:
            bet = 1

        if np.random.choice((True, False), p=[p, 1-p]):
            B += w*bet
        else:
            B -= bet

print(stop_locations)
    