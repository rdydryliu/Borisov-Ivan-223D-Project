from tkinter import *
import sqlite3
from tkinter import ttk


def clear_window():
    """
    Эта функция очищает окно от виджетов
    """
    for widget in window.slaves():
        widget.destroy()


def check(arg):
    """
    Эта функция в зависимости от вызванного аргумента выводит всю базу данных, сортируя её
    """
    clear_window()
    con = sqlite3.connect("students.db")
    cur = con.cursor()
    selection = ''
    if arg == '':
        selection = "SELECT name, second_name, grade FROM Math_grades"
    elif arg == 'name':
        selection = "SELECT name, second_name, grade FROM Math_grades ORDER BY name"
    elif arg == 'second_name':
        selection = "SELECT name, second_name, grade FROM Math_grades ORDER BY second_name"
    elif arg == 'grade':
        selection = "SELECT name, second_name, grade FROM Math_grades ORDER BY grade"
    res = cur.execute(selection)
    stud = res.fetchall()
    con.close()
    names_list = []
    name, second_name, grade = zip(*stud)
    for i in range(len(name)):
        names = name[i] + ' ' + second_name[i] + ' ' + str(grade[i])
        names_list += names,
    names_var = StringVar(value=names_list)
    listbox = Listbox(listvariable=names_var)
    listbox.pack(anchor='center', pady=10)
    scrollbar = ttk.Scrollbar(orient="vertical", command=listbox.yview)
    scrollbar.pack(anchor='center', pady=10)
    listbox["yscrollcommand"] = scrollbar.set
    btn2 = ttk.Button(text='Назад', command=lambda: check_all())
    btn2.pack(anchor='center', pady=10)


def append(name, second_name, grade):
    """
    Эта функция добавляет в таблицу новую строку, если она не является пустой
    """
    try:
        if name == '' or second_name == '' or grade == '' and int(grade) < 0:
            append_student()
        else:
            names = name[0].upper()
            for i in range(len(name)-1):
                names += name[i+1].lower()
            second_names = second_name[0].upper()
            for n in range(len(second_name)-1):
                second_names += second_name[n + 1].lower()
            con = sqlite3.connect("students.db")
            cur = con.cursor()
            cur.execute(f"""
                INSERT INTO Math_grades VALUES
                    ('{names}', '{second_names}', {grade})
            """)
            con.commit()
            con.close()
            append_student()
    except (ValueError, sqlite3.OperationalError):
        append_student()


def found(name, second_name, grade):
    """
    Эта функция позволяет искать строку по разным аргументам
    """
    try:
        clear_window()
        con = sqlite3.connect("students.db")
        cur = con.cursor()
        if name == '' and second_name == '':
            selection = f"select * from Math_grades where grade = {grade}"
        elif name == '' and grade == '':
            selection = f"select * from Math_grades where second_name = '{second_name}'"
        elif second_name == '' and grade == '':
            selection = f"select * from Math_grades where name = '{name}'"
        elif name == '':
            selection = f"""
            select * from Math_grades 
            where second_name = '{second_name}' and grade = {grade}
            """
        elif second_name == '':
            selection = f"""
            select * from Math_grades 
            where name = '{name}'and grade = {grade}
            """
        elif grade == '':
            selection = f"""
            select * from Math_grades 
            where name = '{name}' and second_name = '{second_name}'
            """
        else:
            selection = f"""
            select * from Math_grades 
            where name = '{name}' and second_name = '{second_name}' and grade = {grade}
            """
        res = cur.execute(selection)
        stud = res.fetchall()
        con.commit()
        con.close()
        names_list = []
        name, second_name, grade = zip(*stud)
        for i in range(len(name)):
            names = name[i] + ' ' + second_name[i] + ' ' + str(grade[i])
            names_list += names,
        names_var = StringVar(value=names_list)
        listbox = Listbox(listvariable=names_var)
        listbox.pack(anchor='center', pady=10)
        scrollbar = ttk.Scrollbar(orient="vertical", command=listbox.yview)
        scrollbar.pack(anchor='center', pady=10)
        listbox["yscrollcommand"] = scrollbar.set
        btn2 = ttk.Button(text='Назад', command=lambda: found_student())
        btn2.pack(anchor='center', pady=10)
    except (ValueError, sqlite3.OperationalError):
        found_student()


