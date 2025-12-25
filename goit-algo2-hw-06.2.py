import re
import time
import mmh3
import math
import sys

class HyperLogLog:
    def __init__(self, p=14): 
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2

    def _get_alpha(self):
        if self.p <= 16:
            return 0.673
        elif self.p == 32:
            return 0.697
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * self.m * self.m / Z
        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)
        return E


# 1. Метод завантаження даних обробляє лог-файл, ігноруючи некоректні рядки (10 балів).
def load_ips_from_log(file_path):
    ips = []
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f: # ігноруючи некоректні рядки
        for line in f:
            found_ips = ip_pattern.findall(line)
            for ip in found_ips:
                octets = ip.split(".")
                if all(0 <= int(o) <= 255 for o in octets):
                    ips.append(ip)
    return ips


# 2. Функція точного підрахунку повертає правильну кількість унікальних IP-адрес (10 балів).
def exact_unique_count(ip_list):
    return len(set(ip_list))



if __name__ == "__main__":
    log_file_path = r"C:\Users\Yulii\Projects\!Repository\Algo2\goit-algo2-hw-06\lms-stage-access.log"

    ips = load_ips_from_log(log_file_path)
    print("\n--- Порівняння продуктивності за допомогою реального лог-файлу ---")
    print(f"Завантажено {len(ips)} рядків (IP).")


    start_exact = time.time()
    exact_count = exact_unique_count(ips)
    end_exact = time.time()
    exact_time = end_exact - start_exact
    exact_memory = sys.getsizeof(set(ips)) + sum(sys.getsizeof(ip) for ip in set(ips))

    # 3. HyperLogLog показує результат із прийнятною похибкою (10 балів).
    hll = HyperLogLog(p=14)
    start_hll = time.time()
    for ip in ips:
        hll.add(ip)
    hll_count = hll.count()
    end_hll = time.time()
    hll_time = end_hll - start_hll
    hll_memory = sys.getsizeof(hll.registers)


    # 4. Результати порівняння представлені у вигляді таблиці (10 балів).
    print("\nРезультати порівняння:")
    print(f"{'Метод':<25}{'Унікальні елементи':<20}{'Час виконання (сек.)':<20}{'Пам’ять (байт)'}")
    print(f"{'Точний підрахунок':<25}{exact_count:<20}{exact_time:.6f}{exact_memory:>20}")
    print(f"{'HyperLogLog':<25}{hll_count:<20.1f}{hll_time:.6f}{hll_memory:>20}")




# 5. Код є адаптованим до великих наборів даних (10 балів).
print("\n--- Перевірка адаптованості до великих наборів ---")

large_test_data = [f"user_{i}" for i in range(1_000_000)]

start_exact_large = time.time()
exact_count_large = len(set(large_test_data))
end_exact_large = time.time()
exact_time_large = end_exact_large - start_exact_large
exact_memory_large = sys.getsizeof(set(large_test_data))

# Додали точності HyperLogLog (p=20 замість 14)
hll_large = HyperLogLog(p=20)
start_hll_large = time.time()
for item in large_test_data:
    hll_large.add(item)
hll_count_large = hll_large.count()
end_hll_large = time.time()
hll_time_large = end_hll_large - start_hll_large
hll_memory_large = sys.getsizeof(hll_large.registers)


print(f"{'Метод':<25}{'Унікальні елементи':<20}{'Час виконання (сек.)':<20}{'Пам’ять (байт)'}")
print(f"{'Точний підрахунок':<25}{exact_count_large:<20}{exact_time_large:<20.6f}{exact_memory_large}")
print(f"{'HyperLogLog':<25}{hll_count_large:<20.1f}{hll_time_large:<20.6f}{hll_memory_large}")


# Аналіз результатів порівняння знаходяться в файлі README






