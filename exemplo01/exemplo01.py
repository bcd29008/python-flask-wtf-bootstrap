from flask import Flask, render_template, flash, redirect, url_for

from formularios import LoginForm

SECRET_KEY = 'aula de BCD - string aleatória'


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Autenticação requisitada pelo usuário: {}, com a senha: {}, lembrar-usuário={}'.format(
            form.username.data, form.password.data, form.remember_me.data))
        return redirect(url_for('inicio'))
    return render_template('login.html', title='Autenticação de usuários', form=form)


@app.route('/')
def inicio():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