def delete(name, second_name, grade):
    """
    Эта функция позволяет удалять строку по разным аргументам
    """
    try:
        clear_window()
        con = sqlite3.connect("students.db")
        cur = con.cursor()
        if name == '' and second_name == '':
            selection = f"delete from Math_grades where grade = {grade}"
        elif name == '' and grade == '':
            selection = f"delete from Math_grades where second_name = '{second_name}'"
        elif second_name == '' and grade == '':
            selection = f"delete from Math_grades where name = '{name}'"
        elif name == '':
            selection = f"""
            delete from Math_grades 
            where second_name = '{second_name}' and grade = {grade}
            """
        elif second_name == '':
            selection = f"""
            delete from Math_grades 
            where name = '{name}'and grade = {grade}
            """
        elif grade == '':
            selection = f"""
            delete from Math_grades 
            where name = '{name}' and second_name = '{second_name}'
            """
        else:
            selection = f"""
            delete from Math_grades 
            where name = '{name}' and second_name = '{second_name}' and grade = {grade}
            """
        cur.execute(selection)
        con.commit()
        con.close()
        lbl = Label(text='Удаление завершено')
        lbl.pack(anchor='center', pady=10)
        btn2 = ttk.Button(text='Назад', command=lambda: main())
        btn2.pack(anchor='center', pady=10)
    except (ValueError, sqlite3.OperationalError):
        delete_student()


def update(name1, second_name1, grade1, name2, second_name2, grade2):
    """
    Эта функция меняет полученную строку на другие полученные данные
    """
    try:
        if name1 == '' or name2 == '' or second_name1 == '' or second_name2 == '' or grade1 == '' or grade2 == '' and int(grade1) > 0 and int(grade2) > 0:
            update_student()
        else:
            con = sqlite3.connect("students.db")
            cur = con.cursor()
            res = cur.execute(f"""
            Update Math_grades 
            set name = '{name2}', second_name = '{second_name2}', grade = {grade2} 
            where name = '{name1}' and second_name = '{second_name1}' and grade = {grade1}
            """)
            res.fetchall()
            con.commit()
            con.close()
    except sqlite3.OperationalError:
        update_student()


def update_grade(name, second_name, grade):
    """
    Эта функция позволяет отдельно обновить оценку по полученным аргументам
    """
    try:
        if name == '' or second_name == '' or grade == '' and int(grade) < 0:
            update_student()
        else:
            con = sqlite3.connect("students.db")
            cur = con.cursor()
            res = cur.execute(f"""
            Update Math_grades 
            set grade = {grade} 
            where name = '{name}' and second_name = '{second_name}'
            """)
            res.fetchall()
            con.commit()
            con.close()
    except sqlite3.OperationalError:
        update_student_grade()


def main():
    """
    Эта функция является главной и с помощью интерфейса запускает друние функции
    """
    clear_window()
    ch_btn = ttk.Button(window, text='Вывести Всю базу данных', command=lambda: check_all())
    ch_btn.pack(anchor='center', pady=10)
    app_btn = ttk.Button(window, text='Добавить студента в БД', command=lambda: append_student())
    app_btn.pack(anchor='center', pady=10)
    found_btn = ttk.Button(window, text='Найти студента', command=lambda: found_student())
    found_btn.pack(anchor='center', pady=10)
    del_btn = ttk.Button(window, text='Удалить студента', command=lambda: delete_student())
    del_btn.pack(anchor='center', pady=10)
    up_btn = ttk.Button(window, text='Изменить строку', command=lambda: update_student())
    up_btn.pack(anchor='center', pady=10)
    up_grade_btn = ttk.Button(window, text='Изменить оценку', command=lambda: update_student_grade())
    up_grade_btn.pack(anchor='center', pady=10)
    avg_grade_btn = ttk.Button(window, text='Средняя оценка студентов по предмету', command=lambda: average_grade())
    avg_grade_btn.pack(anchor='center', pady=10)
    exit_btn = ttk.Button(window, text='Выйти', command=lambda: window.destroy())
    exit_btn.pack(anchor='center', pady=10)


