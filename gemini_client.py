import json
import os
import time

# Correct import for Google Generative AI
try:
    import google.generativeai as genai
    from google.generativeai import types
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

# This API key is from Gemini Developer API Key, not vertex AI API Key
if GOOGLE_AI_AVAILABLE:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    # Initialize models
    gemini_flash = genai.GenerativeModel('gemini-2.5-flash')
    gemini_pro = genai.GenerativeModel('gemini-2.5-pro')

def get_agent_response(system_prompt, user_message, context=None, response_format="text"):
    """
    Get response from Gemini for agent interactions
    """
    # If Google AI is not available, fallback to a mock response
    if not GOOGLE_AI_AVAILABLE:
        return "I'm experiencing technical difficulties. Please try again later."
    
    # Combine prompts for Gemini
    full_prompt = f"System: {system_prompt}\n\n"
    if context:
        full_prompt += f"Context: {context}\n\n"
    full_prompt += f"User: {user_message}\n\nAssistant:"
    
    # Retry logic for API calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if response_format == "json":
                response = gemini_pro.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json"
                    )
                )
            else:
                response = gemini_flash.generate_content(full_prompt)
            
            return response.text or "I apologize, but I'm having trouble generating a response right now."
        except Exception as e:
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                return f"I'm experiencing technical difficulties. Please try again. (Error: {str(e)})"

def analyze_conversation_intent(conversation_history, current_message):
    """
    Analyze user intent and conversation stage using Gemini
    """
    context = f"Conversation history: {json.dumps(conversation_history[-5:])}"
    
    system_prompt = """You are an AI that analyzes conversation intent for a loan sales process.
    Determine the user's intent and the appropriate next step. Respond with JSON in this format:
    {
        "intent": "greeting|inquiry|personal_info|loan_details|verification|document_upload|objection|closing",
        "confidence": 0.0-1.0,
        "next_action": "sales_pitch|collect_info|verify_kyc|process_application|request_documents|handle_objection|close_deal",
        "extracted_info": {}
    }"""
    
    # Use retry logic for intent analysis as well
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = get_agent_response(system_prompt, current_message, context, "json")
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            else:
                return None