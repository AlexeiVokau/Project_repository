import random

skipped_chars = ["ь", "ы", "ъ", "й", "ц"]
used_cities = set()

# Загружаем список городов из файла
f = open('cities.txt', "r", encoding="utf-8")
cities_list = [line.strip() for line in f]
f.close()
cities_list = [city.lower() for city in cities_list]


# Сохраняем ходы в файл
def write_answer(filename, city):
    f = open(filename, mode="a", encoding="utf-8")
    f.write(city + "\n")
    f.close()


# Функция для проверки существования города в списке
def is_city_valid(city):
    return city in cities_list


# Функция для поиска города, начинающегося с заданной буквы
def find_city(letter):
    valid_cities = [city for city in cities_list if city.startswith(letter) and city not in used_cities]
    if valid_cities:
        return random.choice(valid_cities)
    else:
        return None


# Основной цикл игры
def game():
    global last_letter
    answer_filename = "answers.txt"
    computer_city = random.choice(cities_list)
    print(f"Начинаем с города: {computer_city.capitalize()}")
    write_answer(filename=answer_filename, city=computer_city)

    ## Счетчик неудачных попыток пользователя
    failed_attempts = 0

    while True:
        for char in skipped_chars:
            computer_city = computer_city.replace(char, "")
        user_city = input(
            f"Введите город, начинающийся на '{computer_city[-1]}': ").lower()

        if user_city in used_cities:
            print("Этот город уже был назван. Попробуйте еще раз.")
            failed_attempts += 1
            if failed_attempts >= 5:
                print("Вы проиграли. Слишком много неудачных попыток.")
                break
            continue
        if not is_city_valid(user_city):
            print("Такого города не существует. Попробуйте еще раз.")
            failed_attempts += 1
            if failed_attempts >= 5:
                print("Вы проиграли. Слишком много неудачных попыток.")
                break
            continue
        # Проверки корректности города
        # Если город корректный, записываем его
        write_answer(filename=answer_filename, city=user_city)
        used_cities.add(user_city)

        # Ход ко#мпьютера
        for char in skipped_chars:
            user_city = user_city.replace(char, "")

        last_letter = user_city[-1]
        next_city = find_city(last_letter)
        if next_city:
            print(f"Компьютер ходит: {next_city.capitalize()}")
            with open('answers.txt', 'a') as f:
                f.write(next_city + "\n")
                used_cities.add(computer_city)
                computer_city = next_city
        else:
            print("Компьютер не смог найти подходящий город. Вы выиграли!")
            break


# Запуск игры
game()