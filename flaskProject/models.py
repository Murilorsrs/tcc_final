from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = 'cadastroUsuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(254))
    telefone = db.Column(db.String(20))
    senha = db.Column(db.String(100))


class Configuracao(db.Model):
    __tablename__ = 'configuracoes'
    id_config = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('cadastroUsuario.id_usuario'), nullable=True)
    umidade_min = db.Column(db.Numeric, nullable=True)
    umidade_max = db.Column(db.Numeric, nullable=True)
    usuario = db.relationship('Usuario', backref=db.backref('configuracoes', lazy=True))


class AgendaIrrigacaoAutomatica(db.Model):
    __tablename__ = 'agendaIrrigacaoAutomatica'
    id_agendaAuto = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('cadastroUsuario.id_usuario'), nullable=True)
    data_ini = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    hora_ini = db.Column(db.Time, nullable=False)
    id_config = db.Column(db.Integer, db.ForeignKey('configuracoes.id_config'), nullable=True)

    usuario = db.relationship('Usuario', backref=db.backref('agendas', lazy=True))
    configuracao = db.relationship('Configuracao', backref=db.backref('agendas', lazy=True))

