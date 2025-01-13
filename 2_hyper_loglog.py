import json
import time
from datasketch import HyperLogLog
from collections import Counter


# Реалізація точного підрахунку унікальних IP
def exact_unique_ips(file_path):
    unique_ips = set()
    processed_lines = 0
    skipped_lines = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                unique_ips.add(log_entry["remote_addr"])
                processed_lines += 1
            except (json.JSONDecodeError, KeyError):
                skipped_lines += 1
    print(f"Оброблено рядків: {processed_lines}, Пропущено рядків: {skipped_lines}")
    return len(unique_ips)


# Реалізація наближеного підрахунку за допомогою HyperLogLog
def hyperloglog_unique_ips(file_path, precision=14):
    hll = HyperLogLog(precision)
    processed_lines = 0
    skipped_lines = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                hll.update(log_entry["remote_addr"].encode("utf-8"))
                processed_lines += 1
            except (json.JSONDecodeError, KeyError):
                skipped_lines += 1
    print(f"Оброблено рядків: {processed_lines}, Пропущено рядків: {skipped_lines}")
    return hll.count()


if __name__ == "__main__":
    log_file = "lms-stage-access.log"

    print("Точний підрахунок...")
    start_time = time.time()
    exact_count = exact_unique_ips(log_file)
    exact_time = time.time() - start_time

    print("Підрахунок за допомогою HyperLogLog...")
    start_time = time.time()
    approx_count = hyperloglog_unique_ips(log_file)
    approx_time = time.time() - start_time

    print("\nРезультати порівняння:")
    print(f"{'Метод':<25}{'Унікальні елементи':<20}{'Час виконання (сек.)':<20}")
    print(f"{'Точний підрахунок':<25}{exact_count:<20}{exact_time:<20.5f}")
    print(f"{'HyperLogLog':<25}{approx_count:<20}{approx_time:<20.5f}")
