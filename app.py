from flask import Flask, render_template, request, abort
import random

app = Flask(__name__)

# Список домашніх тварин
animals = [
    {"type": "кіт", "name": "Барсик", "age": 7, "breed": "Сіамський"},
    {"type": "кіт", "name": "Мурчик", "age": 9, "breed": "Персидський"},
    {"type": "собака", "name": "Рекс", "age": 4, "breed": "Вівчарка"},
    {"type": "собака", "name": "Шарик", "age": 6, "breed": "Лабрадор"},
    {"type": "папуга", "name": "Кеша", "age": 3, "breed": "Корелла"},
    {"type": "папуга", "name": "Джек", "age": 5, "breed": "Ара"},
    {"type": "хом'як", "name": "Сніжок", "age": 2, "breed": "Джунгарський"},
    {"type": "кіт", "name": "Сімба", "age": 10, "breed": "Британський"},
    {"type": "собака", "name": "Бобик", "age": 8, "breed": "Доберман"},
    {"type": "хом'як", "name": "Біляш", "age": 1, "breed": "Сирійський"}
]

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.jinja', animals=animals, title="Список домашніх тварин")

# Завдання 1: Виведення тварин одного виду
@app.route('/type/<animal_type>')
def animals_by_type(animal_type):
    filtered = [animal for animal in animals if animal['type'] == animal_type]
    if not filtered:
        return render_template('not_found.jinja', message="Тварин цього виду не знайдено")
    return render_template('animals_by_type.jinja', animals=filtered, title=f"Тварини виду {animal_type}")

# Завдання 2: Виведення тварин не старше заданого віку
@app.route('/age/<int:max_age>')
def animals_by_age(max_age):
    filtered = [animal for animal in animals if animal['age'] <= max_age]
    if not filtered:
        return render_template('not_found.jinja', message="Тварин відповідного віку не знайдено")
    return render_template('animals_by_age.jinja', animals=filtered, title=f"Тварини до {max_age} років")

# Завдання 3: Найстаріший кіт
@app.route('/oldest-cat')
def oldest_cat():
    cats = [animal for animal in animals if animal['type'] == 'кіт']
    if not cats:
        return render_template('not_found.jinja', message="Котів не знайдено")
    oldest = max(cats, key=lambda cat: cat['age'])
    return render_template('oldest_cat.jinja', cat=oldest, title="Найстаріший кіт")

# Завдання 4: Фільтрація по виду та віку
@app.route('/filter', methods=['GET', 'POST'])
def filter_animals():
    error = None
    filtered = []
    if request.method == 'POST':
        animal_type = request.form.get('type')
        max_age = request.form.get('age')
        direction = request.form.get('direction')

        if not max_age.isdigit():
            error = "Некоректний вік"
        else:
            max_age = int(max_age)
            filtered = [animal for animal in animals if (animal['type'] == animal_type or not animal_type) and animal['age'] <= max_age]
            if direction == 'Oldest':
                filtered = sorted(filtered, key=lambda x: x['age'], reverse=True)
            elif direction == 'Youngest':
                filtered = sorted(filtered, key=lambda x: x['age'])

    return render_template('filter.jinja', title="Фільтр тварин", error=error, filtered=filtered, animals=animals)

# Завдання 5: Гра "Камінь-ножиці-папір"
@app.route('/game', methods=['GET', 'POST'])
def game():
    options = ["Камінь", "Ножиці", "Папір"]
    result = None
    user_choice = None
    computer_choice = None

    if request.method == 'POST':
        user_choice = request.form.get('choice')
        computer_choice = random.choice(options)

        if user_choice == computer_choice:
            result = "Нічия"
        elif (user_choice == "Камінь" and computer_choice == "Ножиці") or \
             (user_choice == "Ножиці" and computer_choice == "Папір") or \
             (user_choice == "Папір" and computer_choice == "Камінь"):
            result = "Ви виграли!"
        else:
            result = "Комп'ютер виграв!"

    return render_template('game.jinja', title="Гра: Камінь-ножиці-папір", result=result, user_choice=user_choice, computer_choice=computer_choice, options=options)

# Сторінка 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.jinja', title="Сторінка не знайдена"), 404

if __name__ == '__main__':
    app.run(debug=True)
