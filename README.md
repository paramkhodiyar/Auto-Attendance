# Auto Attendance

## Overview

The Attendance Proxy App is designed to combat proxy attendance and enhance the accuracy and reliability of attendance tracking in educational settings. By leveraging QR codes, the application enables teachers to generate unique attendance markers for their classes, allowing students to mark their presence without the risk of someone else attending in their place. This innovative approach ensures that attendance records are genuine, promoting accountability among students.

### Objectives

1. **Ensure Authentic Attendance Tracking**: The primary aim of the application is to prevent proxy attendance, where students may attempt to sign in for their absent peers. By requiring students to scan a unique QR code generated for each class, the app provides a more secure method of verifying attendance.

2. **Facilitate Easy Management for Teachers**: Teachers can easily manage attendance records by generating QR codes at the start of each class, simplifying the attendance-taking process and minimizing manual effort.

3. **User-Friendly Interface**: The app is designed to be intuitive for both students and teachers, with straightforward login, registration, and attendance scanning functionalities, encouraging regular use.

4. **Database Integration for Record Keeping**: Utilizing a SQLite database, the application securely stores user information (students and teachers) and attendance records, enabling easy retrieval and analysis of attendance data.

5. **Customizable Attendance Options**: The application allows teachers to set class-specific parameters such as class codes and dates, providing flexibility in managing various classes or sessions.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Components](#components)
   - [Database Initialization](#database-initialization)
   - [User Interface](#user-interface)
   - [Login Functionality](#login-functionality)
   - [Registration Functionality](#registration-functionality)
   - [Student App](#student-app)
   - [Teacher App](#teacher-app)
   - [QR Code Generation](#qr-code-generation)
5. [Key Features](#key-features)
6. [Future Improvements](#future-improvements)

## Prerequisites

- Python 3.x
- Libraries:
  - `qrcode`
  - `sqlite3`
  - `PIL` (Pillow)
  - `customtkinter`

You can install the required libraries using pip:

```bash
pip install qrcode[pil] pillow customtkinter
```

## Installation

1. Clone or download the repository containing the source code.
2. Ensure Python 3.x is installed on your system.
3. Install the required libraries as mentioned in the prerequisites section.
4. Run the application by executing the main script.

```bash
python main.py
```

## Usage

Upon running the application, the login window will appear. Users can choose to log in as a student or a teacher. If they are not registered, they can access the registration form. After logging in, students can scan QR codes to mark their attendance, while teachers can generate QR codes for attendance management.

## Components

### Database Initialization

The application initializes a SQLite database (`attendance.db`) with three tables:

- **students**: Stores student details (ID, username, password).
- **teachers**: Stores teacher details (ID, TCODE, name, password).
- **attendance**: Records attendance with references to students and class details.

```python
def init_db():
    connection = sqlite3.connect("attendance.db")
    cursor = connection.cursor()
    ...
```

### User Interface

The user interface is built using `customtkinter`, providing a dark mode aesthetic. It consists of the following elements:

- **Login Window**: Contains fields for username/password and buttons for student/teacher login and registration.
- **Registration Window**: Allows new users to register as students or teachers.
- **Student App**: Enables students to scan QR codes for attendance.
- **Teacher App**: Allows teachers to generate QR codes for class attendance.

### Login Functionality

The application provides a login mechanism for both students and teachers. Upon entering their credentials, the application checks the database for valid entries.

```python
def login_user():
    username = username_entry.get()
    ...
```

### Registration Functionality

Users can register as students or teachers. The application ensures that usernames and TCODEs are unique by checking the database before registration.

```python
def open_register_window(user_type):
    ...
```

### Student App

Once logged in, students can access the Student App, which allows them to scan QR codes to mark their attendance.

```python
def open_student_app(student_id):
    ...
```

### Teacher App

The Teacher App provides functionalities to generate QR codes for marking attendance and to manage the start and end of classes.

```python
def open_teacher_app(teacher_id):
    ...
```

### QR Code Generation

The application uses the `qrcode` library to generate QR codes for attendance. Teachers can create QR codes containing the class information, which students can then scan.

```python
def generate_qr(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    ...
```

## Key Features

- **User Authentication**: The app supports login functionality for both students and teachers, ensuring that only authorized users can access the system.

- **Registration Process**: New users can easily register as students or teachers, with the system validating unique usernames and TCODEs.

- **QR Code Generation**: Teachers can generate QR codes that encode attendance information, such as class code, date, and a placeholder for start/end times.

- **QR Code Scanning Functionality**: The app is designed to include the ability for students to scan the QR codes displayed by teachers. Upon scanning, the app will record the student's attendance in the database.

- **Attendance Records**: The application maintains a comprehensive record of attendance, allowing both students and teachers to access past attendance data.

- **Secure Password Storage**: User passwords should be hashed before being stored in the database, protecting sensitive information from unauthorized access.

- **Notifications and Alerts**: Implementing a notification system could remind students of upcoming classes and alert teachers if attendance is not marked in a timely manner.

## Future Improvements

1. **Mobile App Version**: Consider developing a mobile version of the application to make it even more accessible for students to mark attendance on-the-go.

2. **Reporting and Analytics**: Introducing features for teachers to generate attendance reports and analytics could provide valuable insights into class participation and engagement.

3. **Integration with Learning Management Systems (LMS)**: Connecting the app with existing LMS platforms could streamline the attendance process further and integrate attendance data into broader academic performance metrics.

4. **Enhanced Security Measures**: Further security measures could be implemented, such as two-factor authentication for teacher logins and encrypted communications between clients and the server.
