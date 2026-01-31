"""
Student Performance Prediction System with Authentication
Complete Flask application with Login/Signup functionality
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# MySQL Configuration for XAMPP
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Empty for XAMPP default
app.config['MYSQL_DB'] = 'student_performance_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Create model directory
MODEL_PATH = 'models/performance_model.pkl'
os.makedirs('models', exist_ok=True)

# Label encoders
encoders = {}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    """Initialize database tables"""
    try:
        cur = mysql.connection.cursor()
        
        # Users table for authentication
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Students table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Performance records table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS performance_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                study_hours FLOAT NOT NULL,
                previous_score FLOAT NOT NULL,
                attendance_percentage FLOAT NOT NULL,
                extracurricular VARCHAR(10) NOT NULL,
                sleep_hours FLOAT NOT NULL,
                tutoring VARCHAR(10) NOT NULL,
                predicted_grade VARCHAR(5),
                actual_grade VARCHAR(5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)
        
        mysql.connection.commit()
        cur.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

def train_model():
    """Train the ML model with sample data"""
    np.random.seed(42)
    n_samples = 500
    
    data = {
        'study_hours': np.random.uniform(1, 10, n_samples),
        'previous_score': np.random.uniform(40, 100, n_samples),
        'attendance': np.random.uniform(50, 100, n_samples),
        'extracurricular': np.random.choice(['Yes', 'No'], n_samples),
        'sleep_hours': np.random.uniform(4, 10, n_samples),
        'tutoring': np.random.choice(['Yes', 'No'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # IMPROVED GRADE CALCULATION
    def calculate_grade(row):
        # Weighted scoring system (more realistic)
        score = (
            row['previous_score'] * 0.40 +      # 40% weightage - most important
            row['attendance'] * 0.25 +          # 25% weightage
            row['study_hours'] * 3.5 +          # Study hours impact
            (5 if row['extracurricular'] == 'Yes' else 0) +  # Bonus points
            row['sleep_hours'] * 1.5 +          # Sleep impact
            (5 if row['tutoring'] == 'Yes' else 0)  # Tutoring bonus
        )
        
        # More realistic grade thresholds
        if score >= 85:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 55:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
    
    df['grade'] = df.apply(calculate_grade, axis=1)
    
    # Encode categorical variables
    le_extra = LabelEncoder()
    le_tutor = LabelEncoder()
    
    df['extracurricular_encoded'] = le_extra.fit_transform(df['extracurricular'])
    df['tutoring_encoded'] = le_tutor.fit_transform(df['tutoring'])
    
    encoders['extracurricular'] = le_extra
    encoders['tutoring'] = le_tutor
    
    # Prepare features and target
    X = df[['study_hours', 'previous_score', 'attendance', 
            'extracurricular_encoded', 'sleep_hours', 'tutoring_encoded']]
    y = df['grade']
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save model and encoders
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({'model': model, 'encoders': encoders}, f)
    
    print("Model trained and saved successfully!")
    return model

def load_model():
    """Load the trained model"""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            saved_data = pickle.load(f)
            return saved_data['model'], saved_data['encoders']
    return None, None

# Initialize database and train model on startup
with app.app_context():
    init_db()
    if not os.path.exists(MODEL_PATH):
        train_model()

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page - Public access"""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            full_name = request.form['full_name']
            
            # Validation
            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('signup'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters!', 'danger')
                return redirect(url_for('signup'))
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            # Insert into database
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (username, email, password, full_name) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, full_name)
            )
            mysql.connection.commit()
            cur.close()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Error: Username or email already exists!', 'danger')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            
            if user and check_password_hash(user['password'], password):
                # Set session
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['full_name'] = user['full_name']
                
                flash(f'Welcome back, {user["full_name"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!', 'danger')
                
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - Protected route"""
    try:
        cur = mysql.connection.cursor()
        
        # Get statistics
        cur.execute("SELECT COUNT(*) as count FROM students")
        total_students = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as count FROM performance_records")
        total_predictions = cur.fetchone()['count']
        
        cur.close()
        
        return render_template('dashboard.html', 
                             total_students=total_students,
                             total_predictions=total_predictions)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('dashboard.html', 
                             total_students=0,
                             total_predictions=0)

# ==================== STUDENT MANAGEMENT ROUTES ====================

@app.route('/students',strict_slashes=False)
@login_required
def students():
    """View all students"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students ORDER BY created_at DESC")
        students = cur.fetchall()
        cur.close()
        return render_template('students.html', students=students)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('students.html', students=[])

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    """Add new student"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            age = int(request.form['age'])
            gender = request.form['gender']
            email = request.form['email']
            
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO students (name, age, gender, email) VALUES (%s, %s, %s, %s)",
                (name, age, gender, email)
            )
            mysql.connection.commit()
            cur.close()
            
            flash('Student added successfully!', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('add_student.html')

@app.route('/predict/<int:student_id>', methods=['GET', 'POST'])
@login_required
def predict(student_id):
    """Predict student performance"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('students'))
    
    if request.method == 'POST':
        try:
            study_hours = float(request.form['study_hours'])
            previous_score = float(request.form['previous_score'])
            attendance = float(request.form['attendance'])
            extracurricular = request.form['extracurricular']
            sleep_hours = float(request.form['sleep_hours'])
            tutoring = request.form['tutoring']
            
            model, encoders = load_model()
            
            if model is None:
                flash('Model not found. Training new model...', 'warning')
                model = train_model()
                model, encoders = load_model()
            
            extra_encoded = encoders['extracurricular'].transform([extracurricular])[0]
            tutor_encoded = encoders['tutoring'].transform([tutoring])[0]
            
            features = np.array([[study_hours, previous_score, attendance, 
                                extra_encoded, sleep_hours, tutor_encoded]])
            
            predicted_grade = model.predict(features)[0]
            
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO performance_records 
                (student_id, study_hours, previous_score, attendance_percentage, 
                extracurricular, sleep_hours, tutoring, predicted_grade)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (student_id, study_hours, previous_score, attendance, 
                  extracurricular, sleep_hours, tutoring, predicted_grade))
            mysql.connection.commit()
            cur.close()
            
            flash(f'Predicted Grade: {predicted_grade}', 'success')
            return redirect(url_for('student_records', student_id=student_id))
        
            
        except Exception as e:
            flash(f'Prediction error: {str(e)}', 'danger')
    
    return render_template('predict.html', student=student)

