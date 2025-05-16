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

BANKS = [
    "HDFC Bank", "State Bank of India", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Bank of Baroda", "Canara Bank"
]
ACCOUNT_TYPES = ["Savings", "Current", "NRE", "NRO", "Salary"]
FREQUENCIES = ["Weekly", "Bi-Monthly", "Monthly", "Quarterly", "Half-yearly", "Yearly", "One time"]
IFSC_CODES = [
    "HDFC0001234", "SBIN0005678", "ICIC0004321", "UTIB0008765", "PUNB0123456", "BARB0KOLKAT", "CNRB0001111"
]


def normalize_key(key):
    return re.sub(r"[\s_/,.:;\(\)'0-9]", "", key.strip().lower())

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
    # 60% male, 40% female profile selection for remitter
    males = [p for p in person_profiles if p.get('Gender', '').lower() == 'male']
    females = [p for p in person_profiles if p.get('Gender', '').lower() == 'female']
    if random.random() < 0.6 and males:
        remitter = random.choice(males)
    elif females:
        remitter = random.choice(females)
    else:
        remitter = random.choice(person_profiles)
    # Beneficiary: random Indian name and plausible account
    beneficiary_name = random.choice([
        "Amit Sharma", "Priya Singh", "Rahul Verma", "Sneha Patel", "Meera Iyer", "Arjun Deshmukh", "Naveen Reddy", "Farah Khan"
    ])
    beneficiary_acc = f"{random.randint(10000000000,99999999999)}"
    beneficiary_bank = random.choice(BANKS)
    beneficiary_acc_type = random.choice(ACCOUNT_TYPES)
    beneficiary_branch = f"{random.choice(['Park Street', 'Salt Lake', 'Andheri', 'MG Road', 'Jubilee Hills'])}, {random.choice(['Kolkata', 'Mumbai', 'Delhi', 'Hyderabad'])}"
    beneficiary_ifsc = random.choice(IFSC_CODES)
    # Remitter details
    remitter_name = remitter["Full Name"]
    remitter_acc = f"{random.randint(10000000000,99999999999)}"
    remitter_email = remitter["Email"]
    remitter_mobile = remitter["Phone"].replace("-", " ")
    # Standing instruction details
    amount = random.randint(1000, 100000)
    amount_words = f"{amount} Rupees Only"
    exec_date = (datetime.date.today() + datetime.timedelta(days=random.randint(1, 10))).strftime("%d/%m/%Y")
    last_date = (datetime.date.today() + datetime.timedelta(days=random.randint(30, 365))).strftime("%d/%m/%Y")
    frequency = random.choice(FREQUENCIES)
    today = datetime.date.today().strftime("%d/%m/%Y")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "branch":
            value = f"{beneficiary_bank} {beneficiary_branch.split(',')[0]} Branch"
        elif k == "date":
            value = today
        elif k == "beneficiaryname":
            value = beneficiary_name
        elif k == "beneficiaryaccountnumber":
            value = beneficiary_acc
        elif k == "beneficiarybank":
            value = beneficiary_bank
        elif k == "beneficiaryaccounttype":
            value = beneficiary_acc_type
        elif k == "beneficiarybranchname&address":
            value = beneficiary_branch
        elif k == "ifsccode":
            value = beneficiary_ifsc
        elif k == "remitterapplicantname":
            value = remitter_name
        elif k == "remitteraccountnumber":
            value = remitter_acc
        elif k == "remitteremailid":
            value = remitter_email
        elif k == "remittermobilenumber":
            value = remitter_mobile
        elif k == "amountinrupees":
            value = amount
        elif k == "amountinwords":
            value = amount_words
        elif k == "executiondateddmmyyyyformat":
            value = exec_date
        elif k == "lastdateddmmyyyy":
            value = last_date
        elif k == "frequency":
            value = frequency
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_33.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_33_filled.txt')
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