def check_all():
    """
    Эта функция запускает функции по выводу всей базы данных и её сортировке
    """
    clear_window()
    no_sort_btn = ttk.Button(text='Не сортировать', command=lambda: check(''))
    no_sort_btn.pack(anchor='center', pady=10)
    name_btn = ttk.Button(text='Сортировать по имени', command=lambda: check('name'))
    name_btn.pack(anchor='center', pady=10)
    second_name_btn = ttk.Button(text='Сортировать по фамилии', command=lambda: check('second_name'))
    second_name_btn.pack(anchor='center', pady=10)
    grade_btn = ttk.Button(text='Сортировать по оценкам', command=lambda: check('grade'))
    grade_btn.pack(anchor='center', pady=10)
    btn2 = ttk.Button(text='Назад', command=lambda: main())
    btn2.pack(anchor='center', pady=10)


def append_student():
    """
    Эта позволяет вводить данные нового студента и запускать функцию добавления
    """
    clear_window()
    name_lbl = Label(text='Имя')
    name_lbl.pack(anchor='center', pady=5)
    name_entry = ttk.Entry()
    name_entry.pack(anchor='center', pady=10)
    second_name_lbl = Label(text='Фамилия')
    second_name_lbl.pack(anchor='center', pady=5)
    second_name_entry = ttk.Entry()
    second_name_entry.pack(anchor='center', pady=10)
    grade_lbl = Label(text='Оценка')
    grade_lbl.pack(anchor='center', pady=5)
    grade_entry = ttk.Entry()
    grade_entry.pack(anchor='n', pady=10)
    app_btn = ttk.Button(window, text='Добавить студента в БД',
                         command=lambda: append(name_entry.get(), second_name_entry.get(), grade_entry.get()))
    app_btn.pack(anchor='center', pady=10)
    back_btn = ttk.Button(window, text='Назад', command=lambda: main())
    back_btn.pack(anchor='center', pady=10)


def found_student():
    """
    Эта функция позволяет вводить аргументы и запускать функции поиска строк по этим аргументам
    """
    clear_window()
    name_lbl = Label(text='Имя')
    name_lbl.pack(anchor='center', pady=5)
    name_entry = ttk.Entry()
    name_entry.pack(anchor='center', pady=10)
    second_name_lbl = Label(text='Фамилия')
    second_name_lbl.pack(anchor='center', pady=5)
    second_name_entry = ttk.Entry()
    second_name_entry.pack(anchor='center', pady=10)
    grade_lbl = Label(text='Оценка')
    grade_lbl.pack(anchor='center', pady=5)
    grade_entry = ttk.Entry()
    grade_entry.pack(anchor='n', pady=10)
    app_btn = ttk.Button(window, text='Найти',
                         command=lambda: found(name_entry.get(), second_name_entry.get(), grade_entry.get()))
    app_btn.pack(anchor='center', pady=10)
    back_btn = ttk.Button(window, text='Назад', command=lambda: main())
    back_btn.pack(anchor='center', pady=10)


def delete_student():
    """
    Эта функция позволяет вводить аргументы и запускать функции удаления строк с этими аргументам
    """
    clear_window()
    name_lbl = Label(text='Имя')
    name_lbl.pack(anchor='center', pady=5)
    name_entry = ttk.Entry()
    name_entry.pack(anchor='center', pady=10)
    second_name_lbl = Label(text='Фамилия')
    second_name_lbl.pack(anchor='center', pady=5)
    second_name_entry = ttk.Entry()
    second_name_entry.pack(anchor='center', pady=10)
    grade_lbl = Label(text='Оценка')
    grade_lbl.pack(anchor='center', pady=5)
    grade_entry = ttk.Entry()
    grade_entry.pack(anchor='n', pady=10)
    del_btn = ttk.Button(window, text='Удалить',
                         command=lambda: delete(name_entry.get(), second_name_entry.get(), grade_entry.get()))
    del_btn.pack(anchor='center', pady=10)
    back_btn = ttk.Button(window, text='Назад', command=lambda: main())
    back_btn.pack(anchor='center', pady=10)


