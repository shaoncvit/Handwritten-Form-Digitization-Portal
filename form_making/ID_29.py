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

UNITS = ["Statistics Division", "Mathematics Division", "Computer Science Division", "Economics Division", "Quality Management Division"]
REASONS = ["Medical leave", "Conference attendance", "Personal work", "Family emergency", "Research visit"]
SUPERVISORS = ["Dr. S. Banerjee", "Prof. A. Sen", "Dr. R. Das", "Prof. M. Iyer"]
WARDENS = ["Mr. P. Kumar", "Ms. R. Das"]
DEANS = ["Dr. P. Chatterjee", "Prof. S. Rao"]


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
    person = random.choice(person_profiles)
    name = person["Full Name"]
    leave_days = random.randint(1, 15)
    leave_start = datetime.date.today() + datetime.timedelta(days=random.randint(1, 30))
    leave_end = leave_start + datetime.timedelta(days=leave_days-1)
    leave_dates = f"{leave_start.strftime('%d/%m/%Y')} to {leave_end.strftime('%d/%m/%Y')}"
    reason = random.choice(REASONS)
    address_on_leave = person["Address"]
    unit = random.choice(UNITS)
    today = datetime.date.today().strftime("%d/%m/%Y")
    supervisor = random.choice(SUPERVISORS)
    warden = random.choice(WARDENS)
    dean = random.choice(DEANS)
    prev_leave_count = random.randint(0, 3)
    prev_leave_days = random.randint(0, 20)
    office_verified = random.choice(["Ms. S. Ghosh", "Mr. A. Dutta", "Ms. P. Roy"])
    office_remarks = random.choice(["No objection", "Leave within permissible limits", "Check previous records"])
    leave_granted = random.choice(["granted", "not granted"])
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "name":
            value = name
        elif k == "leaverequiredfor":
            value = leave_days
        elif k == "daysondates":
            value = leave_dates
        elif k == "reason":
            value = reason
        elif k == "addresswhileonleave":
            value = address_on_leave
        elif k == "signature":
            value = name
        elif k == "unit":
            value = unit
        elif k == "date":
            value = today
        elif k == "signatureofsupervisorconvenerrfadvisorycommitteelheadofunitprofessor-in-charge":
            value = supervisor
        elif k == "signatureofwardenforhosteller":
            value = warden
        elif k == "numberofpreviousleaveapplicationduringtheyear":
            value = prev_leave_count
        elif k == "totalleavenoofdaysalreadytakenduringtheyear":
            value = prev_leave_days
        elif k == "enteredandverifiedby":
            value = office_verified
        elif k == "remarks":
            value = office_remarks
        elif k == "leavegrantednotgranted":
            value = leave_granted
        elif k == "deanofstudies":
            value = dean
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_29.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_29_filled.txt')
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