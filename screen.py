import tkinter as tk
from tkinter import ttk


class TrashApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.actual_trash = 0
        self.trash_capacity = 0

        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Sets main attributes
        self.master.title('Lixeira')
        self.master.geometry('600x400+50+50')
        self.master.resizable(False, False)

        self.trash_capacity_label = ttk.Label(self.master, text='Capacidade máxima de lixo: 0')
        self.trash_capacity_label.pack(ipadx=10, ipady=10)

        self.actual_trash_label = ttk.Label(self.master, text='Quantidade de lixo atual: 0')
        self.actual_trash_label.pack(ipadx=10, ipady=10)

        put_trash_button = ttk.Button(self.master, text='Adicionar lixo', command=self.put_trash_button_callback)
        put_trash_button.pack(ipadx=5, ipady=5, expand=True)

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                              self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

    def put_trash_button_callback(self):
        self.actual_trash += 1
        self.actual_trash_label['text'] = 'Quantidade de lixo atual: ' + str(self.actual_trash)


root = tk.Tk()
myapp = TrashApp(root)

myapp.mainloop()
