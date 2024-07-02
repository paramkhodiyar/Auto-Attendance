## Auto-Attendance ( Concept )

Concept Overview

This project aims to develop a secure and efficient automatic attendance system that eliminates the possibility of proxy attendance. The system leverages the following components:

Android App (Student Side):

Login using unique student credentials provided by the institution.
QR code scanner to register attendance during class sessions.
Secure storage of student login details within the app.


Web Application (Teacher Side):

Secure login for authorized teachers.
Interface to enter class code and date.
Button to generate a unique QR code for each class session.
Option to view and manage attendance records (optional, depending on implementation).


SQL Database:

Stores student login credentials for authentication.
Houses a table structure to record attendance data for each class (student ID, class code, date, start time, end time).
Enforces data integrity and security measures.


Benefits

Reduced Proxy Attendance: Students cannot mark attendance for absent peers as login details are unique and non-transferable.
Improved Efficiency: Streamlined attendance recording process eliminates manual roll calls, saving time and effort for teachers and students.
Enhanced Data Accuracy: Real-time attendance data ensures reliable and accurate records.
Scalability: The system can accommodate a large number of students and courses.

Future Implementation Considerations

Security
Android App Development
Web Application Development
Data Synchronization
Geolocation Integration
