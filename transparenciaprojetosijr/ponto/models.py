from transparenciaprojetosijr.usuarios.models import Usuario
from transparenciaprojetosijr import db

class Ponto(db.Model):

    __tablename__ = "pontos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    presente = db.Column(db.Boolean, nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False)
    data_saida = db.Column(db.DateTime)

    def __init__(self, _usuario, _presente, _dataEntrada):
        self.usuario_id = _usuario
        self.presente = _presente
        self.data_entrada = _dataEntrada


class Presenca(db.Model):

    __tablename__ = "presencas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    horas = db.Column(db.Time, nullable=False)

    def __init__(self, _usuario, _data, _horas):
        self.usuario_id = _usuario
        self.data = _data
        self.horas = _horas
