import mmh3

# 1. Клас BloomFilter реалізує логіку роботи з фільтром Блума (20 балів).
class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        if not item:  
            return
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        if not item:  
            return False
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


# 2. Функція check_password_uniqueness перевіряє нові паролі, використовуючи переданий фільтр (20 балів).            results[password] = "некоректний пароль"
def check_password_uniqueness(bloom_filter, passwords):
    results = {}
    for password in passwords:
        if not password:  
            results[password] = "некоректний пароль"
        elif bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)  
    return results



if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None] # Плюс перевірка порожнього та некоректного значення
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")

# 3. Код виконує приклад використання відповідно до очікуваних результатів (10 балів).






