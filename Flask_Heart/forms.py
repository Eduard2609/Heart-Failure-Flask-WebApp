from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    email   =           StringField('Email', 
                                        validators=[DataRequired(), Email()])
    name    =           StringField('Name', 
                                        validators=[DataRequired(), Length(min=2, max=20)])
    surname =           StringField('Surname', 
                                        validators=[DataRequired(), Length(min=2, max=20)])
    password=           PasswordField('Password',
                                        validators=[DataRequired()])
    confirm_password=   PasswordField('Confirm Password',
                                        validators=[DataRequired(), EqualTo('password')])
    submit  =           SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email   =           StringField('Email', 
                                        validators=[DataRequired(), Email()])
    password=           PasswordField('Password',
                                        validators=[DataRequired()])
    remember=           BooleanField('Remember Me')
    submit  =           SubmitField('Login')

# do not allow empty choice and sumbit if selected the "--Please choose an option--" choice
class NotEmpty(object):
    def __init__(self, message=None):
        if not message:
            message = u'This field is required.'
        self.message = message

    def __call__(self, form, field):
        if field.data == '--Please choose an option--':
            raise ValidationError(self.message)


class SendToHeartApiForm(FlaskForm):
    model = SelectField('Model', choices=[('--Please choose an option--', ''), ('logistic_regression', 'Logistic Regression'), 
    ('random_forest', 'Random Forest'), 
    ('svm', 'Support Vector Machine'), 
    ('dtc', 'Decision Tree Classifier')],
    validators=[DataRequired(), NotEmpty()]) 

    age = StringField('Age', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('--Please choose an option--', ''), ('male', 'Male'), ('female', 'Female')], validators=[DataRequired(), NotEmpty()])
    resting_bp = StringField('Resting Blood Pressure', validators=[DataRequired()])
    cholesterol = StringField('Cholesterol', validators=[DataRequired()])
    fasting_bs = SelectField('Fasting Blood Sugar', choices=[('--Please choose an option--', ''), ('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    max_hr = StringField('Maximum Heart Rate', validators=[DataRequired()])
    exercise_angina = SelectField('Exercise-Induced Angina', choices=[('--Please choose an option--', ''), ('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    oldpeak = StringField('Oldpeak', validators=[DataRequired()])
    chest_pain_type = SelectField('Chest Pain Type', choices=[('--Please choose an option--', ''), ('ASY', 'Asymptomatic'), ('ATA', 'Atypical Angina'), ('NAP', 'Non-Anginal Pain'), ('TA', 'Typical Angina')], validators=[DataRequired()])
    resting_ecg = SelectField('Resting ECG', choices=[('--Please choose an option--', ''), ('LVH', 'LVH'), ('normal', 'Normal'), ('ST', 'ST')], validators=[DataRequired()])
    st_slope = SelectField('ST Slope', choices=[('--Please choose an option--', ''), ('down', 'Downsloping'), ('flat', 'Flat'), ('up', 'Upsloping')], validators=[DataRequired()])
    submit = SubmitField('Submit')