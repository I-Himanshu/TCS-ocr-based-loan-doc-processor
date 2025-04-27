# modules/enhanced_processor.py
import cv2
import pytesseract
import numpy as np
from PIL import Image
from pdf2image import convert_from_bytes
import re
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.medianBlur(gray, 3)
    return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

def extract_fields(text):
    print("Extracting fields from text...")
    print(text)
    patterns = {
        'name': r"(?i)(Name:|Applicant:)\s*(.+)",
        'address': r"(?i)(Address:)\s*(.+)",
        'income': r"(?i)(Income:)\s*(\$?\d+,?\d*)",
        'loan_amount': r"(?i)(Loan Amount:)\s*(\$?\d+,?\d*)"
    }
    
    results = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        results[field] = match.group(2).strip() if match else ''
        print(f"Extracted {field}: {results[field]}")
    results['name'] = results['name'].split()[0] if results['name'] else ''
    results['address'] = results['address'].split(',')[0] if results['address'] else ''
    results['income'] = results['income'].replace('$', '').replace(',', '') if results['income'] else '0'
    results['loan_amount'] = results['loan_amount'].replace('$', '').replace(',', '') if results['loan_amount'] else '0'
    
    return results

def process_uploaded_file(uploaded_file):
    if uploaded_file.type == 'application/pdf':
        images = convert_from_bytes(uploaded_file.read())
    else:
        images = [Image.open(uploaded_file)]
    
    full_text = ""
    for img in images:
        opencv_img = np.array(img)
        processed_img = preprocess_image(cv2.cvtColor(opencv_img, cv2.COLOR_RGB2BGR))
        full_text += pytesseract.image_to_string(processed_img) + "\n"
    
    return full_text