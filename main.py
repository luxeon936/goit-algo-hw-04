import random
import timeit
import sys
import copy

# Збільшення ліміту рекурсії для підтримки сортування великих масивів (для сортування злиттям)
sys.setrecursionlimit(1000000)

# Функція сортування злиттям (рекурсивний підхід)
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Знаходимо середину списку
        L = arr[:mid]  # Ліва частина
        R = arr[mid:]  # Права частина

        # Рекурсивне сортування лівої та правої частин
        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        # Злиття відсортованих підсписків L і R
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Копіювання залишків лівого підсписку
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Копіювання залишків правого підсписку
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# Функція сортування вставками (ітеративний підхід)
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]  # Елемент, який вставляється
        j = i - 1
        # Переміщуємо елементи, які більше за ключ, на одну позицію вправо
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Вбудований алгоритм сортування Python (Timsort) за допомогою функції sorted()
def timsort_builtin(arr):
    return sorted(arr)

# Вбудований алгоритм Timsort, що сортує список на місці
def timsort_inplace(arr):
    arr.sort()

# Генерація наборів даних різного типу для тестування
def generate_datasets(size):
    datasets = {
        'Random': random.sample(range(size * 10), size),  # Випадковий список
        'Sorted': list(range(size)),  # Вже відсортований список
        'Reverse Sorted': list(range(size, 0, -1)),  # Відсортований у зворотному порядку
        'Duplicates': [random.choice(range(size // 10)) for _ in range(size)],  # Список з дублікатами
        'Nearly Sorted': list(range(size))  # Майже відсортований список
    }
    # Вносимо невеликі зміни в майже відсортований список
    for _ in range(size // 100):
        idx1 = random.randint(0, size - 1)
        idx2 = random.randint(0, size - 1)
        datasets['Nearly Sorted'][idx1], datasets['Nearly Sorted'][idx2] = datasets['Nearly Sorted'][idx2], datasets['Nearly Sorted'][idx1]
    return datasets

# Вимірювання часу виконання сортування для заданої функції
def measure_time(sort_func, data):
    # Використовуємо копію даних, щоб не впливати на оригінал
    data_copy = copy.deepcopy(data)
    timer = timeit.Timer(lambda: sort_func(data_copy))
    # Виконуємо сортування один раз і вимірюємо час
    try:
        execution_time = timer.timeit(number=1)
    except RecursionError:
        execution_time = float('inf')  # Якщо виникає помилка рекурсії
    return execution_time

# Основна функція програми
def main():
    sizes = [1000, 5000, 10000]  # Розміри списків для тестування
    algorithms = {
        'Merge Sort': merge_sort,
        'Insertion Sort': insertion_sort,
        'Timsort (sorted)': timsort_builtin,
        'Timsort (list.sort())': timsort_inplace
    }

    # Проходимо по кожному розміру списку
    for size in sizes:
        print(f"\n--- Розмір списку: {size} ---")
        datasets = generate_datasets(size)  # Генеруємо дані для поточного розміру
        for dataset_name, data in datasets.items():
            print(f"\nНабір даних: {dataset_name}")
            results = {}
            # Тестуємо кожен алгоритм сортування
            for algo_name, algo_func in algorithms.items():
                # Для Timsort (sorted) використовуємо функцію sorted(), а для inplace сортування - .sort()
                if algo_name == 'Timsort (sorted)':
                    sort_func = lambda x: sorted(x)
                elif algo_name == 'Timsort (list.sort())':
                    sort_func = lambda x: x.sort()
                else:
                    sort_func = algo_func

                time_taken = measure_time(sort_func, data)  # Вимірюємо час виконання сортування
                results[algo_name] = time_taken

            # Виведення результатів для поточного набору даних
            print(f"{'Алгоритм':<25}{'Час (сек)':>15}")
            for algo, t in results.items():
                print(f"{algo:<25}{t:>15.6f}")
    
    print("\n--- Порівняння завершено ---")

# Запуск програми
if __name__ == "__main__":
    main()
