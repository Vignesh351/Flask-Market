from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField ,SubmitField
from wtforms.validators import Length , EqualTo , Email ,DataRequired , ValidationError
from market.model import user

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        User = user.query.filter_by(username=username_to_check.data).first()
        if User:
            raise ValidationError('Username already exists')
        
    def validate_email_address(self, email_address_to_check):
        email_address = user.query.filter_by(username=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('This email is already registered to an account')

    username = StringField(label='User Name', validators=[Length(min=2 , max=30) , DataRequired()])
    email_address = StringField(label='E-Mail',validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Re-enter Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label="User Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm): 
    submit = SubmitField(label='Purchase Item')


class SellItemForm(FlaskForm): 
    submit = SubmitField(label='Sell Item')