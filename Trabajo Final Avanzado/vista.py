import tkinter as tk
from tkinter import ttk
from modelo import Funciones, MiServidor


class Programa:
    def __init__(self, ventana):
        self.root = ventana
        self.objeto_funciones = Funciones()
        self.objeto_miservidor = MiServidor()

        ##### LABEL #####
        self.titulo = tk.Label(
            self.root,
            text="CRUD",
            font=("Arial", 15, "bold"),
        )
        self.titulo.grid(row=0, column=1)

        self.espacio = tk.Label(self.root, text="")
        self.espacio.grid(row=2, column=1)

        self.buscador = tk.Label(
            self.root, text="Buscar Registro", anchor=tk.E, width=14
        )
        self.buscador.grid(row=1, column=0)

        self.titulo_label = tk.Label(self.root, text="Titulo", anchor=tk.E, width=14)
        self.titulo_label.grid(row=3, column=0)

        self.descripcion_label = tk.Label(
            self.root, text="Descripcion", anchor=tk.E, width=14
        )
        self.descripcion_label.grid(row=4, column=0)

        ##### ENTRY #####
        self.busqueda_entry = tk.Entry(self.root, width=20)
        self.busqueda_entry.grid(row=1, column=1)

        self.titulo_entry = tk.Entry(self.root, width=20)
        self.titulo_entry.grid(row=3, column=1)

        self.descripcion_entry = tk.Entry(self.root, width=20)
        self.descripcion_entry.grid(row=4, column=1)

        ##### TREEVIEW #####
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("titulo", "descripcion")
        self.tree.column("#0", width=80, minwidth=80, anchor=tk.W)
        self.tree.column("titulo", width=120, minwidth=120, anchor=tk.W)
        self.tree.column("descripcion", width=120, minwidth=120, anchor=tk.W)

        self.tree.heading("#0", text="Registro")
        self.tree.heading("titulo", text="Titulo")
        self.tree.heading("descripcion", text="Descripcion")

        self.tree.grid(row=8, column=0, columnspan=4)

        ##### BUTTONS #####
        self.busqueda = tk.Button(
            self.root,
            text="Buscar",
            command=lambda: self.objeto_funciones.buscar(
                self.tree, self.busqueda_entry.get()
            ),
        )
        self.busqueda.grid(row=1, column=2)

        self.alta = tk.Button(
            self.root,
            text="Alta",
            command=lambda: self.objeto_funciones.alta_f(
                self.tree,
                self.titulo_entry.get(),
                self.descripcion_entry.get(),
            ),
        )
        self.alta.grid(row=3, column=2)

        self.baja = tk.Button(
            self.root,
            text="Baja",
            command=lambda: self.objeto_funciones.baja_f(
                self.tree,
            ),
        )
        self.baja.grid(row=4, column=2)

        self.modificacion = tk.Button(
            self.root,
            text="Modificación",
            command=lambda: self.objeto_funciones.modificacion_f(
                self.tree,
                self.titulo_entry.get(),
                self.descripcion_entry.get(),
            ),
        )
        self.modificacion.grid(row=5, column=2)

        self.iniciar = tk.Button(
            self.root,
            text="Iniciar",
            command=lambda: (self.objeto_funciones.actualizar(self.tree), self.objeto_miservidor.probar_conexion(), self.objeto_miservidor.conexion_cliente()),
        )
        self.iniciar.grid(row=0, column=0)

        self.salir = tk.Button(
            self.root,
            text="Salir",
            command=lambda: (self.objeto_miservidor.parar_servidor(),self.root.quit())
        )
        self.salir.grid(row=0, column=3)
