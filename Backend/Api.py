from Clases import *
from xml.dom.minidom import parse, parseString
from flask import Flask, jsonify, request
import re
from datetime import datetime, date

global_categorias = []
global_recursos = []
global_configs = []
global_clientes = []
global_consumos = []
global_facturas = []
global_instancias = []
open("sys.app", "w").close()

app = Flask(__name__)

@app.route("/consultar_datos" )
def consultar_datos():
    usuarios = [x.convertir_json() for x in global_clientes]
    categorias = [x.convertir_json() for x in global_categorias]
    recursos = [x.convertir_json() for x in global_recursos]
    configs =[x.convertir_json() for x in global_configs]
    instancias = [x.convertir_json() for x in global_instancias]
    return jsonify({"usuarios": usuarios,
                    "categorias": categorias,
                    "recursos": recursos,
                    "configs": configs,
                    "instancias": instancias})

@app.route("/crear_recurso", methods = ["POST"])
def crear_recurso():
    n_recurso = Recurso(request.json["id_recurso"], request.json["nombre"],
                        request.json["abrev"], request.json["metrica"],
                        request.json["tipo"], float(request.json["precio"]))

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
    precio_total = 0
    
    for recurso in json_lista_recursos:
        id_recurso = recurso["id_recurso"].strip()
        cantidad = int(recurso["cantidad"])
        rec = [x for x in global_recursos if x.id_recurso == id_recurso]
        precio_total += rec[0].precio*cantidad
        lista_recursos.append(Recurso_conf(id_recurso, cantidad))
        
    
    n_configuracion = Configuracion(request.json["id_configuracion"], request.json["nombre"],
                                    request.json["desc"], precio_total, lista_recursos)

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
                          date.today(), "Vigente", "", request.json["nombre"])
    
    cliente[0].lista_instancias.append(n_instancia)
    global_instancias.append(n_instancia)
    
    return jsonify({"mensaje": "se ha creado la instancia para el usuario "+cliente[0].nombre+" on exito"})

@app.route("/cancelar_instancia", methods = ["POST"])
def cancelar_instancia():
    
    instancia = [x for x in global_instancias if x.id_instancia == request.json["id_instancia"]][0]

    instancia.estado = "Cancelada"
    instancia.f_final = date.today()
    
    return jsonify({"mensaje": "Se ha cancelado la instancia "+instancia.nombre})

