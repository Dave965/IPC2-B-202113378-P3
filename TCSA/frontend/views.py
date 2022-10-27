from django.shortcuts import render
import requests

endpoint = "http://127.0.0.1:3100"

def index(request):
        context = {
                'title': 'Index'}
        return render(request, "index.html", context)

def mensaje_configuracion(request):
        context = {
                'title': 'Mensaje de configuracion'}
        return render(request, "mensaje_config.html", context)

def mensaje_consumo(request):
        context = {
                'title': 'Mensaje de consumo'}
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

