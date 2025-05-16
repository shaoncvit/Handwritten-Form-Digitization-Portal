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

DEPTS = [
    "Physics", "Chemistry", "Mathematics", "Computer Science", "Botany", "Zoology", "History", "Economics"
]
CLASSES = [
    "B.Sc. 1st Year", "B.Sc. 2nd Year", "B.A. 1st Year", "B.A. 2nd Year", "M.Sc. 1st Year", "M.A. 1st Year"
]
CHAIR_NAMES = ["Dr. S. Kaur", "Prof. R. Sharma", "Dr. A. Singh", "Prof. M. Gupta", "Dr. P. Verma"]


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
    name = applicant["Full Name"]
    father_name = f"Mr. {random.choice(['Ashok','Raj','Sumit','Amitabha','Tapash'])} {name.split()[-1]}"
    mother_name = f"Mrs. {random.choice(['Devi', 'Kumari', 'Rani', 'Bala', 'Lata'])} {name.split()[-1]}"
    dept = random.choice(DEPTS)
    class_name = random.choice(CLASSES)
    roll_no = f"{random.randint(100,999)}"
    income = str(random.randint(20000, 120000))
    fee_total = str(random.randint(2000, 10000))
    fee_1 = str(random.randint(1000, int(fee_total)))
    fee_2 = str(int(fee_total) - int(fee_1))
    rec1 = f"R{random.randint(10000,99999)}"
    rec2 = f"R{random.randint(10000,99999)}"
    date1 = (datetime.date.today() - datetime.timedelta(days=random.randint(30, 90))).strftime("%d/%m/%Y")
    date2 = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 29))).strftime("%d/%m/%Y")
    amenities1 = random.choice(["None", "Merit Scholarship", "SC/ST Stipend", "Financial Assistance"])
    amenities2 = random.choice(["None", "Fee Concession", "Sports Quota"])
    today = datetime.date.today().strftime("%d/%m/%Y")
    chair = random.choice(CHAIR_NAMES)
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "session":
            value = f"2023-2024"
        elif k == "nameoftheapplicant":
            value = name
        elif k == "deptt":
            value = dept
        elif k == "class":
            value = class_name
        elif k == "rollno":
            value = roll_no
        elif k == "fathersname":
            value = father_name
        elif k == "mothersname":
            value = mother_name
        elif k == "totalfamilyincomepa":
            value = income
        elif k == "totalfeedepositedbythecandidaters":
            value = fee_total
        elif k == "astinstalmentrs":
            value = fee_1
        elif k == "receiptno":
            value = rec1
        elif k == "date":
            value = date1
        elif k == "bndinstalmentrs":
            value = fee_2
        elif k == "receiptno":
            value = rec2
        elif k == "date":
            value = date2
        elif k == "ischolarshipstipendfinancialassistanceifany":
            value = amenities1
        elif k == "iifeeconcessionifany":
            value = amenities2
        elif k == "signatureoftheapplicant":
            value = name
        elif k == "recommendedchairpersondirector":
            value = chair
        elif k == "signatureoftheheadofthedepttwithofficestamp":
            value = chair
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_42.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_42_filled.txt')
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