# 🎓 Student Management System

A full-stack Student Management System built using Django, designed to manage students, teachers, classes, subjects, attendance, and marks with proper role-based access control.

---

##  Features

### 👨‍💼 Admin
- Add and manage Classes
- Add and manage Subjects mapped to Classes
- Add and manage Students
- Add and manage Teachers
- Admin dashboard to control the entire system

### 👩‍🏫 Teacher
- Secure login with teacher role
- View students class-wise
- Take attendance based on Class and Subject
- Attendance can be taken only once per day
- Add marks for students exam-wise and subject-wise
- View attendance and marks records

### 👨‍🎓 Student
- Secure login with student role
- View personal attendance records
- View marks for each subject and exam
- Access restricted to own data only

---

## 🛠 Tech Stack

- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap 5
- Database: SQLite
- Authentication: Django Authentication System
- UI: Responsive Bootstrap dashboards

---

## 🗂 Project Structure

student_management/
│
├── accounts/        # Authentication and user roles
├── students/        # Student dashboard and attendance view
├── teachers/        # Teacher dashboard, attendance and marks
├── classes/         # Classes and subjects management
├── templates/       # HTML templates
├── static/          # CSS, JS, Bootstrap
└── manage.py

---

## ⚙️ Installation and Setup

1. Clone the repository
git clone https://github.com/yourusername/student-management-system.git

2. Create a virtual environment
python -m venv env
env\Scripts\activate   (Windows)

3. Install dependencies
pip install django

4. Apply migrations
python manage.py migrate

5. Create superuser
python manage.py createsuperuser

6. Run the server
python manage.py runserver

7. Open in browser
http://127.0.0.1:8000/

---

## 🔐 Role-Based Access Control

Admin   → Full access  
Teacher → Attendance and marks management  
Student → View own attendance and marks  

---

## 📌 Key Highlights

- Role-based dashboards
- Class-wise and subject-wise attendance system
- Exam-wise marks management
- Secure authentication and authorization
- Clean and scalable Django architecture
- Responsive UI using Bootstrap

---

## 👨‍💻 Author

Hemant Kumar Vishwakarma
Aspiring Software Developer | Python | Django

---

⭐ If you find this project useful, give it a star!
