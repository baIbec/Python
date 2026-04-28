import tkinter as tk
from tkinter import messagebox
import json
import random

# --- Функции работы с файлами ---
def load_tasks():
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(task_list):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(task_list, file, ensure_ascii=False, indent=4)

# --- Функции интерфейса ---
def update_listbox(filtered_tasks=None):
    task_listbox.delete(0, tk.END)
    # Если фильтр не задан, показываем все задачи
    for task in (filtered_tasks if filtered_tasks is not None else tasks):
        task_listbox.insert(tk.END, task)

def gen_task():
    sp = [
        ['Антуан де Сент-Экзюпери','Доброта','Зорко одно лишь сердце. Самого главного глазами не увидишь'],
        ["Антуан де Сент-Экзюпери","Доброта","Все взрослые сначала были детьми, только мало кто из них об этом помнит"],
        ["Лев Толстой","Мудрость","Чтоб жить честно, надо рваться, путаться, биться, ошибаться, начинать и бросать, и опять начинать..."],
        ["Лев Толстой","Мудрость","И нет величия там, где нет простоты, добра и правды"],
        ["Фёдор Достоевский","Философия","Во всем есть черта, за которую перейти опасно; ибо, раз переступив, воротиться назад невозможно"]
    ]
    # Формируем строку для сохранения в формате: Автор | Тема | Цитата
    author, topic, quote = random.choice(sp)
    task = f"{author} | {topic} | {quote}"
    tasks.append(task)
    save_tasks(tasks)
    update_listbox() # Обновляем сразу весь список

def remove_task():
    selected = task_listbox.curselection()
    if selected:
        index = selected[0]
        tasks.pop(index)
        save_tasks(tasks)
        update_listbox()
    else:
        messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")

def filter_tasks():
    author_filter = entry_author.get().strip().lower()
    topic_filter = entry_topic.get().strip().lower()

    filtered = []
    for task in tasks:
        parts = task.split(' | ')
        if len(parts) != 3:
            continue # Пропускаем, если формат нарушен
        cur_author, cur_topic, _ = parts

        match_author = (author_filter == '' or author_filter in cur_author.lower())
        match_topic = (topic_filter == '' or topic_filter in cur_topic.lower())

        if match_author and match_topic:
            filtered.append(task)
    
    update_listbox(filtered)

def reset_filter():
    entry_author.delete(0, tk.END)
    entry_topic.delete(0, tk.END)
    update_listbox() # Показываем все задачи

# --- Загрузка данных ---
tasks = load_tasks()

# --- Создание окна ---
root = tk.Tk()
root.title("Генератор цитат с фильтрацией")
root.geometry("1000x500")

# --- Поля для фильтрации ---
frame_filters = tk.Frame(root)
frame_filters.pack(pady=10)

tk.Label(frame_filters, text="Автор:").grid(row=0, column=0, padx=5)
entry_author = tk.Entry(frame_filters, width=30)
entry_author.grid(row=0, column=1, padx=5)

tk.Label(frame_filters, text="Тема:").grid(row=0, column=2, padx=5)
entry_topic = tk.Entry(frame_filters, width=30)
entry_topic.grid(row=0, column=3, padx=5)

btn_filter = tk.Button(frame_filters, text="Фильтровать", command=filter_tasks)
btn_filter.grid(row=0, column=4, padx=5)

btn_reset = tk.Button(frame_filters, text="Сбросить фильтр", command=reset_filter)
btn_reset.grid(row=0, column=5, padx=5)

# --- Список задач ---
task_listbox = tk.Listbox(root, width=200, height=15)
task_listbox.pack(pady=20)

# --- Кнопки действий ---
btn_gen = tk.Button(root, text="Генерировать цитату", command=gen_task)
btn_gen.pack(pady=5)

btn_remove = tk.Button(root, text="Удалить выбранную", command=remove_task)
btn_remove.pack(pady=5)

# Запуск интерфейса
root.mainloop()
