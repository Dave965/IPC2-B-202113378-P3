from Clases import *
from flask import Flask, jsonify

global_categorias = []
global_recursos = []
global_configs = []
global_clientes = [Cliente("nit", "nombre", "usuario", "clave", "direccion", "email", [Instancia("1","2104","12/17/2024","cancelada",None),Instancia("2","3104","12/11/2024","activa",None)])]

app = Flask(__name__)

@app.route("/principal")
def principal():
    data = [x.convertir_json() for x in global_clientes]
    return jsonify({"datos": data})

if __name__ == "__main__":
    app.run(debug = True, port = 3100)
