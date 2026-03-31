from flask import Flask, render_template, request, redirect
from models import db, Jogador, Partida, ParticipacaoPartida
import os
from datetime import datetime
from sqlalchemy import func


# Rodar o projeto:
# python app.py
#
# App Futebol

## Como rodar o projeto

# 1. Ativar ambiente virtual
# 2. Rodar:
#    python app.py

# ## Acessar no navegador

# http://127.0.0.1:5000/
# http://127.0.0.1:5000/jogadores

# venv\Scripts\Activate.ps1
# python -m venv venv 
# pip freeze > requirements.txt - 


app = Flask(__name__) 

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'futebol.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Banco criado com sucesso!") 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/jogadores')
def listar_jogadores():
    jogadores = Jogador.query.all()
    return render_template('jogadores.html', jogadores=jogadores)

@app.route('/jogadores/cadastrar', methods=['POST'])
def cadastrar_jogador():
    nome = request.form.get('nome')
    apelido = request.form.get('apelido')
    posicao = request.form.get('posicao')

    novo_jogador = Jogador(
        nome=nome,
        apelido=apelido,
        posicao=posicao
    )

    db.session.add(novo_jogador)
    db.session.commit()

    return redirect('/jogadores')

@app.route('/partidas')
def listar_partidas():
    partidas = Partida.query.order_by(Partida.data.desc()).all()
    return render_template('partidas.html', partidas=partidas)


@app.route('/partidas/nova')
def nova_partida():
    jogadores = Jogador.query.order_by(Jogador.nome.asc()).all()
    return render_template('nova_partida.html', jogadores=jogadores)


@app.route('/partidas/cadastrar', methods=['POST'])
def cadastrar_partida():
    data_str = request.form.get('data')
    jogadores_ids = request.form.getlist('jogadores')

    data_partida = datetime.strptime(data_str, '%Y-%m-%dT%H:%M')

    nova_partida = Partida(data=data_partida)
    db.session.add(nova_partida)
    db.session.commit()

    # Buscar jogadores selecionados
    jogadores = Jogador.query.filter(Jogador.id.in_(jogadores_ids)).all()

    # Dividir em dois times de forma simples
    metade = len(jogadores) // 2
    time_a = jogadores[:metade]
    time_b = jogadores[metade:]

    # Salvar participações
    for jogador in time_a:
        participacao = ParticipacaoPartida(
            jogador_id=jogador.id,
            partida_id=nova_partida.id,
            time='A'
        )
        db.session.add(participacao)

    for jogador in time_b:
        participacao = ParticipacaoPartida(
            jogador_id=jogador.id,
            partida_id=nova_partida.id,
            time='B'
        )
        db.session.add(participacao)

    db.session.commit()

    return redirect('/partidas')

@app.route('/partidas/<int:id>')
def detalhes_partida(id):
    partida = Partida.query.get_or_404(id)

    time_a = ParticipacaoPartida.query.filter_by(partida_id=id, time='A').all()
    time_b = ParticipacaoPartida.query.filter_by(partida_id=id, time='B').all()

    return render_template(
        'detalhes_partida.html',
        partida=partida,
        time_a=time_a,
        time_b=time_b
    )

@app.route('/partidas/<int:id>/atualizar', methods=['POST'])
def atualizar_partida(id):
    participacoes = ParticipacaoPartida.query.filter_by(partida_id=id).all()

    for p in participacoes:
        gols = request.form.get(f'gols_{p.id}')
        assistencias = request.form.get(f'assistencias_{p.id}')
        nota = request.form.get(f'nota_{p.id}')

        p.gols = int(gols) if gols else 0
        p.assistencias = int(assistencias) if assistencias else 0
        p.nota = float(nota) if nota else 0

    db.session.commit()

    return redirect(f'/partidas/{id}')

@app.route('/ranking')
def ranking():
    ranking_jogadores = (
        db.session.query(
            Jogador.nome,
            func.coalesce(func.sum(ParticipacaoPartida.gols), 0).label('total_gols'),
            func.coalesce(func.sum(ParticipacaoPartida.assistencias), 0).label('total_assistencias'),
            func.coalesce(func.avg(ParticipacaoPartida.nota), 0).label('media_nota'),
            func.count(ParticipacaoPartida.id).label('total_partidas')
        )
        .join(ParticipacaoPartida, Jogador.id == ParticipacaoPartida.jogador_id)
        .group_by(Jogador.id, Jogador.nome)
        .order_by(
            func.coalesce(func.avg(ParticipacaoPartida.nota), 0).desc(),
            func.coalesce(func.sum(ParticipacaoPartida.gols), 0).desc()
        )
        .all()
    )

    return render_template('ranking.html', ranking_jogadores=ranking_jogadores)

if __name__ == '__main__':
    app.run(debug=True)

