import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

FILE_NAME = "favorites.json"


# поиск пользователей
def search_user():
    username = entry.get().strip()

    if username == "":
        messagebox.showerror("Ошибка", "Поле не должно быть пустым")
        return

    listbox_results.delete(0, tk.END)

    url = "https://api.github.com/search/users?q=" + username

    try:
        response = requests.get(url)
        data = response.json()

        users = data["items"]

        for user in users:
            listbox_results.insert(tk.END, user["login"])

    except:
        messagebox.showerror("Ошибка", "Не удалось получить данные")


# добавить в избранное
def add_to_favorites():
    selected = listbox_results.curselection()

    if not selected:
        messagebox.showwarning("Внимание", "Сначала выберите пользователя")
        return

    user = listbox_results.get(selected[0])

    favorites = load_favorites()

    if user not in favorites:
        favorites.append(user)
        save_favorites(favorites)
        listbox_favorites.insert(tk.END, user)
    else:
        messagebox.showinfo("Инфо", "Пользователь уже есть в избранном")


# сохранить json
def save_favorites(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# загрузить json
def load_favorites():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return[]
    else:
        return []


# показать избранное при запуске
def show_favorites():
    favorites = load_favorites()
    for user in favorites:
        listbox_favorites.insert(tk.END, user)


# окно
window = tk.Tk()
window.title("GitHub User Finder")
window.geometry("500x450")

label = tk.Label(window, text="Введите GitHub username")
label.pack(pady=5)

entry = tk.Entry(window, width=35)
entry.pack(pady=5)

button_search = tk.Button(window, text="Поиск", command=search_user)
button_search.pack(pady=5)

label_results = tk.Label(window, text="Результаты поиска")
label_results.pack()

listbox_results = tk.Listbox(window, width=50, height=8)
listbox_results.pack(pady=5)

button_add = tk.Button(window, text="Добавить в избранное", command=add_to_favorites)
button_add.pack(pady=5)

label_favorites = tk.Label(window, text="Избранное")
label_favorites.pack()

listbox_favorites = tk.Listbox(window, width=50, height=8)
listbox_favorites.pack(pady=5)

show_favorites()

window.mainloop()
