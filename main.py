import tkinter
from datetime import datetime
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import create_engine, Column, String, Integer,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from CTkMenuBar import *
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.dates import date2num
from matplotlib.ticker import MaxNLocator
from collections import defaultdict
import customtkinter

# Создание базового класса для описания таблицы
Base = declarative_base()


# Определение класса для таблицы настроений
class MoodEntry(Base):
    __tablename__ = 'mood_entries'
    id = Column(Integer, primary_key=True)
    mood = Column(String)
    comment = Column(String)
    user_id = Column(Integer)
    creation_time = Column(DateTime)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    name= Column(String)



# Установка соединения с базой данных
DATABASE_URL = 'postgresql://postgres:0404@localhost:5433/postgres'
engine = create_engine(DATABASE_URL)

# Создание таблицы, если она не существует
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()



def open_settings():
    # Здесь можно добавить логику открытия страницы настроек
    print("Открыть настройки")




def register_user():
    # Создаем новое окно для регистрации
    register_window = ctk.CTk()
    register_window.title("Регистрация")
    register_window.geometry("300x200")

    # Функция для обработки регистрации
    def submit_registration():
        # Получаем данные из полей ввода
        username = username_entry.get()
        password = password_entry.get()

        # Проверяем, что поля не пусты
        if username and password:
            # Проверяем, что пользователя с таким именем еще нет в базе данных
            existing_user = session.query(Users).filter_by(username=username).first()
            if existing_user:
                tkinter.messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует")
            else:
                # Создаем нового пользователя и сохраняем его в базе данных
                new_user = Users(username=username, password=password)
                session.add(new_user)
                session.commit()

                # Выводим сообщение об успешной регистрации
                tkinter.messagebox.showinfo("Успешно", "Пользователь зарегистрирован!")
                # Закрываем окно регистрации
                register_window.destroy()
        else:
            tkinter.messagebox.showerror("Ошибка", "Поля не должны быть пустыми")

    # Поля ввода для имени пользователя и пароля
    username_label = ctk.CTkLabel(register_window, text="Имя пользователя:")
    username_label.pack()
    username_entry = ctk.CTkEntry(register_window)
    username_entry.pack()

    password_label = ctk.CTkLabel(register_window, text="Пароль:")
    password_label.pack()
    password_entry = ctk.CTkEntry(register_window, show="*")  # Скрываем ввод пароля
    password_entry.pack()

    # Кнопка "Зарегистрироваться"
    register_button = ctk.CTkButton(register_window, text="Зарегистрироваться", command=submit_registration)
    register_button.pack()

    # Запускаем цикл обработки событий для окна регистрации
    register_window.mainloop()
def login():
    login_window = ctk.CTk()
    login_window.title("Вход в приложение")
    login_window.geometry("300x200")  # Увеличил высоту окна для помещения двух кнопок

    username_label = ctk.CTkLabel(login_window, text="Имя пользователя:")
    username_label.pack()

    username_entry = ctk.CTkEntry(login_window)
    username_entry.pack()

    password_label = ctk.CTkLabel(login_window, text="Пароль:")
    password_label.pack()

    password_entry = ctk.CTkEntry(login_window, show="*")
    password_entry.pack()

    def submit_login():

        username = username_entry.get()
        password = password_entry.get()
        user_id = check_user_credentials(username, password)
        if user_id is not None:
            login_window.destroy()
            main_app(user_id, username)
    login_button = ctk.CTkButton(login_window, text="Войти", command=submit_login)
    login_button.pack(pady=10)
    register_button = ctk.CTkButton(login_window, text="Нет аккаунта", command=register_user)
    register_button.pack()
    login_window.mainloop()




def check_user_credentials(username, password):
    user = session.query(Users).filter_by(username=username).first()
    if user and user.password == password:
        return user.id
    else:
        return None

