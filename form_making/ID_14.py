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

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
GENDERS = ["Male", "Female"]
MARITAL_STATUSES = ["Married", "Single"]
STATES = list(STATE_SCHOOLS.keys()) + [
    "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Kerala", "Maharashtra", "West Bengal", "Uttar Pradesh", "Delhi", "Gujarat", "Punjab", "Rajasthan"
]

EXAMS = [
    "10th", "12th", "B.Sc.", "B.A.", "B.Com.", "B.Tech", "BBA", "BCA", "M.Sc.", "M.A.", "M.Com.", "M.Tech", "MBA", "MCA"
]

BOARDS = [
    "CBSE", "ICSE", "State Board", "University of Delhi", "University of Calcutta", "Jadavpur University", "Osmania University", "Anna University", "Savitribai Phule Pune University"
]

SUBJECTS = [
    "Physics", "Chemistry", "Mathematics", "English", "History", "Political Science", "Computer Science", "Electronics", "Life Sciences", "Economics", "Commerce", "Management"
]

FATHER_FIRST_NAMES = [
    "Rajesh", "Amit", "Suresh", "Anil", "Vijay", "Sanjay", "Rakesh", "Manoj", "Prakash", "Sunil", "Arun", "Ravi", "Deepak", "Ajay", "Ashok"
]
MOTHER_FIRST_NAMES = [
    "Sunita", "Anita", "Suman", "Kavita", "Neeta", "Poonam", "Rekha", "Seema", "Shobha", "Meena", "Renu", "Geeta", "Anjali", "Neelam", "Priya"
]

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
    father_first = random.choice(FATHER_FIRST_NAMES)
    mother_first = random.choice(MOTHER_FIRST_NAMES)
    father = f"{father_first} {surname}"
    mother = f"{mother_first} {surname}"
    state = person.get("State", random.choice(STATES))
    schools_for_state = STATE_SCHOOLS.get(state, list(STATE_SCHOOLS.values())[0])
    school = random.choice(schools_for_state)
    address = person.get("Address", "123 Main Road, City, State, 123456")
    phone = person.get("Phone", f"+91-{random.randint(7000000000, 9999999999)}")
    # Try to get gender from profile, else infer from first name
    if "Gender" in person:
        gender = person["Gender"]
    else:
        first_name = full_name.split()[0]
        if first_name in FATHER_FIRST_NAMES:
            gender = "Male"
        elif first_name in MOTHER_FIRST_NAMES:
            gender = "Female"
        else:
            gender = random.choice(GENDERS)
    marital_status = random.choice(MARITAL_STATUSES)
    dob = person.get("DOB", (datetime.date.today() - datetime.timedelta(days=random.randint(8000, 12000))).strftime("%d-%m-%Y"))
    dob_dt = datetime.datetime.strptime(dob, "%d-%m-%Y")
    dob_day = dob_dt.day
    dob_month = dob_dt.strftime("%B")
    dob_year = dob_dt.year
    # Academic record
    exam = random.choice(EXAMS)
    year_of_passing = random.randint(2010, 2023)
    board = random.choice(BOARDS)
    marks_obtained = random.randint(300, 495)
    total_marks = 500
    percent = round((marks_obtained / total_marks) * 100, 2)
    subject = random.choice(SUBJECTS)
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "nameinfullblockletters":
            value = full_name
        elif k == "fathersguardiansname":
            value = father
        elif k == "permanenthomeaddress":
            value = address
        elif k == "presentmailingaddress":
            value = address
        elif k == "telephonenowithstdcode":
            value = phone
        elif k == "m":
            value = phone[-10:]
        elif k == "sex":
            value = gender
        elif k == "maritalstatus":
            value = marital_status
        elif k == "dateofbirth":
            value = dob
        elif k == "date":
            value = dob_day
        elif k == "month":
            value = dob_month
        elif k == "year":
            value = dob_year
        elif k == "presentlyenrolledincollegeldepartmentofuniversitygivecompletedetailsincludingrollno":
            value = f"{school}, Roll No: {random.randint(100000,999999)}"
        elif k == "examinationpassed":
            value = exam
        elif k == "yearofpassing":
            value = year_of_passing
        elif k == "boarduniversity":
            value = board
        elif k == "marksobtained":
            value = marks_obtained
        elif k == "totalmarks":
            value = total_marks
        elif k == "%ageofmarksobtained":
            value = percent
        elif k == "subjects":
            value = subject
        # If block/capital letter is requested, convert to uppercase if value is string
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_14.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_14_filled.txt')
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