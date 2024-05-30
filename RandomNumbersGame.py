import random

print("Добро пожаловать в числовую угадайку")

def your_number(num: int, random_n: int):
    random_n = random_n
    num = int(num)
    if num < random_n:
        print("Ваше число меньше загаданного, попробуйте еще разок")
        return False
    elif num > random_n:
        print("Ваше число больше загаданного, попробуйте еще разок")
        return False
    else:
        return True


def valid_n(num: int):
    if 0 < int(num) <= 100:
        return True
    else:
        return False


def valid_int(num):
    if num.isdigit():
        return int(num)
    else:
        return False


def The_Game():
    input_number = input("Введите целое число от 1 до 100: ")
    random_n = random.randint(1, 100)
    total = 0
    while True:
        if valid_int(input_number) == False:
            print("А может быть все-таки введем целое число?")
            input_number = input("Ввод: ")
        elif valid_n(input_number) == False:
            print("От 1 до 100?")
            input_number = input("Ввод: ")
        elif your_number(input_number, random_n) != True:
            input_number = input("Ввод: ")
            total += 1
        elif your_number(input_number, random_n) == True:
            print()
            print("Вы угадали, поздравляем!")
            print(f"Вам потребовалось {total} попыток")
            print()

            break
    answer = input("Желаете продолжить? д/н: ")
    if answer == "д":
        print()
        The_Game()
    else:
        print("Спасибо, что играли в числовую угадайку. Еще увидимся...")

The_Game()