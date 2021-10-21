import tqdm
import numpy as np

def win_lose(p, w, n, Bstart, t):
    win = 0
    lose = 0
    for c in tqdm.tqdm(range(t)):
        B = Bstart
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

    return ((p, w, n, Bstart, t), (win, lose), (win/t)*100)


print(win_lose(0.55, 0.95, 5, 10000, 100000))