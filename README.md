# CapitalInsights - AI-Powered Personal Loan Assistant

## Team: CodingGujarat
### Team Members:
- Aman Nayak
- Hiren Dadhaniya
- Vinit Patel
- Ronak Prajapati

---

## Introduction

### 

Techathon is more than a competition—it is a launchpad for India's brightest young minds to drive change through bold ideas and breakthrough innovation. Since its inception in 2020, Techathon has grown into one of the country's most anticipated campus contests, inspiring students to push boundaries and reimagine possibilities.

Now in its sixth edition, this year's challenge invites participants to explore the frontier of Agent AI, a transformative leap from automation to autonomous, goal-driven systems. The theme sets the stage for visionary solutions that could redefine industries and accelerate India's digital future.

---

## Problem Statement: Challenge II - Banking, Financial Services, and Insurance (BFSI) - Tata Capital

### About the Business
A large-scale Non-Banking Financial Company (NBFC) with a presence across India offers personal loans, home loans, auto loans and more. To increase revenue from existing customers, the NBFC aims to sell personal loans to prospects and its existing customers through a web-based chatbot interface.

The chatbot will serve as a digital sales assistant, where a Master Agent (Agent AI Controller) coordinates multiple Worker AI agents to handle the end-to-end loan sales process — from conversation and verification to credit evaluation, and approval and generating a sanction letter.

### Problem Statement
The NBFC wants to improve its sales success rate for personal loans by using an AI-driven conversational approach. The solution must simulate a human-like sales process, where the Master Agent handles customer conversations, engages customers in a personalized manner and collaborates with multiple Worker AI agents to complete the loan process.

### Goal
Teams must design an Agent AI solution where the Master Agent:
1. Chats with customers landing on the web chatbot via digital ads or marketing emails
2. Understands the customer's needs and convinces them to take a personal loan
3. Orchestrates multiple Worker AI agents to complete all tasks—verification, underwriting and sanction letter generation—before closing the chat.

### Key Deliverable
A 5-slides PPT showcasing the end-to-end journey from the initial chat to sanction letter generation.

---

## Agent AI Roles

### 1. Master Agent (Main Orchestrator)
- Manages the conversation flow with the customer
- Hands over tasks to Worker Agents and coordinates the workflow
- Starts and ends the conversation

### 2. Worker Agents
- **Sales Agent**: Negotiates loan terms, discusses customer needs, amount, tenure and interest rates
- **Verification Agent**: Confirms KYC details (phone, address) from a dummy CRM server
- **Underwriting Agent**: 
  - Fetches a dummy credit score (out of 900) from a mock credit bureau API
  - Validates eligibility:
    - If the loan amount ≤ pre-approved limit, approve instantly
    - If ≤ 2× pre-approved limit, request a salary slip upload. Approve only if expected EMI ≤ 50% of salary
    - Reject if > 2× pre-approved limit or credit score < 700
- **Sanction Letter Generator**: Generates an automated PDF sanction letter if all conditions are met

---

## Data and System Assumptions

- **Synthetic customer data**: Teams must create dummy data for at least 10 customers with details like name, age, city, current loan details, credit score and pre-approved personal loan limit
- **Offer mart server**: A mock server or API hosting pre-approved loan offers
- **CRM server**: Dummy customer KYC data
- **Credit bureau API**: Mock API to fetch credit scores
- **File upload**: Simulated salary slip upload (dummy PDF or image)
- Teams may make any reasonable assumptions as long as the solution feels realistic

---

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **AI Framework**: Google Gemini / OpenAI
- **Agent Communication**: Socket.IO
- **API Mocking**: Python scripts

---

## Project Structure

```
CapitalInsights/
├── agents/
│   ├── __init__.py
│   ├── master_agent.py
│   ├── sales_agent.py
│   ├── sanction_letter_agent.py
│   ├── underwriting_agent.py
│   └── verification_agent.py
├── mock_apis/
│   ├── __init__.py
│   ├── credit_bureau_api.py
│   ├── crm_api.py
│   └── offer_mart_api.py
├── templates/
│   └── index.html
├── app.py
├── gemini_client.py
├── openai_client.py
├── README.md
└── requirements.txt
```

---

## Features

1. **Multi-Agent AI System**: Orchestrated workflow with specialized agents for different loan processing tasks
2. **Interactive Chat Interface**: Real-time conversation with the customer through a web-based chatbot
3. **Dynamic Theme Switching**: Light and dark mode support for enhanced user experience
4. **Visual Progress Tracking**: Timeline-based progress visualization for loan application status
5. **Realistic Loan Processing Simulation**: Mock APIs for credit bureau, CRM, and offer mart
6. **Responsive Design**: Works seamlessly across devices

---

## How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open your browser and navigate to `http://localhost:5000`
