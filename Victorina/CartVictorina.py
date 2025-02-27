import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QComboBox
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Подключение к базе PostgreSQL
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()




# Определение моделей базы данных
class Theme(Base):
    __tablename__ = 'themes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    questions = relationship("Question", back_populates="theme")

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'))
    theme = relationship("Theme", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    is_correct = Column(Integer, nullable=False)  # 1 - правильный, 0 - неправильный
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question", back_populates="answers")

Base.metadata.create_all(engine)

# Окно теста
class QuizWindow(QWidget):
    def __init__(self, theme_id):
        super().__init__()
        self.setWindowTitle("Тестирование")
        self.setGeometry(200, 200, 400, 300)
        self.theme_id = theme_id
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.show_question()

    def show_question(self):
        questions = session.query(Question).filter_by(theme_id=self.theme_id).all()
        if not questions:
            QMessageBox.warning(self, "Ошибка", "В выбранной теме нет вопросов!")
            self.close()
            return

        self.question = random.choice(questions)
        self.label.setText(self.question.text)

        correct_answer = session.query(Answer).filter_by(question_id=self.question.id, is_correct=1).first()
        incorrect_answers = session.query(Answer).filter(Answer.question_id != self.question.id, Answer.is_correct == 1).limit(3).all()

        if len(incorrect_answers) < 3:
            additional_wrong_answers = session.query(Answer).filter(Answer.is_correct == 0).limit(3 - len(incorrect_answers)).all()
            incorrect_answers.extend(additional_wrong_answers)

        answers = [correct_answer] + incorrect_answers
        random.shuffle(answers)

        for btn in self.findChildren(QPushButton):
            self.layout.removeWidget(btn)
            btn.deleteLater()

        for answer in answers:
            btn = QPushButton(answer.text)
            btn.clicked.connect(lambda checked, a=answer: self.check_answer(a))
            self.layout.addWidget(btn)

    def check_answer(self, answer):
        if answer.is_correct:
            QMessageBox.information(self, "Правильно!", "Вы ответили верно!")
        else:
            QMessageBox.warning(self, "Неправильно", "Попробуйте снова!")
        self.show_question()

# Основное окно приложения
class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz App")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.label = QLabel("Выберите действие")
        self.layout.addWidget(self.label)

        self.add_theme_button = QPushButton("Создать тему")
        self.add_theme_button.clicked.connect(self.add_theme)
        self.layout.addWidget(self.add_theme_button)

        self.add_question_button = QPushButton("Добавить вопрос")
        self.add_question_button.clicked.connect(self.add_question)
        self.layout.addWidget(self.add_question_button)

        self.start_button = QPushButton("Начать тест")
        self.start_button.clicked.connect(self.select_theme)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def select_theme(self):
        self.theme_window = QWidget()
        self.theme_window.setWindowTitle("Выберите тему")
        layout = QVBoxLayout()

        self.theme_input = QComboBox()
        themes = session.query(Theme).all()
        for theme in themes:
            self.theme_input.addItem(theme.name, theme.id)
        layout.addWidget(self.theme_input)

        submit_button = QPushButton("Начать тест")
        submit_button.clicked.connect(self.start_quiz)
        layout.addWidget(submit_button)

        self.theme_window.setLayout(layout)
        self.theme_window.show()

    def start_quiz(self):
        self.theme_id = self.theme_input.currentData()
        self.theme_window.close()
        self.quiz_window = QuizWindow(self.theme_id)
        self.quiz_window.show()

    def add_theme(self):
        self.theme_window = QWidget()
        self.theme_window.setWindowTitle("Добавить тему")
        layout = QVBoxLayout()

        self.theme_input = QLineEdit()
        layout.addWidget(self.theme_input)

        submit_button = QPushButton("Сохранить тему")
        submit_button.clicked.connect(self.save_theme)
        layout.addWidget(submit_button)

        self.theme_window.setLayout(layout)
        self.theme_window.show()

    def save_theme(self):
        theme_name = self.theme_input.text()
        if theme_name:
            session.add(Theme(name=theme_name))
            session.commit()
            QMessageBox.information(self, "Успех", "Тема добавлена!")
            self.theme_window.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Введите название темы!")

    def add_question(self):
        self.question_window = QWidget()
        self.question_window.setWindowTitle("Добавить вопрос")
        layout = QVBoxLayout()

        self.theme_select = QComboBox()
        themes = session.query(Theme).all()
        for theme in themes:
            self.theme_select.addItem(theme.name, theme.id)
        layout.addWidget(self.theme_select)

        self.question_input = QLineEdit()
        layout.addWidget(self.question_input)

        self.answer_input = QLineEdit()
        layout.addWidget(self.answer_input)

        submit_button = QPushButton("Сохранить вопрос")
        submit_button.clicked.connect(self.save_question)
        layout.addWidget(submit_button)

        self.question_window.setLayout(layout)
        self.question_window.show()


    def save_question(self):
        question_text = self.question_input.text()
        answer_text = self.answer_input.text()
        theme_id = self.theme_select.currentData()

        if question_text and answer_text:
            question = Question(text=question_text, theme_id=theme_id)
            session.add(question)
            session.commit()

            answer = Answer(text=answer_text, is_correct=1, question_id=question.id)
            session.add(answer)
            session.commit()

            QMessageBox.information(self, "Успех", "Вопрос добавлен!")
            self.question_window.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Введите вопрос и правильный ответ!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec())









