import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror


class ServerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.total_trash = 10
        self.fifth_grid_control = 1

        # Set main attributes
        self.title('Servidor')
        self.geometry('1380x720+50+50')
        self.resizable(False, False)

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        to_be_collect_label = ttk.Label(self, text="Lista a ser coletada:")
        to_be_collect_label.grid(column=4, row=0, sticky=tk.N)

        self.create_trash(0, 1 ,3)

        #self.create_trash(1, 3 , 3)

        #self.create_trash(2, 3 ,3 )

        #self.create_trash(3,3 ,3)

        '''
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=3, row=0, sticky=tk.W, padx=5, pady=5)
        password_label = ttk.Label(self, text="Password:")
        password_label.grid(column=4, row=0, sticky=tk.W, padx=5, pady=5)
        '''

    def create_trash(self, trash_name, trash_percentage, is_locked):
        a = 3//4
        b = 5//4
        c = 9//4
        print(3 % 4)
        print(5 % 4)
        print(9 % 4)

        print(a)
        print(b)
        print(c)

        '''
        for t in range(1, self.total_trash):
            column = t//4
            self._create_trash(column)

        #self._create_trash(a)
        #self._create_trash(b)
        #self._create_trash(c)
        '''

    def _create_trash(self, column, row=0, trash_name='Lixeira 001', trash_percentage=10, is_locked=False):
        trash_label = ttk.Label(self, text=trash_name)
        percentage_text = str(trash_percentage) + '% cheia'
        trash_complete = ttk.Label(self, text=percentage_text)
        if is_locked:
            lock_text = 'Destravar'
        else:
            lock_text = 'Travar'

        trash_lock = ttk.Button(self, text=lock_text)
        trash_to_be_collected = ttk.Button(self, text="Coletar")

        trash_label.grid(column=column, row=0 + column*4, sticky=tk.NW, padx=2, pady=2)
        trash_complete.grid(column=column, row=1 + column*4, sticky=tk.NW, padx=2, pady=2)
        trash_lock.grid(column=column, row=2 + column*4, sticky=tk.NW, padx=2, pady=2)
        trash_to_be_collected.grid(column=column, row=3 + column*4, sticky=tk.NW, padx=2, pady=2)


myapp = ServerApp()
myapp.mainloop()
