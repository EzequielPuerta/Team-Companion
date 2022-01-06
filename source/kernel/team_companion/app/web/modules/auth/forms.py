from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="Ingrese su usuario"), 
        Length(max=64, message="Debe tener a lo sumo 64 caracteres")])
    password = PasswordField("Contraseña", validators=[DataRequired(message="Ingrese su contraseña")])
    remember_me = BooleanField("No cerrar la sesión")
    submit = SubmitField("Ingresar")