def main_app(user_id, username):
    root = ctk.CTk()
    root.title("ТехОсмотр")
    root.geometry("1100x580")

    # Создаем меню бар
    menu = CTkTitleMenu(master=root)
    def exit_app():
        root.destroy()

    mood_options = ["65111", "43114"]
    mood_label = ctk.CTkLabel(root, text="Выберите модель Камаза:")
    mood_label.grid(row=1, column=0, padx=50, pady=10)
    mood_dropdown = ctk.CTkComboBox(root, values=mood_options)
    mood_dropdown.grid(row=2, column=0, padx=50, pady=10)

    vid_to = ["Ежедневное техническое обслуживание (ЕТО)", "Первое техническое обслуживание (ТО-1)", "Второе техническое обслуживание (ТО-2)", "Сезонное техническое обслуживание (СТО)", "Дополнительные работы, выполняемые один раз в год, осенью", "Техническое обслуживание, выполняемое один раз в два года", "Техническое обслуживание ТО-1000", "Техническое обслуживание ТО-5500"]
    mood_label = ctk.CTkLabel(root, text="Выберите вид ТО:")
    mood_label.grid(row=3, column=0, padx=50, pady=10)
    vid_dropdown = ctk.CTkComboBox(root, values=vid_to)
    vid_dropdown.grid(row=4, column=0, padx=50, pady=10)

    def display_text():
        selected_mood = mood_dropdown.get()
        selected_vid_to = vid_dropdown.get()

        # Clear previous text in the label
        text_label['text'] = ""

        if selected_mood == "65111" and selected_vid_to == "Ежедневное техническое обслуживание (ЕТО)":
            filename = "text_file.txt"  # Specify your text file name
            try:
                with open(filename, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        # Create a checkbox for each line of text
                        checkbox = customtkinter.CTkCheckBox(root, text=line.strip())
                        checkbox.grid(row=1,column=2)

            except FileNotFoundError:
                text_label.config(text="Файл не найден.")
        else:
            text_label.config(text="Другой текст или обработка")

    display_button = ctk.CTkButton(root, text="Дальше", command=display_text)
    display_button.grid(row=5, column=0, columnspan=2, pady=10)

    text_label = ctk.CTkLabel(root, text="")
    text_label.grid(row=1, column=3, columnspan=5, pady=10)

    button_1 = menu.add_cascade("настройки")
    button_3 = menu.add_cascade("аккаунт")
    button_2 = menu.add_cascade("выход")
    button_2_dropdown = CustomDropdownMenu(widget=button_2)
    button_2_dropdown.add_option(option="Выход из приложения", command=exit_app)

    dropdown1 = CustomDropdownMenu(widget=button_1)
    dropdown1.add_option(option="Открыть", command=lambda: print("Open"))
    dropdown1.add_option(option="чет еще")

    dropdown3 = CustomDropdownMenu(widget=button_3)
    dropdown3.add_option(option="войти",command=login)
    dropdown3.add_option(option="мой аккаунт", command=lambda: show_account_info(username, user_id, root))

    root.mainloop()


def show_account_info(username, user_id, main_root):
    def go_back_to_main():
        account_window.destroy()
        main_root.deiconify()

    def change_name(new_name):
        if new_name:
            user.name = new_name
            session.commit()
            tkinter.messagebox.showinfo("Успешно", "Имя пользователя успешно изменено")
        else:
            tkinter.messagebox.showerror("Ошибка", "Имя пользователя не может быть пустым")

    account_window = ctk.CTk()
    account_window.title("Мой аккаунт")
    account_window.geometry("1100x580")

    user = session.query(Users).filter_by(username=username).first()

    if user:
        menu = CTkTitleMenu(master=account_window)
        button_2 = menu.add_cascade("Домой")
        button_2_dropdown = CustomDropdownMenu(widget=button_2)
        button_2_dropdown.add_option(option="Домой", command=go_back_to_main)

        # Блок информации о пользователе
        user_info_frame = ctk.CTkFrame(account_window)
        user_info_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=20)

        username_label = ctk.CTkLabel(user_info_frame, text=f"Здравствуйте: {user.name}")
        username_label.pack()

        username_label = ctk.CTkLabel(user_info_frame, text=f"Логин пользователя: {user.username}")
        username_label.pack()

        # Блок смены имени
        row = 2
        new_name_label = ctk.CTkLabel(account_window, text="Новое имя:")
        new_name_entry = ctk.CTkEntry(account_window)
        change_name_button = ctk.CTkButton(account_window, text="Сменить имя", command=lambda: change_name(new_name_entry.get()))
        new_name_label.grid(row=row, column=0, sticky="e")
        new_name_entry.grid(row=row, column=1, padx=10)
        change_name_button.grid(row=row, column=2, padx=10)
        row += 1

        # Блок смены пароля
        new_password_label = ctk.CTkLabel(account_window, text="Новый пароль:")
        new_password_entry = ctk.CTkEntry(account_window, show="*")
        change_password_button = ctk.CTkButton(account_window, text="Сменить пароль", command=lambda: change_password(user, new_password_entry.get()))
        new_password_label.grid(row=row, column=0, padx=5)
        new_password_entry.grid(row=row, column=1)
        change_password_button.grid(row=row, column=2, pady=10)
        row += 1

        # Блок статистики настроений
        mood_stats_label = ctk.CTkLabel(account_window, text="Статистика настроений:")
        mood_stats_label.grid(row=row, column=1, pady=20)
        row += 1

        user_mood_entries = session.query(MoodEntry).filter_by(user_id=user.id).all()

        mood_count = {"Радость": 0, "Грусть": 0, "Раздражение": 0, "Удовлетворение": 0, "Тоска": 0}

        for mood_entry in user_mood_entries:
            mood = mood_entry.mood
            if mood in mood_count:
                mood_count[mood] += 1

        # Убираем нулевые значения из словаря
        non_zero_mood_count = {mood: count for mood, count in mood_count.items() if count > 0}

        mood_stats_frame = ctk.CTkFrame(account_window)
        mood_stats_frame.grid(row=row, column=0, columnspan=3)

        if non_zero_mood_count:
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#242424')

            ax.pie(non_zero_mood_count.values(), labels=non_zero_mood_count.keys(), autopct='%1.1f%%', startangle=90, textprops={'color': 'white', 'fontsize': 12})
            ax.axis('equal')

            canvas = FigureCanvasTkAgg(fig, master=mood_stats_frame)
            canvas.get_tk_widget().pack()
        else:
            no_data_label = ctk.CTkLabel(mood_stats_frame, text="Нет данных для отображения")
            no_data_label.pack(pady=20)

    else:
        error_label = ctk.CTkLabel(account_window, text="Ошибка: Пользователь не найден")
        error_label.grid(row=1, column=1, pady=20)

    account_window.protocol("WM_DELETE_WINDOW", go_back_to_main)
    main_root.withdraw()
    account_window.mainloop()


def change_password(user, new_password):
    if not new_password:
        tkinter.messagebox.showerror("Ошибка", "Введите новый пароль.")
        return

    if user:
        user.password = new_password
        session.commit()
        tkinter.messagebox.showinfo("Успешно", "Пароль успешно изменен!")
    else:
        tkinter.messagebox.showerror("Ошибка", "Пользователь не найден.")



login()