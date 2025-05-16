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
    "State Bank of India"
]
CURRENCIES = ["INR", "USD", "GBP", "EUR"]
OFFICIAL_NAMES = ["Mr. S. Ghosh", "Ms. P. Roy", "Dr. A. Banerjee", "Mr. R. Dutta", "Ms. N. Sen"]


def normalize_key(key):
    return re.sub(r"[\s_/,.:;\\(\\)'0-9]", "", key.strip().lower())

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
    # Up to 3 applicants
    applicants = random.sample(person_profiles, k=min(3, len(person_profiles)))
    # Beneficiary details (can be first applicant or a random person)
    beneficiary = random.choice(applicants)
    # Beneficiary bank details
    beneficiary_bank = random.choice(BANKS)
    beneficiary_acc = f"{random.randint(10000000000,99999999999)}"
    beneficiary_branch = random.choice([
        "Park Street", "Salt Lake", "Andheri", "MG Road", "Jubilee Hills", "Connaught Place", "Bandra"
    ])
    beneficiary_city = beneficiary.get("City", "Mumbai")
    beneficiary_country = beneficiary.get("Country", "India")
    beneficiary_swift = f"SBINUS{random.randint(1000,9999)}"
    beneficiary_postal = beneficiary.get("PIN", "400001")
    # Intermediary bank details
    intermediary_bank = random.choice(BANKS)
    intermediary_branch = random.choice([
        "New York", "London", "Frankfurt", "Singapore", "Dubai"
    ])
    intermediary_address = f"{random.randint(100,999)} {intermediary_branch} Ave, {intermediary_branch}"
    intermediary_swift = f"{intermediary_bank[:4].upper()}US{random.randint(1000,9999)}"
    currency = random.choice(CURRENCIES)
    # Official check address (use first applicant)
    check_applicant = applicants[0]
    # Dates
    today = datetime.date.today().strftime("%d/%m/%Y")
    place = check_applicant.get("City", "Mumbai")
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameinfull":
            value = beneficiary["Full Name"]
        elif k == "mailingaddress":
            value = beneficiary.get("Address", "")
        elif k == "city":
            value = beneficiary.get("City", "")
        elif k == "state":
            value = beneficiary.get("State/Province", "")
        elif k == "country":
            value = beneficiary.get("Country", "India")
        elif k == "postalcode":
            value = beneficiary.get("PIN", "400001")
        elif k == "acno":
            value = beneficiary_acc
        elif k == "nameofbank":
            value = beneficiary_bank
        elif k == "branch":
            value = beneficiary_branch
        elif k == "citycountry":
            value = f"{beneficiary_city}, {beneficiary_country}"
        elif k == "swiftsortcode":
            value = beneficiary_swift
        elif k == "intermediarybankdetails":
            value = intermediary_bank
        elif k == "branch":
            value = intermediary_branch
        elif k == "address":
            value = intermediary_address
        elif k == "swiftsortcode":
            value = intermediary_swift
        elif k == "currency":
            value = currency
        elif k == "city":
            value = check_applicant.get("City", "")
        elif k == "state":
            value = check_applicant.get("State/Province", "")
        elif k == "country":
            value = check_applicant.get("Country", "India")
        elif k == "postalcode":
            value = check_applicant.get("PIN", "400001")
        elif k == "firstapplicant":
            value = applicants[0]["Full Name"]
        elif k == "signature":
            value = applicants[0]["Full Name"]
        elif k == "secondapplicantname":
            value = applicants[1]["Full Name"] if len(applicants) > 1 else ""
        elif k == "thirdapplicantname":
            value = applicants[2]["Full Name"] if len(applicants) > 2 else ""
        elif k == "date":
            value = today
        elif k == "place":
            value = place
        elif k == "associate":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "authorisedofficial":
            value = random.choice(OFFICIAL_NAMES)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_37.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_37_filled.txt')
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