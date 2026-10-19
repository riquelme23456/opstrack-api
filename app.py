from flask import Flask

app = Flask(__name__)


@app.route('/')
def status():
    return {'servico': 'OpsTrack API', 'status': 'online'}


@app.route('/status')
def health_check():
    return {'status': 'ok'}


@app.route('/version')
def version():
    return {'version': '1.2'}


@app.route('/tickets')
def listar_tickets():
    tickets_mock = [
        {'id': 1, 'titulo': 'Impressora do 3o andar sem toner'},
        {'id': 2, 'titulo': 'VPN caindo para usuários remotos'},
    ]
    return {'tickets': tickets_mock}


@app.route('/usuarios')
def listar_usuarios():
    usuarios_mock = [
        {'id': 1, 'nome': 'Fulano de Tal'},
        {'id': 2, 'nome': 'Beltrano'},
    ]
    return {'usuarios': usuarios_mock}


if __name__ == '__main__':
    app.run(debug=True)
