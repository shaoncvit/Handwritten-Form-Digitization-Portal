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

DEGREE_SUBJECTS = {
    "M.Sc.": ["Physics", "Chemistry", "Mathematics", "Computer Science", "Electronics", "Life Sciences"],
    "M.A.": ["English", "History", "Political Science", "Economics"],
    "M.Tech": ["Computer Science", "Electronics"],
    "M.Phil": ["Physics", "Chemistry", "Mathematics", "English", "History", "Electronics", "Life Sciences", "Economics"],
    "Ph.D.": ["Physics", "Chemistry", "Mathematics", "English", "History", "Political Science", "Computer Science", "Electronics", "Life Sciences", "Economics"],
    "MBA": ["Economics"],
    "MCA": ["Computer Science"],
}



BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
DIVISIONS = ["First", "Second", "Third"]
GENDERS = ["Male", "Female"]
NATIONALITIES = ["Indian"]
STATES = [
    "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu", "Kerala", "Maharashtra", "West Bengal", "Uttar Pradesh", "Delhi", "Gujarat", "Punjab", "Rajasthan"
]

COURSES = list(DEGREE_SUBJECTS.keys())

DEPARTMENTS = [
    "Department of Physics", "Department of Chemistry", "Department of Mathematics", "Department of English", "Department of History", "Department of Political Science", "Department of Computer Science", "Department of Electronics", "Department of Life Sciences", "Department of Economics"
]
SCHOOLS = [
    "Jawaharlal Nehru University",
    "Banaras Hindu University",
    "Indian Institute of Science",
    "Indian Institute of Technology Bombay",
    "Indian Institute of Technology Delhi",
    "Indian Institute of Technology Madras",
    "Indian Institute of Technology Kanpur",
    "Indian Institute of Technology Kharagpur",
    "University of Hyderabad",
    "Jadavpur University",
    "University of Calcutta",
    "University of Delhi",
    "Savitribai Phule Pune University",
    "Osmania University",
    "Anna University",
    "Aligarh Muslim University",
    "Jamia Millia Islamia",
    "Visva-Bharati University",
    "Panjab University",
    "Guru Nanak Dev University",
    "Amrita Vishwa Vidyapeetham",
    "Manipal Academy of Higher Education",
    "Birla Institute of Technology and Science, Pilani",
    "Vellore Institute of Technology",
    "SRM Institute of Science and Technology",
    "Christ University, Bangalore",
    "Presidency University, Kolkata",
    "Madras Christian College",
    "St. Xavier's College, Mumbai",
    "Fergusson College, Pune",
    "Loyola College, Chennai"
]

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

def normalize_key(key):
    return re.sub(r"[\\s_/,\\.\\(\\)'0-9]", "", key.strip().lower())

def extract_keys_with_lines(form_text):
    field_pattern = re.compile(r"^(.+?):", re.MULTILINE)
    keys = []
    for idx, line in enumerate(form_text.splitlines()):
        line = line.strip()
        match = field_pattern.match(line)
        if match:
            key = match.group(1).strip()
            keys.append((key, idx))
    print(keys)
    return keys

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    full_name = person["Full Name"]
    surname = full_name.split()[-1]
    father_first = person.get("Father's Name", "Rajesh").split()[0]
    mother_first = person.get("Mother's Name", "Sunita").split()[0]
    father = f"{father_first} {surname}"
    mother = f"{mother_first} {surname}"
    roll_no = f"{random.randint(100000, 999999)}"
    name_hindi = full_name  # For demo, same as English
    degree = random.choice(COURSES)
    subject = random.choice(DEGREE_SUBJECTS[degree])
    dept = f"Department of {subject}"
    state = person.get("State", random.choice(STATES))
    schools_for_state = STATE_SCHOOLS.get(state, SCHOOLS)
    school = random.choice(schools_for_state)
    dob = person.get("DOB", (datetime.date.today() - datetime.timedelta(days=random.randint(8000, 12000))).strftime("%d-%m-%Y"))
    gender = person.get("Gender", random.choice(GENDERS))
    nationality = person.get("Nationality", "Indian")
    blood_group = person.get("Blood Group", random.choice(BLOOD_GROUPS))
    date_of_admission = (datetime.date.today() - datetime.timedelta(days=random.randint(1000, 2000))).strftime("%d-%m-%Y")
    cgpa = round(random.uniform(6.0, 10.0), 2)
    division = random.choice(DIVISIONS)
    date_of_result = (datetime.date.today() - datetime.timedelta(days=random.randint(30, 200))).strftime("%d-%m-%Y")
    month_year_award = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%B %Y")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        key_lower = key.strip().lower().replace(" ","").replace("_","").replace("/","").replace(",","").replace(".","").replace("'","")
        print(key_lower)
        if key_lower == "1rollno":
            form_data[key] = roll_no
        elif key_lower == "2nameofthestudent":
            form_data[key] = full_name
        elif key_lower == "3nameofhindi":
            form_data[key] = name_hindi
        elif key_lower == "4course":
            form_data[key] = degree
        elif key_lower == "5subject":
            form_data[key] = subject
        elif key_lower == "6deptcentre":
            form_data[key] = dept
        elif key_lower == "7school":
            form_data[key] = school
        elif key_lower == "8dateofbirth":
            form_data[key] = dob
        elif key_lower == "9gender(malefemale)":
            form_data[key] = gender
        elif key_lower == "10nationality":
            form_data[key] = nationality
        elif key_lower == "11stateofdomicile":
            form_data[key] = state
        elif key_lower == "12bloodgroup":
            form_data[key] = blood_group
        elif key_lower == "13fathersname":
            form_data[key] = father
        elif key_lower == "14mothersname":
            form_data[key] = mother
        elif key_lower == "15dateofadmissiontothecourse":
            form_data[key] = date_of_admission
        elif key_lower == "16cgpaormarksobtained":
            form_data[key] = cgpa
        elif key_lower == "17divisionobtained":
            form_data[key] = division
        elif key_lower == "18dateofdeclarationofresultbythecesoffice":
            form_data[key] = date_of_result
        elif key_lower == "19monthandyearofaward":
            form_data[key] = month_year_award
        else:
            form_data[key] = ""
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_13.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_13_filled.txt')
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