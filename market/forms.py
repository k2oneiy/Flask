from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from market.models import User


class Registerform(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already Exits")
    def validate_email(self,email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError("Email already Exits")        
    username = StringField(label='User Name',validators=[DataRequired(),Length(min=2,max=6)])
    email = StringField(label='Email',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password',validators=[DataRequired(),Length(min=6)])
    password2 = PasswordField(label='Confirm Password',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Your Account')


class LoginForm(FlaskForm):
    username = StringField(label='username',validators=[DataRequired()])
    password = StringField(label='password',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')
    


