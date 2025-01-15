import time
from multiprocessing import Process, Queue, cpu_count, Pool, Manager


# звичайний алогритм пошуку всіх чисел на які ділиться задане без остачі
def all_divs(numb: int) -> list[int]:
    if numb == 0:
        raise ValueError("0 has not have divisors.")

    # Знаходимо дільники
    return [i for i in range(1, abs(numb) + 1) if numb % i == 0]


# синхронний спосіб розрахунку, ітеративним перебором
def factorize_sync(*number) -> list[list[int]]:
    return [all_divs(n) for n in number]


# асинхронний розрахунк в багатопоточному режимі - Pool
def factorize_async_1(*numbers) -> list[list[int]]:
    threads = len(numbers) if len(numbers) < cpu_count() else cpu_count()
    with Pool(threads) as pool:
        return pool.map(all_divs, numbers)


# 2й спосіб через shared Dict
def worker_1(number: int, shared_dict):
    shared_dict[number] = all_divs(number)


# асинхронний розрахунк в багатопоточному режимі 3 - через спыльну память
def factorize_async_2(*numbers) -> list[list[int]]:
    # Створюємо Manager і спільний словник
    with Manager() as manager:
        shared_dict = manager.dict()
        # Створення та запуск процесів
        processes = []
        for number in numbers:
            p = Process(target=worker_1, args=(number, shared_dict,))
            p.start()
            processes.append(p)

        # Очікуємо завершення всіх процесів
        [p.join() for p in processes]
        # Сортуємо результати за порядком чисел
        # shared_dict.sort(key=lambda x: numbers.index(x[0]))
        # Вивід результатів
        return shared_dict.values()


# 3й спосіб через Queue
# воркер запускає розрахунок і збергігає результат в черзі
def worker_2(number: int, result_queue: Queue):
    result = all_divs(number)
    result_queue.put((number, result))


# асинзронний розрахунк в багатопоточному режимі 1
def factorize_async_3(*numbers) -> list[list[int]]:
    processes = []
    result_queue = Queue()
    # Створюємо окремий процес для кожного числа
    for n in numbers:
        pr = Process(target=worker_2, args=(n, result_queue))
        pr.start()
        processes.append(pr)
    # Збираємо результати
    results = []
    for _ in numbers:
        results.append(result_queue.get())
    # Очікуємо завершення всіх процесів
    [pr.join() for pr in processes]
    # Сортуємо результати за порядком чисел
    results.sort(key=lambda x: numbers.index(x[0]))
    # Повертаємо лише список дільників
    return [result[1] for result in results]


def test(func, in_vals, a_expected, b_expected, c_expected, d_expected):
    start_time = time.time()
    a, b, c, d = func(*in_vals)
    end_time = time.time()
    assert a == a_expected
    assert b == b_expected
    assert c == c_expected
    assert d == d_expected
    print(f"approach: {func.__name__} - duration: {(end_time - start_time):.2f} sec")


if __name__ == "__main__":
    input_vals = [128, 255, 99999, 10651060]
    a_exp = [1, 2, 4, 8, 16, 32, 64, 128]
    b_exp = [1, 3, 5, 15, 17, 51, 85, 255]
    c_exp = [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    d_exp = [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    # запускаємо 1 синхроний і 3 асинхронні тести
    test(factorize_sync, input_vals, a_exp, b_exp, c_exp, d_exp)
    test(factorize_async_1, input_vals, a_exp, b_exp, c_exp, d_exp)
    test(factorize_async_2, input_vals, a_exp, b_exp, c_exp, d_exp)
    test(factorize_async_3, input_vals, a_exp, b_exp, c_exp, d_exp)
