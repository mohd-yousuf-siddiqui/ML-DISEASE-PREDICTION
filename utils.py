import json
from datetime import datetime
from models import Prediction
from app import db

def save_prediction(prediction_type, result, input_data, user_id=None):
    try:
        # Convert dictionaries to JSON strings for SQLite
        result_str = json.dumps(result)
        input_str = json.dumps(input_data)
        
        # Create a new Prediction object for SQLite
        prediction = Prediction(
            user_id=user_id,
            prediction_type=prediction_type,
            result=result_str,
            confidence=result.get('probability', 0),
            input_data=input_str,
            created_at=datetime.utcnow()
        )
        
        # Save to SQLite database
        db.session.add(prediction)
        db.session.commit()
        
        # Also save to MongoDB - need to import mongo from app
        from app import mongo
        mongo.db.predictions.insert_one({
            'user_id': user_id,
            'prediction_type': prediction_type,
            'result': result,  # Can use dict directly in MongoDB
            'confidence': result.get('probability', 0),
            'parameters': input_data,  # Can use dict directly
            'created_at': datetime.utcnow()
        })
        
        return prediction.id
    except Exception as e:
        db.session.rollback()
        raise e

def validate_heart_disease_form(form_data):
    """
    Validate heart disease form data
    
    Args:
        form_data (dict): Form data from request
        
    Returns:
        tuple: (is_valid, errors, cleaned_data)
    """
    errors = {}
    cleaned_data = {}
    
    try:
        # Age validation
        age = form_data.get('age', '')
        try:
            age = int(age)
            if age < 0 or age > 120:
                errors['age'] = "Age must be between 0 and 120"
            else:
                cleaned_data['age'] = age
        except ValueError:
            errors['age'] = "Age must be a number"
            
        # Sex validation
        sex = form_data.get('sex', '')
        if sex not in ['0', '1']:
            errors['sex'] = "Sex must be selected"
        else:
            cleaned_data['sex'] = int(sex)
            
        # Chest Pain Type
        cp = form_data.get('cp', '')
        try:
            cp = int(cp)
            if cp not in [0, 1, 2, 3]:
                errors['cp'] = "Invalid chest pain type"
            else:
                cleaned_data['cp'] = cp
        except ValueError:
            errors['cp'] = "Chest pain type must be selected"
            
        # Resting Blood Pressure
        trestbps = form_data.get('trestbps', '')
        try:
            trestbps = int(trestbps)
            if trestbps < 50 or trestbps > 250:
                errors['trestbps'] = "Blood pressure must be between 50 and 250"
            else:
                cleaned_data['trestbps'] = trestbps
        except ValueError:
            errors['trestbps'] = "Blood pressure must be a number"
            
        # Serum Cholesterol
        chol = form_data.get('chol', '')
        try:
            chol = int(chol)
            if chol < 100 or chol > 600:
                errors['chol'] = "Cholesterol must be between 100 and 600"
            else:
                cleaned_data['chol'] = chol
        except ValueError:
            errors['chol'] = "Cholesterol must be a number"
            
        # Fasting Blood Sugar
        fbs = form_data.get('fbs', '')
        if fbs not in ['0', '1']:
            errors['fbs'] = "Fasting blood sugar must be selected"
        else:
            cleaned_data['fbs'] = int(fbs)
            
        # Resting ECG
        restecg = form_data.get('restecg', '')
        try:
            restecg = int(restecg)
            if restecg not in [0, 1, 2]:
                errors['restecg'] = "Invalid resting ECG value"
            else:
                cleaned_data['restecg'] = restecg
        except ValueError:
            errors['restecg'] = "Resting ECG must be selected"
            
        # Maximum Heart Rate
        thalach = form_data.get('thalach', '')
        try:
            thalach = int(thalach)
            if thalach < 60 or thalach > 220:
                errors['thalach'] = "Maximum heart rate must be between 60 and 220"
            else:
                cleaned_data['thalach'] = thalach
        except ValueError:
            errors['thalach'] = "Maximum heart rate must be a number"
            
        # Exercise Induced Angina
        exang = form_data.get('exang', '')
        if exang not in ['0', '1']:
            errors['exang'] = "Exercise induced angina must be selected"
        else:
            cleaned_data['exang'] = int(exang)
            
        # ST Depression
        oldpeak = form_data.get('oldpeak', '')
        try:
            oldpeak = float(oldpeak)
            if oldpeak < 0 or oldpeak > 10:
                errors['oldpeak'] = "ST depression must be between 0 and 10"
            else:
                cleaned_data['oldpeak'] = oldpeak
        except ValueError:
            errors['oldpeak'] = "ST depression must be a number"
            
        # Slope of Peak Exercise ST Segment
        slope = form_data.get('slope', '')
        try:
            slope = int(slope)
            if slope not in [0, 1, 2]:
                errors['slope'] = "Invalid slope value"
            else:
                cleaned_data['slope'] = slope
        except ValueError:
            errors['slope'] = "Slope must be selected"
            
        # Number of Major Vessels
        ca = form_data.get('ca', '')
        try:
            ca = int(ca)
            if ca not in [0, 1, 2, 3, 4]:
                errors['ca'] = "Invalid number of major vessels"
            else:
                cleaned_data['ca'] = ca
        except ValueError:
            errors['ca'] = "Number of major vessels must be selected"
            
        # Thalassemia
        thal = form_data.get('thal', '')
        try:
            thal = int(thal)
            if thal not in [0, 1, 2, 3]:
                errors['thal'] = "Invalid thalassemia value"
            else:
                cleaned_data['thal'] = thal
        except ValueError:
            errors['thal'] = "Thalassemia must be selected"
            
    except Exception as e:
        errors['general'] = f"Validation error: {str(e)}"
    
    is_valid = len(errors) == 0
    return is_valid, errors, cleaned_data

