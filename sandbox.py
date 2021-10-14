import inspect

hh = inspect.getmodulename(inspect.stack()[-1][1])
print(hh)