from flask import Flask

app = Flask(__name__)


@app.route("/")
def status():
    return {
        "message": "sua criação, esta vivo!"
    }


@app.route("/health")
def health():
    return {
        "status": "ok"
    }

@app.route("/status")
def status_servico():
    return {
        "status": "online",
        "servico": "OpsTrack API"
    }
    @app.route("/tickets")
def listar_tickets():
    return {
        "tickets": [
            {"id": 1, "titulo": "Servidor lesma", "status": "aberto"},
            {"id": 2, "titulo": "falha ao logar", "status": "em andamento, carregando"},
            {"id": 3, "titulo": "Erro de backup", "status": "resolvido"}
        ]
    }
if __name__ == "__main__":
    app.run(debug=True)
