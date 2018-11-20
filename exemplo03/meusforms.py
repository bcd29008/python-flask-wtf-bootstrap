from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FormField, SelectField, FieldList, DateField, \
    DateTimeField
from wtforms.validators import DataRequired

'''
Veja mais na documentação do WTForms

https://wtforms.readthedocs.io/en/stable/
https://wtforms.readthedocs.io/en/stable/fields.html

Um outro pacote interessante para estudar:

https://wtforms-alchemy.readthedocs.io/en/latest/

'''


class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    password = PasswordField('Senha', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    submit = SubmitField('Entrar')



class EnderecoForm(FlaskForm):
    rua = StringField('Endereço', validators=[DataRequired])
    cidade = StringField('Cidade', validators=[DataRequired])
    uf = SelectField(u'Estado',choices=[('sc', 'Santa Catarina'), ('pr', 'Paraná')], validators=[DataRequired])
    cep = StringField('CEP')

class TelefoneForm(FlaskForm):
    codigoPais = IntegerField('Código do país', validators=[DataRequired])
    codigoDDD = IntegerField('DDD', validators=[DataRequired])
    numero = StringField('Número')

class FormDeRegistro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired])
    sobrenome = StringField('Sobrenome', validators=[DataRequired])
    endereco = FormField(EnderecoForm,'Endereço residencial')
    dataNasc = DateField('Data de nascimento', id='datepick',validators=[DataRequired])
    telefoneCelular = FormField(TelefoneForm,'Telefone celular')
    submit = SubmitField('Cadastrar')
