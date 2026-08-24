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
if __name__ == "__main__":
    app.run(debug=True)
