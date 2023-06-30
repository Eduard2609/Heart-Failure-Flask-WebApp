import csv
import os
from flaskheart import app

def save_data_to_csv(user_data, csv_file):
    # Define the path of the CSV file
    csv_path = os.path.join(app.instance_path, csv_file)
    
    # Define the fieldnames for the CSV file
    fieldnames = ['age', 'sex', 'resting_bp', 'cholesterol', 'fasting_bs', 'max_hr', 'exercise_angina', 'oldpeak', 'chest_pain_type', 'resting_ecg', 'st_slope', 'model', 'risk']
    
    if 'risk' not in fieldnames:
        fieldnames.append('risk')
    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_path)
    
    # Create the CSV file if it does not exist
    if not file_exists:
        with open(csv_path, 'w', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header row to the CSV file
            writer.writeheader()
    
    # Open the CSV file in append mode
    with open(csv_path, 'a', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the user data to the CSV file
        writer.writerow(user_data)