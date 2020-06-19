from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField
# Validators
from wtforms.validators import DataRequired, Email, ValidationError,EqualTo,Length
# Import DB Object Classes so that we can access them here
from app.models import User



# ToDo:
# 1. Form input validation
# 2. Form input sanitation
# 
# 


class ItemForm(FlaskForm):
    name = name  = StringField('Item Name', validators=[DataRequired(), Length(min=1,max=140)])
    description = TextAreaField('Describe what you are selling.', validators=[DataRequired(), Length(min=1, max=512)])
    price = StringField('How much are you selling this item for?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SaleForm(FlaskForm):
    name  = StringField('Sale name', validators=[DataRequired(), Length(min=1,max=140)])
    description = TextAreaField('Describe your sale!', validators=[DataRequired(), Length(min=1, max=512)])


    use_saved_address = BooleanField('Use Saved Home Address?')
    save_address      = BooleanField('Save Address to Profile?')


    address_1   = StringField('Address Line 1', validators=[DataRequired()])
    address_2   = StringField('Address Line 2')
    country     = StringField('Country', validators=[DataRequired()])
    state       = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])


    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')




class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    address_1   = StringField('Address Line 1', validators=[DataRequired()])
    address_2   = StringField('Address Line 2')
    country     = StringField('Country', validators=[DataRequired()])
    state       = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])



    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')