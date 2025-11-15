import numpy as np
import pandas as pd
import pickle
import os
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Global variables to hold our models
heart_model = None
diabetes_model = None
pneumonia_model = None

# Scalers for preprocessing
heart_scaler = StandardScaler()
diabetes_scaler = StandardScaler()

def initialize_models():
    """Initialize ML models if they don't exist already"""
    global heart_model, diabetes_model, pneumonia_model
    
    try:
        # Heart Disease Model
        heart_model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Train it with sample data
        # This would typically be loaded from a saved model file
        # For now, we'll create a simple model
        X_heart = np.array([
            # age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
            [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1],  # Positive case
            [37, 1, 2, 130, 250, 0, 1, 187, 0, 3.5, 0, 0, 2],  # Positive case
            [41, 0, 1, 130, 204, 0, 0, 172, 0, 1.4, 2, 0, 2],  # Negative case
            [56, 1, 1, 120, 236, 0, 1, 178, 0, 0.8, 2, 0, 2],  # Negative case
        ])
        y_heart = np.array([1, 1, 0, 0])  # 1 = disease, 0 = no disease
        heart_scaler.fit(X_heart)
        X_heart_scaled = heart_scaler.transform(X_heart)
        heart_model.fit(X_heart_scaled, y_heart)
        
        # Diabetes Model
        diabetes_model = LogisticRegression(random_state=42)
        # Train with sample data
        X_diabetes = np.array([
            # Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
            [6, 148, 72, 35, 0, 33.6, 0.627, 50],  # Positive case
            [1, 85, 66, 29, 0, 26.6, 0.351, 31],   # Negative case
            [8, 183, 64, 0, 0, 23.3, 0.672, 32],   # Positive case
            [1, 89, 66, 23, 94, 28.1, 0.167, 21]   # Negative case
        ])
        y_diabetes = np.array([1, 0, 1, 0])  # 1 = diabetes, 0 = no diabetes
        diabetes_scaler.fit(X_diabetes)
        X_diabetes_scaled = diabetes_scaler.transform(X_diabetes)
        diabetes_model.fit(X_diabetes_scaled, y_diabetes)
        
        # Pneumonia Model
        # For this example, we'll use a simple classifier
        # Normally, for pneumonia detection, you'd use a CNN on chest X-rays
        pneumonia_model = RandomForestClassifier(n_estimators=50, random_state=42)
        
        logging.info("ML models initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing ML models: {str(e)}")
        raise

def predict_heart_disease(features):
    """
    Predict heart disease based on features.
    
    Args:
        features (dict): Dictionary with feature names and values
        
    Returns:
        dict: Prediction result with probability and information
    """
    try:
        # Extract features in the correct order
        feature_list = [
            features.get('age', 0),
            features.get('sex', 0),
            features.get('cp', 0),
            features.get('trestbps', 0),
            features.get('chol', 0),
            features.get('fbs', 0),
            features.get('restecg', 0),
            features.get('thalach', 0),
            features.get('exang', 0),
            features.get('oldpeak', 0),
            features.get('slope', 0),
            features.get('ca', 0),
            features.get('thal', 0)
        ]
        
        # Convert to numpy array and scale
        X = np.array([feature_list])
        X_scaled = heart_scaler.transform(X)
        
        # Get prediction probability
        prediction = heart_model.predict(X_scaled)[0]
        probability = heart_model.predict_proba(X_scaled)[0][1]
        
        result = {
            'prediction': bool(prediction),
            'probability': float(probability),
            'risk_level': 'High' if probability > 0.7 else ('Moderate' if probability > 0.4 else 'Low'),
            'info': {
                'name': 'Heart Disease',
                'description': 'Heart disease describes a range of conditions that affect your heart, including coronary artery disease, heart rhythm problems, and heart defects.',
                'symptoms': [
                    'Chest pain or discomfort', 
                    'Shortness of breath', 
                    'Pain in the neck, jaw, throat, upper abdomen or back',
                    'Numbness or weakness in legs or arms'
                ],
                'prevention': [
                    'Maintain healthy blood pressure and cholesterol levels',
                    'Exercise regularly',
                    'Eat a heart-healthy diet',
                    'Maintain a healthy weight',
                    'Quit smoking and limit alcohol'
                ]
            }
        }
        
        return result
    except Exception as e:
        logging.error(f"Error in heart disease prediction: {str(e)}")
        raise

