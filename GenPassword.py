# Модуль вызваный для генерации случайных паролей.
from random import randint


# Функция для создания определённого количества паролей определённой длины, из списка возможных для генерации элементов.
def password(count_el: int, lengs: int, chars: list):
    list_pass = []
    while count_el:
        for i in range(lengs):
            list_pass.append(chars [ randint( 0, len(chars) - 1 ) ] )
        if count_el != 1:
            list_pass.append(", ")
        count_el -= 1
    return list_pass


# Функция для провекрки интовости вводимых символов и возвращение в виде булево значения.
def valid_num(num: str):
    if num.isdigit():
        return int(num)
    else:
        return False

# Знакомство с пользователем.
# Вынесено за пределы какой либо из функций, дабы не повторялось при провторном использовании программы.
print("Программа служит для создания случайных паролей. \nСейчас вам предстоит ответить на несколько вопросов.")


# Функция запрашивает у поьлзователя количество паролей для генерации, длину паролей,
# а также набор элементов которые должны входить в пароль.
def gen_password():
    # Цикл проверяющий яляется ли ввод пользователя интовым значением.
    count_el = input("Количество паролей для генерации: ")
    while True:
        if valid_num(count_el) == False:
            print("Нужно ввести число: ")
            count_el = input("Ввод: ")
        else:
            count_el = int(count_el)
            break

    # Цикл проверяющий яляется ли ввод пользователя интовым значением.
    lengs = input("Введите длину пароля: ")
    while True:
        if valid_num(lengs) == False:
            print("Нужно ввести число: ")
            lengs = input("Ввод: ")
        else:
            lengs = int(lengs)
            break

    # Элементы, которые можно добавить в список для генерации паролей.
    elements = []
    digits = "0123456789"
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    punctuation = "!#$%&*+-=?@^_."
    dual_symbols = [ "i", "l", "1", "L", "o", "0", "O" ]

    # Цикл, на протяжении которого, у пользователя спрашивается, какие элементы должен или не должен содержать пароль.
    # После чего, они заносятся в список, который в последствии передаётся функции "password".
    while True:
        qustion = input("Включать ли цифры 0123456789? да\нет ")
        if qustion == "да":
            elements.extend(digits)
        qustion_2 = input("Включать ли прописные буквы ABCDEFGHIJKLMNOPQRSTUVWXYZ? да\нет ")
        if qustion_2 == "да":
            elements.extend(lowercase_letters)
        qustion_3 = input("Включать ли строчные буквы abcdefghijklmnopqrstuvwxyz? да\нет ")
        if qustion_3 == "да":
            elements.extend(uppercase_letters)
        qustion_4 = input("Включать ли символы !#$%&*+-=?@^_? да\нет ")
        if qustion_4 == "да":
            elements.extend(punctuation)
        if len(elements) > 0:
            qustion_5 = input("Исключать ли неоднозначные символы il1Lo0O?A да\нет ")
            if qustion_5 == "да":
                for j in range(len(dual_symbols)):
                    if dual_symbols[j] in elements:
                        elements.remove(dual_symbols[j])
        # Выпадает исключение, если пользователь не выбрал ни одного символа.
        else:
            print()
            print("Вы не выбрали ни одого символа для генерации пароля")
            break
        print()
        # Пользователю предоставляются сгенерированные пароли, по его выбору.
        print("Сгенерированные пароли: ", *password(count_el, lengs, elements), sep="")
        break
    print()

    # Запрос на повтор операции по генерации паролей.
    qustion_6 = input("Хотите ещё раз попробовать? да\нет ")
    if qustion_6 == "да":
        gen_password()
    else:
        print("Спасибо за тестирование нашей программы! Ещё увидимся)")


gen_password()