import json
import os
import time

# Use GPT-4o for reliable API responses
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_agent_response(system_prompt, user_message, context=None, response_format="text"):
    """
    Get response from OpenAI for agent interactions
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    if context:
        messages.insert(1, {"role": "system", "content": f"Context: {context}"})
    
    # Retry logic for API calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if response_format == "json":
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    response_format={"type": "json_object"}
                )
            else:
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages
                )
            
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                return f"Error getting AI response: {str(e)}"

def analyze_conversation_intent(conversation_history, current_message):
    """
    Analyze user intent and conversation stage
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