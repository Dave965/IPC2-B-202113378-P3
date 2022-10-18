from Clases import *
from flask import Flask, jsonify

global_categorias = []
global_recursos = []
global_configs = []
global_clientes = [Cliente("nit", "nombre", "usuario", "clave", "direccion", "email", [Instancia("1","2104","12/17/2024","cancelada",None),Instancia("2","3104","12/11/2024","activa",None)])]

app = Flask(__name__)

@app.route("/consultar_datos" )
def consultar_datos():
    usuarios = [x.convertir_json() for x in global_clientes]
    categorias = [x.convertir_json() for x in global_categorias]
    recursos = [x.convertir_json() for x in global_recursos]
    configs =[x.convertir_json() for x in global_configs]
    return jsonify({"usuarios": usuarios,
                    "categorias": categorias,
                    "recursos": recursos,
                    "configs": configs})

@app.route("/crear_recurso", methods = ["POST"])
def crear_recurso():
    n_recurso = Recurso(request.json["id_recurso"], request.json["nombre"],
                        request.json["abrev"], request.json["metrica"],
                        request.json["tipo"], request.json["precio"])

    global_recursos.append(n_recurso)

    return jsonify({"mensaje": "se ha creado el recurso con exito"})

@app.route("/crear_categoria", methods = ["POST"])
def crear_categoria():
    json_lista_configuraciones = request.json["lista_configuraciones"]
    
    lista_configuraciones = [x for x in global_configs if x.id_configuracion in json_lista_configuraciones]
    
    n_categoria = Categoria(request.json["id_categoria"], request.json["nombre"],
                        request.json["desc"], request.json["carga"], lista_configuraciones)

    global_categorias.append(n_categoria)

    return jsonify({"mensaje": "se ha creado la categoria con exito"})

@app.route("/crear_configuracion", methods = ["POST"])
def crear_configuracion():
    json_lista_recursos = request.json["lista_recursos"]
    lista_recursos = []
    
    for recurso in lista_recursos:
        id_recurso = recurso["id_recurso"]
        cantidad = recurso["cantidad"]
        lista_recursos.append(Recurso_conf(id_recurso, cantidad))
        
    
    n_configuracion = Configuracion(request.json["id_configuracion"], request.json["nombre"],
                        request.json["desc"], lista_recursos)

    global_configs.append(n_configuracion)

    return jsonify({"mensaje": "se ha creado la configuracion con exito"})

@app.route("/crear_cliente", methods = ["POST"])
def crear_cliente():
    lista_instancias = []

    n_cliente = Cliente(request.json["nit"], request.json["nombre"],
                        request.json["usuario"], request.json["clave"],
                        request.json["direccion"], request.json["email"],
                        lista_instancias)
    
    global_clientes.append(n_cliente)

    return jsonify({"mensaje": "se ha creado el usuario con exito"})

@app.route("/crear_instancia", methods = ["POST"])
def crear_instancia():
    cliente = [x for x in global_clientes if x.nit == request.json["nit"]]
    
    n_instancia = Instancia(request.json["id_instancia"], request.json["id_config"],
                          request.json["f_inicio"], request.json["estado"], None)
    
    cliente[0].lista_instancias.append(n_instancia)

    return jsonify({"mensaje": "se ha creado la instancia para el usuario "+cliente[0].nombre+"con exito"})






















if __name__ == "__main__":
    app.run(debug = True, port = 3100)




