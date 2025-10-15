import json
import os
from google import genai
from google.genai import types

# IMPORTANT: KEEP THIS COMMENT
# Follow these instructions when using this blueprint:
# - Note that the newest Gemini model series is "gemini-2.5-flash" or gemini-2.5-pro"
#   - do not change this unless explicitly requested by the user

# This API key is from Gemini Developer API Key, not vertex AI API Key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_agent_response(system_prompt, user_message, context=None, response_format="text"):
    """
    Get response from Gemini for agent interactions
    """
    # Combine prompts for Gemini
    full_prompt = f"System: {system_prompt}\n\n"
    if context:
        full_prompt += f"Context: {context}\n\n"
    full_prompt += f"User: {user_message}\n\nAssistant:"
    
    try:
        if response_format == "json":
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Always respond with valid JSON format.",
                    response_mime_type="application/json"
                )
            )
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
        
        return response.text or "I apologize, but I'm having trouble generating a response right now."
    except Exception as e:
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
    
    return get_agent_response(system_prompt, current_message, context, "json")