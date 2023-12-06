from peewee import *


database = SqliteDatabase("crud.db")


class BaseModel(Model):
    class Meta:
        database = database


class Noticia(BaseModel):
    titulo = CharField()
    descripcion = CharField()


try:
    database.connect()
    database.create_tables([Noticia])
    print("Conexión a la base de datos y creación de tablas exitosas.")
except Exception as e:
    print(f"Error: {e}")
finally:
    database.close()