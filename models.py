from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# =========================
# TABELA: Jogador
# =========================
class Jogador(db.Model):
    __tablename__ = 'jogadores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    apelido = db.Column(db.String(50))
    posicao = db.Column(db.String(30))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Jogador {self.nome}>'


# =========================
# TABELA: Partida
# =========================
class Partida(db.Model):
    __tablename__ = 'partidas'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # relacionamento com participações
    participacoes = db.relationship(
        'ParticipacaoPartida',
        back_populates='partida',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Partida {self.id}>'


# =========================
# TABELA: Participação
# =========================
class ParticipacaoPartida(db.Model):
    __tablename__ = 'participacoes_partida'

    id = db.Column(db.Integer, primary_key=True)

    jogador_id = db.Column(
        db.Integer,
        db.ForeignKey('jogadores.id'),
        nullable=False
    )

    partida_id = db.Column(
        db.Integer,
        db.ForeignKey('partidas.id'),
        nullable=False
    )

    time = db.Column(db.String(1))  # A ou B
    gols = db.Column(db.Integer, default=0)
    assistencias = db.Column(db.Integer, default=0)
    nota = db.Column(db.Float)
    presenca = db.Column(db.Boolean, default=True)

    # relacionamentos
    jogador = db.relationship('Jogador', backref='participacoes')
    partida = db.relationship('Partida', back_populates='participacoes')

    def __repr__(self):
        return f'<Participacao J:{self.jogador_id} P:{self.partida_id}>'