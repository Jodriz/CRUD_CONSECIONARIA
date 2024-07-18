from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, DateTimeField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class VehiculoForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class ClienteForm(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired()])
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    vehiculos = SelectField('Vehículo', choices=[])
    submit = SubmitField('Guardar')

class RevisionForm(FlaskForm):
    cambio_filtro = BooleanField('Cambio de Filtro')
    cambio_aceite = BooleanField('Cambio de Aceite')
    cambio_frenos = BooleanField('Cambio de Frenos')
    costo_filtro = FloatField('Costo Filtro')
    costo_aceite = FloatField('Costo Aceite')
    costo_frenos = FloatField('Costo Frenos')
    fecha_recepcion = DateTimeField('Fecha Recepción', format='%Y-%m-%d %H:%M:%S')
    fecha_entrega = DateTimeField('Fecha Entrega', format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField('Guardar')
