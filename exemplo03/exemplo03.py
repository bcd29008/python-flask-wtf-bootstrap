'''

Pequeno exemplo de uso do Flask-Bootstrap

https://pythonhosted.org/Flask-Bootstrap/

https://pythonhosted.org/flask-nav/


Exemplos com Bootstrap - https://getbootstrap.com/docs/3.3/getting-started/#examples

Veja mais detalhes nesse tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-facelift

'''

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link

from meusforms import LoginForm, FormDeRegistro

from dadostabela import *



SECRET_KEY = 'aula de BCD - string aleatória'


app = Flask(__name__)
app.secret_key = SECRET_KEY

boostrap = Bootstrap(app) # isso habilita o template bootstrap/base.html
nav = Nav()
nav.init_app(app) # isso habilita a criação de menus de navegação do pacote Flask-Nav

@nav.navigation()
def meunavbar():
    menu = Navbar('Minha aplicação')
    menu.items = [View('Home', 'inicio'), View('Registro', 'cadastro')]
    menu.items.append(Subgroup('Menu de opções',View('Aluno','aluno'),View('Professor','professor')))
    menu.items.append(View('Login', 'autenticar'))
    menu.items.append(Link('Ajuda','https://www.google.com'))
    return menu


@app.route('/registro', methods=['GET', 'POST'])
def cadastro():
    form = FormDeRegistro()
    if form.validate_on_submit():
        return render_template('index.html', title="Usuário registrado")
    return render_template('registro.html', title='Cadastro de usuário', form=form)


@app.route('/login', methods=['GET', 'POST'])
def autenticar():
    form = LoginForm()
    if form.validate_on_submit():
        return render_template('autenticado.html', title="Usuário autenticado")
    return render_template('login.html', title='Autenticação de usuários', form=form)



@app.route('/')
def inicio():
    return render_template('index.html')




@app.route('/professor')
def professor():
    return render_template('index.html')




@app.route('/aluno')
def aluno():
    '''
    Ilustra um exemplo de como exibir tabelas. Também mostrado um exemplo do flask-bootstrap-table
    As estuturas de dados 'data'e 'columns' estão no script dadostabela.py
    :return:
    '''
    return render_template('alunos.html',data=data,columns=columns)



@app.errorhandler(404)
def page_not_found(e):
    '''
    Para tratar erros de páginas não encontradas - HTTP 404
    :param e:
    :return:
    '''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