# import sys
# import random
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QComboBox
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.orm import sessionmaker, declarative_base, relationship
#
# # Подключение к базе PostgreSQL
# DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base = declarative_base()
#
# # Определение моделей базы данных
# class Theme(Base):
#     __tablename__ = 'themes'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     questions = relationship("Question", back_populates="theme")
#
# class Question(Base):
#     __tablename__ = 'questions'
#     id = Column(Integer, primary_key=True)
#     text = Column(String, nullable=False)
#     theme_id = Column(Integer, ForeignKey('themes.id'))
#     theme = relationship("Theme", back_populates="questions")
#     answers = relationship("Answer", back_populates="question")
#
# class Answer(Base):
#     __tablename__ = 'answers'
#     id = Column(Integer, primary_key=True)
#     text = Column(String, nullable=False)
#     is_correct = Column(Integer, nullable=False)  # 1 - правильный, 0 - неправильный
#     question_id = Column(Integer, ForeignKey('questions.id'))
#     question = relationship("Question", back_populates="answers")
#
# Base.metadata.create_all(engine)
#
# # Основное окно приложения
# class QuizApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Quiz App")
#         self.setGeometry(100, 100, 400, 300)
#
#         self.layout = QVBoxLayout()
#         self.label = QLabel("Выберите действие")
#         self.layout.addWidget(self.label)
#
#         self.add_theme_button = QPushButton("Создать тему")
#         self.add_theme_button.clicked.connect(self.add_theme)
#         self.layout.addWidget(self.add_theme_button)
#
#         self.add_question_button = QPushButton("Добавить вопрос")
#         self.add_question_button.clicked.connect(self.add_question)
#         self.layout.addWidget(self.add_question_button)
#
#         self.start_button = QPushButton("Начать тест")
#         self.start_button.clicked.connect(self.select_theme)
#         self.layout.addWidget(self.start_button)
#
#         self.setLayout(self.layout)
#
    # def add_theme(self):
    #     self.theme_window = QWidget()
    #     self.theme_window.setWindowTitle("Добавить тему")
    #     layout = QVBoxLayout()
    #
    #     self.theme_input = QLineEdit()
    #     layout.addWidget(self.theme_input)
    #
    #     submit_button = QPushButton("Сохранить тему")
    #     submit_button.clicked.connect(self.save_theme)
    #     layout.addWidget(submit_button)
    #
    #     self.theme_window.setLayout(layout)
    #     self.theme_window.show()
    #
    # def save_theme(self):
    #     theme_name = self.theme_input.text()
    #     if theme_name:
    #         session.add(Theme(name=theme_name))
    #         session.commit()
    #         QMessageBox.information(self, "Успех", "Тема добавлена!")
    #         self.theme_window.close()
    #     else:
    #         QMessageBox.warning(self, "Ошибка", "Введите название темы!")
    #
    # def add_question(self):
    #     self.question_window = QWidget()
    #     self.question_window.setWindowTitle("Добавить вопрос")
    #     layout = QVBoxLayout()
    #
    #     self.theme_select = QComboBox()
    #     themes = session.query(Theme).all()
    #     for theme in themes:
    #         self.theme_select.addItem(theme.name, theme.id)
    #     layout.addWidget(self.theme_select)
    #
    #     self.question_input = QLineEdit()
    #     layout.addWidget(self.question_input)
    #
    #     self.answer_input = QLineEdit()
    #     layout.addWidget(self.answer_input)
    #
    #     submit_button = QPushButton("Сохранить вопрос")
    #     submit_button.clicked.connect(self.save_question)
    #     layout.addWidget(submit_button)
    #
    #     self.question_window.setLayout(layout)
    #     self.question_window.show()
    #
    # def save_question(self):
    #     question_text = self.question_input.text()
    #     answer_text = self.answer_input.text()
    #     theme_id = self.theme_select.currentData()
    #
    #     if question_text and answer_text:
    #         question = Question(text=question_text, theme_id=theme_id)
    #         session.add(question)
    #         session.commit()
    #
    #         answer = Answer(text=answer_text, is_correct=1, question_id=question.id)
    #         session.add(answer)
    #         session.commit()
    #
    #         QMessageBox.information(self, "Успех", "Вопрос добавлен!")
    #         self.question_window.close()
    #     else:
    #         QMessageBox.warning(self, "Ошибка", "Введите вопрос и правильный ответ!")

    # def select_theme(self):
    #     self.theme_window = QWidget()
    #     self.theme_window.setWindowTitle("Выберите тему")
    #     layout = QVBoxLayout()
    #
    #     self.theme_input = QComboBox()
    #     themes = session.query(Theme).all()
    #     for theme in themes:
    #         self.theme_input.addItem(theme.name, theme.id)
    #     layout.addWidget(self.theme_input)
    #
    #     submit_button = QPushButton("Начать тест")
    #     submit_button.clicked.connect(self.start_quiz)
    #     layout.addWidget(submit_button)
    #
    #     self.theme_window.setLayout(layout)
    #     self.theme_window.show()
