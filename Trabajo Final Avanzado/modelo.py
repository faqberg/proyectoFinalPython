from tkinter.messagebox import showerror, showinfo
from regex import validar
from base import Noticia
from observador import Entes
import datetime
import subprocess
import os
import threading
import sys

def registro_de_log(log_file):
    def decorador(func):
        def wrapper(*args, **kwargs):
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mensaje_log = f"{fecha} - Función '{func.__name__}'\n"
            
            # Registra el mensaje en el archivo de registro
            with open(log_file, "a") as archivo:
                archivo.write(mensaje_log)
            
            # Llama a la función original
            resultado = func(*args, **kwargs)
            return resultado
        
        return wrapper
    return decorador

# Aplica el decorador a las funciones que queres registrar


class Funciones(Entes):
    @registro_de_log("registro.txt")
    def buscar(self, tree, busqueda_entry):
        """
        Busca a través del valor ingresado en el campo `busqueda_entry` y muestra la fila correspondiente en el `treeview`.

        :param tree: ttk.treeview
        :param busqueda_entry: Valor ingresado por el usuario
        :return: Treeview de la fila buscada
        """
        valor_id = busqueda_entry
        registros = tree.get_children()
        for element in registros:
            tree.delete(element)

        resultado = Noticia.select(
            Noticia.id, Noticia.titulo, Noticia.descripcion
        ).where(Noticia.id == valor_id)
        if not resultado.exists():
            showerror("Error", "El valor buscado no se encuentra en la tabla")
        else:
            for fila in resultado:
                tree.insert(
                    "", "end", text=fila.id, values=(fila.titulo, fila.descripcion)
                )
        

    @registro_de_log("registro.txt")
    def alta_f(
        self,
        tree,
        titulo,
        descripcion,
    ):
        """
        Realiza un insert en la base de datos y muestra todos los valores en el `treeview`.

        :param tree: ttk.treeview
        :param titulo: Valor ingresado por el usuario y usado en la función validar para ver si es alfanumérico
        :param descripcion: Valor ingresado por el usuario
        :return: Nueva fila en la base de datos y nueva vista en el `treeview`
        """
        db = Noticia()
        es_valido = validar(titulo)
        if es_valido is None:
            showerror("Error", "El valor no es alfanumérico")
        else:
            db.titulo = titulo
            db.descripcion = descripcion
            db.save()
        self.actualizar(tree)
        self.notificar(titulo, descripcion)        

    @registro_de_log("registro.txt")
    def actualizar(self, tree):
        """
        Muestra todos los valores de la base de datos en el `treeview`.

        :param tree: ttk.treeview
        :return: Vista en `treeview`
        """
        registros = tree.get_children()
        for element in registros:
            tree.delete(element)

        for fila in Noticia.select():
            tree.insert("", 0, text=fila.id, values=(fila.titulo, fila.descripcion))
        

    @registro_de_log("registro.txt")
    def baja_f(self, tree):
        """
        Elimina la fila seleccionada por el usuario.

        :param tree: ttk.treeview
        :return: Vista nueva en `treeview`
        """
        seleccionado = tree.focus()
        valor_id = tree.item(seleccionado)
        borrar = Noticia.get(Noticia.id == valor_id["text"])
        borrar.delete_instance()
        self.actualizar(tree)
        showinfo("Baja", "El usuario fue dado de baja")
        

    @registro_de_log("registro.txt")
    def modificacion_f(
        self,
        tree,
        titulo_entry,
        descripcion_entry,
    ):
        """
        Modifica la fila seleccionada por el usuario, si el usuario deja un campo vacío lo deja tal cual está.

        :param tree: ttk.treeview
        :param titulo_entry: Valor ingresado por el usuario
        :param descripcion_entry: Valor ingresado por el usuario
        :return: Vista nueva en `treeview`
        """
        seleccionado = tree.focus()
        valor_id = tree.item(seleccionado)
        if titulo_entry == "":
            titulo_tree = valor_id["values"][0]
        else:
            titulo_tree = (titulo_entry,)
        if descripcion_entry == "":
            descripcion_tree = valor_id["values"][1]
        else:
            descripcion_tree = descripcion_entry
        actualizar = Noticia.update(
            titulo=titulo_tree, descripcion=descripcion_tree
        ).where(Noticia.id == valor_id["text"])
        actualizar.execute()
        self.actualizar(tree)
        showinfo("Modificación", "El usuario fue modificado")


procesos = None


class MiServidor:
    
    def __init__(self):
       
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.server_route = os.path.join(self.BASE_DIR, 'servidor.py')
        self.server_route_cli = os.path.join(self.BASE_DIR, 'cliente.py')
        
    def probar_conexion(self):
        global the_process
        if procesos is not None:
            procesos.kill()
            procesos.wait()
            procesos.terminate()
            threading.Thread(target=self.server_init, args=(True,), daemon=True).start()
        else:
            threading.Thread(target=self.server_init, args=(True,), daemon=True).start()
            print("Inicio de Servidor")

    def server_init(self, var):
        global procesos
        stdout = ""
        stderr = ""
        the_route = self.server_route
        if var:
            procesos = subprocess.Popen([sys.executable, the_route])
            stdout, stderr = procesos.communicate()
            self.connection_info = f"Informacion de la Conexion:\n{stdout}\n{stderr}"
        else:
            print("")

    def parar_servidor(self):
        global procesos
        if procesos:
            procesos.kill()
            procesos.wait()
            procesos.terminate()
            procesos = None
            print("Servidor parado")
        else:
            print("El servidor no esta corriendo.")

    def conexion_cliente(self):
        global procesos
        the_route_cli = self.server_route_cli
        procesos = subprocess.Popen([sys.executable, the_route_cli])
        procesos.communicate()
        if procesos.returncode == 0:
            print("Cliente conectado exitosamente")
        else:
            print("Error al conectar al cliente")