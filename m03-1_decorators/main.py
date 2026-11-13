import functools
import time
import random

def timed(func):
    @functools.wraps(func)
    def calculate_time(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} работала {time.perf_counter() - start:.2f} c")
        return result
    return calculate_time

def retry(loops):
    def decorater(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(loops):
                if i + 1 == loops:
                    result = func(*args, **kwargs)
                    print(f"Функция вернула результат на {i + 1} попытке")
                    return result
                try:
                    result = func(*args, **kwargs)
                    print(f"Функция вернула результат на {i + 1} попытке")
                    break
                except Exception as e:
                    print(f"Ошибка во время выполнения функции {func.__name__}: {e}")
                    time.sleep(2**i)
            return result
        return wrapper
    return decorater

@retry(4)      
@timed
def test_func(s: int) -> int:
    time.sleep(s)
    if random.randint(1, 2) == 1:
        raise ValueError("test")
    return s * s

print(test_func(1))