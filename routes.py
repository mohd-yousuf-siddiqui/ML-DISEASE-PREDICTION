from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
import ml_models
from utils import (
    save_prediction, 
    validate_heart_disease_form, 
    validate_diabetes_form,
    validate_pneumonia_form
)
from forms import RegistrationForm, LoginForm
from models import User, Prediction
import logging
import json

# Initialize ML models - will be called from app.py
def initialize():
    ml_models.initialize_models()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/data-flow')
def data_flow():
    return render_template('data_flow.html')

@app.route('/heart-disease', methods=['GET', 'POST'])
def heart_disease():
    if request.method == 'POST':
        try:
            # Validate form data
            is_valid, errors, cleaned_data = validate_heart_disease_form(request.form)
            
            if not is_valid:
                for field, error in errors.items():
                    flash(error, 'danger')
                return render_template('heart_disease.html', form_data=request.form, errors=errors)
            
            # Make prediction
            result = ml_models.predict_heart_disease(cleaned_data)
            
            # Save prediction to session and database
            user_id = current_user.id if current_user.is_authenticated else None
            prediction_id = save_prediction('heart', result, cleaned_data, user_id)
            session['prediction_result'] = {
                'id': prediction_id,
                'type': 'heart',
                'result': result
            }
            
            # Redirect to results page
            return redirect(url_for('results'))
            
        except Exception as e:
            logging.error(f"Error in heart disease prediction: {str(e)}")
            flash(f"An error occurred: {str(e)}", 'danger')
            return render_template('heart_disease.html', form_data={}, errors={})
    
    return render_template('heart_disease.html', form_data={}, errors={})

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'POST':
        try:
            # Validate form data
            is_valid, errors, cleaned_data = validate_diabetes_form(request.form)
            
            if not is_valid:
                for field, error in errors.items():
                    flash(error, 'danger')
                return render_template('diabetes.html', form_data=request.form, errors=errors)
            
            # Make prediction
            result = ml_models.predict_diabetes(cleaned_data)
            
            # Save prediction to session and database
            user_id = current_user.id if current_user.is_authenticated else None
            prediction_id = save_prediction('diabetes', result, cleaned_data, user_id)
            session['prediction_result'] = {
                'id': prediction_id,
                'type': 'diabetes',
                'result': result
            }
            
            # Redirect to results page
            return redirect(url_for('results'))
            
        except Exception as e:
            logging.error(f"Error in diabetes prediction: {str(e)}")
            flash(f"An error occurred: {str(e)}", 'danger')
            return render_template('diabetes.html', form_data={}, errors={})
    
    return render_template('diabetes.html', form_data={}, errors={})

@app.route('/pneumonia', methods=['GET', 'POST'])
def pneumonia():
    if request.method == 'POST':
        try:
            # Validate form data
            is_valid, errors, cleaned_data = validate_pneumonia_form(request.form)
            
            if not is_valid:
                for field, error in errors.items():
                    flash(error, 'danger')
                return render_template('pneumonia.html', form_data=request.form, errors=errors)
            
            # Make prediction
            result = ml_models.predict_pneumonia(cleaned_data)
            
            # Save prediction to session and database
            user_id = current_user.id if current_user.is_authenticated else None
            prediction_id = save_prediction('pneumonia', result, cleaned_data, user_id)
            session['prediction_result'] = {
                'id': prediction_id,
                'type': 'pneumonia',
                'result': result
            }
            
            # Redirect to results page
            return redirect(url_for('results'))
            
        except Exception as e:
            logging.error(f"Error in pneumonia prediction: {str(e)}")
            flash(f"An error occurred: {str(e)}", 'danger')
            return render_template('pneumonia.html', form_data={}, errors={})
    
    return render_template('pneumonia.html', form_data={}, errors={})

@app.route('/results')
def results():
    # Get prediction result from session
    prediction_result = session.get('prediction_result')
    
    if not prediction_result:
        flash('No prediction results found. Please make a prediction first.', 'warning')
        return redirect(url_for('index'))
    
    return render_template('results.html', prediction=prediction_result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating user: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    # Get user's predictions
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).all()
    return render_template('profile.html', predictions=predictions)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    # Get all users and predictions for admin panel
    users = User.query.all()
    predictions = Prediction.query.order_by(Prediction.created_at.desc()).all()
    
    # Calculate timestamp for 24 hours ago for recent predictions
    from datetime import datetime, timedelta
    now_minus_24h = datetime.utcnow() - timedelta(days=1)
    
    return render_template('admin.html', users=users, predictions=predictions, now_minus_24h=now_minus_24h)
