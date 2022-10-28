from django.shortcuts import render
import requests
from .forms import Cargar_datos, Form_cliente, Form_recurso, Form_categoria, Form_configuracion, Form_instancia, Form_fechas
from django.contrib import messages

endpoint = "http://127.0.0.1:3100"

def index(request):
        context = {
                'title': 'Index'}
        return render(request, "index.html", context)

def mensaje_configuracion(request):
        context = {
                'title': 'Mensaje de configuracion'}
        if request.method == 'POST':
                form=Cargar_datos(request.POST,request.FILES)
                if form.is_valid():
                        f = request.FILES['file']
                        xml_binary = f.read()
                        xml = xml_binary.decode('utf-8')
                        response = requests.post(endpoint+"/cargar_config",data=xml)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.danger(request, "Error, formulario no valido")
        else:
                return render(request, "mensaje_config.html")
        return render(request, "mensaje_config.html", context)

def mensaje_consumo(request):
        context = {
                'title': 'Mensaje de consumo'}
        if request.method == 'POST':
                form=Cargar_datos(request.POST,request.FILES)
                if form.is_valid():
                        f = request.FILES['file']
                        xml_binary = f.read()
                        xml = xml_binary.decode('utf-8')
                        response = requests.post(endpoint+"/cargar_consumo",data=xml)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.danger(request, "Error, formulario no valido")
        else:
                return render(request, "mensaje_consumo.html")
        return render(request, "mensaje_consumo.html", context)

def menu_operaciones(request):
        context = {
                'title': 'Menu Operaciones'}
        return render(request, "menu_operaciones.html", context)

def consultar_datos(request):
        r = requests.get(endpoint+"/consultar_datos")
        context = {
                'title': 'Consultar datos',
                'data': r.json()}
        return render(request, "consultar_datos.html", context)

def ayuda(request):
        context = {
                'title': 'Ayuda'}
        return render(request, "ayuda.html", context)

def crear_datos(request):
        context = {
                'title': 'Crear datos'}
        return render(request, "menu_c_datos.html", context)

def crear_recurso(request):
        context = {
                'title': 'Crear recurso'}
        if request.method == 'POST':
                form = Form_recurso(request.POST)
                json_data = {
                        "id_recurso" : request.POST['id_recurso'],
                        "nombre" : request.POST['nombre'],
                        "abrev" : request.POST['abrev'],
                        "metrica" : request.POST['metrica'],
                        "tipo" : request.POST['tipo'],
                        "precio" : request.POST['precio'],
                }
                if form.is_valid():
                        response = requests.post(endpoint+"/crear_recurso",json=json_data)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.error(request, "Error, formulario no valido")
        return render(request, "c_recurso.html", context)

def crear_cliente(request):
        context = {
                'title': 'Nuevo cliente'
                }
        
        if request.method == 'POST':
                form = Form_cliente(request.POST)
                json_data = {
                        "nit" : request.POST['nit'],
                        "nombre" : request.POST['nombre'],
                        "usuario" : request.POST['usuario'],
                        "clave" : request.POST['password'],
                        "direccion" : request.POST['direccion'],
                        "email" : request.POST['email'],
                }

                if form.is_valid():
                        response = requests.post(endpoint+"/crear_cliente",json=json_data)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.error(request, "Error, formulario no valido")
        return render(request, "c_cliente.html", context)

def crear_categoria(request):
        r = requests.get(endpoint+"/consultar_datos").json()
        context = {
                'title': 'Nueva categoria',
                'configuraciones': r["configs"]}
        
        if request.method == 'POST':
                form = Form_categoria(request.POST)
                json_data = {
                        "id_categoria" : request.POST['id_categoria'],
                        "nombre" : request.POST['nombre'],
                        "desc" : request.POST['desc'],
                        "carga" : request.POST['carga'],
                        "lista_configuraciones" : request.POST['configuraciones']
                }

                if form.is_valid():
                        response = requests.post(endpoint+"/crear_categoria",json=json_data)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.error(request, "Error, formulario no valido")
                        
        return render(request, "c_categoria.html", context)

def crear_configuracion(request):
        r = requests.get(endpoint+"/consultar_datos").json()
        context = {
                'title': 'Nueva configuracion',
                'recursos': r["recursos"]}
        
        if request.method == 'POST':
                form = Form_configuracion(request.POST)
                lista_recursos = []
                recs = request.POST.getlist('lista_recursos')
                
                for x in recs:
                        lista_recursos.append({"id_recurso": x, "cantidad": request.POST['cantidad_'+x]})

                json_data = {
                        "id_configuracion" : request.POST['id_configuracion'],
                        "nombre" : request.POST['nombre'],
                        "desc" : request.POST['desc'],
                        "lista_recursos" : lista_recursos
                }

                if form.is_valid():
                        response = requests.post(endpoint+"/crear_configuracion",json=json_data)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.error(request, "Error, formulario no valido")
                        
        return render(request, "c_configuracion.html", context)


def crear_instancia(request):
        r = requests.get(endpoint+"/consultar_datos").json()
        context = {
                'title': 'Nueva instancia',
                'clientes': r["usuarios"],
                'configuraciones': r["configs"]}
        
        if request.method == 'POST':
                form = Form_instancia(request.POST)

                json_data = {
                        "nit" : request.POST['nit'],
                        "nombre" : request.POST['nombre'],
                        "id_instancia" : request.POST['id_instancia'],
                        "id_config" : request.POST['id_config']
                }

                if form.is_valid():
                        response = requests.post(endpoint+"/crear_instancia",json=json_data)
                        messages.info(request, response.json()["mensaje"])
                else:
                        messages.error(request, "Error, formulario no valido")
                     
        return render(request, "c_instancia.html", context)

def cancelar_instancia(request):
        r = requests.get(endpoint+"/consultar_datos").json()
        context = {
                'title': 'Cancelar instancia',
                'clientes': r["usuarios"],
                'instancias': [],
                "seleccionado": ""}

        if request.method == 'POST':
                if request.POST:
                        json_data = {
                                "id_instancia" : request.POST['id_instancia'],
                                }
                        response = requests.post(endpoint+"/cancelar_instancia",json=json_data)
                        messages.error(request, response.json()["mensaje"])
                        
        elif request.method == 'GET':
                if request.GET:
                        context["seleccionado"] = request.GET['nit']
                        cliente = [x for x in context["clientes"] if x["nit"] == request.GET['nit']][0]
                        context["instancias"] = [x for x in r["instancias"] if x["id_instancia"] in cliente["lista_instancias"] and x["estado"].lower() != "cancelada"]
                        return render(request, "cancelar_instancia.html", context)
        else:
                return render(request, "cancelar_instancia.html", context)
        return render(request, "cancelar_instancia.html", context)

def facturar(request):
        context = {
                'title': 'Facturacion'}
        
        if request.method == 'POST':
                form = Form_fechas(request.POST)

                if form.is_valid():
                        json_data = {
                                "fecha_inicio" : request.POST['f_inicio'],
                                "fecha_final" : request.POST['f_final']
                                }
                        response = requests.post(endpoint+"/facturar",json=json_data)
                        messages.info(request, response.json()["mensaje"])
                
        return render(request, "facturacion.html", context)


def reportes(request):
        context = {
                'title': 'Reportes pdf'}
        return render(request, "Reportes", context)
