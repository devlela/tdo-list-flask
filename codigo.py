from flask import Flask, render_template, request, redirect

app = Flask(__name__)
tarefas = []

@app.route("/")
def index():
    return render_template("index.html", tarefas=tarefas)

@app.route("/add", methods=["POST"])
def add():
    tarefa = request.form.get("tarefa")
    if tarefa:
        tarefas.append(tarefa)
    return redirect("/")

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(tarefas):
        tarefas.pop(index)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