@app.route('/student_records/<int:student_id>')
@login_required
def student_records(student_id):
    """View student's performance records"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        
        cur.execute("""
            SELECT * FROM performance_records 
            WHERE student_id = %s 
            ORDER BY created_at DESC
        """, (student_id,))
        records = cur.fetchall()
        cur.close()
        
        return render_template('student_records.html', student=student, records=records)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('students'))
    # Add this route to your app.py (after the add_student route)

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """Edit student information"""
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            age = int(request.form['age'])
            gender = request.form['gender']
            email = request.form['email']
            
            cur.execute("""
                UPDATE students 
                SET name = %s, age = %s, gender = %s, email = %s 
                WHERE id = %s
            """, (name, age, gender, email, student_id))
            mysql.connection.commit()
            cur.close()
            
            flash('Student updated successfully!', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    # GET request - show form with current data
    cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('students'))
    
    return render_template('edit_student.html', student=student)

@app.route('/analytics')
@login_required
def analytics():
    """View analytics dashboard"""
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("SELECT COUNT(*) as count FROM students")
        total_students = cur.fetchone()['count']
        
        cur.execute("SELECT COUNT(*) as count FROM performance_records")
        total_predictions = cur.fetchone()['count']
        
        cur.execute("""
            SELECT predicted_grade, COUNT(*) as count 
            FROM performance_records 
            GROUP BY predicted_grade
        """)
        grade_distribution = cur.fetchall()
        
        cur.close()
        
        return render_template('analytics.html', 
                             total_students=total_students,
                             total_predictions=total_predictions,
                             grade_distribution=grade_distribution)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('analytics.html', 
                             total_students=0, 
                             total_predictions=0,
                             grade_distribution=[])
    # Add this route to your app.py (after the analytics route, before API routes)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Settings page with all GUI components"""
    if request.method == 'POST':
        try:
            # Get form data
            gender = request.form.get('gender')
            notifications = request.form.getlist('notifications[]')
            study_hours = request.form.get('study_hours')
            attendance = request.form.get('attendance')
            courses = request.form.getlist('courses[]')
            notes = request.form.get('notes')
            
            # Display selected settings
            flash(f'Settings saved! Gender: {gender}, Study Hours: {study_hours}, Attendance: {attendance}%', 'success')
            flash(f'Notifications: {", ".join(notifications) if notifications else "None"}', 'info')
            flash(f'Selected Courses: {len(courses)} courses', 'info')
            
            return redirect(url_for('settings'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('settings.html')

@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    """Delete a student"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        mysql.connection.commit()
        cur.close()
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('students'))
# ==================== REST API ENDPOINTS ====================
# Add these routes to your app.py (after the existing routes)

# =========================
# API: STUDENTS ENDPOINTS
# =========================

@app.route('/api/students', methods=['GET'])
def api_get_all_students():
    """
    REST API: Get all students
    Returns: JSON array of all students
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students ORDER BY created_at DESC")
        students = cur.fetchall()
        cur.close()
        
        return jsonify({
            'success': True,
            'count': len(students),
            'data': students
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """
    REST API: Get single student by ID
    Returns: JSON object of student
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        cur.close()
        
        if student:
            return jsonify({
                'success': True,
                'data': student
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/students', methods=['POST'])
def api_create_student():
    """
    REST API: Create new student
    Request Body: JSON with name, age, gender, email
    Returns: JSON with created student data
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['name', 'age', 'gender', 'email']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name, age, gender, email'
            }), 400
        
        name = data['name']
        age = int(data['age'])
        gender = data['gender']
        email = data['email']
        
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO students (name, age, gender, email) VALUES (%s, %s, %s, %s)",
            (name, age, gender, email)
        )
        mysql.connection.commit()
        student_id = cur.lastrowid
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'data': {
                'id': student_id,
                'name': name,
                'age': age,
                'gender': gender,
                'email': email
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    """
    REST API: Update existing student
    Request Body: JSON with name, age, gender, email
    Returns: JSON with updated student data
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['name', 'age', 'gender', 'email']):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name, age, gender, email'
            }), 400
        
        name = data['name']
        age = int(data['age'])
        gender = data['gender']
        email = data['email']
        
        cur = mysql.connection.cursor()
        
        # Check if student exists
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Update student
        cur.execute("""
            UPDATE students 
            SET name = %s, age = %s, gender = %s, email = %s 
            WHERE id = %s
        """, (name, age, gender, email, student_id))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully',
            'data': {
                'id': student_id,
                'name': name,
                'age': age,
                'gender': gender,
                'email': email
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    """
    REST API: Delete student
    Returns: JSON confirmation message
    """
    try:
        cur = mysql.connection.cursor()
        
        # Check if student exists
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        # Delete student
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            'success': True,
            'message': f'Student with ID {student_id} deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =================================
# API: PERFORMANCE RECORDS ENDPOINTS
# =================================

@app.route('/api/records', methods=['GET'])
def api_get_all_records():
    """
    REST API: Get all performance records
    Returns: JSON array of all records
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT pr.*, s.name as student_name 
            FROM performance_records pr
            JOIN students s ON pr.student_id = s.id
            ORDER BY pr.created_at DESC
        """)
        records = cur.fetchall()
        cur.close()
        
        return jsonify({
            'success': True,
            'count': len(records),
            'data': records
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/records/<int:record_id>', methods=['GET'])
def api_get_record(record_id):
    """
    REST API: Get single performance record by ID
    Returns: JSON object of record
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT pr.*, s.name as student_name 
            FROM performance_records pr
            JOIN students s ON pr.student_id = s.id
            WHERE pr.id = %s
        """, (record_id,))
        record = cur.fetchone()
        cur.close()
        
        if record:
            return jsonify({
                'success': True,
                'data': record
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Record not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/records/student/<int:student_id>', methods=['GET'])
def api_get_student_records(student_id):
    """
    REST API: Get all records for a specific student
    Returns: JSON array of student's records
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT * FROM performance_records 
            WHERE student_id = %s 
            ORDER BY created_at DESC
        """, (student_id,))
        records = cur.fetchall()
        cur.close()
        
        return jsonify({
            'success': True,
            'student_id': student_id,
            'count': len(records),
            'data': records
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predict', methods=['POST'])
def api_create_prediction():
    """
    REST API: Create new prediction
    Request Body: JSON with student_id, study_hours, previous_score, etc.
    Returns: JSON with predicted grade
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'study_hours', 'previous_score', 
                          'attendance', 'extracurricular', 'sleep_hours', 'tutoring']
        if not all(key in data for key in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        student_id = int(data['student_id'])
        study_hours = float(data['study_hours'])
        previous_score = float(data['previous_score'])
        attendance = float(data['attendance'])
        extracurricular = data['extracurricular']
        sleep_hours = float(data['sleep_hours'])
        tutoring = data['tutoring']
        
        # Load model
        model, encoders = load_model()
        
        if model is None:
            model = train_model()
            model, encoders = load_model()
        
        # Encode categorical variables
        extra_encoded = encoders['extracurricular'].transform([extracurricular])[0]
        tutor_encoded = encoders['tutoring'].transform([tutoring])[0]
        
        # Prepare features
        features = np.array([[study_hours, previous_score, attendance, 
                            extra_encoded, sleep_hours, tutor_encoded]])
        
        # Predict
        predicted_grade = model.predict(features)[0]
        
        # Save to database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO performance_records 
            (student_id, study_hours, previous_score, attendance_percentage, 
            extracurricular, sleep_hours, tutoring, predicted_grade)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (student_id, study_hours, previous_score, attendance, 
              extracurricular, sleep_hours, tutoring, predicted_grade))
        mysql.connection.commit()
        record_id = cur.lastrowid
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'Prediction created successfully',
            'data': {
                'record_id': record_id,
                'student_id': student_id,
                'predicted_grade': predicted_grade,
                'study_hours': study_hours,
                'previous_score': previous_score,
                'attendance': attendance,
                'extracurricular': extracurricular,
                'sleep_hours': sleep_hours,
                'tutoring': tutoring
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def api_delete_record(record_id):
    """
    REST API: Delete performance record
    Returns: JSON confirmation message
    """
    try:
        cur = mysql.connection.cursor()
        
        # Check if record exists
        cur.execute("SELECT * FROM performance_records WHERE id = %s", (record_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({
                'success': False,
                'error': 'Record not found'
            }), 404
        
        # Delete record
        cur.execute("DELETE FROM performance_records WHERE id = %s", (record_id,))
        mysql.connection.commit()
        cur.close()
        
        return jsonify({
            'success': True,
            'message': f'Record with ID {record_id} deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =======================
# API: ANALYTICS ENDPOINT
# =======================

@app.route('/api/analytics', methods=['GET'])
def api_get_analytics():
    """
    REST API: Get analytics data
    Returns: JSON with statistics
    """
    try:
        cur = mysql.connection.cursor()
        
        # Total students
        cur.execute("SELECT COUNT(*) as count FROM students")
        total_students = cur.fetchone()['count']
        
        # Total predictions
        cur.execute("SELECT COUNT(*) as count FROM performance_records")
        total_predictions = cur.fetchone()['count']
        
        # Grade distribution
        cur.execute("""
            SELECT predicted_grade, COUNT(*) as count 
            FROM performance_records 
            GROUP BY predicted_grade
        """)
        grade_distribution = cur.fetchall()
        
        # Average scores
        cur.execute("""
            SELECT 
                AVG(study_hours) as avg_study_hours,
                AVG(previous_score) as avg_previous_score,
                AVG(attendance_percentage) as avg_attendance,
                AVG(sleep_hours) as avg_sleep_hours
            FROM performance_records
        """)
        averages = cur.fetchone()
        
        cur.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total_students': total_students,
                'total_predictions': total_predictions,
                'grade_distribution': grade_distribution,
                'averages': averages
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ===================
# API: TEST ENDPOINT
# ===================

@app.route('/api/test', methods=['GET'])
def api_test():
    """
    REST API: Test endpoint to verify API is working
    Returns: JSON confirmation message
    """
    return jsonify({
        'success': True,
        'message': 'API is working!',
        'endpoints': {
            'students': {
                'GET /api/students': 'Get all students',
                'GET /api/students/<id>': 'Get single student',
                'POST /api/students': 'Create student',
                'PUT /api/students/<id>': 'Update student',
                'DELETE /api/students/<id>': 'Delete student'
            },
            'records': {
                'GET /api/records': 'Get all records',
                'GET /api/records/<id>': 'Get single record',
                'GET /api/records/student/<id>': 'Get student records',
                'POST /api/predict': 'Create prediction',
                'DELETE /api/records/<id>': 'Delete record'
            },
            'analytics': {
                'GET /api/analytics': 'Get analytics data'
            }
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)