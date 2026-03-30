# eCommerce_project

## Requirements:

- Python 3.12.3
- PostgreSQL
- Redis
- Dependencies from requirements.txt

## Installation:

1. Clone repo with (bash):

git clone https://github.com/JovanBV/eCommerce_project.git
cd eCommerce_project

2. Create virtual environment:

**Linux (bash inside "/ecommerce_project"):**

python3 -m venv venv
source venv/bin/activate
cd eCommerce_project

**Windows (bash inside):**

python3 -m venv venv
venv\Scripts\activate

3. Install dependencies (bash):

pip install -r requirements.txt

## Configuration:

1. Copy the example environment file:

cp .env.example .env

2. Edit .env with your actual credentials:
   - Database connection string
   - Redis host, port, and password
   - JWT key paths

3. Generate JWT keys:

mkdir keys
ssh-keygen -t rsa -b 4096 -m PEM -f keys/private_key.pem -N ""
openssl rsa -in keys/private_key.pem -pubout -outform PEM -out keys/public_key.pem

4. Database setup:
   - Create your PostgreSQL database
   - Tables configuration is available in ecommerce_project/services/db_manager.py
   - Tables will be created automatically on first run

## Execution:

To execute app run (bash):

python3 app.py

To stop, press CTRL+C

## Access to API:

- Base URL: http://localhost:5000
- Available on port 5000

## Initializing the project

You only need to execute the file app.py for it to start, it will insert some key info in the database for the system to work.

Here is the info for the main user, it will allow you to log in with privilege permissions:

{
"email": "admin@project.com",
"name": "Admin",
"password": "Admin123!"
}

## Security Notes

- Never commit .env or keys/ folder to version control
- Change the default admin credentials after first login
- Keep your JWT keys secure
- Use strong passwords for database and Redis in production
