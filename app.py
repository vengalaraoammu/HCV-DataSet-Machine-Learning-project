import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__)
model = pickle.load(open('HCV.pkl', 'rb'))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data
    age = float(request.form['age'])
    gender = request.form['gender']
    bmi = float(request.form['bmi'])
    fever = 'fever' in request.form
    nausea = 'nausea' in request.form
    headache = 'headache' in request.form
    diarrhea = 'diarrhea' in request.form
    fatigue = 'fatigue' in request.form
    jaundice = 'jaundice' in request.form
    epigastric = 'epigastric' in request.form
    wbc = float(request.form['wbc'])
    rbc = float(request.form['rbc'])
    hgb = float(request.form['hgb'])
    plat = float(request.form['plat'])
    ast1 = float(request.form['ast1'])
    alt1 = float(request.form['alt1'])
    alt4 = float(request.form['alt4'])
    alt12 = float(request.form['alt12'])
    alt24 = float(request.form['alt24'])
    alt36 = float(request.form['alt36'])
    alt48 = float(request.form['alt48'])
    alt24w = float(request.form['alt24w'])
    rna_base = float(request.form['rnaBase'])
    rna_4 = float(request.form['rna4'])
    rna_12 = float(request.form['rna12'])
    rna_eot = float(request.form['rnaEOT'])
    rna_ef = float(request.form['rnaEF'])
    grading = float(request.form['grading'])

    # Perform label encoding for gender
    gender_encoded = 0  # Default value for unknown gender
    if gender.lower() == 'male':
        gender_encoded = 1
    elif gender.lower() == 'female':
        gender_encoded = 2

    # Prepare the input data for prediction
    data = [[age, bmi, wbc, rbc, hgb, plat, ast1, alt1, alt4, alt12, alt24, alt36, alt48,
             alt24w, rna_base, rna_4, rna_12, rna_eot, rna_ef, grading, fever, nausea,
             headache, diarrhea, fatigue, jaundice, epigastric, gender_encoded]]

    # Make the prediction
    prediction = model.predict(data)

    predicted_value = prediction

    if predicted_value == 1:
        result = "Stage 1: Portal Fibrosis"
    elif predicted_value == 2:
        result = "Stage 2: Few Septa"
    elif predicted_value == 3:
        result = "Stage 3: Many Septa"
    elif predicted_value == 4:
        result = "Stage 4: Cirrhosis"
    else:
        result = "Unknown stage"

    # Render the result template with the prediction
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run()