def update_student():
    """
    Эта функция позволяет вводить аргументы и запускать функции обновления строк по этим аргументам
    """
    clear_window()
    name1_lbl = Label(text='Имя')
    name1_lbl.pack(anchor='center', pady=5)
    name1_entry = ttk.Entry()
    name1_entry.pack(anchor='center', pady=10)
    second_name1_lbl = Label(text='Фамилия')
    second_name1_lbl.pack(anchor='center', pady=5)
    second_name1_entry = ttk.Entry()
    second_name1_entry.pack(anchor='center', pady=10)
    grade1_lbl = Label(text='Оценка')
    grade1_lbl.pack(anchor='center', pady=5)
    grade1_entry = ttk.Entry()
    grade1_entry.pack(anchor='n', pady=10)
    name2_lbl = Label(text='Новое Имя')
    name2_lbl.pack(anchor='center', pady=5)
    name2_entry = ttk.Entry()
    name2_entry.pack(anchor='center', pady=10)
    second_name2_lbl = Label(text='Новая Фамилия')
    second_name2_lbl.pack(anchor='center', pady=5)
    second_name2_entry = ttk.Entry()
    second_name2_entry.pack(anchor='center', pady=10)
    grade2_lbl = Label(text='Новая Оценка')
    grade2_lbl.pack(anchor='center', pady=5)
    grade2_entry = ttk.Entry()
    grade2_entry.pack(anchor='n', pady=10)
    up_btn = ttk.Button(window, text='Изменить',
                        command=lambda: update(name1_entry.get(), second_name1_entry.get(), grade1_entry.get(), name2_entry.get(), second_name2_entry.get(), grade2_entry.get()))
    up_btn.pack(anchor='center', pady=10)
    back_btn = ttk.Button(window, text='Назад', command=lambda: main())
    back_btn.pack(anchor='center', pady=10)


def update_student_grade():
    """
    Эта функция позволяет вводить аргументы и запускать функцию обновления оценки по этим аргументам
    """
    clear_window()
    name_lbl = Label(text='Имя')
    name_lbl.pack(anchor='center', pady=5)
    name_entry = ttk.Entry()
    name_entry.pack(anchor='center', pady=10)
    second_name_lbl = Label(text='Фамилия')
    second_name_lbl.pack(anchor='center', pady=5)
    second_name_entry = ttk.Entry()
    second_name_entry.pack(anchor='center', pady=10)
    grade_lbl = Label(text='Новая оценка')
    grade_lbl.pack(anchor='center', pady=5)
    grade_entry = ttk.Entry()
    grade_entry.pack(anchor='n', pady=10)
    up_btn = ttk.Button(window, text='Изменить', command=lambda: update_grade(name_entry.get(), second_name_entry.get(), grade_entry.get()))
    up_btn.pack(anchor='center', pady=10)
    back_btn = ttk.Button(window, text='Назад', command=lambda: main())
    back_btn.pack(anchor='center', pady=10)


def average_grade():
    """
    Эта функция выводит средний балл всех студентов по этому предмету
    """
    clear_window()
    con = sqlite3.connect("students.db")
    cur = con.cursor()
    res = cur.execute("SELECT AVG(grade) FROM Math_grades")
    stud = res.fetchall()
    lbl = Label(text=stud)
    lbl.pack(anchor='center', pady=10)
    con.close()
    back_btn = ttk.Button(window, text='Назад', command=lambda: main())
    back_btn.pack(anchor='center', pady=10)


"""
Основная функция, в которой создаётся окно, задаётся соотношение сторон, запускается главная функция 
и ждёт ответа пользователя.
"""
window = Tk()
window.title('База данных студентов')
window.geometry('400x525')
window.resizable(False, False)
main()
window.mainloop()