@app.route("/cargar_config", methods = ["POST"])
def cargar_config():
    clientes_creados = 0
    instancias_creadas = 0
    recursos_creados  = 0
    categorias_creadas = 0
    configs_creadas = 0

    try:
        xml_S = request.get_data().decode('utf-8', 'ignore')
        file = open("sys.app","w")
        file.write(xml_S+"\n")
        file.close()
        
        xml_O = parseString(xml_S)

        listaRecursos = xml_O.getElementsByTagName("listaRecursos")[0]
        Recursos = listaRecursos.getElementsByTagName("recurso")
        for recurso in Recursos:
            id_recurso = recurso.attributes["id"].value.strip()
            nombre = recurso.getElementsByTagName("nombre")[0].firstChild.data.strip()
            abrev = recurso.getElementsByTagName("abreviatura")[0].firstChild.data.strip()
            metrica = recurso.getElementsByTagName("metrica")[0].firstChild.data.strip()
            tipo = recurso.getElementsByTagName("tipo")[0].firstChild.data.strip()
            precio = float(recurso.getElementsByTagName("valorXhora")[0].firstChild.data)

            global_recursos.append(Recurso(id_recurso, nombre, abrev, metrica, tipo, precio))
            recursos_creados += 1

        listaCategorias = xml_O.getElementsByTagName("listaCategorias")[0]
        Categorias = listaCategorias.getElementsByTagName("categoria")
        for categoria in Categorias:
            id_categoria = categoria.attributes["id"].value.strip()
            nombre_categoria = categoria.getElementsByTagName("nombre")[0].firstChild.data.strip()
            desc_categoria = categoria.getElementsByTagName("descripcion")[0].firstChild.data.strip()
            carga = categoria.getElementsByTagName("cargaTrabajo")[0].firstChild.data.strip()
            lista_configuraciones = []
            
            Configuraciones = categoria.getElementsByTagName("configuracion")
            for configuracion in Configuraciones:
                id_configuracion = configuracion.attributes["id"].value.strip()
                configuracion_ya = [x for x in global_configs if x.id_configuracion == id_configuracion]
                if len(configuracion_ya) != 0:
                    lista_configuraciones.append(configuracion_ya[0])
                    continue
                nombre_conf = configuracion.getElementsByTagName("nombre")[0].firstChild.data.strip()
                desc_conf = configuracion.getElementsByTagName("descripcion")[0].firstChild.data.strip()
                lista_recursos = []
                precio_total = 0

                Recursos = configuracion.getElementsByTagName("recurso")
                for recurso in Recursos:
                    id_recurso = recurso.attributes["id"].value.strip()
                    cantidad = int(recurso.firstChild.data)
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
            nit = cliente.attributes["nit"].value.strip()
            nombre = cliente.getElementsByTagName("nombre")[0].firstChild.data.strip()
            usuario = cliente.getElementsByTagName("usuario")[0].firstChild.data.strip()
            clave = cliente.getElementsByTagName("clave")[0].firstChild.data.strip()
            direccion = cliente.getElementsByTagName("direccion")[0].firstChild.data.strip()
            email = cliente.getElementsByTagName("correoElectronico")[0].firstChild.data.strip()
            lista_instancias = []

            Instancias = cliente.getElementsByTagName("instancia")
            for instancia in Instancias:
                id_instancia = instancia.attributes["id"].value
                id_config = instancia.getElementsByTagName("idConfiguracion")[0].firstChild.data.strip()
                fechai = instancia.getElementsByTagName("fechaInicio")[0].firstChild.data.strip()
                match_str = re.search(r'\d{2}/\d{2}/\d{4}', fechai)
                if match_str != None:
                    f_inicio = datetime.strptime(match_str.group(), '%d/%m/%Y').date()
                else:
                    f_inicio = ""
                estado = instancia.getElementsByTagName("estado")[0].firstChild.data.strip()
                if estado.lower() == "cancelada":
                    fechaf = instancia.getElementsByTagName("fechaFinal")[0].firstChild.data.strip()
                    match_str = re.search(r'\d{2}/\d{2}/\d{4}', fechaf)
                    f_final = datetime.strptime(match_str.group(), '%d/%m/%Y').date()
                else:
                    f_final = ""
                nombre_instancia = instancia.getElementsByTagName("nombre")[0].firstChild.data.strip()
                insta = Instancia(id_instancia, id_config, f_inicio, estado, f_final, nombre_instancia)
                lista_instancias.append(insta)
                global_instancias.append(insta)
                instancias_creadas += 1
            
            global_clientes.append(Cliente(nit, nombre, usuario, clave, direccion, email, lista_instancias))
            clientes_creados += 1

    except:
        return jsonify({"mensaje": "Error, no se ha podido cargar la informacion"})
    
    return jsonify({"mensaje": "se han creado "+str(clientes_creados)+" clientes, "+str(instancias_creadas)+" instancias, "
                    +str(recursos_creados)+" recursos, "+str(categorias_creadas)+" categorias y "+str(configs_creadas)+" configuraciones con exito"})

@app.route("/cargar_consumo", methods = ["POST"])
def cargar_consumo():
    consumos_procesados = 0

    try:
        xml_S = request.get_data()

        xml_O = parseString(xml_S)

        Consumos = xml_O.getElementsByTagName("consumo")

        for consumo in Consumos:
            nitCliente = consumo.attributes["nitCliente"].value
            idInstancia = consumo.attributes["idInstancia"].value
            tiempo = float(consumo.getElementsByTagName("tiempo")[0].firstChild.data)
            fechah = consumo.getElementsByTagName("fechaHora")[0].firstChild.data
            match_str = re.search(r'\d{2}/\d{2}/\d{4}', fechah)
            fechaHora = datetime.strptime(match_str.group(), '%d/%m/%Y').date()

            global_consumos.append(Consumo(nitCliente, idInstancia, tiempo, fechaHora))
            consumos_procesados += 1
    except:
        return jsonify({"mensaje": "Error, no se ha podido cargar la informacion"})
    
    return jsonify({"mensaje": "se han procesado "+str(consumos_procesados)+" consumos"})

@app.route("/facturar", methods = ["POST"])
def facturar():
    facturas_creadas = 0
    
    f_inicio = datetime.strptime(request.json["fecha_inicio"], '%Y-%m-%d').date()
    f_final = datetime.strptime(request.json["fecha_final"], '%Y-%m-%d').date()
    consumos_por_facturar = [x for x in global_consumos if x.fechaHora > f_inicio and x.fechaHora < f_final and x.facturado == False]

    for consumo in consumos_por_facturar:
        consumo.facturado = True
        
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
        
