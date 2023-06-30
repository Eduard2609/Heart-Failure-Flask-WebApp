from flask import render_template, flash, redirect, url_for, send_file
from flaskheart import app, db, bcrypt
from flaskheart.forms import  SendToHeartApiForm, RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

from tools.convert_data import convert_data
from tools.connect_api import connect_to_api
from tools.format import format_api_result
from tools.date_csv import save_data_to_csv
from flaskheart.models import User
import csv
import os


#from flaskheart.models import User

from tools.convert_data import convert_data
from tools.connect_api import connect_to_api
from tools.format import format_api_result
import csv
import os

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
        

        if current_user.is_authenticated:

            # Save the user data to the user's CSV file that is called 'name' + 'surname' + '.csv'
            
            csv_file = current_user.csv_file
            # save_data_to_csv(user_data, csv_file)
            # print(user_data)

            # i want to save the data to the all.csv file
            all_csv_file = 'all.csv'
            #save_data_to_csv(user_data, all_csv_file)

            # save user data as a list and print it
            user_data_list = [user_data]
            # print(user_data_list)

            
            # Convert the user data to a format that the Heart API can understand
            user_data = convert_data(user_data)
            # Connect to the Heart API and get the prediction
            selected_model = form.model.data
            prediction = connect_to_api(selected_model, user_data)
            
            # Format the prediction
            prediction = format_api_result(prediction)
        
            #append the prediction to the user_data_list
            probability = float(prediction[prediction.index(':')+2:-1])
            user_data_list.append(probability)
            print(user_data_list)
            user_data_dict = user_data_list[0]
            risk_dict = {'risk': user_data_list[1]}
            user_data_dict.update(risk_dict)
            print(user_data_dict)
            save_data_to_csv(user_data_dict, csv_file)
            save_data_to_csv(user_data_dict, all_csv_file)
            
          
            # user_data_list['risk'] = risk_only
            # print(user_data_list)


            #flash the prediction
            if prediction is not None:
                flash (f'{prediction}''%', 'success')
            else:
                flash (f'API request failed!', 'danger')
        else:
            flash (f'Please login first!', 'danger')
            return redirect(url_for('login'))
    return render_template('home.html', form=form)


def has_valid_history(current_user):
    csv_file_path = os.path.join(app.instance_path, current_user.csv_file)
    return os.path.isfile(csv_file_path)

@app.route('/history')
def history():
    if not current_user.is_authenticated:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    elif current_user.csv_file is None or not has_valid_history(current_user):
        flash('No history available!', 'danger')
        return redirect(url_for('home'))
    else:
        # Get the path to the user's CSV file
        csv_path = os.path.join(app.instance_path, current_user.csv_file)
        
        # Read the user's CSV file
        with open(csv_path, 'r', newline='') as csvfile:
            # Create a CSV reader object
            reader = csv.DictReader(csvfile)
            
            # Convert the CSV data to a list of dictionaries
            data = [row for row in reader]
    return render_template('history.html', data=data)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(email=form.email.data, name=form.name.data, surname=form.surname.data, password=hashed_password, csv_file=form.name.data + form.surname.data + '.csv')
        db.session.add(user)
        db.session.commit()
        flash(f'Hey {form.name.data}! We succesfuly created an account created on {form.email.data}! You can log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Hey {form.email.data}! You are logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccesful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/download_csv')
def download_csv():
    if not current_user.is_authenticated:
        flash('Please login first!', 'danger')
        return redirect(url_for('login'))
    elif current_user.csv_file is None or not has_valid_history(current_user):
        flash('No history available!', 'danger')
        return redirect(url_for('home'))
    else:
        # Get the path to the user's CSV file
        csv_path = os.path.join(app.instance_path, current_user.csv_file)

        # Return the CSV file as a download
        return send_file(csv_path, as_attachment=True)