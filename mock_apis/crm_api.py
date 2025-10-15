import sqlite3
import json
import os
from datetime import datetime

class CRMApi:
    """
    Mock CRM API for customer verification and KYC data
    """
    
    def __init__(self, db_path='customer_data.db'):
        self.db_path = db_path
    
    def initialize_database(self):
        """Initialize SQLite database with synthetic customer data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                city TEXT NOT NULL,
                age INTEGER,
                current_loans TEXT,
                credit_score INTEGER,
                pre_approved_limit INTEGER,
                employment_type TEXT,
                company_name TEXT,
                monthly_income INTEGER,
                created_date TEXT
            )
        ''')
        
        # Insert synthetic customer data (10+ customers as required)
        customers_data = [
            ('Rajesh Kumar', '9876543210', 'rajesh.kumar@email.com', 'Mumbai', 32, 
             json.dumps([{'type': 'home_loan', 'amount': 2500000, 'emi': 25000}]), 785, 500000, 'salaried', 'TCS Limited', 85000),
            
            ('Priya Sharma', '9876543211', 'priya.sharma@email.com', 'Delhi', 28, 
             json.dumps([]), 720, 300000, 'salaried', 'Infosys', 65000),
            
            ('Amit Patel', '9876543212', 'amit.patel@email.com', 'Bangalore', 35, 
             json.dumps([{'type': 'car_loan', 'amount': 800000, 'emi': 18000}]), 760, 600000, 'self_employed', 'Own Business', 120000),
            
            ('Sunita Reddy', '9876543213', 'sunita.reddy@email.com', 'Hyderabad', 30, 
             json.dumps([]), 680, 250000, 'salaried', 'Wipro Technologies', 55000),
            
            ('Vikram Singh', '9876543214', 'vikram.singh@email.com', 'Pune', 29, 
             json.dumps([{'type': 'personal_loan', 'amount': 200000, 'emi': 8500}]), 740, 400000, 'salaried', 'IBM India', 75000),
            
            ('Anjali Gupta', '9876543215', 'anjali.gupta@email.com', 'Chennai', 33, 
             json.dumps([]), 800, 700000, 'salaried', 'HCL Technologies', 95000),
            
            ('Rohit Joshi', '9876543216', 'rohit.joshi@email.com', 'Kolkata', 27, 
             json.dumps([]), 650, 200000, 'salaried', 'Tech Mahindra', 48000),
            
            ('Kavya Menon', '9876543217', 'kavya.menon@email.com', 'Kochi', 31, 
             json.dumps([{'type': 'education_loan', 'amount': 1200000, 'emi': 15000}]), 710, 350000, 'salaried', 'Accenture', 68000),
            
            ('Arjun Nair', '9876543218', 'arjun.nair@email.com', 'Ahmedabad', 34, 
             json.dumps([]), 770, 550000, 'self_employed', 'Consultant', 105000),
            
            ('Deepika Agarwal', '9876543219', 'deepika.agarwal@email.com', 'Jaipur', 26, 
             json.dumps([]), 690, 280000, 'salaried', 'Capgemini', 58000),
            
            ('Manoj Yadav', '9876543220', 'manoj.yadav@email.com', 'Lucknow', 36, 
             json.dumps([{'type': 'home_loan', 'amount': 3000000, 'emi': 28000}]), 750, 450000, 'salaried', 'L&T Infotech', 82000),
            
            ('Ritu Bansal', '9876543221', 'ritu.bansal@email.com', 'Chandigarh', 29, 
             json.dumps([]), 730, 380000, 'salaried', 'Cognizant', 71000)
        ]
        
        for customer in customers_data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO customers 
                    (name, phone, email, city, age, current_loans, credit_score, 
                     pre_approved_limit, employment_type, company_name, monthly_income, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', customer + (datetime.now().isoformat(),))
            except sqlite3.IntegrityError:
                pass  # Skip if customer already exists
        
        conn.commit()
        conn.close()
    
    def verify_customer(self, customer_data):
        """
        Verify customer against CRM database
        """
        phone = customer_data.get('phone', '')
        if not phone:
            return {'verified': False, 'reason': 'no_phone'}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM customers WHERE phone = ?
        ''', (phone,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Customer found in CRM
            columns = ['id', 'name', 'phone', 'email', 'city', 'age', 'current_loans', 
                      'credit_score', 'pre_approved_limit', 'employment_type', 
                      'company_name', 'monthly_income', 'created_date']
            
            customer_details = dict(zip(columns, result))
            customer_details['current_loans'] = json.loads(customer_details['current_loans'])
            
            return {
                'verified': True,
                'customer_details': customer_details,
                'kyc_status': 'complete'
            }
        else:
            return {
                'verified': False,
                'reason': 'not_found',
                'kyc_status': 'required'
            }
    
    def get_customer_by_phone(self, phone):
        """Get customer details by phone number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE phone = ?', (phone,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = ['id', 'name', 'phone', 'email', 'city', 'age', 'current_loans', 
                      'credit_score', 'pre_approved_limit', 'employment_type', 
                      'company_name', 'monthly_income', 'created_date']
            return dict(zip(columns, result))
        return None