import random


# def num_valid_int(num: str):
#     return num.isdigit()


def choice(answers):
    answers = ["Бесспорно", "Мне кажется - да", "Пока неясно, попробуй снова", "Даже не думай",
           "Предрешено", "Вероятнее всего", "Спроси позже", "Мой ответ - нет",
           "Никаких сомнений", "Хорошие перспективы", "Лучше не рассказывать", "По моим данным - нет",
           "Можешь быть уверен в этом", "Да", "Сконцентрируйся и спроси опять", "Весьма сомнительно"]
    return answers[random.randint(1, 20)]


def The_Game():
    print("Привет Мир!")
    name = input("Напиши своё имя: ")
    print(f"Привет {name}, я магический шар, и я знаю ответ на любой твой вопрос.")
    while True:
        print("Напиши, что ты хочешь узнать: ")
        qustion = print(choice(input()))
        print("Хочешь продолжить? д/н")
        answer = input()
        if answer == "д":
            continue
        else:
            print("Надеюсь, мои ответы тебе помогли")
            break




The_Game()