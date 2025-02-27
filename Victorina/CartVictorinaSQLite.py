import sqlite3

def create_database():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()

    # Таблица для тем
    c.execute('''CREATE TABLE IF NOT EXISTS themes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL UNIQUE)''')

    # Таблица для вопросов
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  theme_id INTEGER NOT NULL,
                  question TEXT NOT NULL,
                  correct_answer TEXT NOT NULL,
                  FOREIGN KEY (theme_id) REFERENCES themes (id))''')

    conn.commit()
    conn.close()

create_database()


import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

backgound_color = "#F26849"
backgound_letters = "#b3b4bc"
size_botton = "Arial 25"
size_field = "Arial 25"
size_label = "Arial 25"
size_menu = ("Arial", 20)
pady_botton = 20
pady_label = 10
pady_field = 10

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        # Задаём геометрию главному окну.
        root.geometry(self.center_window(200, 200))
        self.create_main_menu()

    def create_main_menu(self):
        # Кнопка для создания темы
        create_theme_button = tk.Button(self.root, text="Создать тему",
                                        command=self.open_create_theme_window,
                                        # width=20, height=2,
                                        font=size_botton)
        create_theme_button.pack(pady=pady_botton)

        # Кнопка для создания вопроса
        create_question_button = tk.Button(self.root, text="Создать вопрос",
                                           command=self.open_create_question_window,
                                           font=size_botton)
        create_question_button.pack(pady=pady_botton)

        # Кнопка для начала игры
        start_game_button = tk.Button(self.root, text="Начать игру",
                                      command=self.open_start_game_window,
                                      font=size_botton)
        start_game_button.pack(pady=pady_botton)

    def open_create_theme_window(self):
        theme_window = tk.Toplevel(self.root)
        theme_window.geometry(self.center_window(200, 200))
        theme_window.title("Создать тему")

        theme_label = tk.Label(theme_window, text="Название темы:", font=size_label)
        theme_label.pack()

        theme_entry = tk.Entry(theme_window, font=size_field)
        theme_entry.pack()

        create_button = tk.Button(theme_window, text="Создать",
                                  command=lambda: self.create_theme(theme_entry.get(), theme_window),
                                  font=size_botton)
        create_button.pack()

    def create_theme(self, theme_name, window):
        if theme_name:
            conn = sqlite3.connect('quiz.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO themes (name) VALUES (?)", (theme_name,))
                conn.commit()
                messagebox.showinfo("Успех", f"Тема '{theme_name}' создана!")
                window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Ошибка", "Такая тема уже существует!")
            conn.close()
        else:
            messagebox.showwarning("Ошибка", "Введите название темы")

    def open_create_question_window(self):
        question_window = tk.Toplevel(self.root)
        question_window.title("Создать вопрос")
        question_window.geometry(self.center_window(200, 200))
        question_window.config(bg=backgound_color)

        theme_label = tk.Label(question_window,
                               text="Выберите тему:",
                               font=size_label,
                               background=backgound_letters,
                               pady=pady_label)
        theme_label.pack()

        self.theme_var = tk.StringVar(question_window)
        self.theme_var.set("Выберите тему")

        themes = self.get_themes()
        theme_menu = tk.OptionMenu(question_window, self.theme_var, *themes)
        theme_menu.config(font=(size_menu)) # Устанавливаем размер выпадающего списка

        menu = question_window.nametowidget(theme_menu['menu'])
        menu.config(font=(size_menu))  # Устанавливаем шрифт для выпадающего списка

        theme_menu.pack()


        question_label = tk.Label(question_window, text="Вопрос:", font=size_label)
        question_label.pack()

        self.question_entry = tk.Entry(question_window, font=size_field)
        self.question_entry.pack()

        correct_answer_label = tk.Label(question_window, text="Правильный ответ:", font=size_label)
        correct_answer_label.pack()

        self.correct_answer_entry = tk.Entry(question_window, font=size_field)
        self.correct_answer_entry.pack()

        create_button = tk.Button(question_window, text="Создать",
                                  command=self.create_question,
                                  font=size_botton)
        create_button.pack()

    def get_themes(self):
        conn = sqlite3.connect('quiz.db')
        c = conn.cursor()
        c.execute("SELECT name FROM themes")
        themes = c.fetchall()
        conn.close()
        return [theme[0] for theme in themes]

    def create_question(self):
        theme_name = self.theme_var.get()
        question_text = self.question_entry.get()
        correct_answer = self.correct_answer_entry.get()

        if theme_name == "Выберите тему":
            messagebox.showwarning("Ошибка", "Выберите тему")
            return

        if not question_text or not correct_answer:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        conn = sqlite3.connect('quiz.db')
        c = conn.cursor()
        c.execute("SELECT id FROM themes WHERE name=?", (theme_name,))
        theme_id = c.fetchone()[0]

        c.execute("INSERT INTO questions (theme_id, question, correct_answer) VALUES (?, ?, ?)",
                  (theme_id, question_text, correct_answer))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Вопрос создан!")
        self.question_entry.delete(0, tk.END)
        self.correct_answer_entry.delete(0, tk.END)

    def open_start_game_window(self):
        game_window = tk.Toplevel(self.root)
        game_window.geometry(self.center_window(200, 200))
        game_window.config(bg=backgound_color)
        game_window.title("Начать игру")

        theme_label = tk.Label(game_window, text="Выберите тему:",
                               font=size_label,
                               pady=pady_label)
        theme_label.pack()

        self.game_theme_var = tk.StringVar(game_window)
        self.game_theme_var.set("Выберите тему")

        themes = self.get_themes()
        theme_menu = tk.OptionMenu(game_window, self.game_theme_var, *themes)
        theme_menu.config(font=(size_menu)) # Устанавливаем размер выпадающего списка

        menu = game_window.nametowidget(theme_menu['menu'])
        menu.config(font=(size_menu))  # Устанавливаем шрифт для выпадающего списка

        theme_menu.pack()

        start_button = tk.Button(game_window, text="Начать",
                                 command=self.start_game,
                                 font=size_botton)
        start_button.pack()

    def start_game(self):
        theme_name = self.game_theme_var.get()
        if theme_name == "Выберите тему":
            messagebox.showwarning("Ошибка", "Выберите тему")
            return

        conn = sqlite3.connect('quiz.db')
        c = conn.cursor()
        c.execute("SELECT id FROM themes WHERE name=?", (theme_name,))
        theme_id = c.fetchone()[0]

        c.execute("SELECT id, question, correct_answer FROM questions WHERE theme_id=?", (theme_id,))
        questions = c.fetchall()
        print("questions", questions)
        conn.close()

        if not questions:
            messagebox.showwarning("Ошибка", "Нет вопросов по выбранной теме")
            return

        self.current_question = random.choice(questions)
        self.show_question(theme_id)

    def show_question(self, theme_id):
        question_window = tk.Toplevel(self.root)
        question_window.geometry(self.center_window(200, 200))
        question_window.config(bg=backgound_color)
        question_window.title("Вопрос")

        question_label = tk.Label(question_window, text=self.current_question[1])
        question_label.pack()


        conn = sqlite3.connect('quiz.db')
        c = conn.cursor()

        # Получаем правильный ответ
        correct_answer = self.current_question[2]

        print("theme_id", theme_id)
        # # Получаем неправильные ответы из других вопросов
        c.execute("SELECT * FROM questions")
        print(c.fetchall())
        # wrong_answers = [answer[0] for answer in set(c.fetchall())]
        # conn.close()
        #
        # # Формируем список всех ответов (правильный + неправильные)
        # all_answers = [correct_answer] + wrong_answers
        # random.shuffle(all_answers)  # Перемешиваем ответы
        #
        # # Ограничиваем количество ответов до 4
        # all_answers = set(all_answers)
        #
        # # Создаем кнопки для каждого ответа
        # for answer in all_answers:
        #     answer_button = tk.Button(question_window, text=answer,
        #                               command=lambda a=answer: self.check_answer(a, question_window))
        #     answer_button.pack()

    def center_window(self, width: int | float, height: int | float) -> str:
        """
        Метод, который принимает желаемые значения высоты и ширины экрана.
        :param width: Ширина.
        :param height: Высота.
        :return: Выводит окно нужных размеров.
        """
        coordinate_x = width_screen - width
        coordinate_y = height_screen - height
        width_size = width * 2
        height_size = height * 2
        return f"{width_size}x{height_size}+{coordinate_x}+{coordinate_y}"

    # def check_answer(self, answer, window):
    #     if answer == self.current_question[2]:
    #         messagebox.showinfo("Результат", "Правильно!")
    #     else:
    #         messagebox.showinfo("Результат", "Неправильно!")
    #     window.destroy()
    #     self.start_game()  # Переход к следующему вопросу

if __name__ == "__main__":
    root = tk.Tk()
    # Константные занчения половины высоты и ширины экрана.
    width_screen = root.winfo_screenwidth() // 2
    height_screen = root.winfo_screenheight() // 2
    app = QuizApp(root)
    root.mainloop()