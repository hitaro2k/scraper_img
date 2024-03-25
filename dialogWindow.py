import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def get_word_from_user(callback):
    def on_word_submit():
        word = entry.get()
        callback(word)

    def choose_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            print("Выбрана папка:", folder_path)
            callback(folder_path)

    root = tk.Tk()
    root.title("Parser Hitaro")
    root.geometry("600x500")

    entry = ttk.Entry(root)
    entry.pack(pady=20)
    entry.focus()

    submit_button = ttk.Button(root, text="Search Image", command=on_word_submit)
    submit_button.pack(pady=5)

    choose_folder_button = ttk.Button(root, text="Select folder", command=choose_folder)
    choose_folder_button.pack(pady=10)

    root.mainloop()

