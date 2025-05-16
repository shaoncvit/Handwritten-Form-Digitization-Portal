import os
import re
import random
import datetime
import sys

# Ensure the parent directory is in sys.path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from personal_info import person_profiles

FORMS_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_text'
FORMS_FILL_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_filled'

CATEGORIES = ["SC", "ST", "OBC", "Minority", "Others"]
OCCUPATIONS = ["Service", "Business", "Teacher", "Doctor", "Engineer", "Farmer", "Retired", "Student", "Homemaker"]
BANKS = [
    "State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Bank of Baroda"
]
IFSC_CODES = [
    "SBIN0005678", "HDFC0001234", "ICIC0004321", "UTIB0008765", "PUNB0123456", "BARB0KOLKAT"
]


def normalize_key(key):
    return re.sub(r"[\s_/,.:;\(\)']", "", key.strip().lower())

def extract_keys_with_lines(form_text):
    field_pattern = re.compile(r"^(.+?):", re.MULTILINE)
    keys = []
    for idx, line in enumerate(form_text.splitlines()):
        line = line.strip()
        match = field_pattern.match(line)
        if match:
            key = match.group(1).strip()
            keys.append((key, idx))
    return keys

def fill_form(keys_with_lines):
    # Use a single student profile for all fields
    student = random.choice([p for p in person_profiles if p.get('Gender', '').lower() == 'male' or p.get('Gender', '').lower() == 'female'])
    # Names
    student_name = student["Full Name"]
    father_name = f"Mr. {random.choice(['Ashok','Raj','Sumit','Amitabha','Tapash'])} {student_name.split()[-1]}"
    mother_name = f"Mrs.{random.choice(['Devi', 'Kumari', 'Rani', 'Bala', 'Lata'])} {student_name.split()[-1]}"
    guardian_name = student_name
    # IDs
    wbscc_id = f"WBSCC{random.randint(100000,999999)}"
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(18*365, 25*365))).strftime("%d/%m/%Y")
    category = random.choice(CATEGORIES)
    sex = student.get('Gender', 'Male' if random.random() < 0.6 else 'Female')
    qualification = "B.A. 1st Year, 78%" if sex == "Female" else "B.Sc. 1st Year, 82%"
    occupation = random.choice(OCCUPATIONS)
    income = str(random.randint(100000, 1200000))
    pan = f"ABCDE{random.randint(1000,9999)}F"
    aadhar = f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
    # Address, contact, email
    address = student.get("Address", "")
    contact = student.get("Phone", "")
    email = student.get("Email", "")
    # Bank details
    bank = random.choice(BANKS)
    branch = random.choice(["Park Street", "Salt Lake", "Andheri", "MG Road", "Jubilee Hills", "Connaught Place", "Bandra"])
    sb_account = f"{random.randint(10000000000,99999999999)}"
    ifsc = random.choice(IFSC_CODES)
    # Short address logic
    parts = [
        student.get("Flat/Door/Block No", ""),
        student.get("Premises", ""),
        student.get("Road/Street/Lane", ""),
        student.get("Area/Locality", ""),
        student.get("Town/City/District", "")
    ]
    short_addr = ', '.join([part for part in parts if part])
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "name":
            value = student_name
        elif k == "wbsccapplicationid":
            value = wbscc_id
        elif k == "fathershusbandsname":
            value = father_name
        elif k == "mothersname":
            value = mother_name
        elif k == "legalguardianco-borrower":
            value = father_name
        elif k == "dateofbirth":
            value = dob
        elif k == "category":
            value = category + " " + category + " " + category
        elif k == "sex":
            value = sex
        elif k == "educationalqualificationwith%marks":
            value = qualification
        elif k == "occupation":
            value = occupation
        elif k == "incomefromallsources":
            value = income
        elif k == "panno":
            value = pan
        elif k == "aadharno*":
            value = aadhar
        elif k == "address":
            value = short_addr
        elif k == "contactno":
            value = contact
        elif k == "e-mailid":
            value = email
        elif k == "presentbankerdetails":
            value = bank
        elif k == "bankbranch":
            value = branch
        elif k == "sbaccountno":
            value = sb_account
        elif k == "nameofthebank":
            value = bank
        elif k == "ifsc":
            bank_ifsc = {
                "Bank of Baroda": "BARB0",
                "State Bank of India": "SBIN0",
                "HDFC Bank": "HDFC0",
                "ICICI Bank": "ICIC0",
                "Punjab National Bank": "PUNB0"
            }
            prefix = bank_ifsc.get(bank, "BANK0")
            value = prefix + "001234"
        elif k == "directindirectliabilitydetails":
            value = random.choice([
                "No direct/indirect liability",
                "None",
                "Education loan outstanding: ₹50,000",
                "Credit card balance: ₹10,000",
                "Personal loan: ₹1,20,000"
            ])
        else:
            value = ""
        form_data[key] = value
    return form_data

def fill_form_text(form_text, form_data):
    def replacer(match):
        key = match.group(1).strip()
        value = form_data.get(key, "")
        return f"{key}: {value}"
    field_pattern = re.compile(r"^(.+?):", re.MULTILINE)
    filled_text = field_pattern.sub(replacer, form_text)
    return filled_text

def main():
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_39.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_39_filled.txt')
    with open(FORM_PATH, 'r') as f:
        form_text = f.read()
    keys_with_lines = extract_keys_with_lines(form_text)
    form_data = fill_form(keys_with_lines)
    filled_text = fill_form_text(form_text, form_data)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(filled_text)
    print(f"Filled form saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 