Vehicle Price Prediction App
============================

Description
-----------
This is a Flask web application that predicts the market value of a vehicle based on its specifications. It uses a pre-trained Machine Learning model (XGBoost/Lasso pipeline) to provide instant price estimates. The app features a modern, responsive user interface and handles all necessary data preprocessing automatically.

Prerequisites
-------------
- Python 3.8 or higher
- pip (Python package installer)

Installation
------------
1. Navigate to the project directory:
   cd "velhicle app"

2. Install the required dependencies:
   pip install flask pandas joblib scikit-learn xgboost

Running the Application
-----------------------
1. Start the Flask server:
   python app.py

2. Open your web browser and go to:
   http://127.0.0.1:5000/

Usage
-----
- Select the vehicle Make, Model, and other details from the dropdowns.
- Enter the Year, Mileage, and other numerical values.
- Click "Predict Price" to see the estimated value.

Files
-----
- app.py: The main Flask application file.
- preprocessing_utils.py: Helper functions for data processing.
- model.pkl: The trained machine learning model.
- featured_data.csv: Dataset used to populate form options.
- templates/: HTML files for the web interface.
- static/: CSS and other static assets.
