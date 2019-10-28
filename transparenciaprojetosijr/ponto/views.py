from flask import Blueprint, render_template, redirect, flash, request, abort, url_for
from transparenciaprojetosijr.usuarios.forms import LoginForm, AdicionarUserForm, LogoutForm
from transparenciaprojetosijr import login_required, db
from transparenciaprojetosijr.ponto.models import Ponto, Presenca
from transparenciaprojetosijr.usuarios.models import Usuario
from datetime import datetime, time
from flask_login import current_user

ponto = Blueprint('ponto', __name__, template_folder='templates')

@ponto.route("/", methods=['POST', 'GET'])
@login_required()
def indexponto():

    login = LoginForm()
    adicionarUser = AdicionarUserForm()
    logout = LogoutForm()

    membroPresente = db.session.query(Ponto, Usuario).outerjoin(Ponto, Usuario.id == Ponto.usuario_id).filter_by(presente=True).first()
    existeMembro = False
    membrosPresentes = db.session.query(Ponto, Usuario).outerjoin(Ponto, Usuario.id == Ponto.usuario_id).filter_by(presente=True)

    if membroPresente:
       existeMembro = True

    return render_template("indexponto.html", login=login, adicionarUser=adicionarUser, logout=logout, existeMembro=existeMembro, membrosPresentes=membrosPresentes)

@ponto.route("/baterponto/<int:user_id>", methods=['POST', 'GET'])
@login_required()
def baterponto(user_id):
    
    id = user_id

    _ponto = Ponto.query.filter_by(usuario_id=id).first()
    if not _ponto:
        new_ponto = Ponto(current_user.id, True, datetime.now())
        db.session.add(new_ponto)
        db.session.commit()
    else:
        _ponto.data_saida = datetime.now()
        _ponto.presente = False

        dataResult = _ponto.data_saida-_ponto.data_entrada
        dataResult = str(dataResult)
        dataResult = dataResult.split(":")
        horas = int(dataResult[0])
        minutos = int(dataResult[1])
        
        tempo = time(horas,minutos,0)

        _presenca = Presenca(id,_ponto.data_entrada, tempo)

        db.session.add(_presenca)
        db.session.delete(_ponto)

        db.session.commit()

    return redirect(url_for("ponto.indexponto"))


@ponto.route("/relatorio")
@login_required()
def relatorio():

    login = LoginForm()
    adicionarUser = AdicionarUserForm()
    logout = LogoutForm()

    relatorioMembro = db.session.query(Presenca, Usuario).outerjoin(Presenca, Usuario.id == Presenca.usuario_id).filter_by(usuario_id=current_user.id)

    usuarios = Usuario.query.all()

    return render_template("presencatotal.html", login=login, adicionarUser=adicionarUser, logout=logout, relatorioMembro=relatorioMembro, usuarios=usuarios)

@ponto.route("/relatoriopessoal/<int:user_id>")
@login_required(['admin'])
def relatoriopessoal(user_id):

    login = LoginForm()
    adicionarUser = AdicionarUserForm()
    logout = LogoutForm()
    usuario = Usuario.query.get(user_id)

    relatorioMembro = db.session.query(Presenca, Usuario).outerjoin(Presenca, Usuario.id == Presenca.usuario_id).filter_by(usuario_id=user_id)

    return render_template("presenca.html", login=login, adicionarUser=adicionarUser, logout=logout, relatorioMembro=relatorioMembro, usuario=usuario)