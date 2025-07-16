from flask import Flask, render_template, request
from src.predictor import load_model, make_prediction
import sqlite3

app = Flask(__name__)

# Load trained model
model = load_model()

# Initialize database
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            hours_studied REAL,
            attendance REAL,
            past_score REAL,
            prediction TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    age = int(request.form['age'])
    hours_studied = float(request.form['hours_studied'])
    attendance = float(request.form['attendance'])
    past_score = float(request.form['past_score'])
    
    # Predict
    prediction = make_prediction(model, [[age, hours_studied, attendance, past_score]])
    result = 'Pass' if prediction == 1 else 'Fail'
    
    # Save to DB
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('INSERT INTO predictions (age, hours_studied, attendance, past_score, prediction) VALUES (?, ?, ?, ?, ?)',
              (age, hours_studied, attendance, past_score, result))
    conn.commit()
    conn.close()
    
    return render_template('result.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
