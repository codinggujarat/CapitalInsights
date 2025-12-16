from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import json
import os
import sqlite3
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ------------------ Agents ------------------
from agents.master_agent import MasterAgent
from agents.sales_agent import SalesAgent
from agents.verification_agent import VerificationAgent
from agents.underwriting_agent import UnderwritingAgent
from agents.sanction_letter_agent import SanctionLetterAgent

# ------------------ Mock APIs ------------------
from mock_apis.crm_api import CRMApi
from mock_apis.credit_bureau_api import CreditBureauApi
from mock_apis.offer_mart_api import OfferMartApi

# ------------------ OpenAI Setup ------------------
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in your environment or .env file")

openai.api_key = OPENAI_API_KEY

# ------------------ Flask App ------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# ------------------ Initialize mock APIs ------------------
crm_api = CRMApi()
credit_bureau_api = CreditBureauApi()
offer_mart_api = OfferMartApi()

# ------------------ Initialize agents ------------------
sales_agent = SalesAgent()
verification_agent = VerificationAgent(crm_api)
underwriting_agent = UnderwritingAgent(credit_bureau_api, offer_mart_api)
sanction_letter_agent = SanctionLetterAgent()

master_agent = MasterAgent(
    sales_agent=sales_agent,
    verification_agent=verification_agent,
    underwriting_agent=underwriting_agent,
    sanction_letter_agent=sanction_letter_agent
)

# ------------------ Active sessions ------------------
active_sessions = {}

# ------------------ Routes ------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_sanction_letter/<filename>')
def download_sanction_letter(filename):
    secure_name = secure_filename(filename)
    if not secure_name.endswith('.pdf'):
        return "Invalid file type", 400
    filepath = os.path.join('sanction_letters', secure_name)
    if not os.path.exists(filepath):
        return "File not found", 404
    return send_file(filepath, as_attachment=True)

# ------------------ SocketIO Events ------------------
@socketio.on('connect')
def handle_connect():
    session_id = str(uuid.uuid4())
    active_sessions[request.sid] = {
        'session_id': session_id,
        'conversation_history': [],
        'customer_data': {},
        'loan_application': {},
        'current_stage': 'initial'
    }
    welcome_message = master_agent.start_conversation()
    emit('bot_message', {
        'message': welcome_message,
        'timestamp': datetime.now().isoformat(),
        'agent': 'Master Agent'
    })

@socketio.on('disconnect')
def handle_disconnect():
    active_sessions.pop(request.sid, None)

@socketio.on('user_message')
def handle_user_message(data):
    if request.sid not in active_sessions:
        return
    session = active_sessions[request.sid]
    user_message = data['message']

    # Add user message to history
    session['conversation_history'].append({
        'type': 'user',
        'message': user_message,
        'timestamp': datetime.now().isoformat()
    })

    # Process via master agent
    response = master_agent.process_message(
        user_message=user_message,
        session_data=session
    )

    # Add bot response to history
    session['conversation_history'].append({
        'type': 'bot',
        'message': response['message'],
        'agent': response['agent'],
        'timestamp': datetime.now().isoformat()
    })

    # Update session with any updates
    session.update(response.get('session_updates', {}))

    emit('bot_message', {
        'message': response['message'],
        'timestamp': datetime.now().isoformat(),
        'agent': response['agent'],
        'requires_upload': response.get('requires_upload', False),
        'loan_approved': response.get('loan_approved', False),
        'sanction_letter_url': response.get('sanction_letter_url')
    })

@socketio.on('file_upload')
def handle_file_upload(data):
    if request.sid not in active_sessions:
        return
    session = active_sessions[request.sid]
    file_data = data['file_data']
    file_type = data['file_type']

    # Process file through underwriting agent
    response = underwriting_agent.process_salary_slip(file_data, file_type, session)

    # Update session
    session.update(response.get('session_updates', {}))

    # Check if loan was approved and we should move to sanction letter stage
    if response.get('session_updates', {}).get('current_stage') == 'sanction_letter':
        # Generate sanction letter immediately
        sanction_response = sanction_letter_agent.generate_sanction_letter(session)
        # Update session with sanction letter updates
        session.update(sanction_response.get('session_updates', {}))
        
        emit('bot_message', {
            'message': sanction_response['message'],
            'timestamp': datetime.now().isoformat(),
            'agent': sanction_response['agent'],
            'loan_approved': sanction_response.get('loan_approved', False),
            'sanction_letter_url': sanction_response.get('sanction_letter_url')
        })
    else:
        emit('bot_message', {
            'message': response['message'],W
            'timestamp': datetime.now().isoformat(),
            'agent': 'Underwriting Agent',
            'loan_approved': response.get('loan_approved', False),
            'sanction_letter_url': response.get('sanction_letter_url')
        })

# ------------------ Main ------------------
if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('sanction_letters', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('agents', exist_ok=True)
    os.makedirs('mock_apis', exist_ok=True)

    # Initialize database
    crm_api.initialize_database()

    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, log_output=False)
