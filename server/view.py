import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror


class ServerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set main attributes
        self.title('Servidor')
        self.geometry('1380x720+50+50')
        self.resizable(False, False)

        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=3)


myapp = ServerApp()
myapp.mainloop()
