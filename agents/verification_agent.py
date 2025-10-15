import json
from openai_client import get_agent_response

class VerificationAgent:
    """
    Verification Agent - Confirms KYC details from CRM server
    """
    
    def __init__(self, crm_api):
        self.crm_api = crm_api
    
    def verify_customer(self, session_data):
        """
        Verify customer KYC details against CRM database
        """
        customer_data = session_data.get('customer_data', {})
        
        # Verify with CRM
        verification_result = self.crm_api.verify_customer(customer_data)
        
        if verification_result['verified']:
            # Customer found in CRM, update with additional data
            customer_data.update(verification_result['customer_details'])
            
            return {
                'message': (f"Great news! I've verified your details in our system. "
                           f"I can see you're an existing customer with us. "
                           f"Let me now check your eligibility and pre-approved loan offers..."),
                'agent': 'Verification Agent',
                'session_updates': {
                    'customer_data': customer_data,
                    'verification_status': 'verified',
                    'current_stage': 'underwriting'
                }
            }
        else:
            # New customer, proceed with verification
            # In real scenario, this would trigger KYC process
            return {
                'message': ("I don't see you as an existing customer, but that's perfectly fine! "
                           "As a new customer, you're eligible for our special introductory rates. "
                           "Let me check your eligibility and loan options..."),
                'agent': 'Verification Agent',
                'session_updates': {
                    'customer_data': customer_data,
                    'verification_status': 'new_customer',
                    'current_stage': 'underwriting'
                }
            }