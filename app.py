import pandas as pd
import joblib
import os
from flask import Flask, render_template, request
from preprocessing_utils import preprocess_input, get_unique_values

app = Flask(__name__)

MODEL_PATH = 'model.pkl'
DATA_PATH = 'featured_data.csv'

model = None
dropdown_options = {}

def load_resources():
    global model, dropdown_options
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        else:
            print(f"Error: Model file not found at {MODEL_PATH}")

        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)
            categorical_cols = [
                'make', 'model', 'fuel', 'transmission', 'trim', 
                'body', 'exterior_color', 'interior_color', 'drivetrain'
            ]
            for col in categorical_cols:
                dropdown_options[col] = get_unique_values(df, col)
            print("Data loaded and dropdown options extracted.")
        else:
            print(f"Error: Data file not found at {DATA_PATH}")
            
    except Exception as e:
        print(f"Error loading resources: {e}")

load_resources()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', options=dropdown_options)

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return render_template('index.html', options=dropdown_options, error="Model not loaded.")

    try:
        input_data = {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'year': request.form.get('year'),
            'cylinders': request.form.get('cylinders'),
            'fuel': request.form.get('fuel'),
            'mileage': request.form.get('mileage'),
            'transmission': request.form.get('transmission'),
            'trim': request.form.get('trim'),
            'body': request.form.get('body'),
            'doors': request.form.get('doors'),
            'exterior_color': request.form.get('exterior_color'),
            'interior_color': request.form.get('interior_color'),
            'drivetrain': request.form.get('drivetrain')
        }

        processed_df = preprocess_input(input_data)
        
        prediction = model.predict(processed_df)[0]
        
        formatted_price = f"${prediction:,.2f}"
        
        return render_template('result.html', prediction=formatted_price, inputs=input_data)

    except Exception as e:
        print(f"Prediction error: {e}")
        return render_template('index.html', options=dropdown_options, error=f"An error occurred during prediction: {e}")

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(debug=True)
