class Entes:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        self.observadores.remove(obj)

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)


class ObservarFunciones(Entes):
    def __init__(self):
        self.estado = None

    def set_estado(self, *args):
        self.notificar(args)

    def get_estado(self):
        return self.estado


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ObservadorUno(Observador):
    def __init__(self, obj):
        self.observador_uno = obj
        self.observador_uno.agregar(self)

    def update(self, *args):
        print(f'Datos capturados por ObservadorUno (alta) : {args}')
