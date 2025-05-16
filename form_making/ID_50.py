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

RELIGIONS = ["Hindu", "Muslim", "Christian", "Sikh", "Jain", "Buddhist"]
CASTE_CATEGORIES = ["General", "OBC", "SC", "ST"]
COURSES = ["Science", "Commerce", "Arts", "Computer Science", "Mathematics", "Biology"]
MEDIUMS = ["English", "Hindi", "Bengali", "Marathi"]


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
    full_name = applicant["Full Name"].split()
    # Assume first and last word as first name and surname
    student_first = full_name[0].title()
    student_surname = full_name[-1].title() if len(full_name) > 1 else "Kumar"
    father_first = random.choice(["Ashok", "Raj", "Sumit", "Amitabha", "Tapash", "Suresh", "Ramesh", "Sanjay", "Vikram"])
    father_surname = student_surname
    dob_dt = datetime.date.today() - datetime.timedelta(days=random.randint(5000, 7000))
    dob = dob_dt.strftime("%d")
    dob_month = dob_dt.strftime("%B")
    dob_year = dob_dt.strftime("%Y")
    gender = applicant.get("Gender", gender_choice.title())
    nationality = "Indian"
    religion = random.choice(RELIGIONS)
    caste = random.choice(CASTE_CATEGORIES)
    father_occupation = random.choice(["Engineer", "Teacher", "Doctor", "Businessman", "Accountant", "Manager", "Professor", "Shopkeeper"])
    course = random.choice(COURSES)
    medium = random.choice(MEDIUMS)
    city = applicant.get("Town/City/District", applicant.get("City", ""))
    po_ps = city  # For simplicity, use city as PO/PS
    state = applicant.get("State/Province", "West Bengal")
    phone = applicant.get("Phone", "")

    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "studentsfirstname":
            value = student_first
        elif k == "studentssurname":
            value = student_surname
        elif k == "fathersfirstname":
            value = father_first
        elif k == "fatherssurname":
            value = father_surname
        elif k == "dobdate":
            value = dob
        elif k == "month":
            value = dob_month
        elif k == "year":
            value = dob_year
        elif k == "gender":
            value = gender.title()
        elif k == "nationality":
            value = nationality
        elif k == "religion":
            value = religion
        elif k == "castecategory":
            value = caste
        elif k == "fathersoccupation":
            value = father_occupation
        elif k == "courseappliedfor":
            value = course
        elif k == "medium":
            value = medium
        elif k == "city":
            value = city
        elif k == "pops":
            value = po_ps
        elif k == "state":
            value = state
        elif k == "phonenumber":
            value = phone
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_50.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_50_filled.txt')
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