import random
import time

class CreditBureauApi:
    """
    Mock Credit Bureau API for fetching credit scores
    """
    
    def __init__(self):
        # Predefined credit scores for demo customers
        self.credit_scores = {
            '9876543210': 785,  # Rajesh Kumar
            '9876543211': 720,  # Priya Sharma
            '9876543212': 760,  # Amit Patel
            '9876543213': 680,  # Sunita Reddy
            '9876543214': 740,  # Vikram Singh
            '9876543215': 800,  # Anjali Gupta
            '9876543216': 650,  # Rohit Joshi
            '9876543217': 710,  # Kavya Menon
            '9876543218': 770,  # Arjun Nair
            '9876543219': 690,  # Deepika Agarwal
            '9876543220': 750,  # Manoj Yadav
            '9876543221': 730,  # Ritu Bansal
        }
    
    def get_credit_score(self, phone):
        """
        Fetch credit score from bureau (simulated)
        Returns score out of 900 as specified in requirements
        """
        # Simulate API delay
        time.sleep(0.5)
        
        if phone in self.credit_scores:
            return self.credit_scores[phone]
        else:
            # Generate random score for new customers
            # Weighted towards good scores to increase approval rates
            score_ranges = [
                (650, 700, 0.2),   # Poor: 20%
                (700, 750, 0.3),   # Fair: 30%
                (750, 800, 0.3),   # Good: 30%
                (800, 850, 0.2),   # Excellent: 20%
            ]
            
            rand = random.random()
            cumulative = 0
            
            for min_score, max_score, probability in score_ranges:
                cumulative += probability
                if rand <= cumulative:
                    return random.randint(min_score, max_score)
            
            return random.randint(750, 800)  # Default to good score
    
    def get_credit_report(self, phone):
        """
        Get detailed credit report (simplified for demo)
        """
        credit_score = self.get_credit_score(phone)
        
        # Generate mock credit report data
        report = {
            'credit_score': credit_score,
            'score_range': '300-900',
            'last_updated': '2025-09-20',
            'credit_utilization': random.randint(15, 45),
            'payment_history': 'Good' if credit_score > 720 else 'Fair',
            'credit_accounts': random.randint(3, 8),
            'credit_age_months': random.randint(24, 120),
            'recent_inquiries': random.randint(0, 3),
            'bureau_name': 'TransUnion CIBIL'
        }
        
        return report