import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

root = tk.Tk()


class TrashApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.actual_trash = 0
        self.trash_capacity = 0

        self.pack()

        # Sets main attributes
        self.master.title('Lixeira')
        self.master.geometry('600x400+50+50')
        self.master.resizable(False, False)

        # Entry
        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Labels
        self.trash_capacity_label = ttk.Label(self.master, text='Capacidade máxima de lixo: 0')
        self.trash_capacity_label.pack(ipadx=10, ipady=10)
        self.actual_trash_label = ttk.Label(self.master, text='Quantidade de lixo atual: 0')
        self.actual_trash_label.pack(ipadx=10, ipady=10)

        # Buttons
        self.put_trash_button = ttk.Button(self.master, text='Adicionar lixo', command=self.put_trash_button_callback)
        self.put_trash_button.pack(ipadx=5, ipady=5, expand=False)
        self.clear_trash_button = ttk.Button(self.master, text='Esvaziar lixeira', command=self.clear_trash_button_callback)
        self.clear_trash_button.pack(ipadx=5, ipady=5, expand=False)
        self.lock_trash_button = ttk.Button(self.master, text='Travar lixeira', command=self.lock_trash_button_callback)
        self.lock_trash_button.pack(ipadx=5, ipady=5, expand=False)

        # String Variable
        self.trash_capacity_stringVar = tk.StringVar()
        self.trash_capacity_stringVar.set("0")
        self.entrythingy["textvariable"] = self.trash_capacity_stringVar

        # Binds
        self.entrythingy.bind('<Key-Return>', self._set_trash_capacity)

    def _set_trash_capacity(self, event):
        # print("Hi. The current entry content is:", self.trash_capacity_stringVar.get())
        if self._is_capacity_valid():
            self.trash_capacity = int(self.trash_capacity_stringVar.get())
            self.trash_capacity_label['text'] = 'Capacidade máxima de lixo: ' + str(self.trash_capacity)
            print('True')

    def _is_capacity_valid(self):
        if not TrashApp._check_int(self.trash_capacity_stringVar.get()):
            showerror('Erro', 'A capacidade digitada deve ser um número inteiro')
            return False
        capacity_typed = int(self.trash_capacity_stringVar.get())
        if capacity_typed < 0:
            showerror('Erro', 'A capacidade máxima da lixeira que foi digitada não pode ser menor que zero')
            return False
        if capacity_typed < self.actual_trash:
            showerror('Erro', 'A capacidade máxima da lixeira que foi digitada é menor que a quantidade de lixo atual')
            return False
        return True

    def put_trash_button_callback(self):
        if self._is_possible_to_put_more_trash():
            self.actual_trash += 1
            self._change_actual_trash_label()

    def clear_trash_button_callback(self):
        self.actual_trash = 0
        self._change_actual_trash_label()

    def _change_actual_trash_label(self):
        self.actual_trash_label['text'] = 'Quantidade de lixo atual: ' + str(self.actual_trash)

    def _is_possible_to_put_more_trash(self):
        if self.trash_capacity > self.actual_trash:
            return True
        return False

    def lock_trash_button_callback(self):
        self.put_trash_button.state(['disabled'])

    @staticmethod
    def _check_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False


myapp = TrashApp(root)
myapp.mainloop()