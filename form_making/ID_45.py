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

CATEGORIES = ["GE", "SC", "ST", "OBC", "PH", "DP"]
REASONS = [
    "Taking up an employment", "Financial Problems", "Non-availability of Hostel", "Personal Problems", "Other"
]
COURSES = [
    "M.Sc. Physics", "M.A. English", "M.Tech. CSE", "MBA", "Ph.D. Chemistry", "M.Sc. Mathematics"
]
BANKS = [
    "State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Bank of Baroda"
]
BRANCHES = [
    "Gachibowli", "Central University", "Hitech City", "Secunderabad", "Ameerpet"
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
    student = random.choice([p for p in person_profiles if p.get('Gender', '').lower() in ['male', 'female']])
    name = student["Full Name"]
    father_name = f"Mr. {random.choice(['Ashok','Raj','Sumit','Amitabha','Tapash'])} {name.split()[-1]}"
    course = random.choice(COURSES)
    category = random.choice(CATEGORIES)
    date_join = (datetime.date.today() - datetime.timedelta(days=random.randint(365, 1460))).strftime("%d/%m/%Y")
    hallticket = f"HT{random.randint(100000,999999)}"
    date_leave = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 364))).strftime("%d/%m/%Y")
    joining_univ = random.choice(["Yes", "No"])
    joining_course = random.choice(COURSES) if joining_univ == "Yes" else ""
    reason = random.choice(REASONS)
    other_reason = "" if reason != "Other" else "Migration to another city"
    fee_date = (datetime.date.today() - datetime.timedelta(days=random.randint(30, 365))).strftime("%d/%m/%Y")
    fee_amt = str(random.randint(1000, 20000))
    bank = random.choice(BANKS)
    acc_no = f"{random.randint(10000000000,99999999999)}"
    branch = random.choice(BRANCHES)
    ifsc = f"SBIN{random.randint(1000000,9999999)}"
    today = datetime.date.today().strftime("%d/%m/%Y")
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameofthestudent":
            value = name
        elif k == "fathersname":
            value = father_name
        elif k == "courseofstudy":
            value = course
        elif k == "category":
            value = category
        elif k == "dateofjoining":
            value = date_join
        elif k == "hallticketenrolno":
            value = hallticket
        elif k == "dateofleaving":
            value = date_leave
        elif k == "joininganotheruniversity":
            value = joining_univ
        elif k == "course":
            value = joining_course
        elif k == "reasonsforleavingpleasefilltickappropriatereason":
            value = reason
        elif k == "anyotherreasonpleasespecify":
            value = other_reason
        elif k == "tuitionandotherfeespaidondt":
            value = fee_date
        elif k == "rs":
            value = fee_amt
        elif k == "bankname":
            value = bank
        elif k == "bankaccountno":
            value = acc_no
        elif k == "branchnameandifsccode":
            value = f"{branch}, {ifsc}"
        elif k == "date":
            value = today
        elif k == "signatureofthestudent":
            value = name
        elif k == "deanoftheschoolheadofthedepartmentcentre":
            value = f"Dr. {random.choice(['Rao', 'Sharma', 'Gupta', 'Iyer', 'Patel'])}"
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_45.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_45_filled.txt')
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