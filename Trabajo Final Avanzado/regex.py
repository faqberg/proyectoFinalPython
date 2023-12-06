import re


def validar(titulo_entry):
    patron = re.compile(r"^[a-zA-Z0-9]+$")
    es_valido = re.match(patron, titulo_entry)
    return es_valido
