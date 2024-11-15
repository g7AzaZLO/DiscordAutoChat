from deep_translator import GoogleTranslator
from random import choice, sample
from string import punctuation
from swift import words

# Генератор текста
def generatetext():
    try:
        s1 = list(filter(lambda x: x not in punctuation, words))  # Убираем знаки препинания
        s2 = sample(s1, choice(range(5, 15)))  # Выбираем случайное количество слов
        s2[0] = s2[0].capitalize()  # Первое слово с заглавной буквы
        return ' '.join(s2) + '.'  # Возвращаем текст с точкой в конце
    except Exception as e:
        print(f"[X] Ошибка генерации текста: {e}")
        return "Ошибка генерации текста."

# Основная функция перевода текста
def main():
    try:
        text = generatetext()
        print(f"[X] Сгенерированный текст: {text}")
        translated = GoogleTranslator(source='auto', target='cn').translate(text)
        print(f"[X] Переведённый текст: {translated}")
        return translated
    except Exception as e:
        print(f"[X] Ошибка в генерации или переводе: {e}")
        return "Ошибка перевода."

