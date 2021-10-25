# import tqdm
# import numpy as np

# def win_lose(p, w, n, Bstart, t):
#     win = 0
#     lose = 0
#     for c in tqdm.tqdm(range(t)):
#         B = Bstart
#         while True:
#             if B < 1:
#                 lose += 1
#                 break
#             if B >= 2*Bstart:
#                 win += 1
#                 break

#             bet = B/n

#             if bet < 1:
#                 bet = 1

#             if np.random.choice((True, False), p=[p, 1-p]):
#                 B += w*bet
#             else:
#                 B -= bet

#     return ((p, w, n, Bstart, t), (win, lose), (win/t)*100)


# print(win_lose(0.5, 1.1, 5, 10000, 100000))   

from pushover import init, Client

init("aq7rx1r3o55k6rtobcq8xwv66u8jgw")
Client("ud1pmkki74te12d3bicw24r99kb38z").send_message("Hello!", title="Hello")