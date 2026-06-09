# ============================================================
#  app.py  —  Servidor Flask + SocketIO do Transpilador FIN
# ============================================================

import os
import sys
import subprocess
import tempfile
import threading
import queue

from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
SRC_DIR    = os.path.join(BASE_DIR, 'src')
ANTLR_DIR  = os.path.join(BASE_DIR, 'antlr')
TESTES_DIR = os.path.join(BASE_DIR, 'testes')
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, ANTLR_DIR)

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from FINLexer  import FINLexer
from FINParser import FINParser
from semantic_antlr import SemanticError, analyze
from codegen_antlr  import generate

app = Flask(__name__, static_folder=BASE_DIR)
app.config['SECRET_KEY'] = 'fin-transpilador'
socketio = SocketIO(app, cors_allowed_origins="*")

# Guarda processos ativos por sessão
processos = {}


class FINErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f'Linha {line}, coluna {column}: {msg}')


def transpile_source(source: str):
    stream       = InputStream(source)
    lexer        = FINLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser       = FINParser(token_stream)

    error_listener = FINErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.prog()

    if error_listener.errors:
        return None, '[Erro Sintático] ' + ' | '.join(error_listener.errors)

    try:
        symbols = analyze(tree, parser)
        code    = generate(tree, symbols)
        return code, None
    except SemanticError as e:
        return None, f'[Erro Semântico] {e}'
    except Exception as e:
        return None, f'[Erro Interno] {e}'


# ── Rotas HTTP ───────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'interface.html')


@app.route('/transpilar', methods=['POST'])
def transpilar():
    data   = request.get_json()
    source = data.get('codigo', '')
    if not source.strip():
        return jsonify({'python': '', 'erro': None})
    code, erro = transpile_source(source)
    return jsonify({'python': code or '', 'erro': erro})


@app.route('/testes', methods=['GET'])
def listar_testes():
    try:
        arquivos = sorted([f for f in os.listdir(TESTES_DIR) if f.endswith('.fin')])
        return jsonify({'arquivos': arquivos})
    except Exception as e:
        return jsonify({'arquivos': [], 'erro': str(e)})


@app.route('/testes/<nome>', methods=['GET'])
def carregar_teste(nome):
    if not nome.endswith('.fin'):
        return jsonify({'conteudo': '', 'erro': 'Arquivo inválido.'}), 400
    path = os.path.join(TESTES_DIR, nome)
    if not os.path.exists(path):
        return jsonify({'conteudo': '', 'erro': 'Arquivo não encontrado.'}), 404
    with open(path, encoding='utf-8') as f:
        conteudo = f.read()
    return jsonify({'conteudo': conteudo, 'nome': nome})


# ── WebSocket — execução interativa ─────────────────────────
@socketio.on('iniciar_execucao')
def iniciar_execucao(data):
    sid      = request.sid
    codigo   = data.get('codigo', '')

    if not codigo.strip():
        emit('saida', {'texto': 'Nenhum código para executar.', 'tipo': 'erro'})
        emit('fim')
        return

    # Salva código em arquivo temporário
    tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.py', delete=False, encoding='utf-8'
    )
    tmp.write(codigo)
    tmp.close()

    def rodar():
        try:
            proc = subprocess.Popen(
                [sys.executable, '-u', tmp.name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,
            )
            processos[sid] = proc

            # Lê stdout linha por linha
            for linha in iter(proc.stdout.readline, ''):
                socketio.emit('saida', {'texto': linha.rstrip('\n'), 'tipo': 'saida'}, to=sid)

            proc.wait()
            os.unlink(tmp.name)

            if proc.returncode != 0:
                erro = proc.stderr.read()
                if erro:
                    socketio.emit('saida', {'texto': erro, 'tipo': 'erro'}, to=sid)

        except Exception as e:
            socketio.emit('saida', {'texto': str(e), 'tipo': 'erro'}, to=sid)
        finally:
            processos.pop(sid, None)
            socketio.emit('fim', {}, to=sid)

    t = threading.Thread(target=rodar, daemon=True)
    t.start()


@socketio.on('enviar_input')
def enviar_input(data):
    sid   = request.sid
    valor = data.get('valor', '') + '\n'
    proc  = processos.get(sid)
    if proc and proc.stdin:
        try:
            proc.stdin.write(valor)
            proc.stdin.flush()
            # Ecoa o input na tela do usuário
            socketio.emit('saida', {'texto': valor.rstrip('\n'), 'tipo': 'input'}, to=sid)
        except Exception:
            pass


@socketio.on('parar_execucao')
def parar_execucao():
    sid  = request.sid
    proc = processos.get(sid)
    if proc:
        proc.terminate()
        processos.pop(sid, None)
    socketio.emit('fim', {}, to=sid)


@socketio.on('disconnect')
def disconnect():
    sid  = request.sid
    proc = processos.get(sid)
    if proc:
        proc.terminate()
        processos.pop(sid, None)


if __name__ == '__main__':
    print('=' * 50)
    print('  Transpilador FIN rodando em:')
    print('  http://localhost:5000')
    print('=' * 50)
    socketio.run(app, debug=True, port=5000)
