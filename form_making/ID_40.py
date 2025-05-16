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
    "Data Structures", "Algorithms", "Machine Learning", "Computer Networks", "Operating Systems", "Database Systems", "Artificial Intelligence", "Discrete Mathematics"
]
TA_SHIP = ["Quarter", "Half", "Full"]
FACULTY_NAMES = ["Dr. S. Rao", "Prof. A. Gupta", "Dr. P. Sharma", "Prof. R. Singh", "Dr. M. Iyer"]


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
    # Use a single TA profile
    ta = random.choice([p for p in person_profiles if p.get('Gender', '').lower() == 'male' or p.get('Gender', '').lower() == 'female'])
    ta_name = ta["Full Name"]
    roll_no = f"IIITH{random.randint(100000,999999)}"
    email = ta.get("Email", "")
    mobile = ta.get("Phone", "")
    subject = random.choice(SUBJECTS)
    date_assume = (datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))).strftime("%d/%m/%Y")
    sb_account = f"{random.randint(10000000000,99999999999)}"
    ta_ship = random.choice(TA_SHIP)
    other_jobs = random.choice(["NO", "YES"])
    other_jobs_details = "" if other_jobs == "NO" else "Research Assistant at IIITH"
    today = datetime.date.today().strftime("%d/%m/%Y")
    advisor = random.choice(FACULTY_NAMES)
    chair = random.choice(FACULTY_NAMES)
    course_faculty = random.choice([f for f in FACULTY_NAMES if f != chair])
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameoftheta":
            value = ta_name
        elif k == "rollno":
            value = roll_no
        elif k == "emailid":
            value = email
        elif k == "mobileno":
            value = mobile
        elif k == "subject":
            value = subject
        elif k == "dateofassumingastacommencementoftutorialclasses":
            value = date_assume
        elif k == "sblotherbankpersonalsbaccountno":
            value = sb_account
        elif k == "tashiprecommendedpermonthpleasetick":
            value = ta_ship
        elif k == "otherassistantshipsjobsif":
            value = other_jobs
        elif k == "ifyesgivedetailsandgetsignatureofrelevantfacultyadvisor":
            value = other_jobs_details
        elif k == "date":
            value = today
        elif k == "signatureoftheadvisor":
            value = advisor
        elif k == "signatureofthestudent":
            value = ta_name
        elif k == "signatureofthechair-tashipcommittee":
            value = chair
        elif k == "signatureofthecoursefaculty":
            value = course_faculty
        elif k == "tareportingformformonsoon20":
            value = random.randint(24, 25)
        elif k == "spring20":
            value = random.randint(25, 26)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_40.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_40_filled.txt')
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