from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, BooleanField, TextAreaField , IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_uploads import UploadSet, IMAGES

class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired(),Length(min=3, max=15)])

    email = StringField('Email',validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):
    
    email = StringField('Email' )

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')


photos = UploadSet('photos', IMAGES)



class RegisterProductForm(FlaskForm):

    productname = StringField('Product Name',validators=[DataRequired(),Length(min=3,max=50)])
    
    description = TextAreaField('Description',validators=[DataRequired()])

    videoId = StringField('Video ID')

    maxEntries = IntegerField('Maximum Entries')

    photo = FileField(validators=[FileAllowed(photos, 'Image only!')])

    submit = SubmitField('Add Product')



