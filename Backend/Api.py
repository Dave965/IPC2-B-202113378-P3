from Clases import *
from xml.dom.minidom import parse, parseString
from flask import Flask, jsonify, request
import re
from datetime import datetime

global_categorias = []
global_recursos = []
global_configs = []
global_clientes = []
global_consumos = []
global_facturas = []

#Cliente("nit", "nombre", "usuario", "clave", "direccion", "email", [Instancia("1","2104","12/17/2024","cancelada",None),Instancia("2","3104","12/11/2024","activa",None)])

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
                        request.json["tipo"], int(request.json["precio"]))

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

@app.route("/cargar_config", methods = ["POST"])
def cargar_config():
    clientes_creados = 0
    instancias_creadas = 0
    recursos_creados  = 0
    categorias_creadas = 0
    configs_creadas = 0
    
    xml_S = request.get_data()

    xml_O = parseString(xml_S)

    listaRecursos = xml_O.getElementsByTagName("listaRecursos")[0]
    Recursos = listaRecursos.getElementsByTagName("recurso")
    for recurso in Recursos:
        id_recurso = recurso.attributes["id"].value
        nombre = recurso.getElementsByTagName("nombre")[0].firstChild.data
        abrev = recurso.getElementsByTagName("abreviatura")[0].firstChild.data
        metrica = recurso.getElementsByTagName("metrica")[0].firstChild.data
        tipo = recurso.getElementsByTagName("tipo")[0].firstChild.data
        precio = float(recurso.getElementsByTagName("valorXhora")[0].firstChild.data)

        global_recursos.append(Recurso(id_recurso, nombre, abrev, metrica, tipo, precio))
        recursos_creados += 1

    listaCategorias = xml_O.getElementsByTagName("listaCategorias")[0]
    Categorias = listaCategorias.getElementsByTagName("categoria")
    for categoria in Categorias:
        id_categoria = categoria.attributes["id"].value
        nombre_categoria = categoria.getElementsByTagName("nombre")[0].firstChild.data
        desc_categoria = categoria.getElementsByTagName("descripcion")[0].firstChild.data
        carga = categoria.getElementsByTagName("cargaTrabajo")[0].firstChild.data
        lista_configuraciones = []
        
        Configuraciones = categoria.getElementsByTagName("configuracion")
        for configuracion in Configuraciones:
            id_configuracion = configuracion.attributes["id"].value
            nombre_conf = configuracion.getElementsByTagName("nombre")[0].firstChild.data
            desc_conf = configuracion.getElementsByTagName("descripcion")[0].firstChild.data
            lista_recursos = []
            precio_total = 0

            Recursos = configuracion.getElementsByTagName("recurso")
            for recurso in Recursos:
                id_recurso = recurso.attributes["id"].value
                cantidad = float(recurso.firstChild.data)
                try:
                    rec = [x for x in global_recursos if x.id_recurso == id_recurso]
                    precio_total += rec[0].precio*cantidad
                except:
                    print("no existe el recurso en la base de datos de recursos")

                lista_recursos.append(Recurso_conf(id_recurso, cantidad))
                
            Config = Configuracion(id_configuracion, nombre_conf, desc_conf, precio_total, lista_recursos)
            global_configs.append(Config)
            lista_configuraciones.append(Config)
            configs_creadas += 1

        global_categorias.append(Categoria(id_categoria, nombre_categoria, desc_categoria, carga, lista_configuraciones))
        categorias_creadas += 1
        
    listaClientes = xml_O.getElementsByTagName("listaClientes")[0]
    Clientes = listaClientes.getElementsByTagName("cliente")
    for cliente in Clientes:
        nit = cliente.attributes["nit"].value
        nombre = cliente.getElementsByTagName("nombre")[0].firstChild.data
        usuario = cliente.getElementsByTagName("usuario")[0].firstChild.data
        clave = cliente.getElementsByTagName("clave")[0].firstChild.data
        direccion = cliente.getElementsByTagName("direccion")[0].firstChild.data
        email = cliente.getElementsByTagName("correoElectronico")[0].firstChild.data
        lista_instancias = []

        Instancias = cliente.getElementsByTagName("instancia")
        for instancia in Instancias:
            id_instancia = instancia.attributes["id"].value
            id_config = instancia.getElementsByTagName("idConfiguracion")[0].firstChild.data
            fechai = instancia.getElementsByTagName("fechaInicio")[0].firstChild.data
            match_str = re.search(r'\d{2}/\d{2}/\d{4}', fechai)
            if len(match_str) > 0:
                f_inicio = datetime.strptime(match_str.group(), '%d/%m/%Y').date()
            else:
                f_inicio = ""
            estado = instancia.getElementsByTagName("estado")[0].firstChild.data
            if estado.lower() == "cancelada":
                fechaf = instancia.getElementsByTagName("fechaFinal")[0].firstChild.data
                match_str = re.search(r'\d{2}/\d{2}/\d{4}', fechaf)
                f_final = datetime.strptime(match_str.group(), '%d/%m/%Y').date()
            else:
                f_final = ""
            nombre_instancia = instancia.getElementsByTagName("nombre")[0].firstChild.data
            lista_instancias.append(Instancia(id_instancia, id_config, f_inicio, estado, f_final, nombre_instancia))
            instancias_creadas += 1
        
        global_clientes.append(Cliente(nit, nombre, usuario, clave, direccion, email, lista_instancias))
        clientes_creados += 1

    return jsonify({"mensaje": "se han creado "+str(clientes_creados)+" clientes, "+str(instancias_creadas)+" instancias, "
                    +str(recursos_creados)+" recursos, "+str(categorias_creadas)+" categorias y "+str(configs_creadas)+" configuraciones con exito"})

