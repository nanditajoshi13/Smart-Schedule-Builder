# Smart-Schedule-Builder
A Simple **Flask-based web application** that allows users to **register, set up their preferences. and login**, as of yet, with a clean, modern interface.  
User credentials are stored in a lightweight SQLite database ('users.db'), making it easy to run without extra dependencies.
  
## Features
- User Registration (name, username, password)
- User Login with validation
- Extended setup form for role, working hours, flexible hours, breaks and many more
- Dashboard displaying all saved details dynamically from the database
- Modern, responsive UI (HTML + CSS)
- File-based storage ('users.db')
- Toggle between Register and Login forms
- Built with Python + Flask
- Page redirection from login -> setup -> dashboard

## Tech Stack
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (Fetch API)
- **Database:** SQLite ('users.db')

# Getting Started
**SYSTEM REQUIREMENTS** - Python 3.14+, Flask, Flask-CORS  
1. Copy the Python and HTML files from the repositories into a separate folder.
2. Ensure all files are in the same folder and filenames match the repository.
3. Run **controller.py** to start the server.
4. Open the provided URL in any browser to use the program.

## Upcoming Updates
- Dark mode
- Reminders and notifications
- PostgreSQL support for production use
- Password hashing for security

## Authors
- [Nandita Joshi](https://github.com/nanditajoshi13)
- [Vanshika](https://github.com/Vanshika4705)
