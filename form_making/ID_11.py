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
    "B.Sc. (Hons) Physics", "B.A. (Hons) English", "B.E. Electrical Engineering", "M.A. History", "M.Sc. Chemistry", "B.Tech Computer Science", "M.Tech Electronics"
]

CLEARANCE_REPORTS = {
    1: ["No dues pending.", "All dues cleared."],
    2: ["Not a hostel boarder.", "Hostel boarder, no dues."],
    3: ["No hostel dues.", "Not applicable (not a boarder)."],
    4: ["No dues including hostel.", "All accounts clear."],
    5: ["No library dues. All books returned.", "All books returned, no dues."],
    6: ["No placement cell dues.", "No dues."]
}

FACULTY_NAMES = [
    "Dr. Anil Kumar", "Dr. Priya Sharma", "Dr. Suresh Reddy", "Dr. Meena Iyer", "Dr. Rajiv Menon", "Dr. Kavita Das", "Dr. Arvind Joshi", "Dr. Sunita Rao", "Dr. Manoj Singh", "Dr. Neha Gupta"
]

EMAILS = [p["Email"] for p in person_profiles if "Email" in p]
MOBILES = [p["Phone"] for p in person_profiles if "Phone" in p]


def extract_keys_with_lines(form_text):
    field_pattern = re.compile(r"^([0-9A-Za-z&/()' .\-]+):", re.MULTILINE)
    keys = []
    for idx, line in enumerate(form_text.splitlines()):
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append((key, idx))

    # print(keys)
    return keys

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    full_name = person["Full Name"]
    course = random.choice(COURSES)
    year = str(random.randint(2021, 2024))
    exam_roll = f"EX{random.randint(100000, 999999)}"
    review = random.choice(["Yes", "No"])
    regn = f"JU{random.randint(201700000, 202399999)}"
    regn_session = f"{random.randint(2019, 2022)}-{random.randint(2023, 2025)}"
    class_roll = str(random.randint(1, 120))
    email = person.get("Email", random.choice(EMAILS))
    mobile = person.get("Phone", random.choice(MOBILES))
    today = datetime.date.today().strftime("%d-%m-%Y")
    signature = full_name
    coe_officer = random.choice(FACULTY_NAMES)
    clearance = {
        1: random.choice(CLEARANCE_REPORTS[1]),
        2: random.choice(CLEARANCE_REPORTS[2]),
        3: random.choice(CLEARANCE_REPORTS[3]),
        4: random.choice(CLEARANCE_REPORTS[4]),
        5: random.choice(CLEARANCE_REPORTS[5]),
        6: random.choice(CLEARANCE_REPORTS[6]),
    }
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        key_lower = key.strip().lower().replace(" ","").replace("_","").replace("/","").replace(",","").replace(".","").replace("'","")
        print(key_lower)
        if key_lower.startswith("name"):  # Name(in CAPITAL LETTERS)
            form_data[key] = full_name
        elif key_lower.startswith("courseofstudypassed"):
            form_data[key] = course
        elif key_lower.startswith("yearofpassing"):
            form_data[key] = year
        elif key_lower.startswith("examrollnooffinalsem"):
            form_data[key] = exam_roll
        elif key_lower.startswith("whetheralreadyorwillapplyforreview"):
            form_data[key] = review
        elif key_lower.startswith("registrationno"):
            form_data[key] = f"{regn} ({regn_session})"
        elif key_lower.startswith("classrollno"):
            form_data[key] = class_roll
        elif key_lower.startswith("emailaddress"):
            form_data[key] = email
        elif key_lower.startswith("mobileno"):
            form_data[key] = mobile
        elif key_lower.startswith("date"):
            form_data[key] = today
        elif key_lower.startswith("signatureofcandidate"):
            form_data[key] = signature
        elif key_lower.startswith("officeofthecoe"):
            form_data[key] = coe_officer
        elif key_lower == "1musterrollsection(pleasereporthisherdues)":
            form_data[key] = clearance[1]
        elif key_lower == "2deanofstudents(pleaseconfirmwhetherhelsheisahostelboarder)":
            form_data[key] = clearance[2]
        elif key_lower == "3hostelsupdt(pleaseconfirmwhetherhisherduesifhesheisahostelboarder)":
            form_data[key] = clearance[3]
        elif key_lower == "4accounts(pleasementionhisherduesincludinghosteldues)":
            form_data[key] = clearance[4]
        elif key_lower == "5librarian(pleasereport1hisherduesifany2whetherheshehasreturnallbooks)":
            form_data[key] = clearance[5]
        elif key_lower == "6placementcell(pleasereporthisherduesifany)":
            form_data[key] = clearance[6]
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_11.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_11_filled.txt')
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
