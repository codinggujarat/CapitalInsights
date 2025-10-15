import json
import random
from openai_client import get_agent_response

class UnderwritingAgent:
    """
    Underwriting Agent - Handles credit scoring and eligibility validation
    """
    
    def __init__(self, credit_bureau_api, offer_mart_api):
        self.credit_bureau_api = credit_bureau_api
        self.offer_mart_api = offer_mart_api
    
    def process_application(self, session_data):
        """
        Process loan application through underwriting logic
        """
        customer_data = session_data.get('customer_data', {})
        
        # Get credit score
        credit_score = self.credit_bureau_api.get_credit_score(customer_data.get('phone'))
        
        # Get pre-approved offer
        offer = self.offer_mart_api.get_offer(customer_data)
        
        # Apply underwriting logic with error handling
        try:
            loan_amount = int(customer_data.get('loan_amount', 0))
        except (ValueError, TypeError):
            loan_amount = 0
            
        try:
            monthly_income = int(customer_data.get('monthly_income', 0))
        except (ValueError, TypeError):
            monthly_income = 0
            
        pre_approved_limit = offer.get('pre_approved_limit', 0)
        
        # Store credit and offer data
        session_data['credit_score'] = credit_score
        session_data['offer_details'] = offer
        session_data['loan_application'] = {
            'requested_amount': loan_amount,
            'pre_approved_limit': pre_approved_limit,
            'credit_score': credit_score
        }
        
        # Underwriting decision logic
        if credit_score < 700:
            return self._reject_application("credit_score", session_data)
        
        if loan_amount <= pre_approved_limit:
            return self._approve_instantly(session_data)
        
        elif loan_amount <= (2 * pre_approved_limit):
            return self._request_salary_slip(session_data)
        
        else:
            return self._reject_application("amount_too_high", session_data)
    
    def process_salary_slip(self, file_data, file_type, session_data):
        """
        Process uploaded salary slip and make final decision
        """
        customer_data = session_data.get('customer_data', {})
        loan_amount = int(customer_data.get('loan_amount', 0))
        monthly_income = int(customer_data.get('monthly_income', 0))
        
        # Simulate salary slip processing
        # In real scenario, this would use OCR and document analysis
        extracted_salary = self._extract_salary_from_slip(file_data, monthly_income)
        
        # Calculate EMI (simplified calculation)
        interest_rate = 0.12  # 12% annual
        tenure_months = 36  # 3 years default
        monthly_emi = self._calculate_emi(loan_amount, interest_rate, tenure_months)
        
        # Check if EMI is <= 50% of salary
        emi_ratio = monthly_emi / extracted_salary
        
        if emi_ratio <= 0.5:
            return self._approve_with_documents(session_data, monthly_emi, tenure_months)
        else:
            return self._reject_application("high_emi_ratio", session_data)
    
    def _approve_instantly(self, session_data):
        """Approve loan instantly"""
        return {
            'message': ("Congratulations! Your loan has been instantly approved! "
                       "Based on your excellent credit profile and our relationship, "
                       "we're pleased to offer you the requested amount at our best rates. "
                       "Let me generate your sanction letter now..."),
            'agent': 'Underwriting Agent',
            'session_updates': {
                'current_stage': 'sanction_letter',
                'approval_status': 'approved',
                'approval_type': 'instant'
            }
        }
    
    def _request_salary_slip(self, session_data):
        """Request salary slip for verification"""
        return {
            'message': ("Your application looks promising! To approve the requested amount, "
                       "I need to verify your income. Please upload your latest salary slip "
                       "or income proof, and I'll process your application immediately."),
            'agent': 'Underwriting Agent',
            'requires_upload': True,
            'session_updates': {'current_stage': 'document_upload'}
        }
    
    def _approve_with_documents(self, session_data, monthly_emi, tenure_months):
        """Approve after document verification"""
        return {
            'message': (f"Excellent! Your salary slip has been verified. Your loan of "
                       f"₹{session_data['customer_data']['loan_amount']:,} is approved! "
                       f"Your EMI will be ₹{monthly_emi:,.0f} for {tenure_months} months. "
                       f"Let me generate your sanction letter..."),
            'agent': 'Underwriting Agent',
            'session_updates': {
                'current_stage': 'sanction_letter',
                'approval_status': 'approved',
                'approval_type': 'document_verified',
                'emi_details': {'monthly_emi': monthly_emi, 'tenure_months': tenure_months}
            }
        }
    
    def _reject_application(self, reason, session_data):
        """Reject application with reason"""
        rejection_messages = {
            'credit_score': ("I appreciate your interest in our personal loan. Unfortunately, "
                           "based on current credit bureau information, we're unable to approve "
                           "your application at this time. We'd be happy to reconsider in the future "
                           "as your credit profile improves."),
            'amount_too_high': ("Thank you for considering us for your loan needs. The requested amount "
                              "exceeds our current lending criteria for your profile. We'd be happy to "
                              "discuss a smaller loan amount that fits your eligibility."),
            'high_emi_ratio': ("Thank you for providing your income documentation. While we appreciate "
                             "your application, the EMI for the requested amount would exceed our "
                             "comfortable lending ratio. We'd be glad to discuss a smaller loan amount.")
        }
        
        return {
            'message': rejection_messages.get(reason, "We're unable to approve your application at this time."),
            'agent': 'Underwriting Agent',
            'session_updates': {
                'current_stage': 'rejected',
                'approval_status': 'rejected',
                'rejection_reason': reason
            }
        }
    
    def _extract_salary_from_slip(self, file_data, declared_income):
        """Simulate salary extraction from uploaded slip"""
        # In real scenario, this would use OCR and NLP
        # For simulation, we'll use declared income with some variance
        variance = random.uniform(0.9, 1.1)
        return int(declared_income * variance)
    
    def _calculate_emi(self, principal, annual_rate, months):
        """Calculate EMI using standard formula"""
        monthly_rate = annual_rate / 12
        emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
        return emi