from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
import datetime
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'super-secret-skillify-key'

# Normally you'd connect to a real MongoDB URI:
# client = MongoClient("mongodb://localhost:27017/")
# db = client.skillify_db

# Mock DB for demonstration (In-memory dicts instead of MongoDB instances, 
# but styled to represent the schema as requested for working code without needing a mongo instance locally)
# If Mongo is available, simply switch the client.
class MockDB:
    def __init__(self):
        self.notifications = []
        
    def insert_notification(self, doc):
        doc['_id'] = str(ObjectId())
        self.notifications.append(doc)
        return doc['_id']

    def fetch_user_notifications(self, user_id):
        return sorted([n for n in self.notifications if n['user_id'] == user_id], 
                      key=lambda x: x['timestamp'], reverse=True)

    def mark_read(self, n_id):
        for n in self.notifications:
            if n['_id'] == n_id:
                n['read_status'] = True

    def clear_all(self, user_id):
        self.notifications = [n for n in self.notifications if n['user_id'] != user_id]

db = MockDB()

# Seed a user session for testing
@app.before_request
def mock_login():
    if 'user_id' not in session:
        session['user_id'] = 'user_123'
        session['user_name'] = 'Alex'

@app.route('/')
def home():
    return render_template('dashboard.html', user={'name': session.get('user_name')})

# HTML views
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user={'name': session.get('user_name')})

import smtplib
from email.message import EmailMessage

def send_email_notification(user_email, message):
    """
    Optional SMTP email notification.
    Requires configuring SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, etc.
    """
    try:
        # msg = EmailMessage()
        # msg.set_content(message)
        # msg['Subject'] = 'New Skillify Notification'
        # msg['From'] = 'notify@skillify.com'
        # msg['To'] = user_email
        # server = smtplib.SMTP('smtp.example.com', 587)
        # server.starttls()
        # server.login('user', 'password')
        # server.send_message(msg)
        # server.quit()
        print(f"SMTP Mock: Email would be sent to {user_email}: {message}")
    except Exception as e:
        print("SMTP Error:", e)

# API Routes
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    notifs = db.fetch_user_notifications(user_id)
    return jsonify({'notifications': notifs})

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    """ Trigger event manually (for demonstration) """
    data = request.json
    types = ['session', 'feedback', 'system']
    ntype = data.get('type', 'system')
    if ntype not in types:
        ntype = 'system'
        
    doc = {
        'user_id': data.get('user_id', session.get('user_id')),
        'message': data.get('message', 'A new event occurred!'),
        'type': ntype,
        'read_status': False,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    
    db.insert_notification(doc)
    
    # Trigger Optional Email Notification using smtp
    send_email_notification('user@example.com', doc['message'])
    
    return jsonify({'status': 'success', 'notification': doc}), 201

@app.route('/api/notifications/<notif_id>/read', methods=['POST'])
def mark_notification_read(notif_id):
    user_id = session.get('user_id')
    db.mark_read(notif_id)
    return jsonify({'status': 'success'})

@app.route('/api/notifications/clear', methods=['POST'])
def clear_notifications():
    user_id = session.get('user_id')
    db.clear_all(user_id)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Initial seeding test data
    db.insert_notification({
        'user_id': 'user_123',
        'message': 'Session request received for Advanced React',
        'type': 'session',
        'read_status': False,
        'timestamp': (datetime.datetime.utcnow() - datetime.timedelta(minutes=2)).isoformat() + 'Z'
    })
    app.run(debug=True, port=5000)
