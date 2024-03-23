from models import Business
from flask_wtf import FlaskForm
from flask_user import UserManager
from flask_user.forms import (RegisterForm, password_validator,
                              unique_email_validator)
from wtforms import (StringField, PasswordField, SubmitField,
                     SelectField, HiddenField, IntegerField)
from wtforms.validators import (DataRequired, Length, Email,
                                ValidationError, NumberRange)
from wtforms.fields.html5 import EmailField, DateField
from bson.objectid import ObjectId
import datetime

namevalue = 'Nombre'
namemsg = 'El nombre deberia tener entre 5 y 20 caracteres.'
btnSubmitLbl = 'Guardar'
provLbl = 'Elegir proveedor'
inValidLbl = 'Por favor ingrese un numero valido'

def unique_business_validator(form, field):
    '''
    Form validation that the business name is unique.
    '''
    existing_business = Business.objects(business_name=field.data).first()

    if existing_business:
        raise ValidationError('El nombre de usuario ya existe.')


class CustomRegisterForm(RegisterForm):
    name = StringField(label=namevalue,
                       validators=[DataRequired(),
                                   Length(min=5, max=20,
                                   message=namemsg
                                          )])
    business_name = StringField(label='Nombre de usuario',
                                validators=[DataRequired(),
                                            unique_business_validator])


class CustomUserManager(UserManager):
    def customize(self, app):
        # Configure customized forms
        self.RegisterFormClass = CustomRegisterForm


class UserAccess(FlaskForm):
    name = StringField(validators=[Length(min=5, max=20,
                       message=namemsg),
                                   DataRequired()],
                       render_kw={'placeholder': namevalue})
    email = EmailField(validators=[Email(), DataRequired(),
                                   unique_email_validator],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField(validators=[DataRequired(),
                                         password_validator],
                             render_kw={'placeholder': 'Contraseña'})
    roles = SelectField(choices=[('', 'Elige un rol'),
                                 ('admin', 'admin'),
                                 ('staff', 'staff')],
                        validators=[DataRequired()])


class CategoryForm(FlaskForm):
    category_name = StringField(validators=[DataRequired()],
                                render_kw={'placeholder': 'Nombre de categoría'})
    submit = SubmitField(label=btnSubmitLbl)


class SupplierForm(FlaskForm):
    supplier_name = StringField(validators=[DataRequired()],
                                render_kw={'placeholder': 'Nombre del proveedor'})
    contact_person = StringField(render_kw={'placeholder': 'Persona de contacto'})
    address = StringField(render_kw={'placeholder': 'Dirección'})
    phone = IntegerField(validators=[DataRequired(
                         message='Por favor ingrese solo numeros para el teléfono')],
                         render_kw={'placeholder': 'Teléfono'})
    email = EmailField(render_kw={'placeholder': 'Email'})
    submit = SubmitField(label=btnSubmitLbl)


class ProductForm(FlaskForm):
    name = StringField(validators=[DataRequired()],
                       render_kw={'placeholder': 'Nombre de producto'})
    category_id = SelectField(label='Elegir categoría',
                              coerce=ObjectId,
                              validators=[DataRequired()])
    brand = StringField(render_kw={'placeholder': 'Nombre de la marca'})
    supplier_id = SelectField(label=provLbl,
                              coerce=ObjectId,
                              validators=[DataRequired()])
    unit_of_measurement = StringField(
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Unidad de medida'})
    min_stock_allowed = IntegerField(
                        validators=[DataRequired(),
                                    NumberRange(min=0, max=1000,
                                    message='Las existencias minimas deben ser entre 0 y 1000')],
                        render_kw={'placeholder': 'Existencias minimas permitidas'})
    current_stock = IntegerField(default=0,
                                 render_kw={'placeholder': 'Existencias actuales'})
    stock_change = IntegerField(render_kw={'placeholder': 'Modificar existencias'})
    submit = SubmitField(label=btnSubmitLbl)


class PendingStockForm(FlaskForm):
    supplier_id = SelectField(label=provLbl,
                              validators=[DataRequired()])
    delivery_date = DateField(label='Fecha esperada de entrega',
                              validators=[DataRequired()],
                              render_kw={'min': datetime.date.today()})
    submit = SubmitField(label=btnSubmitLbl)

class AddProduct(FlaskForm):
    id = HiddenField()
    name = StringField(validators=[DataRequired()],
                       render_kw={'placeholder': 'Buscar producto',
                                  'class': 'form-control search',
                                  'autocomplete': 'off'})
    expected_stock = IntegerField(validators=[DataRequired(),
                                  NumberRange(min=1, max=100,
                                  message=inValidLbl)],
                                  render_kw={'placeholder': 'Existencias esperadas'})
    received_stock = IntegerField(validators=[DataRequired(),
                                  NumberRange(min=0, max=100,
                                  message=inValidLbl)])
    unit_of_measurement = StringField()
