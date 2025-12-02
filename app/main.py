from flask import Flask, jsonify, request
import psycopg2
import os
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "users_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

@app.route("/")
def index():
    return "<h1>Welcome to the DevOps Practice App 🚀</h1>"

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/users", methods=["GET", "POST"])
def users():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        cur.execute("INSERT INTO users (name) VALUES (%s);", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"User '{name}' added"}), 201

    cur.execute("SELECT id, name FROM users;")
    users = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
