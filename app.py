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

