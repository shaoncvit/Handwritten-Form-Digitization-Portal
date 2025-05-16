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

INSURANCE_COMPANIES = [
    "LIC of India", "ICICI Lombard", "HDFC ERGO", "Bajaj Allianz", "Max Bupa", "Star Health"
]
PHYSICIANS = [
    "Dr. S. Ghosh", "Dr. A. Banerjee", "Dr. R. Dutta", "Dr. N. Sen", "Dr. P. Roy"
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
    # Gender distribution: 60% male, 40% female
    gender_choice = random.choices(['male', 'female'], weights=[60, 40])[0]
    candidates = [p for p in person_profiles if p.get('Gender', '').lower() == gender_choice]
    if not candidates:
        candidates = person_profiles
    applicant = random.choice(candidates)
    name = applicant["Full Name"].title()
    dob_dt = datetime.date.today() - datetime.timedelta(days=random.randint(2500, 4000))
    dob = dob_dt.strftime("%d/%m/%Y")
    address = ', '.join(filter(None, [
        applicant.get("Flat/Door/Block No", ""),
        applicant.get("Premises", ""),
        applicant.get("Road/Street/Lane", ""),
        applicant.get("Area/Locality", ""),
        applicant.get("Town/City/District", "")
    ]))
    city = applicant.get("Town/City/District", applicant.get("City", ""))
    zip_code = applicant.get("PIN", "")
    email = applicant.get("Email", "")
    age = str(random.randint(6, 12))
    last_grade = str(random.randint(1, 6))
    gender = applicant.get("Gender", gender_choice.title())
    parent_name = f"{random.choice(['Mr.', 'Mrs.'])} {name.split()[-1]}"
    home_phone = "+91 3{}".format(random.randint(100000000, 999999999))
    work_phone = "+91 4{}".format(random.randint(100000000, 999999999))
    cell_phone = applicant.get("Phone", "+91 9{}".format(random.randint(100000000, 999999999)))
    # Emergency contacts
    emergency_contacts = [
        (f"{random.choice(['Mr.', 'Mrs.', 'Ms.'])} {random.choice(['Sharma', 'Patel', 'Reddy', 'Khan', 'Ghosh', 'Roy'])}", "+91-8{}".format(random.randint(100000000, 999999999)))
        for _ in range(2)
    ]
    # Health insurance
    insurance = random.choice(INSURANCE_COMPANIES)
    insurance_phone = "+91-7{}".format(random.randint(100000000, 999999999))
    group_number = str(random.randint(100000, 999999))
    id_number = str(random.randint(10000000, 99999999))
    physician = random.choice(PHYSICIANS)
    physician_phone = "+91 6{}".format(random.randint(100000000, 999999999))
    authorized_pickup = f"{random.choice(['Mr.', 'Mrs.', 'Ms.'])} {random.choice(['Sharma', 'Patel', 'Reddy', 'Khan', 'Ghosh', 'Roy'])}"
    # Special concerns
    special_concerns = random.choice([
        "None", "Peanut allergy", "Asthma", "Diabetes", "Requires inhaler", "Lactose intolerant"
    ])

    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "childsname":
            value = name
        elif k == "dateofbirth":
            value = dob
        elif k == "address":
            value = address
        elif k == "city":
            value = city
        elif k == "zip":
            value = zip_code
        elif k == "emailaddress":
            value = email
        elif k == "age":
            value = age
        elif k == "lastschoolgradecompleted":
            value = last_grade
        elif k == "malefemale":
            value = gender.title()
        elif k == "parentguardiansname":
            value = parent_name
        elif k == "homephone":
            value = home_phone
        elif k == "workphone":
            value = work_phone
        elif k == "cellphone":
            value = cell_phone
        elif k == "incaseofemergencycontact":
            value = emergency_contacts[0][0]
        elif k == "phone":
            # There are two phone fields for emergency contacts
            if idx > 0 and keys_with_lines[idx-1][0].strip().lower().startswith("in case of emergency"):
                value = emergency_contacts[0][1]
            elif idx > 1 and keys_with_lines[idx-2][0].strip().lower().startswith("in case of emergency"):
                value = emergency_contacts[1][1]
            elif keys_with_lines[idx-1][0].strip().lower().startswith("physician"):
                value = physician_phone
            elif keys_with_lines[idx-1][0].strip().lower().startswith("health insurance"):
                value = insurance_phone
            else:
                value = work_phone
        elif k == "specialconcernsallergiesmedicationsmedicalconditionsetc":
            value = special_concerns
        elif k == "healthinsurancecompany":
            value = insurance
        elif k == "groupnumber":
            value = group_number
        elif k == "idnumber":
            value = id_number
        elif k == "physiciansname":
            value = physician
        elif k == "personsauthorizedtopickupchild":
            value = authorized_pickup
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_35.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_35_filled.txt')
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