import cv2
import pytesseract
import numpy as np
from PIL import Image
from pdf2image import convert_from_bytes

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.medianBlur(gray, 3)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh

def extract_fields(text):
    fields = {
        'name': [],
        'address': [],
        'income': [],
        'loan_amount': []
    }
    
    keywords = {
        'name': ['name', 'full name', 'applicant'],
        'address': ['address', 'street', 'city', 'state', 'zip'],
        'income': ['income', 'salary', 'annual income', 'monthly income'],
        'loan_amount': ['loan amount', 'amount requested', 'requested amount']
    }

    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        for field in keywords:
            for kw in keywords[field]:
                if kw in line_lower:
                    if ':' in line:
                        value = line.split(':', 1)[1].strip()
                    else:
                        value = lines[i+1].strip() if i+1 < len(lines) else ''
                    if value:
                        fields[field].append(value)
                    break

    results = {}
    for field in fields:
        values = [v for v in fields[field] if v]
        results[field] = values[0] if values else ''
    
    return results

def process_uploaded_file(uploaded_file):
    images = []
    if uploaded_file.type == 'application/pdf':
        images = convert_from_bytes(uploaded_file.read())
    else:
        images = [Image.open(uploaded_file)]
    
    full_text = ""
    for img in images:
        opencv_image = np.array(img)
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)
        processed_image = preprocess_image(opencv_image)
        text = pytesseract.image_to_string(processed_image)
        full_text += text + "\n"
    
    return full_text