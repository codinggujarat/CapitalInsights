import json
from gemini_client import get_agent_response

class SalesAgent:
    """
    Sales Agent - Handles loan negotiations, discusses customer needs, and collects information
    """
    
    def __init__(self):
        self.required_info = ['name', 'phone', 'email', 'city', 'monthly_income', 'loan_amount', 'loan_purpose']
    
    def handle_sales_conversation(self, user_message, session_data, intent_data):
        """
        Handle sales conversation and persuade customer
        """
        customer_data = session_data.get('customer_data', {})
        
        # Extract any information from this conversation FIRST
        extracted_info = self._extract_information(user_message, customer_data)
        if extracted_info:
            customer_data.update(extracted_info)
        
        # Check if we have enough info to proceed
        if self._has_basic_info(customer_data):
            return {
                'message': ("Perfect! I have all the information I need. Let me verify your details "
                           "and check your eligibility for our best rates. This will just take a moment..."),
                'agent': 'Sales Agent',
                'session_updates': {
                    'current_stage': 'verification',
                    'customer_data': customer_data
                }
            }
        
        # Generate personalized sales response
        system_prompt = f"""You are a friendly and persuasive personal loan sales agent for Tata Capital.
        Your goal is to convince the customer to take a personal loan and collect their information.
        
        Customer data collected so far: {json.dumps(customer_data)}
        User intent: {intent_data.get('intent', 'inquiry')}
        
        Guidelines:
        - Be conversational and helpful
        - Highlight benefits: competitive rates, quick approval, flexible terms
        - Address any concerns naturally
        - Gradually collect missing information: name, phone, email, city, monthly income, loan amount, purpose
        - Don't ask for all information at once
        - Be persuasive but not pushy
        - If they show interest, start collecting personal details
        - DO NOT ask for information that is already provided in the customer data
        
        Respond in a single paragraph, naturally guiding them toward providing information."""
        
        response = get_agent_response(system_prompt, user_message)
        
        # Check if we have enough info to proceed to collection stage
        missing_info = [field for field in self.required_info if field not in customer_data]
        
        if len(missing_info) <= 3:  # Move to structured collection when most info is available
            next_stage = 'collect_personal_info'
        else:
            next_stage = 'sales_pitch'
        
        return {
            'message': response,
            'agent': 'Sales Agent',
            'session_updates': {
                'current_stage': next_stage,
                'customer_data': customer_data
            }
        }
    
    def collect_personal_information(self, user_message, session_data):
        """
        Collect personal information from customer
        """
        customer_data = session_data.get('customer_data', {})
        
        # Extract information from user message
        extracted_info = self._extract_information(user_message, customer_data)
        customer_data.update(extracted_info)
        
        # Check what information we still need
        missing_info = [field for field in self.required_info if field not in customer_data]
        
        if not missing_info:
            # All information collected, move to verification
            return {
                'message': ("Excellent! I have all your details. Let me quickly verify your information "
                           "in our system and check your pre-approved loan offers..."),
                'agent': 'Sales Agent',
                'session_updates': {
                    'customer_data': customer_data,
                    'current_stage': 'verification'
                }
            }
        
        # Ask for next piece of missing information
        next_question = self._get_next_question(missing_info[0])
        
        return {
            'message': next_question,
            'agent': 'Sales Agent',
            'session_updates': {'customer_data': customer_data}
        }
    
    def _has_basic_info(self, customer_data):
        """Check if we have basic required information"""
        return all(field in customer_data for field in self.required_info)
    
    def _extract_information(self, user_message, existing_data):
        """Extract information from user message using AI"""
        system_prompt = f"""Extract personal information from the user's message.
        Current data: {json.dumps(existing_data)}
        
        Look for: name, phone, email, city, monthly_income (as number), loan_amount (as number), loan_purpose
        
        Respond with JSON containing only the new information found:
        {{"field_name": "value"}}
        
        For numbers, extract only the numeric value. For loan_purpose, use categories like: 
        home_improvement, debt_consolidation, medical, education, business, personal, wedding, travel
        
        IMPORTANT: Only extract information that is clearly stated in the user message. Do not make assumptions.
        If no new information is found, return an empty JSON object {{}}"""
        
        try:
            response = get_agent_response(system_prompt, user_message, response_format="json")
            if response:
                # Parse the JSON response
                extracted_data = json.loads(response)
                
                # Clean up the extracted data
                cleaned_data = {}
                for key, value in extracted_data.items():
                    if key in ['monthly_income', 'loan_amount']:
                        # Ensure numeric values are integers
                        try:
                            cleaned_data[key] = int(value)
                        except (ValueError, TypeError):
                            # If conversion fails, keep original value
                            cleaned_data[key] = value
                    elif key == 'phone':
                        # Clean phone numbers (remove spaces, dashes, etc.)
                        if isinstance(value, str):
                            cleaned_data[key] = ''.join(filter(str.isdigit, value))
                        else:
                            cleaned_data[key] = value
                    else:
                        cleaned_data[key] = value
                
                return cleaned_data
            else:
                return {}
        except Exception as e:
            # Return empty dict on any error
            return {}
    
    def _get_next_question(self, field):
        """Get appropriate question for missing field"""
        questions = {
            'name': "Great! Could you please tell me your full name?",
            'phone': "Perfect! What's the best phone number to reach you at?",
            'email': "And your email address for our records?",
            'city': "Which city are you currently residing in?",
            'monthly_income': "To find the best loan options for you, what's your approximate monthly income?",
            'loan_amount': "How much would you like to borrow? We offer loans from ₹50,000 to ₹40 lakhs.",
            'loan_purpose': "What will you be using this loan for? This helps us tailor the best terms for you."
        }
        return questions.get(field, "Could you provide more details about your requirements?")