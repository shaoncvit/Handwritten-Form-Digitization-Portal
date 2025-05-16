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

PURPOSES = [
    "Conference", "Alumni Meet", "Family Visit", "Official Work", "Medical", "Tourism"
]
RELATIONSHIPS = [
    "Self", "Friend", "Colleague", "Family", "Relative"
]
OFFICIALS = ["Mr. S. Ghosh", "Ms. P. Roy", "Dr. A. Banerjee", "Mr. R. Dutta", "Ms. N. Sen"]


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
    # Applicant and up to 3 visitors
    applicant = random.choice([p for p in person_profiles if p.get('Gender', '').lower() in ['male', 'female']])
    visitors = random.sample([p for p in person_profiles if p != applicant], k=min(3, len(person_profiles)-1))
    visitor_names = [v["Full Name"] for v in visitors]
    visitor_addr = visitors[0].get("Address", "") if visitors else applicant.get("Address", "")
    visitor_mob = visitors[0].get("Phone", "") if visitors else applicant.get("Phone", "")
    # Booking details
    rooms = random.randint(1, 3)
    suites = random.randint(0, 2)
    start_date = (datetime.date.today() + datetime.timedelta(days=random.randint(1, 10))).strftime("%d/%m/%Y")
    end_date = (datetime.date.today() + datetime.timedelta(days=random.randint(11, 20))).strftime("%d/%m/%Y")
    receipt_no = f"R{random.randint(10000,99999)}"
    receipt_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 10))).strftime("%d/%m/%Y")
    rent = str(1000*rooms + 1500*suites)
    cash_cheque = random.choice(["Cash", "Cheque"])
    cheque_no = f"CHQ{random.randint(100000,999999)}" if cash_cheque == "Cheque" else ""
    cheque_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 10))).strftime("%d/%m/%Y") if cash_cheque == "Cheque" else ""
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameofpuaamemberpuemployee":
            value = applicant["Full Name"]
        elif k == "contactaddress":
            value = applicant.get("Address", "")
        elif k == "mobno":
            value = applicant.get("Phone", "")
        elif k == "namesofvisitors":
            value = ", ".join(visitor_names)
        elif k == "contactaddressofvisitors":
            value = visitor_addr
        elif k == "mobno":
            value = visitor_mob
        elif k == "purposeofvisit":
            value = random.choice(PURPOSES)
        elif k == "relationshipwithapplicant":
            value = random.choice(RELATIONSHIPS)
        elif k == "noofroomsrequired":
            value = str(rooms)
        elif k == "rooms":
            value = str(rooms)
        elif k == "suites":
            value = str(suites)
        elif k == "datesforbooking":
            value = start_date
        elif k == "to":
            value = end_date
        elif k == "rentpaidvidereceiptno":
            value = receipt_no
        elif k == "dated":
            value = receipt_date
        elif k == "forrs":
            value = rent
        elif k == "cashchequeno":
            value = cash_cheque
        elif k == "dated":
            value = cheque_date
        elif k == "chequeno":
            value = cheque_no
        elif k == "signatureofapplicant":
            value = applicant["Full Name"]
        elif k == "address":
            value = applicant.get("Address", "")
        elif k == "receivedanamountofrs":
            value = rent
        elif k == "videourreceiptno":
            value = receipt_no
        elif k == "date":
            value = receipt_date
        elif k == "cash":
            value = cash_cheque
        elif k == "cheque":
            value = cash_cheque
        elif k == "chequeno":
            value = cheque_no
        elif k == "dated":
            value = cheque_date
        elif k == "andsuiteshasbeenbookedforyoufrom":
            value = start_date
        elif k == "and":
            value = end_date
        elif k == "approvedby":
            value = random.choice(OFFICIALS)
        elif k == "dealingofficial":
            value = random.choice(OFFICIALS)
        elif k == "deanalumnirelations":
            value = random.choice(OFFICIALS)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_43.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_43_filled.txt')
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