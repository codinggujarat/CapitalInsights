import os
import random
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import uuid

class SanctionLetterAgent:
    """
    Sanction Letter Generator - Creates automated PDF sanction letters
    """
    
    def __init__(self):
        self.output_dir = 'sanction_letters'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_sanction_letter(self, session_data):
        """
        Generate PDF sanction letter for approved loans
        """
        customer_data = session_data.get('customer_data', {})
        loan_application = session_data.get('loan_application', {})
        emi_details = session_data.get('emi_details', {})
        
        # Generate unique filename
        filename = f"sanction_letter_{customer_data.get('name', 'customer').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        self._create_sanction_letter_pdf(filepath, customer_data, loan_application, emi_details)
        
        return {
            'message': (f"🎉 Congratulations {customer_data.get('name', '')}! Your personal loan has been approved! "
                       f"I've generated your official sanction letter with all the loan details. "
                       f"You can download it using the link below. Our team will contact you within "
                       f"24 hours to complete the formalities. Welcome to the Tata Capital family!"),
            'agent': 'Sanction Letter Agent',
            'loan_approved': True,
            'sanction_letter_url': f'/download_sanction_letter/{filename}',
            'session_updates': {'current_stage': 'completed', 'sanction_letter_generated': True}
        }
    
    def _create_sanction_letter_pdf(self, filepath, customer_data, loan_application, emi_details):
        """Create the actual PDF sanction letter"""
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.darkblue,
            spaceAfter=20
        )
        
        # Header
        story.append(Paragraph("TATA CAPITAL LIMITED", title_style))
        story.append(Paragraph("Personal Loan Sanction Letter", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Reference details
        ref_no = f"TC/PL/{datetime.now().year}/{random.randint(100000, 999999)}"
        date_str = datetime.now().strftime("%B %d, %Y")
        
        story.append(Paragraph(f"<b>Reference No:</b> {ref_no}", header_style))
        story.append(Paragraph(f"<b>Date:</b> {date_str}", header_style))
        story.append(Spacer(1, 12))
        
        # Customer details
        story.append(Paragraph("<b>Dear " + customer_data.get('name', 'Valued Customer') + ",</b>", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Approval message
        approval_text = """
        We are pleased to inform you that your application for a Personal Loan has been approved. 
        The sanction is subject to the terms and conditions mentioned below and execution of necessary documents.
        """
        story.append(Paragraph(approval_text, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Loan details table
        loan_amount = customer_data.get('loan_amount', 0)
        interest_rate = "12.00%"  # Standard rate
        tenure = emi_details.get('tenure_months', 36)
        monthly_emi = emi_details.get('monthly_emi', 0)
        
        loan_data = [
            ['Loan Details', ''],
            ['Sanctioned Amount', f"₹ {loan_amount:,}"],
            ['Interest Rate (Per Annum)', interest_rate],
            ['Loan Tenure', f"{tenure} months"],
            ['Monthly EMI', f"₹ {monthly_emi:,.0f}" if monthly_emi else "As per agreed terms"],
            ['Processing Fee', "₹ 2,500 + GST"],
            ['Loan Purpose', customer_data.get('loan_purpose', 'Personal').title()]
        ]
        
        loan_table = Table(loan_data, colWidths=[3*inch, 2.5*inch])
        loan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(loan_table)
        story.append(Spacer(1, 20))
        
        # Terms and conditions
        terms_title = Paragraph("<b>Terms and Conditions:</b>", styles['Heading3'])
        story.append(terms_title)
        
        terms = [
            "1. This sanction letter is valid for 30 days from the date of issue.",
            "2. Loan disbursal is subject to verification of documents and completion of legal formalities.",
            "3. EMI payment will commence from the month following the disbursal.",
            "4. Prepayment of loan is allowed with applicable charges as per loan agreement.",
            "5. Loan is subject to terms and conditions of the loan agreement."
        ]
        
        for term in terms:
            story.append(Paragraph(term, styles['Normal']))
            story.append(Spacer(1, 6))
        
        story.append(Spacer(1, 20))
        
        # Closing
        closing_text = """
        We look forward to serving you and thank you for choosing Tata Capital for your financial needs.
        
        For any queries, please contact our customer service at 1800-209-8800.
        
        Warm Regards,
        
        Credit Team
        Tata Capital Limited
        """
        story.append(Paragraph(closing_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)

