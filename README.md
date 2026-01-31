# 🎓 Student Performance Prediction System

A comprehensive web-based application that uses Machine Learning to predict student academic performance and provides complete student management functionality.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [User Guide](#user-guide)
- [REST API Documentation](#rest-api-documentation)
- [GUI Components](#gui-components)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## 🌟 Overview

The **Student Performance Prediction System** is a full-stack web application designed to help educational institutions predict student performance using artificial intelligence. The system provides comprehensive student management, performance tracking, and analytics capabilities.

### Key Highlights:
- 🤖 AI-powered grade prediction using Random Forest Classifier
- 👥 Complete student management system (CRUD operations)
- 📊 Interactive analytics dashboard with visualizations
- 🔐 Secure user authentication and authorization
- 🌐 RESTful API with JSON responses
- 💾 MySQL database for data persistence
- 📱 Responsive and modern user interface

---

## ✨ Features

### 1. **User Authentication**
- Secure user registration and login
- Password hashing for security
- Session management
- Protected routes requiring authentication

### 2. **Student Management**
- Add new students with detailed information
- View all students in a searchable table
- Edit existing student records
- Delete students (with cascade deletion of related records)
- Individual student profile pages

### 3. **Performance Prediction**
- AI-powered grade prediction (A, B, C, D, F)
- Based on multiple factors:
  - Study hours per day
  - Previous exam scores
  - Attendance percentage
  - Extracurricular activities
  - Sleep hours
  - Tutoring status
- Real-time predictions with instant results

### 4. **Performance Tracking**
- Historical record of all predictions
- Individual student performance history
- Track progress over time
- Date-stamped records

### 5. **Analytics Dashboard**
- Total students count
- Total predictions made
- Grade distribution visualization
- Average metrics (study hours, attendance, etc.)
- Interactive charts using Chart.js

### 6. **Settings & Preferences**
- Customizable user settings
- Notification preferences
- Study goals configuration
- Course selection

### 7. **REST API**
- 12 RESTful endpoints
- JSON request/response format
- Complete CRUD operations
- API testing interface included

---

## 🛠️ Technologies Used

### Backend:
- **Python 3.11+** - Programming language
- **Flask 2.3.0** - Web framework
- **MySQL** - Database management system
- **Flask-MySQLdb** - MySQL integration
- **Werkzeug** - Password hashing and security

### Machine Learning:
- **scikit-learn 1.2.2** - ML algorithms
- **pandas 2.0.0** - Data manipulation
- **numpy 1.24.0** - Numerical computing
- **Random Forest Classifier** - Prediction model

### Frontend:
- **HTML5** - Structure
- **CSS3** - Styling
- **Bootstrap 5.1.3** - UI framework
- **JavaScript** - Interactivity
- **Font Awesome 6.0** - Icons
- **Chart.js** - Data visualization

### Development Tools:
- **XAMPP** - Local development environment
- **VS Code** - Code editor
- **Git** - Version control
- **Postman** - API testing

---

## 💻 System Requirements

### Minimum Requirements:
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for package installation

### Software Requirements:
- Python 3.8+
- MySQL Server (via XAMPP or standalone)
- Web browser (Chrome, Firefox, Edge, Safari)
- Text editor or IDE

---

## 📥 Installation & Setup

### Step 1: Clone or Download Project

```bash
# If using Git
git clone https://github.com/yourusername/student-performance-system.git
cd student-performance-system

# Or download ZIP and extract
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
```
Flask==2.3.0
flask-mysqldb==1.0.1
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.2.2
mysqlclient==2.1.1
```

---

## 🗄️ Database Configuration

### Option 1: Using XAMPP (Recommended for Windows)

1. **Install XAMPP**
   - Download from: https://www.apachefriends.org/
   - Install and launch XAMPP Control Panel

2. **Start MySQL**
   - Click "Start" button next to MySQL
   - Wait for green status indicator

3. **Create Database**
   - Click "Admin" button next to MySQL (opens phpMyAdmin)
   - Or visit: `http://localhost/phpmyadmin`
   - Click "New" in left sidebar
   - Database name: `student_performance_db`
   - Collation: `utf8mb4_general_ci`
   - Click "Create"

4. **Import Schema (Optional)**
   - Click on `student_performance_db`
   - Click "Import" tab
   - Choose `database_schema.sql` file
   - Click "Go"

### Option 2: Using Standalone MySQL

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE student_performance_db;

# Exit
EXIT;
```

### Database Credentials Configuration

Edit `app.py` lines 22-26:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Empty for XAMPP default
app.config['MYSQL_DB'] = 'student_performance_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
```

**Note**: Tables will be created automatically on first run!

---

## 🚀 Running the Application

### Start the Application

```bash
# Make sure virtual environment is activated
# Make sure MySQL is running in XAMPP

# Run the application
python app.py
```

### Expected Output:

```
Database initialized successfully!
Model trained and saved successfully!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### First-Time Setup

1. Click "Sign Up" to create an account
2. Fill in your details (username, email, password)
3. Click "Sign Up"
4. Login with your credentials
5. Start using the system!

---

## 📁 Project Structure

```
student_performance_system/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── database_schema.sql             # Database schema
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template with navigation
│   ├── index.html                 # Home page
│   ├── login.html                 # Login page
│   ├── signup.html                # Registration page
│   ├── dashboard.html             # User dashboard
│   ├── students.html              # Students list
│   ├── add_student.html           # Add student form
│   ├── edit_student.html          # Edit student form
│   ├── predict.html               # Prediction form
│   ├── student_records.html       # Performance records
│   ├── analytics.html             # Analytics dashboard
│   ├── settings.html              # Settings page
│   └── api_test.html              # API testing interface (optional)
│
└── models/                         # ML models (auto-generated)
    └── performance_model.pkl      # Trained ML model
```

---

## 📖 User Guide

### For Students/Teachers:

#### 1. **Creating an Account**
- Click "Sign Up" on home page
- Enter full name, username, email, password
- Click "Sign Up" button
- Login with your credentials

#### 2. **Adding Students**
- Navigate to "Add Student" from menu
- Fill in student information:
  - Full name
  - Age
  - Gender
  - Email address
- Click "Add Student"

#### 3. **Making Predictions**
- Go to "Students" page
- Click green "Predict" button next to a student
- Enter performance factors:
  - Study hours per day
  - Previous exam score
  - Attendance percentage
  - Extracurricular activities (Yes/No)
  - Sleep hours per day
  - Taking tutoring (Yes/No)
- Click "Predict Grade"
- View predicted grade (A, B, C, D, or F)

#### 4. **Viewing Records**
- Go to "Students" page
- Click blue "Records" button next to a student
- View all historical predictions
- See performance trends over time

#### 5. **Editing Students**
- Go to "Students" page
- Click yellow "Edit" button next to a student
- Update student information
- Click "Update Student"

#### 6. **Viewing Analytics**
- Click "Analytics" in navigation menu
- View:
  - Total students count
  - Total predictions made
  - Grade distribution chart
  - Average performance metrics

#### 7. **Configuring Settings**
- Click "Settings" in navigation menu
- Configure:
  - Personal preferences
  - Notification settings
  - Study goals
  - Course selections

---

## 🔌 REST API Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Authentication
Currently no authentication required for API endpoints (can be added).

### Response Format
All endpoints return JSON responses with the following structure:

**Success Response:**
```json
{
  "success": true,
  "data": {...},
  "count": 10,
  "message": "Operation successful"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here"
}
```

---

### API Endpoints

#### **Students API**

##### 1. Get All Students
```
GET /api/students
```

**Response:**
```json
{
  "success": true,
  "count": 4,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 18,
      "gender": "Male",
      "email": "john@example.com",
      "created_at": "2024-12-18 10:30:00"
    }
  ]
}
```

##### 2. Get Single Student
```
GET /api/students/<id>
```

**Example:** `GET /api/students/1`

##### 3. Create Student
```
POST /api/students
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Jane Smith",
  "age": 20,
  "gender": "Female",
  "email": "jane@example.com"
}
```

##### 4. Update Student
```
PUT /api/students/<id>
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Updated",
  "age": 19,
  "gender": "Male",
  "email": "john.updated@example.com"
}
```

##### 5. Delete Student
```
DELETE /api/students/<id>
```

---

#### **Performance Records API**

##### 6. Get All Records
```
GET /api/records
```

##### 7. Get Single Record
```
GET /api/records/<id>
```

##### 8. Get Student's Records
```
GET /api/records/student/<student_id>
```

##### 9. Create Prediction
```
POST /api/predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "student_id": 1,
  "study_hours": 6.0,
  "previous_score": 80.0,
  "attendance": 90.0,
  "extracurricular": "Yes",
  "sleep_hours": 7.0,
  "tutoring": "No"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Prediction created successfully",
  "data": {
    "record_id": 5,
    "student_id": 1,
    "predicted_grade": "A"
  }
}
```

##### 10. Delete Record
```
DELETE /api/records/<id>
```

---

#### **Analytics API**

##### 11. Get Analytics
```
GET /api/analytics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_students": 10,
    "total_predictions": 25,
    "grade_distribution": [
      {"predicted_grade": "A", "count": 5},
      {"predicted_grade": "B", "count": 10}
    ],
    "averages": {
      "avg_study_hours": 5.5,
      "avg_previous_score": 75.2
    }
  }
}
```

---

#### **Utility API**

##### 12. Test API
```
GET /api/test
```

Returns list of all available endpoints.

---

### Testing the API

#### Using Browser (GET requests only):
```
http://127.0.0.1:5000/api/test
http://127.0.0.1:5000/api/students
http://127.0.0.1:5000/api/analytics
```

#### Using Postman:
1. Download Postman from https://www.postman.com/
2. Create new request
3. Set method (GET, POST, PUT, DELETE)
4. Enter URL
5. For POST/PUT: Add JSON body
6. Click Send

#### Using cURL:
```bash
# GET request
curl http://127.0.0.1:5000/api/students

