################## MODULOS ################

from tkinter import *
from vista import Programa
import observador


class Controller:
    def __init__(self, root):
        self.root_controller = root
        self.objeto_vista = Programa(self.root_controller)
        self.el_observador = observador.ObservadorUno(self.objeto_vista.objeto_funciones)


if __name__ == "__main__":
    root = Tk()
    mi_app = Controller(root)
    root.mainloop()