@app.route("/detalle_factura", methods = ["POST"])
def detalle_factura():
    id_factura = request.json["id_factura"]
    archivo = "                            Detalle para la Factura "+id_factura+"\n"
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
            tiempo_total_instancia += x.tiempo

        archivo += "    Instancia: "+instancia.nombre+"\n"
        archivo += "    Tiempo utilizado: "+str(tiempo_total_instancia)+" horas\n"
        conf = [x for x in global_configs if x.id_configuracion == instancia.id_config][0]
        archivo += "    Aporte: Q"+str(round(tiempo_total_instancia*conf.precio_total, 2))+"\n"
        archivo += "        Detalle de recursos: \n"
        for recurso in conf.lista_recursos:
            rec = [x for x in global_recursos if x.id_recurso == recurso.id_recurso][0]
            archivo += "            Recurso: "+rec.id_recurso+"\n"
            archivo += "                Nombre: "+rec.nombre+" "+rec.metrica+"\n"
            archivo += "                Cantidad: "+str(recurso.cantidad)+"\n"
            archivo += "                Aporte: Q"+str(round(tiempo_total_instancia*rec.precio*recurso.cantidad, 2))+"\n"

        total += tiempo_total_instancia*conf.precio_total


    archivo += "Total: Q"+str(round(total, 2))+"\n"

    print(archivo)
    return jsonify({"detalle": archivo})
    
@app.route("/analisis_cat", methods = ["POST"])
def analisis_cat():
    archivo = "                            Analisis de Categoria y configuraciones\n"
    f_inicio = datetime.strptime(request.json["fecha_inicio"], '%Y-%m-%d').date()
    f_final = datetime.strptime(request.json["fecha_final"], '%Y-%m-%d').date()

    archivo += "Fecha inicial:"+str(f_inicio)+"\n"
    archivo += "Fecha final:"+str(f_final)+"\n"
    
    categorias = []
    configuraciones = []
    consumos_por_analizar = [x for x in global_consumos if x.fechaHora > f_inicio and x.fechaHora < f_final]
    print(consumos_por_analizar)
    for configuracion in global_configs:
        aporte = 0
        instancias_con_configuracion = [x.id_instancia for x in global_instancias if x.id_config == configuracion.id_configuracion]
        for consumo in consumos_por_analizar:
            if consumo.idInstancia in instancias_con_configuracion:
                aporte += configuracion.precio_total * consumo.tiempo
        configuraciones.append((configuracion,round(aporte, 2)))

    for categoria in global_categorias:
        aporte = 0
        for conf in configuraciones:
            if conf[0] in categoria.lista_configuraciones:
                aporte += conf[1]
        categorias.append((categoria, round(aporte, 2)))

    archivo += "Categorias\n"
    categorias.sort(key= lambda e: e[1], reverse = True)
    configuraciones.sort(key= lambda e: e[1], reverse = True)
    i = 1
    for categoria in categorias:
        archivo += "    "+str(i)+". "+categoria[0].id_categoria+": Q"+str(categoria[1])+"\n"
        i+=1

    archivo += "Configuraciones\n"
    i = 1
    for conf in configuraciones:
        archivo += "    "+str(i)+". "+conf[0].id_configuracion+": Q"+str(conf[1])+"\n"
        i+=1

    print(archivo)
    return jsonify({"resultado": archivo})


@app.route("/analisis_rec", methods = ["POST"])
def analisis_rec():
    archivo = "                                          Analisis de Recursos\n"
    f_inicio = datetime.strptime(request.json["fecha_inicio"], '%Y-%m-%d').date()
    f_final = datetime.strptime(request.json["fecha_final"], '%Y-%m-%d').date()
    
    archivo += "Fecha inicial:"+str(f_inicio)+"\n"
    archivo += "Fecha final:"+str(f_final)+"\n"

    consumos_por_analizar = [x for x in global_consumos if x.fechaHora > f_inicio and x.fechaHora < f_final]

    recursos = [[x,0] for x in global_recursos]

    for consumo in consumos_por_analizar:
        instancia = [x for x in global_instancias if x.id_instancia == consumo.idInstancia][0]
        configuracion = [x for x in global_configs if instancia.id_config == x.id_configuracion][0]
        for recurso in configuracion.lista_recursos:
            cantidad = recurso.cantidad
            rec = [x for x in recursos if x[0].id_recurso == recurso.id_recurso][0]
            rec[1] += round(cantidad*rec[0].precio*consumo.tiempo, 2)
    
    recursos.sort(key= lambda e: e[1], reverse = True)
    archivo += "Recursos\n"
    i = 1
    for recurso in recursos:
        archivo += "    "+str(i)+". "+recurso[0].id_recurso+": Q"+str(recurso[1])+"\n"
        i+=1

    print(archivo)
    return jsonify({"resultado": archivo})

@app.route("/get_facturas")
def get_facturas():
    return jsonify({"facturas": [x.id_factura for x in global_facturas]})


if __name__ == "__main__":
    app.run(debug = True, port = 3100)




