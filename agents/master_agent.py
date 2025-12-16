import json
from gemini_client import get_agent_response, analyze_conversation_intent

class MasterAgent:
    """
    Master Agent - Main orchestrator that manages conversation flow and coordinates worker agents
    """
    
    def __init__(self, sales_agent, verification_agent, underwriting_agent, sanction_letter_agent):
        self.sales_agent = sales_agent
        self.verification_agent = verification_agent
        self.underwriting_agent = underwriting_agent
        self.sanction_letter_agent = sanction_letter_agent
        
        self.conversation_stages = {
            'initial': 'greeting_and_interest',
            'greeting_and_interest': 'sales_pitch',
            'sales_pitch': 'collect_personal_info',
            'collect_personal_info': 'verification',
            'verification': 'underwriting',
            'underwriting': 'sanction_letter',
            'sanction_letter': 'completed',
            'rejected': 'completed'
        }
    
    def start_conversation(self):
        """Start the conversation with a welcome message"""
        return ("Hello! Welcome to Tata Capital Personal Loans. I'm here to help you find the perfect "
                "personal loan solution for your needs. Whether you're looking to consolidate debt, "
                "fund a major purchase, or cover unexpected expenses, we have competitive rates and "
                "flexible terms. How can I assist you today?")
    
    def process_message(self, user_message, session_data):
        """
        Process user message and coordinate with appropriate worker agents
        """
        current_stage = session_data.get('current_stage', 'initial')
        conversation_history = session_data.get('conversation_history', [])
        
        # Analyze user intent
        try:
            intent_analysis = analyze_conversation_intent(conversation_history, user_message)
            if intent_analysis:
                intent_data = json.loads(intent_analysis)
            else:
                intent_data = {"intent": "inquiry", "next_action": "sales_pitch"}
        except:
            intent_data = {"intent": "inquiry", "next_action": "sales_pitch"}
        
        # Route to appropriate agent based on stage and intent
        if current_stage in ['initial', 'greeting_and_interest']:
            return self._handle_initial_stage(user_message, session_data, intent_data)
        elif current_stage == 'sales_pitch':
            return self.sales_agent.handle_sales_conversation(user_message, session_data, intent_data)
        elif current_stage == 'collect_personal_info':
            return self.sales_agent.collect_personal_information(user_message, session_data)
        elif current_stage == 'verification':
            return self.verification_agent.verify_customer(session_data)
        elif current_stage == 'underwriting':
            return self.underwriting_agent.process_application(session_data)
        elif current_stage == 'document_upload':
            return self._handle_document_stage(user_message, session_data)
        elif current_stage == 'sanction_letter':
            return self.sanction_letter_agent.generate_sanction_letter(session_data)
        else:
            return {
                'message': "Thank you for your interest in our personal loan services. Have a great day!",
                'agent': 'Master Agent',
                'session_updates': {'current_stage': 'completed'}
            }
    
    def _handle_initial_stage(self, user_message, session_data, intent_data):
        """Handle initial conversation and move to sales pitch"""
        # Extract information even in initial stage
        customer_data = session_data.get('customer_data', {})
        
        if any(word in user_message.lower() for word in ['loan', 'money', 'borrow', 'finance', 'need', 'help']):
            session_data['current_stage'] = 'sales_pitch'
            return self.sales_agent.handle_sales_conversation(user_message, session_data, intent_data)
        else:
            return {
                'message': ("I understand you might be exploring financial options. Personal loans can be a great "
                           "solution for various needs - from home improvements to debt consolidation or unexpected "
                           "expenses. Would you like to know more about our personal loan offerings and see if "
                           "you qualify for pre-approved rates?"),
                'agent': 'Master Agent',
                'session_updates': {'current_stage': 'greeting_and_interest'}
            }
    
    def _handle_document_stage(self, user_message, session_data):
        """Handle document upload stage"""
        return {
            'message': ("Please upload your latest salary slip so we can finalize your loan application. "
                       "This helps us verify your income and complete the approval process."),
            'agent': 'Master Agent',
            'requires_upload': True,
            'session_updates': {}
        }