def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache.get(args)
        result = func(*args)
        cache[args] = result
        return result

    return wrapper