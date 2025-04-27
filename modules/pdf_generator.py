# modules/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def create_loan_agreement(data):
    filename = f"loan_contract_{data['name']}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 750, "Loan Agreement")
    c.line(72, 745, 540, 745)
    
    # Content
    c.setFont("Helvetica", 12)
    y_position = 700
    lines = [
        f"Borrower Name: {data['name']}",
        f"Loan Amount: ${data.get('loan_amount', '0')}",
        f"Approval Date: {datetime.now().strftime('%Y-%m-%d')}",
        f"Risk Score: {data.get('risk_score', 650)}",
        "Terms: 60 monthly payments at 4.5% APR",
        "Signature: ___________________________"
    ]
    
    for line in lines:
        c.drawString(72, y_position, line)
        y_position -= 30
    
    c.save()
    return filename