@app.route("/cargar_consumo" )
def cargar_consumo():
    consumos_procesados = 0

    xml_S = request.get_data()

    xml_O = parseString(xml_S)

    Consumos = xml_O.getElementsByTagName("consumo")

    for consumo in consumos:
        nitCliente = consumo.attributes["nitCliente"].value
        idInstancia = consumo.attributes["idInstancia"].value
        tiempo = float(consumo.getElementsByTagName("tiempo")[0].firstChild.data)
        fechah = consumo.getElementsByTagName("fechaHora")[0].firstChild.data
        match_str = re.search(r'\d{2}/\d{2}/\d{4}', fechah)
        fechaHora = datetime.strptime(match_str.group(), '%d/%m/%Y').date()

        global_consumos.append(Consumo(nitCliente, idInstancia, tiempo, fechaHora))
        consumos_procesados += 1
        

    return jsonify({"mensaje": "se han procesado "+str(consumos_procesados)+" consumos"})

@app.route("/facturar" )
def facturar():
    facturas_creadas = 0
    
    f_inicio = datetime.strptime(request.json["fecha_inicio"].group(), '%d/%m/%Y').date()
    f_final = datetime.strptime(request.json["fecha_final"].group(), '%d/%m/%Y').date()

    consumos_por_facturar = [x for x in global_consumos if x.fechaHora > f_inicio and x.fechaHora < f_final and x.facturado == False]

    if len(consumos_por_facturar) == 0:
        return jsonify({"mensaje": "Nada por facturar, intente con otra fecha"})

    for cliente in global_clientes:
        id_factura = str(len(global_facturas)+1).zfill(12)
        nitCliente = cliente.nit
        fechaFactura = f_final
        consumos = [x for x in consumos_por_facturar if x.nitCliente == nitCliente]
        if len(consumos) > 0:
            global_facturas.append(Factura(id_factura, nitCliente, fechaFactura, consumos))
            facturas_creadas += 1

    return jsonify({"mensaje": "se han creado "+str(facturas_creadas)+" facturas"})
        
@app.route("/detalle_factura" )
def detalle_factura():
    id_factura = request.json["factura"]
    archivo = "              Detalle para la Factura "+id_factura+"\n"
    total = 0
    factura = [x for x in global_facturas if x.id_factura == id_factura][0]
    cliente  = [x for x in global_clientes if x.nit == factura.nitCliente][0]

    archivo += "Nit del cliente: "+cliente.nit+"\n"
    archivo += "Fecha de facturacion: "+str(factura.fechaFactura)+"\n"
    
    instancias_revisadas = []
    
    for consumo in factura.consumos:
        if consumo.idInstancia in instancias_revisadas:
            continue
        consumos_misma_instancia = [x for x in factura.consumos if x.idInstancia not in instancias_revisadas and x.idInstancia == consumo.idInstancia]
        instancias_revisadas.append(consumo.idInstancia)
        instancia = [x for x in cliente.lista_instancias if x.id_instancia == consumo.idInstancia][0]
        tiempo_total_instancia = 0
        for x in consumos_misma_instancia:
            tiempo_total_instancia += consumo.tiempo

        archivo += "    Instancia: "+instancia.nombre+"\n"
        archivo += "    Tiempo utilizado: "+str(tiempo_total_instancia)+" horas\n"
        conf = [x for x in global_configs if x.id_configuracion == instancia.id_config][0]
        archivo += "    Aporte: Q"+str(round(tiempo_total_instancia*conf.precio_total, 2))+" horas\n"
        archivo += "        Detalle de recursos: \n"
        for recurso in conf.lista_recursos:
            rec = [x for x in global_recursos if x.id_recurso == recurso.id_recurso]
            archivo += "            Recurso: "+rec.id_recurso+"\n"
            archivo += "                Nombre: "+rec.nombre+"\n"
            archivo += "                Cantidad: "+recurso.cantidad+"\n"
            archivo += "                Aporte: Q"+str(round(tiempo_total_instancia*rec.precio, 2))+"\n"

        total += tiempo_total_instancia*conf.precio_total


    archivo += "Total: Q"+str(round(total, 2))+"\n"

    return jsonify({"detalle": archivo})
    




if __name__ == "__main__":
    app.run(debug = True, port = 3100)




