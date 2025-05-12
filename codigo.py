import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Utiliza a variável de ambiente para a chave secreta, garantindo persistência entre reinicializações.
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(24))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Configuração básica de logging para identificar erros no servidor.
logging.basicConfig(level=logging.INFO)

# Modelo de Tarefa para armazenamento no banco de dados.
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)

# Cria as tabelas necessárias antes do primeiro request.
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    try:
        tarefas = Tarefa.query.all()
    except Exception as e:
        logging.error("Erro ao carregar tarefas: %s", e)
        tarefas = []
    return render_template("index.html", tarefas=tarefas)

@app.route("/add", methods=["POST"])
def add():
    conteudo = request.form.get("tarefa")
    if conteudo:
        try:
            nova_tarefa = Tarefa(conteudo=conteudo)
            db.session.add(nova_tarefa)
            db.session.commit()
            flash("Tarefa adicionada com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            logging.error("Erro ao adicionar tarefa: %s", e)
            flash("Erro ao adicionar tarefa.", "danger")
    else:
        flash("Erro: tarefa vazia não pode ser adicionada.", "danger")
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    try:
        tarefa = Tarefa.query.get_or_404(id)
        db.session.delete(tarefa)
        db.session.commit()
        flash("Tarefa removida com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        logging.error("Erro ao remover tarefa: %s", e)
        flash("Erro ao remover tarefa.", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Em produção, lembre-se de desabilitar o modo debug.
    app.run(debug=True)