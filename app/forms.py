from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostGeneratorForm(FlaskForm):
    tone = StringField('Tone', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    generate_image = BooleanField('Generate Image')
    autopost = BooleanField('Auto Post to VK')
    submit = SubmitField('Generate Post')
    
class SettingsForm(FlaskForm):
    vk_api_key = StringField('VK API Key', validators=[DataRequired()])
    vk_group_id = IntegerField('VK Group ID', validators=[DataRequired()])

    def validate_vk_group_id(form, field):
        if field.data >= 0:
            raise ValidationError('VK Group ID must be a negative integer.')
    submit = SubmitField('Save Settings')