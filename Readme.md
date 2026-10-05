Python Flask
Here is a complete, production-ready Docker Compose sample project for a Python Flask application connected to a PostgreSQL database.
1. Project Directory Structure
Create a new directory on your machine and set up the following files:
text
my-flask-app/
├── compose.yaml
├── Dockerfile
├── requirements.txt
├── app.py
└── templates/
    └── index.html
Use code with caution.
________________________________________
2. Sample Project Files
requirements.txt (Python dependencies)
text
Flask==3.0.3
psycopg2-binary==2.9.9
Use code with caution.
app.py (Flask application core logic)
python
import os
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    # Connects using the service name 'database' defined in compose.yaml
    conn = psycopg2.connect(
        host='database',
        database=os.environ.get('POSTGRES_DB', 'my_database'),
        user=os.environ.get('POSTGRES_USER', 'admin'),
        password=os.environ.get('POSTGRES_PASSWORD', 'secret_password')
    )
    return conn

@app.route('/')
def index():
    db_status = "Disconnected"
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        db_status = f"Connected! PostgreSQL Version: {db_version[0]}"
        cur.close()
        conn.close()
    except Exception as e:
        db_status = f"Connection failed: {str(e)}"

    return render_template('index.html', db_status=db_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
Use code with caution.
templates/index.html (Frontend UI template)
html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Docker Compose Sample</title>
</head>
<body>
    <h1>Hello from Flask inside Docker!</h1>
    <p><strong>Database Status:</strong> {{ db_status }}</p>
</body>
</html>
Use code with caution.
Dockerfile (Instructions for building the Flask container)
dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for compiling certain packages if necessary
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
Use code with caution.
compose.yaml (Orchestrates the Flask application and the PostgreSQL database)
yaml
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - POSTGRES_DB=my_database
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret_password
    volumes:
      - .:/app
    depends_on:
      database:
        condition: service_healthy

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=my_database
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d my_database"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
Use code with caution.
________________________________________
3. Workflow & Commands to Run This Stack
Navigate to your my-flask-app/ directory in the terminal and use these commands:
•	docker compose up --build -d – Builds your local Flask image for the first time (or rebuilds if you change requirements.txt/Dockerfile) and launches both services in the background.
•	Access the App – Open your web browser and go to http://localhost:5000. You should see the welcome page stating that it successfully connected to the PostgreSQL database.
•	Hot-Reloading – Because of the volume mapping (.:/app) in the configuration, you can modify app.py or index.html locally on your computer, and the changes will refresh instantly inside the container without requiring a rebuild!
•	docker compose exec web python -m unittest – Runs tests inside your active Python environment.
•	docker compose down -v – Destroys the infrastructure and cleans up the persistent database volume when you are finished.
________________________________________

