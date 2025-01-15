# Library Management System

## Overview
The **Library Management System** is a web-based application designed to make library operations seamless and efficient for both librarians and users. This system allows users to borrow and return books, while librarians can manage books, users, and track overdue records. The application provides a user-friendly interface with real-time updates and data integrity.

---

## Team Members - Team 7
- **Abhishek Hosmani** - Project Head [https://github.com/ABHI10-GT3]
- **Harshita Purohit** - Feature Implementation [https://github.com/purohitharshita]
- **Ifrah Naaz** - Feature Implementation [https://github.com/ifrahnz26]
- **Joshua Leo** - Reviewer [https://github.com/Joshualeo257]
- **Nandita Nayak** - Documentation Head [https://github.com/NanditaNayakk]

---

## Features
### User Features:
- **Borrow Books**: Browse and borrow available books.
- **Return Books**: Return borrowed books with ease.
- **View Borrowed Books**: Keep track of borrowed books and due dates.

### Librarian Features:
- **Manage Books**: Add, update, or remove books from the library.
- **Manage Users**: View user details and their current borrowed books.
- **Overdue Tracking**: Monitor overdue books and send reminders.

---

## Screenshots
<img src="https://github.com/user-attachments/assets/a42a5b69-b148-43eb-a341-f729f870c57c" alt="Example Image" style="width:400px; height:250px;">
<img src="https://github.com/user-attachments/assets/99c3442b-a9f5-4bd6-8969-ecee8efda245" alt="Example Image" style="width:400px; height:250px;">
<img src="https://github.com/user-attachments/assets/1c9e8272-2da7-43f0-bc33-e54d5c454bbf" alt="Example Image" style="width:400px; height:250px;">
<img src="https://github.com/user-attachments/assets/ae78744a-f672-41a9-8bf4-08a57e860bfc" alt="Example Image" style="width:400px; height:250px;">
<img src="https://github.com/user-attachments/assets/8bef4895-1f04-4216-b007-32bc7454e1b5" alt="Example Image" style="width:400px; height:250px;">
<img src="https://github.com/user-attachments/assets/0e62ff14-78f9-42a2-aa5c-07a97455e629" alt="Example Image" style="width:400px; height:250px;">

---

## Technologies Used
- **Frontend**: HTML, CSS
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Tools**: Virtual Environment (venv), VS Code
- **Deployment**: Localhost

---

## Installation

### Prerequisites:
- Python 3.10 or higher
- MySQL installed and running
- A code editor (e.g., VS Code)

### Steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/ABHI10-GT3/Library-Management-System.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd library-management-system
   ```

3. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

5. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up the database**:
   - Create a MySQL database and note down the credentials.
   - Update the `.env` file with the database details:
     ```env
     DB_HOST=localhost
     DB_USER=your_username
     DB_PASSWORD=your_password
     DB_NAME=library_db
     ```
   - Run the SQL schema file provided in the project root directory to initialize the database:
     ```bash
     mysql -u your_username -p < database_setup.sql
     ```

7. **Run the application**:
   ```bash
   python app.py
   ```

8. **Access the application**:
   - Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage
1. **User Login**:
   - Users can log in to borrow, return, and track their books.
2. **Librarian Dashboard**:
   - Librarians can log in to manage books, track overdue books, and manage users.

---

## File Structure
```
library-management-system/
│
├── app.py                 # Main Flask application
├── templates/             # HTML templates for the frontend
├── static/                # Static files (CSS, images)
├── database_setup.sql     # Database schema
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
├── CONTRIBUTING.md        # Contribution guidelines
├── CODE_OF_CONDUCT.md     # Code of conduct
└── LICENSE                # License information
```

---

## Contributing
We welcome contributions! Please refer to the `CONTRIBUTING.md` file for detailed guidelines.

---

## License
This project is licensed under the MIT License.

---
