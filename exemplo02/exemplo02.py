'''

Pequeno exemplo de como autenticar usuário usando o flask-sqlalchemy e flask-wtf.

Recursos protegidos só poderão ser acessados por usuários que já passaram pela autenticação

http://flask-sqlalchemy.pocoo.org/2.3/

http://flask.pocoo.org/docs/1.0/patterns/wtforms/

https://flask-wtf.readthedocs.io/en/stable/

https://wtforms.readthedocs.io/en/stable/

'''

from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from loginform import LoginForm

SECRET_KEY = 'aula de BCD - string aleatória'


app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo-02.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

# Para gerar o banco de dados pela 1a. vez:
#
# Executar a shell interativa do python3 e dentro dela digitar:
#
# from exemplo02 import db, Usuario
# db.create_all()

class Usuario(db.Model):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = kwargs.pop('username')
        self.email = kwargs.pop('email')
        self.password_hash = generate_password_hash(kwargs.pop('password_hash'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@app.route('/login', methods=['GET', 'POST'])
def autenticar():

    form = LoginForm()

    if form.validate_on_submit():

        # Veja mais em: http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
        usuario = Usuario.query.filter_by(username=form.username.data).first_or_404()

        if (usuario.check_password(form.password.data)):
            session['logged_in'] = True
            session['usuario'] = usuario.username
            return render_template('autenticado.html', title="Usuário autenticado", user=session.get('usuario'))
        else:
            flash('Usuário ou senha inválidos')
            return redirect(url_for('inicio'))

    return render_template('login.html', title='Autenticação de usuários', form=form)


@app.route('/painel')
def painel():
    '''
    Somente usuários autenticados poderão acessar essa URL
    :return: página com dados pessoais do usuário que está autenticado
    '''
    if session.get('logged_in'):
        # Veja mais em: http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
        usuario = Usuario.query.filter_by(username=session.get('usuario')).first_or_404()
        return render_template('dados.html', title="Usuário autenticado", user=usuario)
    return redirect(url_for('inicio'))


@app.route('/')
def inicio():
    '''
    Se não existir a chave 'logged_in' = True na sessão, então redireciona para página de login
    :return: página para fazer login ou página para usuários autenticados
    '''
    if not session.get('logged_in'):
        return redirect(url_for('autenticar'))
    else:
        return render_template('autenticado.html', title='Usuário autenticado', user=session.get('usuario'))



@app.route("/logout")
def logout():
    '''
    Para encerrar a sessão autenticada de um usuário
    :return: redireciona para a página inicial
    '''
    session['logged_in'] = False
    return redirect(url_for('inicio'))



@app.errorhandler(404)
def page_not_found(e):
    '''
    Para tratar erros de páginas não encontradas - HTTP 404
    :param e:
    :return:
    '''
    return render_template('404.html'), 404



@app.route('/criar')
def criando_usuario_inadequadamente():
    '''
    Exemplo de como criar um usuário na base de uma maneira nada adequada.

    Deve-se invocar a URL da seguinte forma: http://localhost:5000/criar?login=juca&email=a@a.com&password=1234
    :return: simples String informando que o usuário foi criado ou que o login já existe
    '''
    pessoaLogin = str(request.args.get('login'))
    pessoaEmail = str(request.args.get('email'))
    pessoaPassword = str(request.args.get('password'))
    if pessoaLogin == 'None' or pessoaPassword == 'None':
        return "É necessário informar login e password. Ex: http://localhost:5000/criar?login=juca&email=a@a.com&password=1234"

    # Veja como fazer consultas no manual: http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
    if Usuario.query.filter_by(username=pessoaLogin).first() != None:
        return "O login {} já existe. Por favor, escolha outro.".format(pessoaLogin)

    novo_usuario = Usuario(username=pessoaLogin, email=pessoaEmail,password_hash=pessoaPassword)
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Usuário {} criado com sucesso'.format(pessoaLogin))
    return redirect(url_for('inicio'))


# Para criar um usuário manualmente no console do Python
# from exemplo02 import db, Usuario
# teste = Usuario(username='jucaa', email='jucaa@email.com')
# teste.set_password('senha1233')
# db.session.add(teste)
# db.session.commit()
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