# POST request
curl -X POST http://127.0.0.1:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","age":18,"gender":"Male","email":"test@example.com"}'
```

---

## 🎨 GUI Components

### Complete List of GUI Components Implemented:

| Component | Location | Description |
|-----------|----------|-------------|
| **Menu Bar** | All pages | Navigation bar with links |
| **Menu Items** | All pages | Dashboard, Students, Analytics, Settings |
| **Button** | All pages | Submit, Save, Cancel, Edit, Delete |
| **Table** | students.html, analytics.html | Data display in tabular format |
| **TextField** | Multiple pages | Single-line text input |
| **TextArea** | predict.html, settings.html | Multi-line text input |
| **RadioButton** | settings.html | Gender selection (single choice) |
| **CheckBox** | settings.html | Notification preferences (multiple) |
| **DropDown Box** | Multiple pages | Gender, extracurricular, tutoring |
| **Password Field** | login.html, signup.html | Secure password input |
| **List** | settings.html | Course selection, priority tasks |
| **Scrollbar** | settings.html | For long content areas |
| **Slider** | settings.html | Study hours, attendance goals |
| **Progress Bar** | settings.html | Visual attendance indicator |

**Total Interfaces:** 11 pages
**Total Components:** 14+ different component types

---

## 📸 Screenshots

### Authentication
- Login page with email/password fields
- Signup page with registration form
- Password field with secure input

### Dashboard
- Welcome message with user name
- Statistics cards (students, predictions)
- Quick action buttons
- Navigation menu bar

### Student Management
- Students table with all records
- Add student form (TextField, DropDown)
- Edit student form
- Action buttons (Predict, Records, Edit, Delete)

### Prediction System
- Prediction form with multiple inputs
- Real-time grade prediction
- Success message with predicted grade
- Redirect to performance records

### Performance Records
- Historical prediction table
- Date-stamped records
- Grade badges with color coding
- Individual student records view

### Analytics Dashboard
- Total counts display
- Grade distribution bar chart
- Visual data representation
- Interactive charts

### Settings Page
- Radio buttons (Gender selection)
- Check boxes (Notifications)
- Sliders (Study hours, Attendance)
- Lists with scrollbars (Courses, Tasks)
- TextArea with scrollbar (Notes)

### API Testing
- API testing interface
- JSON response display
- Interactive buttons for each endpoint
- Request/response visualization

---

## 🔮 Future Enhancements

### Planned Features:
- [ ] Email notifications for low predictions
- [ ] Export data to PDF/Excel
- [ ] Comparison with class averages
- [ ] Teacher/Student role-based access
- [ ] Parent portal access
- [ ] Mobile application
- [ ] Advanced ML models (Neural Networks)
- [ ] Real-time performance monitoring
- [ ] Integration with Learning Management Systems
- [ ] Batch student import (CSV upload)
- [ ] Custom reporting tools
- [ ] API authentication with JWT
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Attendance tracking integration

### Technical Improvements:
- [ ] Add unit tests
- [ ] Implement caching (Redis)
- [ ] Add logging system
- [ ] Database migrations (Alembic)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Load balancing
- [ ] API rate limiting

---

## 🐛 Troubleshooting

### Common Issues and Solutions:

#### Issue 1: "Can't connect to MySQL server"
**Solution:**
- Ensure XAMPP MySQL is running (green status)
- Check database credentials in app.py
- Verify database name is correct

#### Issue 2: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue 3: "Access denied for user 'root'"
**Solution:**
- Check MySQL password in app.py
- For XAMPP, default password is empty: `''`

#### Issue 4: Port 5000 already in use
**Solution:**
```python
# In app.py, change the last line:
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

