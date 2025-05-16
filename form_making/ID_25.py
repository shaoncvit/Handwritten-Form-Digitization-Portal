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
    "State Bank of India", "Punjab National Bank", "Bank of Baroda", "HDFC Bank", "ICICI Bank", "Axis Bank", "Canara Bank", "Union Bank of India"
]
BRANCHES = [
    "Jadavpur", "Salt Lake", "Garia", "Howrah", "Park Street", "Dum Dum", "Behala", "Ballygunge"
]
IFS_CODES = [
    "SBIN0000093", "PUNB0038000", "BARB0JADAVP", "HDFC0000240", "ICIC0000123", "UTIB0000123", "CNRB0001234", "UBIN0530786"
]
EXAMS = [
    "B.Tech 8th Semester", "M.Sc. Physics Final", "Ph.D. Viva", "B.A. English Hons.", "M.A. History", "B.Sc. Chemistry Practical"
]
JOURNEY_FROM = ["Jadavpur University", "Salt Lake", "Howrah", "Dum Dum", "Ballygunge"]
JOURNEY_TO = ["Jadavpur University", "Salt Lake", "Howrah", "Dum Dum", "Ballygunge"]


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
    person = random.choice(person_profiles)
    examiner_name = person["Full Name"].upper()
    address = person["Address"]
    contact = person["Phone"].replace("-", " ")
    exam = random.choice(EXAMS)
    journey_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y")
    journey_from = random.choice(JOURNEY_FROM)
    journey_to = random.choice([loc for loc in JOURNEY_TO if loc != journey_from])
    bank = random.choice(BANKS)
    branch = random.choice(BRANCHES)
    ifs = random.choice(IFS_CODES)
    acc_no = f"{random.randint(10000000000,99999999999)}"
    # Allowance logic: within Kolkata/Howrah = 400, outside = 500
    if (journey_from in ["Kolkata", "Howrah"] and journey_to in ["Kolkata", "Howrah"]):
        amount = 400
    else:
        amount = 500
    remarks = random.choice(["", "As per university rules", "Approved by HOD"])
    today = datetime.date.today().strftime("%d-%m-%Y")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        value = ""
        if k == "nameincapitalletters":
            value = examiner_name
        elif k == "address":
            value = address
        elif k == "contactnopreferablyamobileno":
            value = contact
        elif k == "nameofexamination":
            value = exam
        elif k == "dateofjourney":
            value = journey_date
        elif k == "from":
            value = journey_from
        elif k == "to":
            value = journey_to
        elif k == "nameofbank":
            value = bank
        elif k == "nameofbranch":
            value = branch
        elif k == "ifscode":
            value = ifs
        elif k == "accountno":
            value = acc_no
        elif k == "amounttobepaidasconvallowance*":
            value = amount
        elif k == "remarks":
            value = remarks
        elif k == "date":
            value = today
        elif k == "signatureofexternalexaminerforwarded":
            value = examiner_name
        elif k == "signatureofheadofthedepartment":
            value = random.choice(["Dr. S. Mukherjee", "Prof. A. Banerjee", "Dr. R. Das"])
        elif k == "thecontrollerofexaminations":
            value = "Dr. P. Chatterjee"
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_25.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_25_filled.txt')
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