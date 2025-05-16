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

STATE_SCHOOLS = {
    "West Bengal": [
        "Jadavpur University",
        "University of Calcutta",
        "Presidency University, Kolkata"
    ],
    "Delhi": [
        "University of Delhi",
        "Jawaharlal Nehru University",
        "Jamia Millia Islamia"
    ],
    "Telangana": [
        "University of Hyderabad",
        "Osmania University"
    ],
    "Tamil Nadu": [
        "Anna University",
        "Madras Christian College",
        "Loyola College, Chennai"
    ],
    "Maharashtra": [
        "Savitribai Phule Pune University",
        "Fergusson College, Pune"
    ],
    "Karnataka": [
        "Manipal Academy of Higher Education"
    ],
    "Uttar Pradesh": [
        "Aligarh Muslim University"
    ],
    "Punjab": [
        "Panjab University",
        "Guru Nanak Dev University"
    ],
    "Gujarat": [
        "Indian Institute of Technology Gandhinagar"
    ],
    "Rajasthan": [
        "Birla Institute of Technology and Science, Pilani"
    ],
    "Andhra Pradesh": [
        "Andhra University"
    ],
    "Kerala": [
        "Amrita Vishwa Vidyapeetham"
    ],
    # Add more as needed
}

FATHER_FIRST_NAMES = [
    "Rajesh", "Amit", "Suresh", "Anil", "Vijay", "Sanjay", "Rakesh", "Manoj", "Prakash", "Sunil", "Arun", "Ravi", "Deepak", "Ajay", "Ashok"
]
MOTHER_FIRST_NAMES = [
    "Sunita", "Anita", "Suman", "Kavita", "Neeta", "Poonam", "Rekha", "Seema", "Shobha", "Meena", "Renu", "Geeta", "Anjali", "Neelam", "Priya"
]
OCCUPATIONS = [
    "Teacher", "Engineer", "Doctor", "Businessman", "Government Employee", "Farmer", "Shopkeeper", "Accountant", "Manager", "Clerk"
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
GENDERS = ["Male", "Female"]
NATIONALITIES = ["Indian"]
STATES = list(STATE_SCHOOLS.keys()) + [
    "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Kerala", "Maharashtra", "West Bengal", "Uttar Pradesh", "Delhi", "Gujarat", "Punjab", "Rajasthan"
]

UNIVERSITIES = [
    u for schools in STATE_SCHOOLS.values() for u in schools
]

INCOMES = ["1,50,000", "2,00,000", "3,00,000", "4,50,000", "5,00,000", "6,00,000", "8,00,000", "10,00,000"]


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

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    full_name = person["Full Name"]
    surname = full_name.split()[-1]
    # Gender logic: try to infer from first name
    first_name = full_name.split()[0]
    if "Gender" in person:
        gender = person["Gender"]
    elif first_name in FATHER_FIRST_NAMES:
        gender = "Male"
    elif first_name in MOTHER_FIRST_NAMES:
        gender = "Female"
    else:
        gender = random.choice(GENDERS)
    father_first = random.choice(FATHER_FIRST_NAMES)
    father = f"{father_first} {surname}"
    occupation = random.choice(OCCUPATIONS)
    income = random.choice(INCOMES)
    state = person.get("State", random.choice(STATES))
    address = person.get("Address", "123 Main Road, City, State, 123456")
    phone = person.get("Phone", f"+91-{random.randint(7000000000, 9999999999)}")
    dob = person.get("DOB", (datetime.date.today() - datetime.timedelta(days=random.randint(8000, 12000))).strftime("%d-%m-%Y"))
    dob_dt = datetime.datetime.strptime(dob, "%d-%m-%Y")
    dob_day = dob_dt.day
    dob_month = dob_dt.strftime("%B")
    dob_year = dob_dt.year
    university = random.choice(STATE_SCHOOLS.get(state, UNIVERSITIES))
    year_of_passing = random.randint(2015, 2023)
    nationality = person.get("Nationality", "Indian")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "nameoftheapplicantincapitalletters":
            value = full_name
        elif k == "afathersnameincapitalletters":
            value = father
        elif k == "bdesignationoccupation":
            value = occupation
        elif k == "cannualincomeofthefatherguardian":
            value = income
        elif k == "dateofbirth":
            value = dob
        elif k == "day":
            value = dob_day
        elif k == "month":
            value = dob_month
        elif k == "year":
            value = dob_year
        elif k == "aaddressforcorrespondence":
            value = address
        elif k == "bpermanentaddress":
            value = address
        # elif k == "ccontacttelnorstdcode":
        #     value = phone
        elif k == "ccontacttelnorstdcode":
            value = "0191" + phone[-8:] # Jammu STD code as example
        elif k == "m":
            value = phone[-9:]
        elif k == "tickwhicheverisapplicablesex":
            value = gender
        elif k == "universityfromwhichthebachelorsdegreecompleted":
            value = university
        elif k == "yearofpassing":
            value = year_of_passing
        elif k == "nationality":
            value = nationality
        elif k == "stateofdomicile":
            value = state
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_15.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_15_filled.txt')
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