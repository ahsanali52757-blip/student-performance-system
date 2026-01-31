-- ============================================
-- Student Performance Prediction System
-- Database Schema
-- ============================================
-- Version: 2.0
-- Created: December 2024
-- Database: MySQL 5.7+ / MariaDB
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS student_performance_db;

-- Use the database
USE student_performance_db;

-- ============================================
-- TABLE 1: users
-- Purpose: Store user authentication data
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT 'Unique username for login',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT 'User email address',
    password VARCHAR(255) NOT NULL COMMENT 'Hashed password',
    full_name VARCHAR(100) NOT NULL COMMENT 'User full name',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation date',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores user authentication and profile information';

-- ============================================
-- TABLE 2: students
-- Purpose: Store student information
-- ============================================

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique student ID',
    name VARCHAR(100) NOT NULL COMMENT 'Student full name',
    age INT NOT NULL COMMENT 'Student age',
    gender VARCHAR(10) NOT NULL COMMENT 'Student gender (Male/Female/Other)',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT 'Student email address',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation date',
    CHECK (age >= 5 AND age <= 100),
    CHECK (gender IN ('Male', 'Female', 'Other')),
    INDEX idx_student_name (name),
    INDEX idx_student_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores student personal information and details';

-- ============================================
-- TABLE 3: performance_records
-- Purpose: Store student performance predictions
-- ============================================

CREATE TABLE IF NOT EXISTS performance_records (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique record ID',
    student_id INT NOT NULL COMMENT 'Foreign key to students table',
    study_hours FLOAT NOT NULL COMMENT 'Daily study hours',
    previous_score FLOAT NOT NULL COMMENT 'Previous exam score percentage',
    attendance_percentage FLOAT NOT NULL COMMENT 'Class attendance percentage',
    extracurricular VARCHAR(10) NOT NULL COMMENT 'Participates in extracurricular activities (Yes/No)',
    sleep_hours FLOAT NOT NULL COMMENT 'Daily sleep hours',
    tutoring VARCHAR(10) NOT NULL COMMENT 'Takes tutoring (Yes/No)',
    predicted_grade VARCHAR(5) DEFAULT NULL COMMENT 'Predicted grade (A/B/C/D/F)',
    actual_grade VARCHAR(5) DEFAULT NULL COMMENT 'Actual grade received (optional)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Prediction date and time',
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (study_hours >= 0 AND study_hours <= 24),
    CHECK (previous_score >= 0 AND previous_score <= 100),
    CHECK (attendance_percentage >= 0 AND attendance_percentage <= 100),
    CHECK (extracurricular IN ('Yes', 'No')),
    CHECK (sleep_hours >= 0 AND sleep_hours <= 24),
    CHECK (tutoring IN ('Yes', 'No')),
    CHECK (predicted_grade IN ('A', 'B', 'C', 'D', 'F', NULL)),
    CHECK (actual_grade IN ('A', 'B', 'C', 'D', 'F', NULL)),
    INDEX idx_student_id (student_id),
    INDEX idx_predicted_grade (predicted_grade),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Stores student performance predictions and historical data';

-- ============================================
-- Additional indexes for performance optimization
-- ============================================

CREATE INDEX idx_student_grade ON performance_records(student_id, predicted_grade);
CREATE INDEX idx_date_range ON performance_records(created_at, student_id);

-- ============================================
-- Success message
-- ============================================

SELECT 'Database schema created successfully!' AS Status;
SELECT 'Tables: users, students, performance_records' AS Tables_Created;
SELECT 'Ready to use with Flask application!' AS Ready;