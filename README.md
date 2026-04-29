# Hproject – Team Registry Portal

This project is a Django-based web application developed as part of a group coursework at the University of Westminster. The system replaces a spreadsheet-based team registry with a database-driven web portal that allows users to view, search, and manage organisational team information.

---

## Features
- User authentication (login, logout, password reset)
- Teams directory with search functionality
- Team detail pages (members, repositories, dependencies)
- Email team functionality
- Meeting scheduling
- Organisation and department structure
- Data visualisation
- Reports and export functionality
- Admin dashboard for managing system data

---

## Technologies Used
- Python (Django)
- SQLite (database)
- HTML, CSS, Bootstrap
- JavaScript (basic interactivity)

---

## How to Run the Project
1. Clone the repository:
   git clone <REPO_LINK>

2. Navigate to the backend folder:
   cd Hproject-backend

3. Create a virtual environment:
   python -m venv venv

4. Activate the virtual environment:
   venv\Scripts\activate

5. Install dependencies:
   pip install django django-cors-headers openpyxl

6. Apply migrations:
   python manage.py migrate

7. Run the development server:
   python manage.py runserver

8. Open in browser

---

## Test Accounts
Admin Account:
Username: <ADMIN_USERNAME>
Password: <ADMIN_PASSWORD>

Standard User:
Username: <USER_USERNAME>
Password: <USER_PASSWORD>

---

## Project Structure
accounts/ – authentication and user management  
teams/ – team directory, detail pages, email, scheduling  
organisation/ – departments and organisational structure  
schedule/ – meeting features  
datavis/ – data visualisation  
reports/ – reporting and export  
templates/ – shared frontend templates  
static/ – CSS and static files  

---

## Notes
- The database is included for testing purposes  
- No absolute file paths are used  
- The application is designed to run in a development environment  

---