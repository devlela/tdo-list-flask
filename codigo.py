import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
# Configurações: chave secreta, banco de dados e desativação do tracker de modificações
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Modelo de Tarefa para armazenamento no banco de dados
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)

# Cria as tabelas antes do primeiro request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    tarefas = Tarefa.query.all()
    return render_template("index.html", tarefas=tarefas)

@app.route("/add", methods=["POST"])
def add():
    conteudo = request.form.get("tarefa")
    if conteudo:
        nova_tarefa = Tarefa(conteudo=conteudo)
        db.session.add(nova_tarefa)
        db.session.commit()
        flash("Tarefa adicionada com sucesso!", "success")
    else:
        flash("Erro: tarefa vazia não pode ser adicionada.", "danger")
    return redirect(url_for("index"))

# A exclusão agora é feita via POST para evitar deleções acidentais
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    flash("Tarefa removida com sucesso!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)