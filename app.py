import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QListWidget, QStackedWidget, QTextBrowser, QListWidgetItem,
                               QMessageBox, QToolBar, QAction, QSizePolicy, QLineEdit, QTextEdit)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5 import QtGui


class BaseScreen(QWidget):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.layout = QVBoxLayout(self)

    def show_main_screen(self):
        self.app.stacked_widget.setCurrentIndex(0)

    
class SwimDiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Swim Diary")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QtGui.QIcon("wave_icon.png"))

        self.setStyleSheet("QMainWindow::title {background-color: black; color: white;}")
        self.showMaximized()
        self.completed_lessons_label = QLabel(self)
        self.notes_count_label = QLabel(self)

        self.init_lessons_database()
        self.init_completed_lessons_database()
        self.init_notes_database() 

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.set_dark_theme()
        self.setWindowIcon(QIcon('wave_icon.png'))

        self.create_main_screen()
        self.create_completed_lessons_screen()
        self.create_profile_screen()
        self.create_lesson_details_screen()
        self.create_notes_screen() 
        self.create_note_details_screen() 
        self.create_add_note_screen()

        self.create_navigation_toolbar()

        self.stacked_widget.setCurrentIndex(0)
        
    def show_notes_screen(self):
        self.stacked_widget.setCurrentIndex(4)
    def show_add_note_screen(self):
        self.stacked_widget.setCurrentIndex(6) 


    def set_dark_theme(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #2E2E2E;
            color: #FFFFFF;
            padding: 20px;
        }
        QMenuBar {
            background-color: #2E2E2E;
            color: #FFFFFF;
            padding: 10px;
        }
        QMenuBar::item {
            background-color: #2E2E2E;
            color: #FFFFFF;
            padding: 10px 20px;
        }
        QMenuBar::item:selected {
            background-color: #555555;
        }
        QMenu {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QMenu::item {
            background-color: #2E2E2E;
            color: #FFFFFF;
            padding: 10px 20px;
        }
        QMenu::item:selected {
            background-color: #555555;
        }
        QMenuBar, QToolBar {
            background-color: #555555;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 10px;
            padding: 5px;
        }
        QToolBar::handle {
            background-color: #2E2E2E;
            color: #FFFFFF;
            padding: 15px;
        }
        QToolButton {
            background-color: #555555;
            color: #FFFFFF;
            border: 1px solid #555555;
            border-radius: 10px;
            padding: 15px;
        }
        QToolButton:checked {
            background-color: #2E2E2E;
        }
        QStatusBar {
            background-color: #555555;
            color: #FFFFFF;
            padding: 10px;
        }
        QListWidget {
            background-color: #404040;
            color: #FFFFFF;
            border: 1px solid #404040;
            border-radius: 10px;
            padding: 20px;
        }
        QListWidget::item {
            background-color: #2E2E2E;
            color: #FFFFFF;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border: 1px solid #404040;
        }
        QLabel {
            color: #FFFFFF;
            padding: 10px;
        }
        QTextBrowser {
            background-color: #404040;
            color: #FFFFFF;
            border: 1px solid #404040;
            border-radius: 10px;
            padding: 20px;
        }
        QPushButton {
        background-color: #555555;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 5px;
        padding: 10px;
        font-family: Inter;
    }
    QPushButton:hover {
        background-color: #2E2E2E;
    }
    """)

    def update_profile_counts(self):
        completed_lessons_count = self.get_completed_lessons_count()
        total_lessons_count = self.get_total_lessons_count()
        self.completed_lessons_label.setText(f"Количество пройденных уроков: {completed_lessons_count}/{total_lessons_count}")

        notes_count = self.get_notes_count()
        self.notes_count_label.setText(f"Количество заметок: {notes_count}")

    def init_lessons_database(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('lessons.db')
        if not db.open():
            print("Cannot open database")
            return False

        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")

        query.exec_("SELECT COUNT(*) FROM lessons")
        query.next()
        if query.value(0) == 0:
            lessons_data = [
            ("Введение в плавание", "Основы плавания, правильное дыхание и позиция тела в воде."),
            ("Стрельба ногами", "Техника движения ногами при плавании на спине и на груди."),
            ("Кроль", "Обучение технике плавания кролем, различные подвижные элементы."),
            ("Брасс", "Освоение стиля брасс, коррекция движений рук и ног."),
            ("Баттерфляй", "Техника баттерфляя и ее особенности."),
            ("Спасательные приемы", "Основы безопасности в воде и спасательные приемы."),
            ("Длинные дистанции", "Тренировка выносливости и техники длиннопрофильного плавания."),
            ("Старт с блока", "Правильная техника старта с бокса и плавный вход в воду."),
            ("Силовые тренировки", "Укрепление мышц, необходимых для успешного плавания."),
            ("Техника плавания в открытой воде", "Особенности плавания в озерах, реках и морях."),
            ("Плавание с маской и трубкой", "Освоение техники плавания с маской и дыхательной трубкой."),
            ("Плавание с ластами", "Тренировки с ластами для улучшения силы и техники ног."),
            ("Тренировки на скорость", "Методики тренировок для улучшения плавательной скорости."),
            ("Игры в воде", "Развлекательные упражнения для разнообразия тренировок."),
            ("Техника взятия глубины", "Учимся плавать в глубокой воде и преодолевать страх перед глубиной."),
            ("Плавание на спине", "Освоение техники плавания на спине и коррекция движений."),
            ("Плавание под водой", "Тренировки на удержание дыхания и плавание под водой."),
            ("Работа с плавательными инструментами", "Использование плавательных досок, ласт и других инструментов."),
            ("Плавание в группе", "Освоение навыков плавания в группе и синхронные движения."),
            ("Плавание на дистанции с препятствиями", "Преодоление препятствий во время плавания."),
            ("Техника отдыха в воде", "Учимся правильно отдыхать и восстанавливаться в воде."),
            ("Плавание с детьми", "Основы безопасного плавания с детьми и обучение детей плаванию."),
            ("Техника плавания на короткие дистанции", "Тренировки на улучшение скорости на коротких дистанциях."),
            ("Завершающие уроки и оценка прогресса", "Подведение итогов обучения, оценка прогресса и рекомендации для дальнейших тренировок.")
            ]

            for lesson in lessons_data:
                query.exec_("INSERT INTO lessons (name, description) VALUES ('{}', '{}')".format(lesson[0], lesson[1]))

    def init_completed_lessons_database(self):
        db = QSqlDatabase.addDatabase('QSQLITE', 'completed_lessons')
        db.setDatabaseName('completed_lessons.db')
        if not db.open():
            print("Cannot open completed_lessons database")
            return False

        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS completed_lessons (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")

    def init_notes_database(self):
        db = QSqlDatabase.addDatabase('QSQLITE', 'notes')
        db.setDatabaseName('notes.db')
        if not db.open():
            print("Cannot open notes database")
            return False

        query = QSqlQuery()
        query.exec_("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")

    def load_lessons(self):
        query = QSqlQuery("SELECT name FROM lessons")
        while query.next():
            lesson_name = query.value(0)
            item = QListWidgetItem(lesson_name)
            self.lessons_list.addItem(item)
            self.apply_rounded_style(item)

    def apply_rounded_style(self, item):
        item.setData(Qt.UserRole, "rounded")

    def show_lesson_details(self, item):
        lesson_name = item.text()

        if self.is_lesson_completed(lesson_name):
            self.show_completed_lesson_details(lesson_name)
        else:
            self.show_incomplete_lesson_details(lesson_name)

    def show_completed_lesson_details(self, lesson_name):
        self.lesson_name_label.setText(lesson_name)
        query = QSqlQuery(f"SELECT description FROM lessons WHERE name = '{lesson_name}'")
        if query.next():
            lesson_description = query.value(0)
            self.lesson_description_browser.setPlainText(lesson_description)
        self.complete_lesson_button.setText("Урок выполнен")
        self.complete_lesson_button.setEnabled(False)

        self.stacked_widget.setCurrentIndex(3)
    def show_incomplete_lesson_details(self, lesson_name):
        self.lesson_name_label.setText(lesson_name)
        query = QSqlQuery(f"SELECT description FROM lessons WHERE name = '{lesson_name}'")
        if query.next():
            lesson_description = query.value(0)
            self.lesson_description_browser.setPlainText(lesson_description)
        self.complete_lesson_button.setText("Выполнить урок")
        self.complete_lesson_button.setEnabled(True) 
        self.stacked_widget.setCurrentIndex(3)

    def is_lesson_completed(self, lesson_name):
        query = QSqlQuery(f"SELECT COUNT(*) FROM completed_lessons WHERE name = '{lesson_name}'")
        query.next()
        return query.value(0) > 0

    def create_main_screen(self):
        main_screen = QWidget(self)
        layout = QVBoxLayout(main_screen)
        title_label = QLabel("Уроки по плаванию", main_screen)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: 18pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        self.lessons_list = QListWidget(main_screen)
        self.load_lessons()
        self.lessons_list.itemClicked.connect(self.show_lesson_details)
        layout.addWidget(self.lessons_list)
        self.stacked_widget.addWidget(main_screen)

    def load_completed_lessons(self):
        query = QSqlQuery("SELECT name FROM completed_lessons")
        while query.next():
            lesson_name = query.value(0)
            item = QListWidgetItem(lesson_name)
            self.completed_lessons_list.addItem(item)
            self.apply_rounded_style(item)

    def create_completed_lessons_screen(self):
        completed_lessons_screen = BaseScreen(self)
        title_label = QLabel("Выполненные уроки", completed_lessons_screen)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: 18pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        completed_lessons_screen.layout.addWidget(title_label)
        self.completed_lessons_list = QListWidget(completed_lessons_screen)
        self.load_completed_lessons()
        completed_lessons_screen.layout.addWidget(self.completed_lessons_list)
        self.stacked_widget.addWidget(completed_lessons_screen)

    def get_completed_lessons_count(self):
        query = QSqlQuery("SELECT COUNT(*) FROM completed_lessons")
        query.next()
        return query.value(0)

    def get_total_lessons_count(self):
        query = QSqlQuery("SELECT COUNT(*) FROM lessons")
        query.next()
        return query.value(0)

    def update_lessons_list(self):
        self.completed_lessons_list.clear()
        self.load_completed_lessons()

    def create_profile_screen(self):
        profile_screen = BaseScreen(self)
        title_label = QLabel("Мой профиль", profile_screen)
        title_label.setFont(QFont("Inter", 25, QFont.Bold))
        title_label.setAlignment(Qt.AlignHCenter)
        profile_screen.layout.addWidget(title_label)
        profile_icon_label = QLabel(profile_screen)
        profile_pixmap = QPixmap('profile_pic.png')
        profile_icon_label.setPixmap(profile_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        profile_icon_label.setAlignment(Qt.AlignHCenter)
        profile_screen.layout.addWidget(profile_icon_label)
        self.completed_lessons_label = QLabel(profile_screen)
        self.completed_lessons_label.setStyleSheet("font: 12pt 'Inter'; margin-top: 10px;")
        self.completed_lessons_label.setAlignment(Qt.AlignHCenter)
        profile_screen.layout.addWidget(self.completed_lessons_label)
        self.notes_count_label = QLabel(profile_screen)
        self.notes_count_label.setStyleSheet("font: 12pt 'Inter'; margin-top: 5px;")
        self.notes_count_label.setAlignment(Qt.AlignHCenter)
        profile_screen.layout.addWidget(self.notes_count_label)
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        profile_screen.layout.addWidget(spacer)
        self.stacked_widget.addWidget(profile_screen)

    def create_lesson_details_screen(self):
        lesson_details_screen = BaseScreen(self)
        self.lesson_name_label = QLabel(lesson_details_screen)
        self.lesson_name_label.setStyleSheet("font: 18pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        lesson_details_screen.layout.addWidget(self.lesson_name_label)
        self.lesson_description_browser = QTextBrowser(lesson_details_screen)
        self.lesson_description_browser.setStyleSheet("font: 13pt 'Inter'; font-weight: light; margin-bottom: 10px;")
        lesson_details_screen.layout.addWidget(self.lesson_description_browser)
        self.complete_lesson_button = QPushButton("Выполнить урок", lesson_details_screen)
        self.complete_lesson_button.clicked.connect(self.complete_lesson)
        lesson_details_screen.layout.addWidget(self.complete_lesson_button)
        self.stacked_widget.addWidget(lesson_details_screen)

    def create_notes_screen(self):
        notes_screen = BaseScreen(self)
        title_label = QLabel("Заметки о тренировках", notes_screen)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: 18pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        notes_screen.layout.addWidget(title_label)
        self.notes_list = QListWidget(notes_screen)
        self.load_notes()
        self.notes_list.itemClicked.connect(self.show_note_details)
        notes_screen.layout.addWidget(self.notes_list)
        add_note_button = QPushButton(QIcon('plus_icon.png'), "Добавить заметку", notes_screen)
        add_note_button.clicked.connect(self.show_add_note_screen)
        add_note_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 10px; 
                padding: 10px;
                font-family: Inter;
            }
            QPushButton:hover {
                background-color: #2E2E2E;
            }
        """)
        notes_screen.layout.addWidget(add_note_button)
        self.stacked_widget.addWidget(notes_screen)


    def get_notes_count(self):
        query = QSqlQuery("SELECT COUNT(*) FROM notes")
        query.next()
        return query.value(0)
    
    def create_add_note_screen(self):
        add_note_screen = BaseScreen(self)
        title_label = QLabel("Создание новой заметки", add_note_screen)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font: 18pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        add_note_screen.layout.addWidget(title_label)
        name_label = QLabel("Имя заметки:", add_note_screen)
        name_label.setStyleSheet("font: 15pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        add_note_screen.layout.addWidget(name_label)
        self.note_name_input = QLineEdit(add_note_screen)
        self.note_name_input.setStyleSheet("""
        QLineEdit {
            background-color: #404040;
            color: #FFFFFF;
            border: 1px solid #404040;
            border-radius: 5px;
            padding: 8px;
            font-family: Inter;
        }
        QLineEdit:focus {
            border: 2px solid #45aaf2;
        }
    """)
        add_note_screen.layout.addWidget(self.note_name_input)
        description_label = QLabel("Описание:", add_note_screen)
        description_label.setStyleSheet("font: 15pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        add_note_screen.layout.addWidget(description_label)
        self.note_description_input = QTextEdit(add_note_screen)
        self.note_description_input.setStyleSheet("""
        QTextEdit {
            background-color: #404040;
            color: #FFFFFF;
            border: 1px solid #404040;
            border-radius: 5px;
            padding: 8px;
            font-family: Inter;
        }
        QTextEdit:focus {
            border: 2px solid #45aaf2;
        }
    """)
        add_note_screen.layout.addWidget(self.note_description_input)
        create_note_button = QPushButton("Создать заметку", add_note_screen)
        create_note_button.clicked.connect(self.create_note)
        create_note_button.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 10px; 
                padding: 10px;
                font-family: Inter;
            }
            QPushButton:hover {
                background-color: #2E2E2E;
            }
        """)
        add_note_screen.layout.addWidget(create_note_button)
        self.stacked_widget.addWidget(add_note_screen)

    def create_note(self):
        note_name = self.note_name_input.text()
        note_description = self.note_description_input.toPlainText()
        if note_name and note_description:
            query = QSqlQuery(f"INSERT INTO notes (name, description) VALUES ('{note_name}', '{note_description}')")
            if query.isActive():
                print(f"Note '{note_name}' added!")
                QMessageBox.information(self, 'Заметка добавлена', f'Заметка "{note_name}" успешно добавлена!')
                self.update_notes_list()
                self.show_notes_screen()
                self.update_profile_counts()

    def update_notes_list(self):
        self.notes_list.clear()
        self.load_notes()

    def create_note_details_screen(self):
        note_details_screen = BaseScreen(self)
        self.note_name_label = QLabel(note_details_screen)
        self.note_name_label.setStyleSheet("font: 18pt 'Inter'; font-weight: bold; margin-bottom: 10px;")
        note_details_screen.layout.addWidget(self.note_name_label)
        self.note_description_browser = QTextBrowser(note_details_screen)
        self.note_description_browser.setStyleSheet("font: 13pt 'Inter'; font-weight: light; margin-bottom: 10px;")
        note_details_screen.layout.addWidget(self.note_description_browser)
        self.stacked_widget.addWidget(note_details_screen)

    def load_notes(self):
        query = QSqlQuery("SELECT name FROM notes")
        while query.next():
            note_name = query.value(0)
            item = QListWidgetItem(note_name)
            self.apply_rounded_style(item)
            self.notes_list.addItem(item)

    def show_note_details(self, item):
        note_name = item.text()
        self.note_name_label.setText(note_name)
        query = QSqlQuery(f"SELECT description FROM notes WHERE name = '{note_name}'")
        if query.next():
            note_description = query.value(0)
            self.note_description_browser.setPlainText(note_description)
        self.stacked_widget.setCurrentIndex(5) 

    def create_navigation_toolbar(self):
        navigation_toolbar = QToolBar(self)
        navigation_toolbar.setMovable(False)
        self.addToolBar(Qt.BottomToolBarArea, navigation_toolbar)
        navigation_toolbar.setStyleSheet("QToolBar { border: 20px; background-color: #555555; }")
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        navigation_toolbar.addWidget(spacer)
        completed_lessons_action = QAction(QIcon('dialog-ok-apply.png'), "Выполненные уроки", self)
        completed_lessons_action.triggered.connect(self.show_completed_lessons)
        navigation_toolbar.addAction(completed_lessons_action)
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        navigation_toolbar.addWidget(spacer)
        home_action = QAction(QIcon('go-home.png'), "Главный экран", self)
        home_action.triggered.connect(self.show_main_screen)
        navigation_toolbar.addAction(home_action)
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        navigation_toolbar.addWidget(spacer)
        profile_action = QAction(QIcon('preferences-system.png'), "Мой профиль", self)
        profile_action.triggered.connect(self.show_profile)
        navigation_toolbar.addAction(profile_action)
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        navigation_toolbar.addWidget(spacer)
        notes_action = QAction(QIcon('notes_icon.png'), "Заметки", self)
        notes_action.triggered.connect(self.show_notes_screen)
        navigation_toolbar.addAction(notes_action)
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        navigation_toolbar.addWidget(spacer)

    def show_main_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_completed_lessons(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_profile(self):
        self.stacked_widget.setCurrentIndex(2)

    def complete_lesson(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index == 3:
            lesson_name = self.lesson_name_label.text()
            query = QSqlQuery(f"INSERT INTO completed_lessons (name) VALUES ('{lesson_name}')")
            if query.isActive():
                print(f"Lesson '{lesson_name}' completed!")
                QMessageBox.information(self, 'Урок выполнен', f'Урок "{lesson_name}" успешно выполнен!')
                self.update_lessons_list()
                self.show_completed_lessons()
                self.update_profile_counts() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    swim_diary_app = SwimDiaryApp()
    swim_diary_app.show()
    sys.exit(app.exec_())
