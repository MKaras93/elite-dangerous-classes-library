def return_first_match(func, items):
    return next(item for item in items if func(item))
