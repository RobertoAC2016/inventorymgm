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
btnSubmitLbl = 'Enviar'

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
                                render_kw={'placeholder': 'Category name'})
    submit = SubmitField(label=btnSubmitLbl)


class SupplierForm(FlaskForm):
    supplier_name = StringField(validators=[DataRequired()],
                                render_kw={'placeholder': 'Supplier\'s name'})
    contact_person = StringField(render_kw={'placeholder': 'Contact person'})
    address = StringField(render_kw={'placeholder': 'Address'})
    phone = IntegerField(validators=[DataRequired(
                         message='Please input correct digits for phone')],
                         render_kw={'placeholder': 'Phone'})
    email = EmailField(render_kw={'placeholder': 'Email'})
    submit = SubmitField(label=btnSubmitLbl)


class ProductForm(FlaskForm):
    name = StringField(validators=[DataRequired()],
                       render_kw={'placeholder': 'Product name'})
    category_id = SelectField(label='Choose category',
                              coerce=ObjectId,
                              validators=[DataRequired()])
    brand = StringField(render_kw={'placeholder': 'Brand name'})
    supplier_id = SelectField(label='Choose supplier',
                              coerce=ObjectId,
                              validators=[DataRequired()])
    unit_of_measurement = StringField(
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Unit of measurement'})
    min_stock_allowed = IntegerField(
                        validators=[DataRequired(),
                                    NumberRange(min=0, max=100,
                                    message='Min stock should be between 0 to 100')],
                        render_kw={'placeholder': 'Minimum stock allowed'})
    current_stock = IntegerField(default=0,
                                 render_kw={'placeholder': 'Current stock'})
    stock_change = IntegerField(render_kw={'placeholder': 'Stock change'})
    submit = SubmitField(label=btnSubmitLbl)


class PendingStockForm(FlaskForm):
    supplier_id = SelectField(label='Choose supplier',
                              validators=[DataRequired()])
    delivery_date = DateField(label='Expected delivery date',
                              validators=[DataRequired()],
                              render_kw={'min': datetime.date.today()})
    submit = SubmitField(label=btnSubmitLbl)


class AddProduct(FlaskForm):
    id = HiddenField()
    name = StringField(validators=[DataRequired()],
                       render_kw={'placeholder': 'Search product',
                                  'class': 'form-control search',
                                  'autocomplete': 'off'})
    expected_stock = IntegerField(validators=[DataRequired(),
                                  NumberRange(min=1, max=100,
                                  message='Please input valid number')],
                                  render_kw={'placeholder': 'Expected stock'})
    received_stock = IntegerField(validators=[DataRequired(),
                                  NumberRange(min=0, max=100,
                                  message='Please input valid number')])
    unit_of_measurement = StringField()
