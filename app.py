from flask import Flask, request, render_template, jsonify
import pandas as pd
from models import *
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Configure the database URI for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medease.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids tracking overhead

db.init_app(app)

with app.app_context():
    db.create_all()

# Load and preprocess the dataset
file_path = 'Specialist.xlsx'  # Ensure this file is in the same directory as app.py
data = pd.read_excel(file_path)

def preprocess_data(data):
    # Clean the dataset: remove unnamed columns and standardize column names
    if data.columns[0].startswith('Unnamed'):
        data = data.drop(columns=[data.columns[0]])
    data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]
    return data

data_cleaned = preprocess_data(data)

def recommend_specialist(input_symptoms, data):
    # Process symptoms to match dataset columns
    input_symptoms = [symptom.strip().lower().replace(' ', '_') for symptom in input_symptoms if symptom.strip()]

    # Check for invalid symptoms
    invalid_symptoms = [symptom for symptom in input_symptoms if symptom not in data.columns]
    if invalid_symptoms:
        return {'error': f"Invalid symptoms: {', '.join(invalid_symptoms)}"}

    matching_specialists = []  # List to store matched specialists
    for idx, row in data.iterrows():
        # Check if all symptoms match for a doctor recommendation
        if all(row.get(symptom, 0) == 1 for symptom in input_symptoms):
            matching_specialists.append(row['disease'])  # Ensure 'disease' is the correct column name

    # Return error if no specialists found
    if not matching_specialists:
        return {'error': "No specialists found for the given symptoms."}
    
    return {'recommendations': list(set(matching_specialists))}  # Return unique specialists

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = None
    error = None  # Variable to hold error messages
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        input_symptoms = [symptom.strip() for symptom in symptoms.split(",")]
        try:
            recommendations = recommend_specialist(input_symptoms, data_cleaned)
            if 'error' in recommendations:
                error = recommendations['error']
                recommendations = None  # Reset recommendations on error
        except ValueError as e:
            error = str(e)
    
    return render_template('index.html', recommendations=recommendations, error=error)

@app.route('/book', methods=['GET'])
def book():
    return render_template('book.html')

@app.route('/recommend_doctors', methods=['POST'])
def recommend_doctors():
    symptoms = request.form.get('symptoms')
    input_symptoms = [symptom.strip() for symptom in symptoms.split(",")]
    recommendations = recommend_specialist(input_symptoms, data_cleaned)

    if 'error' in recommendations:
        return render_template('book.html', error=recommendations['error'])

    return render_template('book.html', recommendations=recommendations['recommendations'])

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query').lower()
    suggestions = [col.replace('_', ' ') for col in data_cleaned.columns if query in col]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