#
#     def start_quiz(self):
#         self.theme_id = self.theme_input.currentData()
#         self.theme_window.close()
#         self.show_question()
#
#     def show_question(self):
#         questions = session.query(Question).filter_by(theme_id=self.theme_id).all()
#         if not questions:
#             QMessageBox.warning(self, "Ошибка", "В выбранной теме нет вопросов!")
#             return
#
#         question = random.choice(questions)
#         self.label.setText(question.text)
#
#         correct_answer = session.query(Answer).filter_by(question_id=question.id, is_correct=1).first()
#         incorrect_answers = session.query(Answer).filter(Answer.is_correct == 1, Answer.question_id != question.id).limit(3).all()
#
#         answers = [correct_answer] + incorrect_answers
#         random.shuffle(answers)
#
#         for btn in self.findChildren(QPushButton):
#             if btn.text() not in ["Создать тему", "Добавить вопрос", "Начать тест"]:
#                 self.layout.removeWidget(btn)
#                 btn.deleteLater()
#
#         for answer in answers:
#             btn = QPushButton(answer.text)
#             btn.clicked.connect(lambda checked, a=answer: self.check_answer(a))
#             self.layout.addWidget(btn)
#
#     def check_answer(self, answer):
#         if answer.is_correct:
#             QMessageBox.information(self, "Правильно!", "Вы ответили верно!")
#         else:
#             QMessageBox.warning(self, "Неправильно", "Попробуйте снова!")
#         self.show_question()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = QuizApp()
#     window.show()
#     sys.exit(app.exec())

























