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
    "M.Sc. Physics", "M.Sc. Chemistry", "M.Sc. Mathematics", "M.A. English", "M.A. History", "M.A. Political Science", "MCA", "MBA", "M.Tech Computer Science", "M.Tech Electronics", "PhD Physics", "PhD Life Sciences", "PhD Economics", "Integrated M.Sc.-PhD Biology"
]

FATHERS = [
    "Rajesh Kumar", "Suresh Singh", "Amitabh Das", "Prakash Chandra", "Rameshwar Sharma", "Sanjay Patel", "Vijay Menon", "Anil Reddy", "Subhash Ghosh", "Manoj Joshi"
]

DEPARTMENTS = [
    "School of Physics", "School of Chemistry", "School of Mathematics", "Department of English", "Department of History", "Department of Political Science", "School of Computer and Information Sciences", "School of Management Studies", "School of Life Sciences", "School of Economics"
]

PLACES = [
    "Hostel Block A", "Library", "Canteen", "Main Gate", "Bus Stop", "Department Building", "Sports Complex", "Classroom 203", "Parking Area"
]

EFFORTS = [
    "Yes, searched the area but could not find it.",
    "Yes, enquired with security and friends, but not found.",
    "No, realized the loss after returning to hostel.",
    "Yes, checked lost and found, but not recovered."
]

FEES_PAID = ["200", "250", "50", "100", "150"]

SIGNATURES = [
    "(Signed) Student", "(Signed) Dean", "(Signed) Head of Dept.", "(Signed) Deputy Registrar"
]

NOTE_TEXTS = [
    "Submit a copy of the loss certificate issued by the Police Station.",
    "Application processed as per university rules.",
    "Contact the admin office for further queries.",
    "All details verified and approved."
]

FEES_TEXTS = [
    "Duplicate ID card Rs. 200/-; Semester Card Rs. 50/-", "Duplicate ID card Rs. 250/-; Semester Card Rs. 50/-"]

FACULTY_NAMES = [
    "Dr. Anil Kumar", "Dr. Priya Sharma", "Dr. Suresh Reddy", "Dr. Meena Iyer", "Dr. Rajiv Menon", "Dr. Kavita Das", "Dr. Arvind Joshi", "Dr. Sunita Rao", "Dr. Manoj Singh", "Dr. Neha Gupta"
]

def extract_keys_with_lines(form_text):
    # Extract (key, line_no) for all fields with colon
    field_pattern = re.compile(r"^([0-9A-Za-z&/()' .\-]+):", re.MULTILINE)
    keys = []
    for idx, line in enumerate(form_text.splitlines()):
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append((key, idx))
    return keys

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    full_name = person.get("Full Name", "")
    father = random.choice(FATHERS)
    reg_no = f"UH{random.randint(201700000, 202399999)}"
    course = random.choice(COURSES)
    validity = f"{random.randint(2021,2023)}-{random.randint(2024,2026)}"
    lost_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 60))).strftime("%d-%m-%Y")
    lost_place = random.choice(PLACES)
    effort = random.choice(EFFORTS)
    fees = random.choice(FEES_PAID)
    today = datetime.date.today().strftime("%d-%m-%Y")
    dean_head = random.choice(DEPARTMENTS)
    signature_student = full_name
    signature_dean = random.choice(FACULTY_NAMES)
    signature_registrar = random.choice(FACULTY_NAMES)
    printed_on = (datetime.date.today() + datetime.timedelta(days=random.randint(1, 3))).strftime("%d-%m-%Y")
    printed_by = random.choice(["Admin Staff", "Office Assistant", "Registrar Office"])
    note = random.choice(NOTE_TEXTS)
    fees_text = random.choice(FEES_TEXTS)

    # Track which field is which by order for repeated fields
    date_fields = [i for i, (k, _) in enumerate(keys_with_lines) if k.strip().lower() == "date"]
    filled_dates = {}
    if len(date_fields) >= 2:
        filled_dates[date_fields[0]] = today  # Application date
        filled_dates[date_fields[1]] = printed_on  # Approval/print date
    elif len(date_fields) == 1:
        filled_dates[date_fields[0]] = today

    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        key_lower = key.replace(" ","").replace("_","").replace("/","").replace(",","").replace(".","").replace("'","").replace("(&e)","").lower()
        # Special handling for repeated Date fields
        if idx in filled_dates:
            form_data[key] = filled_dates[idx]
        elif "registrationno" in key_lower:
            form_data[key] = reg_no
        elif "nameofthestudent" in key_lower:
            form_data[key] = full_name
        elif "fathersname" in key_lower:
            form_data[key] = father
        elif "coursesubject" in key_lower:
            form_data[key] = course
        elif "validityofthelostsemestercard" in key_lower:
            form_data[key] = validity
        elif "dateonwhichidsemestercardwaslostandplacewhereitwaslost" in key_lower:
            form_data[key] = f"{lost_date}, {lost_place}"
        elif "statewhetheranyeffortismadetotrace" in key_lower:
            form_data[key] = effort
        elif "detailsoffeespaid" in key_lower:
            form_data[key] = f"Rs. {fees}/- paid online"
        elif "signatureofthestudent" in key_lower:
            form_data[key] = signature_student
        elif "recommendationofthedeanoftheschoolheadofthedept" in key_lower:
            form_data[key] = dean_head
        elif "signatureofthedeanheadwithofficeseal" in key_lower:
            form_data[key] = signature_dean
        elif "deputyregistrarae" in key_lower or "deputyregistrar" in key_lower:
            form_data[key] = signature_registrar
        elif "idsemestercardprintedon" in key_lower:
            form_data[key] = printed_on
        elif key_lower == "by":
            form_data[key] = printed_by
        elif "receivedtheidsemestercard" in key_lower:
            form_data[key] = signature_student
        elif key_lower == "note":
            form_data[key] = note
        elif key_lower == "fees":
            form_data[key] = fees_text
        else:
            form_data[key] = ""
    return form_data

def fill_form_text(form_text, form_data):
    def replacer(match):
        key = match.group(1).strip()
        value = form_data.get(key, "")
        return f"{key}: {value}"
    field_pattern = re.compile(r"^([0-9A-Za-z&/()' .\-]+):.*$", re.MULTILINE)
    filled_text = field_pattern.sub(replacer, form_text)
    return filled_text

def main():
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_9.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_9_filled.txt')
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
