from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    submit = SubmitField("Login")
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AssetForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=4, max=64)])
    description = StringField("Description", validators=[DataRequired(), Length(min=4, max=128)])
    location = StringField("Location", validators=[DataRequired(), Length(min=4, max=64)])
    category = StringField("Category", validators=[DataRequired(), Length(min=4, max=64)])
    status = StringField("Status", validators=[DataRequired(), Length(min=4, max=64)])
    submit = SubmitField("Create Asset")

class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")