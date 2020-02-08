import sqlite3 as db
from sqlite3 import Error
from sqlite3 import OperationalError
from sqlite3 import IntegrityError
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk


def sql_connection():       # Соединение с БД
    try:
        con = db.connect('profile.db')
        return con
    except Error:
        print(Error)


def click_add_table():      # Добавление таблицы
    try:
        con = sql_connection()
        cursor_main = con.cursor()
        cursor_main.execute(
            'CREATE TABLE students(id integer PRIMARY KEY AUTOINCREMENT NOT NULL, name text, sex text, class text)')
        con.commit()
        btn_add_table.configure(text="Successful", bg="green")
        btn_delete_table.configure(text="Delete Table", bg="red")
        get_data_combobox()
    except OperationalError:
        print(OperationalError)
        btn_add_table.configure(text="Already Exists", bg="yellow")


def click_delete_table():   # Удаление таблицы
    try:
        con = sql_connection()
        cursor_main = con.cursor()
        cursor_main.execute('DROP TABLE students')
        con.commit()
        btn_delete_table.configure(text="Successful", bg="green")
        btn_add_table.configure(text="Create Table", bg="red")
        get_data_combobox()
    except OperationalError:
        btn_delete_table.configure(text="No Tables", bg="yellow")


def click_data_insert():    # Добавление строки
    try:
        con = sql_connection()
        cursor_main = con.cursor()
        stud = (txt_name.get(), txt_sex.get(), txt_class.get())
        cursor_main.execute('''
            INSERT INTO students (name, sex, class)
            VALUES(:dname, :dsex, :dclass)''',
                           {'dname': stud[0], 'dsex': stud[1], 'dclass': stud[2]})
        con.commit()
        get_data_combobox()
        clear_txt()
    except IntegrityError:
        print(IntegrityError)
        btn_insert_data.configure(text="Error", bg="yellow")


def get_number():           # Узнать количество строк
    con = sql_connection()
    cursor_main = con.cursor()
    cursor_main.execute('SELECT COUNT(*) FROM students')
    return cursor_main.fetchone()[0] + 1


def click_data_get():       # Взять строку из бд
    name_get = combo.get()
    con = sql_connection()
    cursor_main = con.cursor()
    cursor_main.execute('SELECT name, sex, class FROM students WHERE name=:dname', {'dname': name_get})
    stud = cursor_main.fetchone()
    txt_name.insert(0, stud[0])
    txt_sex.insert(0, stud[1])
    txt_class.insert(0, stud[2])
    print(cursor_main.fetchone())


def get_data_combobox():    # Записать имена в комбобокс
    try:
        con = sql_connection()
        cursor_main = con.cursor()
        cursor_main.execute('SELECT name FROM students')
        combo['values'] = cursor_main.fetchall()
        combo.current(0)
    except OperationalError:
        print(OperationalError)
    except TclError:
        print(TclError)


def click_data_delete():    # Удалить строку в бд
    name_get = combo.get()
    con = sql_connection()
    cursor_main = con.cursor()
    cursor_main.execute('DELETE FROM students WHERE name=:dname', {'dname': name_get})
    con.commit()
    get_data_combobox()
    clear_txt()


def click_data_update():    # Обновить строку в бд
    name_get = combo.get()
    con = sql_connection()
    cursor_main = con.cursor()
    stud = (txt_name.get(), txt_sex.get(), txt_class.get())
    cursor_main.execute('''
        UPDATE students SET name=:dname, sex=:dsex, class=:dclass 
        WHERE name=:fname
    ''', {'fname': name_get, 'dname': stud[0], 'dsex': stud[1], 'dclass': stud[2]})
    click_data_get()
    con.commit()
    get_data_combobox()


def clear_txt():            # Очистить текстовые поля
    txt_name.delete(0, END)
    txt_sex.delete(0, END)
    txt_class.delete(0, END)

# Инициализация окна
window = Tk()
window.title("XANTHI")
tabs = ttk.Notebook(window)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tabs.add(tab1, text='Tables')
tabs.add(tab2, text='Data')
# Вкладка 1
btn_add_table = Button(tab1, text="Create Table", bg="red", command=click_add_table)
btn_add_table.grid(column=0, row=0)
btn_delete_table = Button(tab1, text="Delete Table", bg="red", command=click_delete_table)
btn_delete_table.grid(column=0, row=1)
# Вкладка 2
lbl_name = Label(tab2, text="Name", font=("Consolas", 15), fg="red")
lbl_name.grid(column=0, row=0)
lbl_sex = Label(tab2, text="Sex", font=("Consolas", 15), fg="red")
lbl_sex.grid(column=1, row=0)
lbl_class = Label(tab2, text="Class", font=("Consolas", 15), fg="red")
lbl_class.grid(column=2, row=0)
btn_insert_data = Button(tab2, text="Insert Data", bg="green", command=click_data_insert)
btn_insert_data.grid(column=2, row=3)
btn_get_data = Button(tab2, text="Get Data", bg="green", command=click_data_get)
btn_get_data.grid(column=2, row=4)
btn_delete_data = Button(tab2, text="Delete Data", bg="red", command=click_data_delete)
btn_delete_data.grid(column=2, row=6)
btn_update_data = Button(tab2, text="Update Data", bg="yellow", command=click_data_update)
btn_update_data.grid(column=2, row=5)
txt_name = Entry(tab2, width=10)
txt_name.grid(column=0, row=1)
txt_sex = Entry(tab2, width=10)
txt_sex.grid(column=1, row=1)
txt_class = Entry(tab2, width=10)
txt_class.grid(column=2, row=1)
# Инициализация комбобокса
combo = Combobox(tab2)
combo.config(width=8)
combo.grid(column=0, row=3)
get_data_combobox()
window.geometry('410x240')
tabs.pack(expand=1, fill='both')
window.mainloop()
