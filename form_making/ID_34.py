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

EXAMS = [
    "B.A. in English 1st Year 1st Sem. Supple", "B.Sc. in Physics 2nd Year 2nd Sem.", "B.Tech in CSE 3rd Year 1st Sem.",
    "M.A. in History 1st Year 2nd Sem.", "M.Sc. in Chemistry 2nd Year 1st Sem.", "Ph.D. in Mathematics 1st Year"
]
REASONS = [
    "Correction of Name", "Correction of Registration No.", "Revision of CGPA", "Revision of BPX", "Correction of Class Roll No."
]
COURSES = [
    "B.A. in English", "B.Sc. in Physics", "B.Tech in CSE", "M.A. in History", "M.Sc. in Chemistry", "Ph.D. in Mathematics"
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
    # 60% male, 40% female profile selection
    males = [p for p in person_profiles if p.get('Gender', '').lower() == 'male']
    females = [p for p in person_profiles if p.get('Gender', '').lower() == 'female']
    if random.random() < 0.6 and males:
        person = random.choice(males)
    elif females:
        person = random.choice(females)
    else:
        person = random.choice(person_profiles)
    name = person["Full Name"].upper()
    reg_no = f"JU{random.randint(100000,999999)}/20{random.randint(10,23)}"
    session = f"20{random.randint(18,22)}-{random.randint(19,23)}"
    class_roll = random.randint(1, 120)
    contact = person["Phone"].replace("-", " ")
    email = person["Email"]
    exam = random.choice(EXAMS)
    reason = random.choice(REASONS)
    course = random.choice(COURSES)
    today = datetime.date.today().strftime("%d/%m/%Y")
    form_data = {}
    official_names = ["Mr. S. Ghosh", "Ms. P. Roy", "Dr. A. Banerjee", "Mr. R. Dutta", "Ms. N. Sen"]
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameoftheexaminationegbainenglishstyearstsemsupple":
            value = exam
        elif k == "respectivesessionyear":
            value = session
        elif k == "reasonforcorrectioneg":
            value = reason
        elif k == "nameincapitalletters":
            value = name
        elif k == "registrationnowithitssession":
            value = reg_no
        elif k == "classrollno":
            value = class_roll
        elif k == "contactnopreferablyamobileno":
            value = contact
        elif k == "e-mailaddress":
            value = email
        elif k == "date":
            value = today
        elif k == "signature":
            value = name
        elif k == "receivedanapplicationforcorrectedrevisedgradecardsmark-sheetsfrom":
            value = name
        elif k == "astudentof":
            value = exam
        elif k == "courseofstudyhavingregistrationno":
            value = reg_no
        elif k == "of":
            value = session
        elif k == "date":
            value = today
        elif k == "signatureofofficialexaminationoffice":
            value = random.choice(official_names)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_34.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_34_filled.txt')
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