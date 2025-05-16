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

ACCOUNT_TYPES = ["Checking", "Money Market Deposit", "Certificate of Deposit"]
EMPLOYMENT_STATUSES = ["Employed", "Self-employed", "Retired", "Unemployed", "Student", "Others"]
OCCUPATIONS = ["Software Engineer", "Teacher", "Doctor", "Business Owner", "Accountant", "Student", "Consultant", "Manager"]
BUSINESSES = ["Infosys", "TCS", "Wipro", "Reliance", "HDFC", "ICICI", "Self-Employed", "Freelancer", "Jadavpur University", "IIT Bombay"]


def normalize_key(key):
    return re.sub(r"[\s_/,.:;\\(\\)']", "", key.strip().lower())

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
    # 60% male, 40% female profile selection
    males = [p for p in person_profiles if p.get('Gender', '').lower() == 'male']
    females = [p for p in person_profiles if p.get('Gender', '').lower() == 'female']
    if random.random() < 0.6 and males:
        person = random.choice(males)
    elif females:
        person = random.choice(females)
    else:
        person = random.choice(person_profiles)
    # Name splitting
    name_parts = person["Full Name"].split()
    first = name_parts[0]
    last = name_parts[-1] if len(name_parts) > 1 else ""
    middle = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
    # Account types (randomly check 1-3)
    checked_accounts = random.sample(ACCOUNT_TYPES, k=random.randint(1, len(ACCOUNT_TYPES)))
    # PAN/SSN/TIN
    pan = f"ABCDE{random.randint(1000,9999)}F"
    # Employment
    employment_status = random.choice(EMPLOYMENT_STATUSES)
    occupation = random.choice(OCCUPATIONS)
    employer = random.choice(BUSINESSES) if employment_status in ["Employed", "Self-employed"] else ""
    # Home address
    home_addr = person.get("Address", "")
    city = person.get("City", "")
    state = person.get("State/Province", "")
    country = person.get("Country", "India")
    pin = person.get("PIN", "400001")
    # Work/college address
    work_addr = ""
    if employment_status == "Student":
        work_addr = f"{random.choice(['Jadavpur University', 'IIT Bombay', 'Delhi University'])}, {city}, {state}"
    elif employment_status in ["Employed", "Self-employed"]:
        work_addr = f"{employer}, {city}, {state}"
    # Email/contacts
    email = person.get("Email", "")
    home_phone = person.get("Phone", "")
    mobile = person.get("Phone", "")
    work_phone = f"+91 {random.randint(9000000000,9999999999)}"
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "customerid":
            value = f"CUST{random.randint(100000,999999)}"
        elif k == "name":
            value = person["Full Name"]
        elif k == "first":
            value = first
        elif k == "middle":
            if not middle:  # If no middle name from person's full name
                value = random.choice(["Kumar", "Prasad", "Chandra", "Nath", "Dev", "Mohan", ""]) # Add some common middle names
            else:
                value = middle
        elif k == "lastsurname":
            value = last
        elif k == "typeofaccountholdcheckingmoneymarketdepositcertificateofdeposit":
            value = ", ".join(checked_accounts)
        elif k == "socialsecuritynotaxidentificationnopermanentaccountnumberpan*indiancitizen":
            value = pan
        elif k == "employeddetails":
            value = employment_status
        elif k == "occupation":
            value = occupation
        elif k == "nameofemployerincaseemployedornamenatureofbusinessincaseselfemployed":
            value = person["Full Name"]
        elif k == "homeaddress":
            value = home_addr
        elif k == "workaddress":
            value = work_addr
        elif k == "addressline1":
            value = home_addr.split(",")[0] if home_addr else ""
        elif k == "addressline2":
            value = home_addr.split(",")[1] if home_addr and len(home_addr.split(",")) > 1 else ""
        elif k == "addressline3":
            value = home_addr.split(",")[2] if home_addr and len(home_addr.split(",")) > 2 else ""
        elif k == "city":
            value = city
        elif k == "state":
            value = state
        elif k == "country":
            value = country
        elif k == "zipcode":
            value = pin
        elif k == "email":
            value = email
        elif k == "contact/mobilenumber":
            value = mobile
        elif k == "home":
            value = home_phone
        elif k == "mobile":
            value = mobile
        elif k == "work":
            value = work_phone
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_38.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_38_filled.txt')
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