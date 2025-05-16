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

SUBJECTS = [
    "Marksheet Verification", "Degree Certificate Issue", "Admission Details", "Faculty Appointment", "Research Grant Information", "Hostel Allotment", "Exam Results", "Fee Structure"
]
DEPTS = [
    "Examination Branch", "Registrar Office", "Accounts Department", "Academic Section", "Library", "Hostel Office"
]
POST_TYPES = ["Ordinary", "Registered", "Speed"]
PERIODS = ["2022-2023", "2021-2022", "2020-2021", "2019-2020"]


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
    # Use a single applicant profile
    applicant = random.choice([p for p in person_profiles if p.get('Gender', '').lower() in ['male', 'female']])
    name = applicant["Full Name"].upper()
    father_name = f"Mr. {random.choice(['Ashok','Raj','Sumit','Amitabha','Tapash'])} {name.split()[-1]}"
    address = applicant.get("Address", "")
    short_addr = ', '.join([
        applicant.get("Flat/Door/Block No", ""),
        applicant.get("Premises", ""),
        applicant.get("Road/Street/Lane", ""),
        applicant.get("Area/Locality", ""),
        applicant.get("Town/City/District", "")
    ])
    phone = applicant.get("Phone", "")
    email = applicant.get("Email", "")
    dept = random.choice(DEPTS)
    subject = random.choice(SUBJECTS)
    period = random.choice(PERIODS)
    info_details = random.choice([
        "Certified copy of marksheet for semester 4.",
        "Details of fee payment for academic year.",
        "Copy of degree certificate.",
        "Faculty appointment order copy."
    ])
    post_type = random.choice(POST_TYPES)
    agree_fee = random.choice(["Yes", "No"])
    fee_receipt = f"SBI{random.randint(10000,99999)}"
    fee_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d/%m/%Y")
    fee_amount = random.choice(["10", "50", "100"])
    dd_no = f"DD{random.randint(100000,999999)}"
    dd_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d/%m/%Y")
    dd_amount = random.choice(["10", "50", "100"])
    bpl = random.choice(["Yes", "No"])
    place = applicant.get("City", "Chandigarh")
    today = datetime.date.today().strftime("%d/%m/%Y")
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "casefileno":
            value = f"PU{random.randint(1000,9999)}"
        elif k == "depttbranch":
            value = dept
        elif k == "nameofapplicantcapitalletter":
            value = name
        elif k == "fatherhusbandname":
            value = father_name
        elif k == "permanentaddress":
            value = short_addr
        elif k == "correspondenceaddress":
            value = address
        elif k == "asubjectmatterofinformation":
            value = subject
        elif k == "btheperiodtowhichtheinformationrelates":
            value = period
        elif k == "cspecificdetailsofinformationrequired":
            value = info_details
        elif k == "whetherinformationisrequiredbypostorinpersontheactualpostalchargesshallbeincludedinprovidingtheinformation":
            value = random.choice(["Post", "In person"])
        elif k == "eincasebypostthenindicatewhetherordinaryregisteredorspeed":
            value = post_type
        elif k == "doyouagreetopaytherequiredfeecharges":
            value = agree_fee
        elif k == "thedetailsoffeedepositedincode nom0170orbyddoripo.":
            value = fee_receipt
        elif k == "iuniversitysbicounterreceiptno":
            value = fee_receipt
        elif k == "dated":
            value = fee_date
        elif k == "rs":
            value = fee_amount
        elif k == "iiddipono":
            value = dd_no
        elif k == "dated":
            value = dd_date
        elif k == "rs":
            value = dd_amount
        elif k == "iuniversitysbicounterreceiptno":
            value = bpl
        elif k == "place":
            value = place
        elif k == "date":
            value = today
        elif k == "address":
            value = short_addr
        elif k == "phonemobileno.":
            value = phone
        elif k == "e-mailaddress":
            value = email
        elif k == "fullsignatureoftheapplicant":
            value = name
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_41.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_41_filled.txt')
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