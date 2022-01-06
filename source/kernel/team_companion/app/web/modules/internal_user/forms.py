from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class CRUDModifyInternalUserForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="Ingrese un usuario."),
        Length(max=64, message="Debe tener a lo sumo 64 caracteres.")])

    is_admin = BooleanField("¿Es administrador?")
    submit = SubmitField("Aceptar")

class CRUDAddInternalUserForm(CRUDModifyInternalUserForm):
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="Ingrese una contraseña."),
        EqualTo('confirm', message="Las contraseñas deben coincidir.")])

    confirm = PasswordField("Repita la contraseña.")
    is_admin = BooleanField("¿Es administrador?", render_kw={"checked": True})