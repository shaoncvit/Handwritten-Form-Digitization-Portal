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
CATEGORIES = ["General", "OBC", "SC", "ST", "EWS"]
OTHER_CATEGORIES = ["PWD", "Sports Quota", "Defence"]
LOCALITIES = ["Urban", "Rural"]
PROGRAMMES = ["Bachelor of Education", "B.Ed.", "B.Sc.", "B.A.", "B.Com."]


def normalize_key(key):
    return re.sub(r"[\s_/,\.\(\)'0-9]", "", key.strip().lower())

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
    mother_first = random.choice(MOTHER_FIRST_NAMES)
    father = f"{father_first} {surname}"
    mother = f"{mother_first} {surname}"
    state = person.get("State", random.choice(STATES))
    address = person.get("Address", "123 Main Road, City, State, 123456")
    phone = person.get("Phone", f"+91-{random.randint(7000000000, 9999999999)}")
    dob = person.get("DOB", (datetime.date.today() - datetime.timedelta(days=random.randint(8000, 12000))).strftime("%d-%m-%Y"))
    dob_dt = datetime.datetime.strptime(dob, "%d-%m-%Y")
    dob_day = dob_dt.day
    dob_month = dob_dt.strftime("%B")
    dob_year = dob_dt.year
    programme = random.choice(PROGRAMMES)
    category = random.choice(CATEGORIES)
    other_category = random.choice(OTHER_CATEGORIES)
    blood_group = person.get("Blood Group", random.choice(BLOOD_GROUPS))
    marital_status = random.choice(["Married", "Unmarried"])
    nationality = person.get("Nationality", "Indian")
    locality = random.choice(LOCALITIES)
    pin_code = re.search(r"(\d{6})", address)
    pin_code = pin_code.group(1) if pin_code else str(random.randint(110001, 999999))
    dd_no = str(random.randint(100000, 999999))
    amount = random.choice(["1000", "1500", "2000"])
    bank_name = random.choice([
        "State Bank of India", "Punjab National Bank", "ICICI Bank", "HDFC Bank", "Axis Bank", "Bank of Baroda"
    ])
    dd_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k== "sno":
            value = str(random.randint(1, 100))
        elif k == "ddno":
            value = dd_no
        elif k == "amount":
            value = amount
        elif k == "bankname":
            value = bank_name
        elif k == "date":
            value = dd_date
        elif k == "programmename":
            value = programme
        elif k == "name":
            value = full_name
        elif k == "fathersname":
            value = father
        elif k == "mothersname":
            value = mother
        elif k == "aaddress":
            value = address
        elif k == "bpincode":
            value = pin_code
        elif k == "ccontactno":
            value = phone[-10:]
        elif k == "de-mailid":
            value = f"user{random.randint(1000,9999)}@gmail.com"
        elif k == "dob":
            value = dob
        elif k == "locality":
            value = locality
        elif k == "gendermf":
            value = gender[0]  # 'M' or 'F'
        elif k == "maritalstatus":
            value = marital_status
        elif k == "bloodgroup":
            value = blood_group
        elif k == "category":
            value = category
        elif k == "othercategory":
            value = other_category
        elif k == "nationality":
            value = nationality

        else:
            value = ""
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_16.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_16_filled.txt')
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