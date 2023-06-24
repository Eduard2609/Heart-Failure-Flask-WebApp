import os
import csv
from flask import Flask, render_template, flash, redirect, url_for
from forms import  SendToHeartApiForm, RegistrationForm, LoginForm
from tools.convert_data import convert_data
from tools.connect_api import connect_to_api
from tools.format import format_api_result

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cheie_secreta'

# Define the path to the data directory
data_dir = os.path.join(app.instance_path, 'data')

# Create the data directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SendToHeartApiForm()
    if form.validate_on_submit():
        # Process the form data and store it in a variable
        user_data = {
            'age': form.age.data,
            'sex': form.sex.data,
            'resting_bp': form.resting_bp.data,
            'cholesterol': form.cholesterol.data,
            'fasting_bs': form.fasting_bs.data,
            'max_hr': form.max_hr.data,
            'exercise_angina': form.exercise_angina.data,
            'oldpeak': form.oldpeak.data,
            'chest_pain_type': form.chest_pain_type.data,
            'resting_ecg': form.resting_ecg.data,
            'st_slope': form.st_slope.data,
            'model': form.model.data
        }
        # Save the user data to a CSV file
        save_data_to_csv(user_data)
        # Convert the user data to a format that the Heart API can understand
        user_data = convert_data(user_data)
        # Connect to the Heart API and get the prediction
        selected_model = form.model.data
        prediction = connect_to_api(selected_model, user_data)
        # Format the prediction
        prediction = format_api_result(prediction)
        #flash the prediction
        if prediction is not None:
            flash (f'{prediction}''%', 'success')
        else:
            flash (f'API request failed!', 'danger')
    return render_template('home.html', form=form)

def save_data_to_csv(user_data):
    # Define the name and path of the CSV file
    filename = 'user_data.csv'
    filepath = os.path.join(app.instance_path, 'data', filename)
    
    # Create the CSV file if it doesn't exist
    if not os.path.exists(filepath):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(user_data.keys())
    
    # Open the CSV file in append mode and write the user data to it
    with open(filepath, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(user_data.values())

@app.route('/history')
def history():
    return render_template('history.html', title='History')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Hey {form.name.data}! We succesfuly created an account created on {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccesful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)



if __name__ == '__main__':
    app.run(debug=True)