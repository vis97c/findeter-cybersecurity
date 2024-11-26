import os
from flask import Flask, request, render_template, jsonify, redirect, session
from middleware import Middleware
from utils.storage import RequestsStorageManager, ClassificationsStorageManager

# INIT APP
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
Middleware(app) # Check for malicious requests before loading the endpoint/page

# GET LOGS
request_log_manager = RequestsStorageManager()
classification_manager = ClassificationsStorageManager()

# ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'): return redirect('/')

    return render_template('admin.html')

# REST API

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid payload. Username and password are required."}), 400

    username = data['username']
    password = data['password']

    if username == "admin" and password == "insecure_password":
        session['logged_in'] = True
        return jsonify({"data": True, "message": "Login successful!"}), 200
    else:
        return jsonify({"data": None, "error": "Invalid username or password."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()

    return jsonify({"data": True, "message": "Logged out successfully!"}), 200

# Get unclassified logs
@app.route('/logs/unclassified', methods=['GET'])
def get_unclassified_logs():
    if not session.get('logged_in'): return jsonify({"data": None, "error": "Unauthorized"}), 401
    
    unclassified_logs = classification_manager.get_unclassified_logs()

    return jsonify(unclassified_logs), 200

# Classify log
@app.route('/logs/classify', methods=['POST'])
def classify_log():
    if not session.get('logged_in'): return jsonify({"data": None, "error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or 'request' not in data or 'is_safe' not in data:
        return jsonify({"data": None, "error": "Invalid payload. 'request' and 'is_safe' are required."}), 400

    classification_manager.save({
        "request": data['request'],
        "is_safe": data['is_safe']
    })

    return jsonify({"data": True, "message": "Classification saved successfully."}), 200
