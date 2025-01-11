import time
from collections import Counter
from hyperloglog import HyperLogLog
import re


# Функція для завантаження даних з лог-файлу
def load_data(file_path):
    ip_pattern = re.compile(r"\\b(?:\\d{1,3}\\.){3}\\d{1,3}(?::\\d+)?\\b")
    valid_ips = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                valid_ips.append(match.group())
    print(f"Завантажено рядків: {len(valid_ips)}")
    if valid_ips:
        print(f"Приклад IP: {valid_ips[:5]}")
    return valid_ips


# Функція для точного підрахунку унікальних IP-адрес
def count_unique_ips_exact(data):
    return len(set(data))


# Функція для підрахунку унікальних IP-адрес за допомогою HyperLogLog
def count_unique_ips_hll(data):
    hll = HyperLogLog(0.01)
    for ip in data:
        hll.add(ip)
    return len(hll)


# Функція для порівняння продуктивності
def compare_methods(file_path):
    data = load_data(file_path)

    start_time_exact = time.time()
    exact_count = count_unique_ips_exact(data)
    time_exact = time.time() - start_time_exact

    # HyperLogLog підрахунок
    start_time_hll = time.time()
    hll_count = count_unique_ips_hll(data)
    time_hll = time.time() - start_time_hll

    print("Результати порівняння:")
    print(f"{'Метод':<25}{'Унікальні елементи':<20}{'Час виконання (сек.)':<20}")
    print(f"{'Точний підрахунок':<25}{exact_count:<20}{time_exact:<20.6f}")
    print(f"{'HyperLogLog':<25}{hll_count:<20}{time_hll:<20.6f}")


if __name__ == "__main__":
    log_file_path = ".\lms-stage-access.log"
    compare_methods(log_file_path)
