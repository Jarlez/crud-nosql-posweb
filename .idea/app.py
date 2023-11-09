from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')
collection_carros = client.veiculos.carro

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listar")
def lista():
    carros = collection_carros.find()
    return render_template("listar.html", carros=carros)

@app.route("/cadastrar")
def insere_veiculo():
    return render_template("cadastrar.html")

@app.route("/cadastrar_bd", methods=['POST'])
def cadastra_veiculo():
    novo_carro = {field: request.form[field] for field in ["marca", "modelo", "ano", "categoria", "preco", "tipo"]}
    collection_carros.insert_one(novo_carro)
    return redirect("/listar")

@app.route("/<id>/editar")
def editar_carro(id):
    carro = collection_carros.find_one({"_id": ObjectId(id)})
    return render_template("/atualizar.html", carro=carro)

@app.route("/atualizar_bd", methods=["POST"])
def atualiza_carro():
    id_carro = request.form['id']
    dados_atualizados = {field: request.form[field] for field in ["marca", "modelo", "ano", "categoria", "preco", "tipo"]}
    collection_carros.update_one({"_id": ObjectId(id_carro)}, {"$set": dados_atualizados})
    return redirect("/listar")

@app.route("/<id>/excluir")
def excluir_veiculo(id):
    collection_carros.delete_one({"_id": ObjectId(id)})
    return redirect("/listar")

if __name__ == '__main__':
    app.run(debug=True)