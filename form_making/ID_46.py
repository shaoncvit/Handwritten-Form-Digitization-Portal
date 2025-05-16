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

COURSES = [
    "M.Sc. Physics", "M.A. English", "M.Tech. CSE", "MBA", "Ph.D. Chemistry", "M.Sc. Mathematics"
]
REASONS = [
    "Course completion", "Withdrawal of admission", "Personal reasons"
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
    course = random.choice(COURSES)
    enrol_no = f"ENR{random.randint(100000,999999)}"
    date_join = (datetime.date.today() - datetime.timedelta(days=random.randint(365, 1460))).strftime("%d/%m/%Y")
    date_leave = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 364))).strftime("%d/%m/%Y")
    reason = random.choice(REASONS)
    lib_deposit = str(random.randint(500, 2000))
    lab_deposit = str(random.randint(500, 2000))
    hostel_deposit = str(random.randint(500, 2000))
    address = ', '.join([
        student.get("Flat/Door/Block No", ""),
        student.get("Premises", ""),
        student.get("Road/Street/Lane", ""),
        student.get("Area/Locality", ""),
        student.get("Town/City/District", "")
    ])
    sb_ac = f"{random.randint(10000000000,99999999999)}"
    today = datetime.date.today().strftime("%d/%m/%Y")
    hod = f"Dr. {random.choice(['Rao', 'Sharma', 'Gupta', 'Iyer', 'Patel'])}"
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameofthestudent":
            value = name
        elif k == "coursesubject":
            value = course
        elif k == "enrolmentnumber":
            value = enrol_no
        elif k == "dateofjoiningofthecourse":
            value = date_join
        elif k == "dateofleavingofthecourse":
            value = date_leave
        elif k == "reasonsforleavingcoursecompletionwithdrawalofadmissionetc":
            value = reason
        elif k == "alibrarydepositl":
            value = lib_deposit
        elif k == "blaboratorydeposit":
            value = lab_deposit
        elif k == "chosteldepositifany":
            value = hostel_deposit
        elif k == "mailingaddresstoreceivebackcautiondeposit":
            value = address
        elif k == "sbihcubracno":
            value = sb_ac
        elif k == "signatureofthestudent":
            value = name
        elif k == "signatureoftheheadofthedepartmentcentredeanoftheschool":
            value = hod
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_46.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_46_filled.txt')
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