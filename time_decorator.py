import time
from functools import wraps


def timeit(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"{method.__name__} => {(end_time-start_time)*1000:.5f} ms")

        return result

    return wrapper
    
@timeit
def func(n):
    return list(range(n))
    
if __name__ == '__main__':
  res = func(3)
