# Context-Aware Encrypted File Sharing System
SecureShare AES is a file sharing system designed with both security and control in mind. Instead of just storing files safely, it also focuses on controlling who can access them, when they can access them, and how many times they can download them.

All files are encrypted before being stored, and they are only decrypted when a user meets specific access conditions like role, time window, and download limits. The goal of this project is to combine encryption with real-time access decision-making.

## Features

### Security
* AES-256 encryption is applied before storing any file
* Each file uses a unique initialization vector (IV)
* No original files are stored in plaintext
* A central encryption key is used for secure processing
### Context-Aware Access Control
* Role-based access control (Admin, User, Viewer)
* Time-based restrictions (for example, access only during certain hours)
* Download limits for each file
* All rules are checked dynamically during every access request
### Logging and Monitoring
* Every access attempt is logged
* Both successful and denied requests are recorded
* Reasons for denial are stored for transparency
* Helps in tracking user activity and auditing
### Interface
* Clean and simple dark-themed UI
* Responsive design for different devices
* Drag-and-drop file upload
* Real-time preview of access rules while uploading

## System Architecture
The system consists of a client interface connected to a Flask backend.
The Flask application handles routes, templates, and static files. The backend is supported by:
* SQLite database for storing users, files, rules, and logs
* Encrypted file storage where files are saved in encrypted format
* A context engine that checks role, time, and download limits

## Getting Started
### Prerequisites
* Python 3.8 or above
* pip
### Installation
1. Clone the repository git clone https://github.com/YOUR_USERNAME/secureshare-aes.git cd secureshare-aes
2. Create a virtual environment python -m venv venv
3. Activate the environment --  Windows: venv\Scripts\activate Linux/ | Mac: source venv/bin/activate
4. Install dependencies pip install -r requirements.txt
5. Initialize the database python init_db.py
6. Run the application python app.py
7. Open in browser  http://localhost:5000

## Project Structure
The project is organized into the following main components:
* app.py – main Flask application
* init_db.py – database setup script
* utils/ – encryption and logging logic
* templates/ – HTML pages
* static/ – CSS and JavaScript files

## Access Control
### Roles
*Admin*
* Can upload files
* Can download all files
* Can view logs

*User*
* Can upload files
* Can download their own files
* Can download others' files if permitted

*Viewer*
* Cannot upload
* Can only download if access is granted

### During Upload
When uploading a file, the following can be configured:
* Allowed role
* Start and end time
* Maximum download count

### Access Logic
A file can be accessed only if:
* The user’s role matches the allowed role
* The current time falls within the defined time range
* The download limit has not been exceeded
All conditions must be satisfied for access to be granted.

## Security Design
### Upload Process
The file is taken from the user, encrypted using AES-256, and then stored as an encrypted file.
### Download Process
When a request is made:
* The system checks all access conditions
* If allowed, the file is decrypted temporarily
* The file is sent to the user
* The temporary decrypted file is deleted afterward

## Database Schema
The system uses four main tables:
### Users
* Stores username, password, and role
### Files
* Stores file metadata and encrypted file path
### Access Control
* Stores rules like role, time window, and download limits
### Access Logs
* Stores logs of all access attempts with status and reason

## Use Cases
* Secure document sharing within organizations
* Controlled file access for teams
* Temporary access for external users
* One-time downloads using limited access rules

## Testing
* Create users with different roles
* Upload files with specific rules
* Try accessing files using different roles
* Check logs to verify correct behavior

## Troubleshooting
### Database issues
* Re-run the database initialization script
### File access issues
* Check permissions of storage folders
### Encryption errors
* Verify that the encryption key is consistent
### Files not visible
* Check database entries
