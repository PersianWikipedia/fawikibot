# Author: Amir Sarabadani
# License: MIT


def cache(func):
    _cache = {}
    def func_wrapper(*args, **kwargs):
        if tuple([args, tuple(kwargs), func.__name__]) in _cache:
            return _cache[tuple([args, tuple(kwargs), func.__name__])]
        else:
            _cache[tuple([args, tuple(kwargs), func.__name__])] = func(*args, **kwargs)
            return func(*args, **kwargs)
    return func_wrapper

if __name__ == "__main__":
    @cache
    def a(b):
        return b+1

    print(a(1))
    print('call from cache')
    print(a(1))

