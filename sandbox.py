import tqdm
import numpy as np

def win_lose(p, w, n, Bstart, t):
    win = 0
    lose = 0
    for c in tqdm.tqdm(range(t)):
        B = Bstart
        k = 1
        while True:
            if B < 1:
                lose += 1
                break
            if B >= 2*Bstart:
                win += 1
                break

            bet = B/n

            if bet < 1:
                bet = 1

            if np.random.choice((True, False), p=[p, 1-p]):
                B += w*bet
            else:
                B -= bet
            k += 1
    return (win, lose)


print(win_lose(0.5, 0.6, 5, 10000, 100000))