import trash
import view


class Bridge:
    def __init__(self):
        self.main_trash = trash.Trash()
        self.main_view = view.TrashApp(view.root)

    def run(self):
        self.main_view.mainloop()


b = Bridge()
b.run()