#### Issue 5: "Template not found"
**Solution:**
- Verify all HTML files are in `templates/` folder
- Check file names match exactly (case-sensitive)

#### Issue 6: Machine learning model errors
**Solution:**
- Delete `models/` folder
- Restart application (model will retrain automatically)

---

## 📞 Support

For issues, questions, or contributions:

- **Email:** ahsanali7@gmail.com
- **GitHub Issues:** https://github.com/ahsan ali/student-performance-system/issues
- **Documentation:** This README file

---

## 👥 Contributors

- **Your Name** - Developer
- **Institution** - Academic Project
- **Course** - Web Development / Machine Learning
- **Semester** - [Your Semester/Year]

---

## 📝 License

This project is created for educational purposes as part of academic coursework.

---

## 🙏 Acknowledgments

- Flask documentation and community
- scikit-learn machine learning library
- Bootstrap framework for UI components
- Font Awesome for icons
- Chart.js for data visualization
- Stack Overflow community for troubleshooting help

---

## 📅 Version History

### Version 2.0 (Phase 2 - Current)
- ✅ Added REST API endpoints
- ✅ Implemented all GUI components
- ✅ Added Settings page
- ✅ API testing interface
- ✅ Complete documentation

### Version 1.0 (Phase 1)
- ✅ Basic student management
- ✅ ML prediction system
- ✅ User authentication
- ✅ Database integration
- ✅ Analytics dashboard

---

## 🎓 Academic Context

**Course:** Web Development / Software Engineering
**Project Type:** Phase 2 - Full Stack Web Application
**Requirements Met:**
- ✅ MySQL Database Integration
- ✅ User Authentication (Login/Signup)
- ✅ CRUD Operations (3 services)
- ✅ REST API with JSON responses
- ✅ 10+ GUI Interfaces
- ✅ All required GUI components
- ✅ Complete documentation

---

**Made with ❤️ for learning and academic excellence**

---

*Last Updated: December 2025*