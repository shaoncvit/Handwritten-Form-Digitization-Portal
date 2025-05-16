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

POSTS = [
    "Clerk", "Junior Assistant", "Library Attendant", "Lab Attendant", "Data Entry Operator", "Peon"
]
DEPTS = [
    "Accounts", "Library", "Examination", "Administration", "Computer Centre", "Hostel Office"
]
NATIONALITIES = ["Indian"]
MARITALS = ["Single", "Married", "Divorced", "Widowed"]
CASTE = ["Yes", "No"]

QUALS = [
    ("Matric", "CBSE", "English, Hindi, Math, Science", "2012", "450/500", "First", "-"),
    ("10+2", "CBSE", "Physics, Chemistry, Math", "2014", "470/500", "First", "Scholarship"),
    ("B.Sc.", "Panjab University", "Physics, Math", "2017", "800/1000", "First", "Gold Medal"),
    ("M.Sc.", "Panjab University", "Physics", "2019", "850/1000", "First", "-"),
    ("M.Phil", "Panjab University", "Physics", "2021", "-", "-", "-"),
    ("Ph.D", "Panjab University", "Physics", "2023", "-", "-", "-"),
    ("Other", "-", "-", "-", "-", "-", "-")
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
    # Use a single applicant profile
    applicant = random.choice([p for p in person_profiles if p.get('Gender', '').lower() in ['male', 'female']])
    name = applicant["Full Name"].upper()
    father_name = f"Mr. {random.choice(['Ashok','Raj','Sumit','Amitabha','Tapash'])} {name.split()[-1]}"
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(25*365, 35*365))).strftime("%d/%m/%Y")
    pob = random.choice(["Chandigarh", "Ludhiana", "Amritsar", "Patiala", "Delhi"])
    nationality = random.choice(NATIONALITIES)
    marital = random.choice(MARITALS)
    caste = random.choice(CASTE)
    perm_addr = ', '.join([
        applicant.get("Flat/Door/Block No", ""),
        applicant.get("Premises", ""),
        applicant.get("Road/Street/Lane", ""),
        applicant.get("Area/Locality", ""),
        applicant.get("Town/City/District", "")
    ]).upper()
    pres_addr = applicant.get("Address", "").upper()
    phone = applicant.get("Phone", "")
    email = applicant.get("Email", "")
    min_pay = str(random.randint(20000, 40000))
    joining = f"{random.randint(7, 30)} days"
    post = random.choice(POSTS)
    advt_no = f"PU/{random.randint(100,999)}/2024"
    dept = random.choice(DEPTS)
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "serialno":
            value = f"PU{random.randint(1000,9999)}"
        elif k == "diaryno":
            value = f"D{random.randint(10000,99999)}"
        elif k == "date":
            value = datetime.date.today().strftime("%d/%m/%Y")
        elif k == "nameofthepost":
            value = post
        elif k == "advtno":
            value = advt_no
        elif k == "department":
            value = dept
        elif k == "anameinfullmrmrsmsincapitals":
            value = name
        elif k == "fathersname":
            value = father_name
        elif k == "dateofbirth":
            value = dob
        elif k == "placeofbirth":
            value = pob
        elif k == "nationality":
            value = nationality
        elif k == "maritalstatus":
            value = marital
        elif k == "memberofscheduledcastebackwardclass":
            value = caste
        elif k == "permanentaddressincapitals":
            value = perm_addr
        elif k == "presentaddressforcorrespondenceincapitals":
            value = pres_addr
        elif k == "mobiletelephone":
            value = phone
        elif k == "e-mail":
            value = email
        elif k == "cminimumpayacceptable":
            value = min_pay
        elif k == "joiningtimeifselected":
            value = joining
        elif k == "matric":
            value = f"CBSE, English, Hindi, Math, Science, {random.randint(2010,2015)}, {random.randint(400,490)}/500, First, -"
        elif k == "+pre-medpre-engg":
            value = f"12th, CBSE, PCM, {random.randint(2012,2017)}, {random.randint(450,490)}/500, First, -"
        elif k == "babscbcometc":
            value = f"B.Sc., {random.choice(['Delhi University', 'Panjab University'])}, {random.choice(['Physics', 'Chemistry', 'Math'])}, {random.randint(2015,2020)}, {random.randint(750,950)}/1000, First, {random.choice(['Gold Medal', 'Silver Medal', '-'])}"
        elif k == "mamscmcometc":
            value = f"M.Sc., {random.choice(['Delhi University', 'Panjab University'])}, {random.choice(['Physics', 'Chemistry', 'Math'])}, {random.randint(2017,2022)}, {random.randint(750,950)}/1000, First, {random.choice(['Gold Medal', 'Silver Medal', '-'])}"
        elif k == "mphil":
            value = f"M.Phil, {random.choice(['Delhi University', 'Panjab University'])}, {random.choice(['Physics', 'Chemistry', 'Math'])}, {random.randint(2019,2023)}, -, -, -"
        elif k == "phd":
            value = f"Ph.D, {random.choice(['Delhi University', 'Panjab University'])}, {random.choice(['Physics', 'Chemistry', 'Math'])}, {random.randint(2021,2024)}, -, -, -"
        elif k == "anyotherexampleasespecify":
            value = "Other, -, -, -, -, -, -"
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_44.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_44_filled.txt')
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