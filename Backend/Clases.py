class Cliente:
    def __init__(self, nit, nombre, usuario, clave, direccion, email, lista_instancias):
        self.nit = nit
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.direccion = direccion
        self.email = email
        self.lista_instancias = lista_instancias

    def convertir_json(self):
        json_final = {}
        json_final["nit"] = self.nit
        json_final["nombre"] = self.nombre
        json_final["usuario"] = self.usuario
        json_final["clave"] = self.clave
        json_final["direccion"] = self.direccion
        json_final["email"] = self.email

        lista_instancias = []
        
        for instancia in self.lista_instancias:
            lista_instancias.append(instancia.convertir_json())

        json_final["lista_instancias"] = lista_instancias

        return json_final
            

class Instancia:
    def __init__(self, id_instancia, id_config, f_inicio, estado, f_final):
        self.id_instancia = id_instancia
        self.id_config = id_config
        self.f_inicio = f_inicio
        self.estado = estado
        self.f_final = f_final
        self.tiempo = 0

    def convertir_json(self):
        json_final = {}
        json_final["id_instancia"] = self.id_instancia
        json_final["id_config"] = self.id_config
        json_final["f_inicio"] = self.f_inicio
        json_final["estado"] = self.estado
        json_final["f_final"] = self.f_final
        json_final["tiempo"] = self.tiempo

        return json_final
        
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
