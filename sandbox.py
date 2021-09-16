#%%
import numpy as np
import tqdm
import sympy
#%%
def list_creator (p, w, n, t, Bstart ):
    stop_locations = []
    for c in tqdm.tqdm(range(t)):
        B = Bstart
        k = 1
        while True:
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
            k += 1
    return stop_locations

# %%
l1 = list_creator(0.7, 0.6, 2, 100000, 10000)

#%%
print(sum(l1)/len(l1))


# %%
B, n = sympy.symbols('B n')
z = sympy.floor(sympy.log(n/B, (n-1)/n) + 1)
end_formula = z + sympy.floor(B*((n-1)/n)**z)
end_formula.subs(B, 100).subs(n, 100)
# %%
def win_lose (p, w, n, t, Bstart ):
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

# %%
win_lose(0.7, 0.6, 2, 100000, 10000)
# %%
data = win_lose(0.7, 0.6, 3, 100000, 10000)
data
data[0]/sum(data)
# %%
data = win_lose(0.7, 0.6, 4, 100000, 10000)
print(data)
data[0]/sum(data)
# %%
data = win_lose(0.7, 0.6, 5, 100000, 10000)
print(data)
data[0]/sum(data)
# %%
data = win_lose(0.7, 0.6, 5, 1000000, 10000)
print(data)
data[0]/sum(data)
# %%
