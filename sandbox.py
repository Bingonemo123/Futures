def timeout(timeout):
    def deco(func):
        return func.__name__
    return deco


@timeout(3)
def h ():
    return 'JJf'


print(h)