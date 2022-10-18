class Cliente:
    def __init__(self, nit, nombre, usuario, clave, direccion, email, lista_instancias):
        self.nit = nit
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.direccion = direccion
        self.email = email
        self.lista_instancias = lista_instancias

class Instancia:
    def __init__(self, id_instancia, id_config, f_inicio, estado, f_final):
        self.id_instancia = id_instancia
        self.id_config = id_config
        self.f_inicio = f_inicio
        self.estado = estado
        self.f_final = f_final
        self.tiempo = 0
        
class Recurso:
    def __init__(self, id_recurso, nombre, abrev, metrica, tipo, precio):
        self.id_recurso = id_recurso
        self.nombre = nombre
        self.abrev = abrev
        self.metrica = metrica
        self.tipo = tipo
        self.precio = precio

class Configuracion:
    def __init__(self, id_configuracion, nombre, desc, lista_recursos):
        self.id_configuracion = id_configuracion
        self.nombre = nombre
        self.desc = desc
        self.lista_recursos = lista_recursos

class Categoria:
    def __init__(self, id_categoria, nombre, desc, carga, lista_configuraciones):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.desc = desc
        self.carga = carga
        self.lista_configuraciones = lista_configuraciones

class Recurso_conf:
    def __init__(self, id_recurso, cantidad):
        self.id_recurso = id_recurso
        self.cantidad = cantidad
