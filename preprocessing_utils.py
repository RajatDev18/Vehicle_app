import pandas as pd
import numpy as np

def calculate_vehicle_age(year, current_year=2025):
    """Calculates vehicle age based on the reference year."""
    return current_year - year

def calculate_annual_mileage(mileage, vehicle_age):
    """Calculates annual mileage, handling division by zero."""
    if vehicle_age > 0:
        return mileage / vehicle_age
    return mileage

def get_mileage_bucket(x):
    """Categorizes mileage into buckets."""
    if 0 <= x <= 100:
        return 'brand new'
    elif 100 < x <= 500:
        return 'test driven'
    elif 500 < x <= 2000:
        return 'slightly used'
    elif 2000 < x <= 5000:
        return 'early used'
    else:
        return 'light used demo'

def simplify_transmission(x):
    """Simplifies transmission categories."""
    x = str(x).lower()
    if 'cvt' in x:
        return 'cvt'
    elif 'dual' in x or 'dct' in x:
        return 'dual clutch'
    elif 'manual' in x or 'm/t' in x:
        return 'manual'
    elif '1-speed' in x or 'battery' in x or 'electric' in x:
        return 'single-speed (EV)'
    elif 'automatic' in x or 'a/t' in x:
        return 'automatic'
    else:
        return 'other'

def simplify_fuel(x):
    """Merges fuel categories."""
    if x == 'PHEV Hybrid Fuel':
        return 'Hybrid'
    elif x == 'Diesel (B20 capable)':
        return 'Diesel'
    else:
        return x

def get_unique_values(df, column):
    """Returns sorted unique values for a column, dropping NaNs."""
    if column in df.columns:
        return sorted(df[column].dropna().unique().tolist())
    return []

def preprocess_input(data):
    """
    Preprocesses a dictionary of input data into a DataFrame compatible with the model.
    
    Args:
        data (dict): Dictionary containing raw input values.
        
    Returns:
        pd.DataFrame: A single-row DataFrame with engineered features.
    """
    df = pd.DataFrame([data])
    
    numeric_cols = ['year', 'cylinders', 'mileage', 'doors']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['vehicle_age'] = calculate_vehicle_age(df['year'])
    df['annual_mileage'] = df.apply(lambda row: calculate_annual_mileage(row['mileage'], row['vehicle_age']), axis=1)
    df['mileage_bucket'] = df['mileage'].apply(get_mileage_bucket)
    df['turbo'] = 0
    
    expected_cols = [
        'make', 'model', 'year', 'cylinders', 'fuel', 'mileage', 
        'transmission', 'trim', 'body', 'doors', 'exterior_color', 
        'interior_color', 'drivetrain', 'mileage_bucket', 'turbo', 
        'vehicle_age', 'annual_mileage'
    ]
    
    for col in expected_cols:
        if col not in df.columns:
            df[col] = 0
    return df[expected_cols]
