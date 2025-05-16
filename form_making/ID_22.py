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

FATHER_FIRST_NAMES = [
    "Rajesh", "Amit", "Suresh", "Anil", "Vijay", "Sanjay", "Rakesh", "Manoj", "Prakash", "Sunil", "Arun", "Ravi", "Deepak", "Ajay", "Ashok"
]
MOTHER_FIRST_NAMES = [
    "Sunita", "Anita", "Suman", "Kavita", "Neeta", "Poonam", "Rekha", "Seema", "Shobha", "Meena", "Renu", "Geeta", "Anjali", "Neelam", "Priya"
]
GENDERS = ["Male", "Female"]
CITIES = ["Jammu", "Srinagar", "Udhampur", "Baramulla", "Kathua", "Poonch", "Rajouri", "Anantnag", "Pulwama", "Doda"]
DEPARTMENTS = [
    "Physics", "Chemistry", "Mathematics", "English", "History", "Political Science", "Computer Science", "Electronics", "Life Sciences", "Economics"
]
DESIGNATIONS = [
    "Assistant Professor", "Associate Professor", "Professor", "Lecturer", "Reader", "Head of Department"
]
CATEGORIES = ["SC", "ST", "OBC", "General", "EWS"]
NATIONALITIES = ["Indian"]


def normalize_key(key):
    return re.sub(r"[\s_/,.\(\)'0-9]", "", key.strip().lower())

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

def random_name():
    first = random.choice(FATHER_FIRST_NAMES + MOTHER_FIRST_NAMES)
    last = random.choice(["Sharma", "Singh", "Gupta", "Raina", "Koul", "Choudhary", "Rathore", "Verma", "Kumar", "Pandit"])
    return f"{first} {last}"

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    applicant_name = random_name()
    parent_name = f"{random.choice(FATHER_FIRST_NAMES + MOTHER_FIRST_NAMES)} {applicant_name.split()[-1]}"
    department = random.choice(DEPARTMENTS)
    designation = random.choice(DESIGNATIONS)
    grade = random.choice(["Academic Level 10", "Academic Level 11", "Academic Level 12", "Academic Level 13A"])
    last_promotion = (datetime.date.today() - datetime.timedelta(days=random.randint(365, 2000))).strftime("%d-%m-%Y")
    position_applied = random.choice(DESIGNATIONS)
    eligibility_date = (datetime.date.today() - datetime.timedelta(days=random.randint(30, 365))).strftime("%d-%m-%Y")
    dob = person.get("DOB", (datetime.date.today() - datetime.timedelta(days=random.randint(12000, 20000))).strftime("%d-%m-%Y"))
    dob_place = random.choice(CITIES)
    sex = random.choice(["Male", "Female"])
    marital_status = random.choice(["Married", "Unmarried"])
    nationality = person.get("Nationality", "Indian")
    category = random.choice(CATEGORIES)
    address_corr = person.get("Address", random.choice(CITIES) + ", Jammu & Kashmir, 180001")
    address_perm = person.get("Address", random.choice(CITIES) + ", Jammu & Kashmir, 180001")
    contact_no = f"+91 {random.randint(7000000000, 9999999999)}"
    email = f"{applicant_name.split()[0].lower()}@gmail.com"
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "nameinblockletter":
            value = applicant_name
        elif k == "fathersnamemothersname":
            value = parent_name
        elif k == "department":
            value = department
        elif k == "currentdesignation&grade":
            value = f"{designation}, {grade}"
        elif k == "dateoflastpromotion":
            value = last_promotion
        elif k == "whichpositionandgradepayareyouanapplicantundercas":
            value = position_applied
        elif k == "dateofeligibilityforpromotion":
            value = eligibility_date
        elif k == "dateandplaceofbirth":
            value = f"{dob}, {dob_place}"
        elif k == "sex":
            value = sex
        elif k == "maritalstatus":
            value = marital_status
        elif k == "nationality":
            value = nationality
        elif k == "indicatewhetherbelongstoscstobccategory":
            value = category
        elif k == "addressforcorrespondencewithpincode":
            value = address_corr
        elif k == "apermanentaddresswithpincode":
            value = address_perm
        elif k == "bcontactno":
            value = contact_no
        elif k == "cemail":
            value = email
        else:
            value = ""
        if is_block and isinstance(value, str):
            value = value.upper()
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_22.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_22_filled.txt')
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