def validate_diabetes_form(form_data):
    """
    Validate diabetes form data
    
    Args:
        form_data (dict): Form data from request
        
    Returns:
        tuple: (is_valid, errors, cleaned_data)
    """
    errors = {}
    cleaned_data = {}
    
    try:
        # Pregnancies
        pregnancies = form_data.get('pregnancies', '')
        try:
            pregnancies = int(pregnancies)
            if pregnancies < 0 or pregnancies > 20:
                errors['pregnancies'] = "Pregnancies must be between 0 and 20"
            else:
                cleaned_data['pregnancies'] = pregnancies
        except ValueError:
            errors['pregnancies'] = "Pregnancies must be a number"
            
        # Glucose
        glucose = form_data.get('glucose', '')
        try:
            glucose = int(glucose)
            if glucose < 0 or glucose > 300:
                errors['glucose'] = "Glucose must be between 0 and 300"
            else:
                cleaned_data['glucose'] = glucose
        except ValueError:
            errors['glucose'] = "Glucose must be a number"
            
        # Blood Pressure
        blood_pressure = form_data.get('blood_pressure', '')
        try:
            blood_pressure = int(blood_pressure)
            if blood_pressure < 0 or blood_pressure > 200:
                errors['blood_pressure'] = "Blood pressure must be between 0 and 200"
            else:
                cleaned_data['blood_pressure'] = blood_pressure
        except ValueError:
            errors['blood_pressure'] = "Blood pressure must be a number"
            
        # Skin Thickness
        skin_thickness = form_data.get('skin_thickness', '')
        try:
            skin_thickness = int(skin_thickness)
            if skin_thickness < 0 or skin_thickness > 100:
                errors['skin_thickness'] = "Skin thickness must be between 0 and 100"
            else:
                cleaned_data['skin_thickness'] = skin_thickness
        except ValueError:
            errors['skin_thickness'] = "Skin thickness must be a number"
            
        # Insulin
        insulin = form_data.get('insulin', '')
        try:
            insulin = int(insulin)
            if insulin < 0 or insulin > 900:
                errors['insulin'] = "Insulin must be between 0 and 900"
            else:
                cleaned_data['insulin'] = insulin
        except ValueError:
            errors['insulin'] = "Insulin must be a number"
            
        # BMI
        bmi = form_data.get('bmi', '')
        try:
            bmi = float(bmi)
            if bmi < 0 or bmi > 70:
                errors['bmi'] = "BMI must be between 0 and 70"
            else:
                cleaned_data['bmi'] = bmi
        except ValueError:
            errors['bmi'] = "BMI must be a number"
            
        # Diabetes Pedigree Function
        diabetes_pedigree = form_data.get('diabetes_pedigree', '')
        try:
            diabetes_pedigree = float(diabetes_pedigree)
            if diabetes_pedigree < 0 or diabetes_pedigree > 3:
                errors['diabetes_pedigree'] = "Diabetes pedigree must be between 0 and 3"
            else:
                cleaned_data['diabetes_pedigree'] = diabetes_pedigree
        except ValueError:
            errors['diabetes_pedigree'] = "Diabetes pedigree must be a number"
            
        # Age
        age = form_data.get('age', '')
        try:
            age = int(age)
            if age < 0 or age > 120:
                errors['age'] = "Age must be between 0 and 120"
            else:
                cleaned_data['age'] = age
        except ValueError:
            errors['age'] = "Age must be a number"
            
    except Exception as e:
        errors['general'] = f"Validation error: {str(e)}"
    
    is_valid = len(errors) == 0
    return is_valid, errors, cleaned_data

def validate_pneumonia_form(form_data):
    """
    Validate pneumonia form data
    
    Args:
        form_data (dict): Form data from request
        
    Returns:
        tuple: (is_valid, errors, cleaned_data)
    """
    errors = {}
    cleaned_data = {}
    
    try:
        # Temperature
        temperature = form_data.get('temperature', '')
        try:
            temperature = float(temperature)
            if temperature < 95 or temperature > 108:
                errors['temperature'] = "Temperature must be between 95 and 108°F"
            else:
                cleaned_data['temperature'] = temperature
        except ValueError:
            errors['temperature'] = "Temperature must be a number"
            
        # Cough Severity
        cough_severity = form_data.get('cough_severity', '')
        try:
            cough_severity = int(cough_severity)
            if cough_severity < 0 or cough_severity > 10:
                errors['cough_severity'] = "Cough severity must be between 0 and 10"
            else:
                cleaned_data['cough_severity'] = cough_severity
        except ValueError:
            errors['cough_severity'] = "Cough severity must be a number"
            
        # Breathing Difficulty
        breathing_difficulty = form_data.get('breathing_difficulty', '')
        try:
            breathing_difficulty = int(breathing_difficulty)
            if breathing_difficulty < 0 or breathing_difficulty > 10:
                errors['breathing_difficulty'] = "Breathing difficulty must be between 0 and 10"
            else:
                cleaned_data['breathing_difficulty'] = breathing_difficulty
        except ValueError:
            errors['breathing_difficulty'] = "Breathing difficulty must be a number"
            
        # Oxygen Level
        oxygen_level = form_data.get('oxygen_level', '')
        try:
            oxygen_level = int(oxygen_level)
            if oxygen_level < 70 or oxygen_level > 100:
                errors['oxygen_level'] = "Oxygen level must be between 70 and 100"
            else:
                cleaned_data['oxygen_level'] = oxygen_level
        except ValueError:
            errors['oxygen_level'] = "Oxygen level must be a number"
            
    except Exception as e:
        errors['general'] = f"Validation error: {str(e)}"
    
    is_valid = len(errors) == 0
    return is_valid, errors, cleaned_data
