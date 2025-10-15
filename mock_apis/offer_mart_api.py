import json

class OfferMartApi:
    """
    Mock Offer Mart API for pre-approved loan offers
    """
    
    def __init__(self):
        # Pre-approved limits based on customer profiles
        self.offers = {
            '9876543210': {'pre_approved_limit': 500000, 'interest_rate': 10.5, 'tenure_max': 60},
            '9876543211': {'pre_approved_limit': 300000, 'interest_rate': 12.0, 'tenure_max': 48},
            '9876543212': {'pre_approved_limit': 600000, 'interest_rate': 11.0, 'tenure_max': 60},
            '9876543213': {'pre_approved_limit': 250000, 'interest_rate': 13.5, 'tenure_max': 36},
            '9876543214': {'pre_approved_limit': 400000, 'interest_rate': 11.5, 'tenure_max': 48},
            '9876543215': {'pre_approved_limit': 700000, 'interest_rate': 10.0, 'tenure_max': 72},
            '9876543216': {'pre_approved_limit': 200000, 'interest_rate': 14.0, 'tenure_max': 36},
            '9876543217': {'pre_approved_limit': 350000, 'interest_rate': 12.5, 'tenure_max': 48},
            '9876543218': {'pre_approved_limit': 550000, 'interest_rate': 10.8, 'tenure_max': 60},
            '9876543219': {'pre_approved_limit': 280000, 'interest_rate': 13.0, 'tenure_max': 42},
            '9876543220': {'pre_approved_limit': 450000, 'interest_rate': 11.2, 'tenure_max': 54},
            '9876543221': {'pre_approved_limit': 380000, 'interest_rate': 11.8, 'tenure_max': 48},
        }
    
    def get_offer(self, customer_data):
        """
        Get pre-approved offer for customer
        """
        phone = customer_data.get('phone', '')
        monthly_income = customer_data.get('monthly_income', 0)
        
        if phone in self.offers:
            return self.offers[phone]
        else:
            # Generate offer for new customer based on income
            if isinstance(monthly_income, str):
                try:
                    monthly_income = int(monthly_income)
                except:
                    monthly_income = 50000  # Default
            
            # Calculate pre-approved limit as 6-8x monthly income
            income_multiplier = 6.5
            if monthly_income > 100000:
                income_multiplier = 8.0
            elif monthly_income > 75000:
                income_multiplier = 7.5
            elif monthly_income > 50000:
                income_multiplier = 7.0
            
            pre_approved_limit = int(monthly_income * income_multiplier)
            
            # Determine interest rate based on income tier
            if monthly_income > 100000:
                interest_rate = 10.5
                tenure_max = 72
            elif monthly_income > 75000:
                interest_rate = 11.5
                tenure_max = 60
            elif monthly_income > 50000:
                interest_rate = 12.5
                tenure_max = 48
            else:
                interest_rate = 14.0
                tenure_max = 36
            
            offer = {
                'pre_approved_limit': min(pre_approved_limit, 4000000),  # Cap at 40 lakhs
                'interest_rate': interest_rate,
                'tenure_max': tenure_max
            }
            
            return offer
    
    def get_loan_products(self):
        """
        Get available loan products
        """
        return {
            'personal_loans': {
                'amount_range': {'min': 50000, 'max': 4000000},
                'interest_rate_range': {'min': 10.0, 'max': 15.0},
                'tenure_range': {'min': 12, 'max': 72},
                'processing_fee': 2500,
                'features': [
                    'No collateral required',
                    'Quick approval',
                    'Flexible repayment',
                    'Competitive rates'
                ]
            }
        }