def predict_diabetes(features):
    """
    Predict diabetes based on features.
    
    Args:
        features (dict): Dictionary with feature names and values
        
    Returns:
        dict: Prediction result with probability and information
    """
    try:
        # Extract features in the correct order
        feature_list = [
            features.get('pregnancies', 0),
            features.get('glucose', 0),
            features.get('blood_pressure', 0),
            features.get('skin_thickness', 0),
            features.get('insulin', 0),
            features.get('bmi', 0),
            features.get('diabetes_pedigree', 0),
            features.get('age', 0)
        ]
        
        # Convert to numpy array and scale
        X = np.array([feature_list])
        X_scaled = diabetes_scaler.transform(X)
        
        # Get prediction probability
        prediction = diabetes_model.predict(X_scaled)[0]
        probability = diabetes_model.predict_proba(X_scaled)[0][1]
        
        result = {
            'prediction': bool(prediction),
            'probability': float(probability),
            'risk_level': 'High' if probability > 0.7 else ('Moderate' if probability > 0.4 else 'Low'),
            'info': {
                'name': 'Diabetes',
                'description': 'Diabetes is a chronic disease that occurs when the pancreas is no longer able to make insulin, or when the body cannot make good use of the insulin it produces.',
                'symptoms': [
                    'Frequent urination', 
                    'Increased thirst', 
                    'Unexplained weight loss',
                    'Extreme hunger',
                    'Blurred vision'
                ],
                'prevention': [
                    'Maintain a healthy weight',
                    'Be physically active',
                    'Eat a healthy diet with plenty of fruits and vegetables',
                    'Limit alcohol and sugary beverages',
                    'Quit smoking'
                ]
            }
        }
        
        return result
    except Exception as e:
        logging.error(f"Error in diabetes prediction: {str(e)}")
        raise

def predict_pneumonia(features):
    """
    For the example, we'll return a simple result based on a few basic parameters.
    
    In a real implementation, this would analyze chest X-ray images using a CNN model.
    """
    try:
        # For this example, we'll use a very simplified approach
        # In reality, pneumonia detection typically uses image analysis of chest X-rays
        
        # Simple rule-based model for demonstration purposes
        # This is NOT how real pneumonia detection works
        temperature = features.get('temperature', 98.6)
        cough_severity = features.get('cough_severity', 0)
        breathing_difficulty = features.get('breathing_difficulty', 0)
        oxygen_level = features.get('oxygen_level', 98)
        
        # Calculate a simple risk score
        risk_score = 0
        if temperature > 100.4:
            risk_score += (temperature - 100.4) * 10
        
        risk_score += cough_severity * 10
        risk_score += breathing_difficulty * 15
        
        if oxygen_level < 95:
            risk_score += (95 - oxygen_level) * 20
            
        probability = min(risk_score / 100, 0.99)
        prediction = probability > 0.5
        
        result = {
            'prediction': bool(prediction),
            'probability': float(probability),
            'risk_level': 'High' if probability > 0.7 else ('Moderate' if probability > 0.4 else 'Low'),
            'info': {
                'name': 'Pneumonia',
                'description': 'Pneumonia is an infection that inflames the air sacs in one or both lungs. The air sacs may fill with fluid or pus, causing cough with phlegm, fever, chills, and difficulty breathing.',
                'symptoms': [
                    'Chest pain when breathing or coughing', 
                    'Confusion or changes in mental awareness (in adults age 65 and older)',
                    'Cough, which may produce phlegm',
                    'Fatigue',
                    'Fever, sweating and shaking chills',
                    'Lower than normal body temperature (in adults older than age 65 and people with weak immune systems)',
                    'Nausea, vomiting or diarrhea',
                    'Shortness of breath'
                ],
                'prevention': [
                    'Get vaccinated',
                    'Ensure children get vaccinated',
                    'Practice good hygiene',
                    'Don\'t smoke',
                    'Keep your immune system strong'
                ]
            }
        }
        
        return result
    except Exception as e:
        logging.error(f"Error in pneumonia prediction: {str(e)}")
        raise
