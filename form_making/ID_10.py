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

CATEGORIES = ["General", "SC", "ST", "OBC", "Permanently Disabled"]
SYLLABUS = ["OLD", "NEW"]
REGULARITY = ["Regular", "Suplimentary"]
EXAM_NAMES = [
    "B.Sc. (Hons) Physics Semester IV", "B.A. (Hons) English Semester VI", "B.E. Electrical Engineering Semester II", "M.A. History Semester I", "M.Sc. Chemistry Semester III", "B.Tech Computer Science Semester V", "M.Tech Electronics Semester II"
]
DEPARTMENTS = [
    "Physics", "English", "Electrical Engineering", "History", "Chemistry", "Computer Science", "Electronics"
]
PAPERS = [
    "Quantum Mechanics", "Solid State Physics", "Indian Writing in English", "Modern European History", "Organic Chemistry", "Data Structures", "Digital Signal Processing", "Power Systems", "Microprocessors", "Thermodynamics", "Control Systems", "Shakespearean Drama", "Statistical Mechanics", "Analog Electronics"
]
PRACTICALS = [
    "Physics Lab IV", "Chemistry Lab III", "Programming Lab", "Electronics Lab II", "History Project", "English Seminar", "Electrical Machines Lab"
]

FACULTY_NAMES = [
    "Dr. Anil Kumar", "Dr. Priya Sharma", "Dr. Suresh Reddy", "Dr. Meena Iyer", "Dr. Rajiv Menon", "Dr. Kavita Das", "Dr. Arvind Joshi", "Dr. Sunita Rao", "Dr. Manoj Singh", "Dr. Neha Gupta"
]

RUPEES_WORDS = [
    "Two Hundred", "Three Hundred", "One Hundred Fifty", "Four Hundred", "Five Hundred"
]

ADDRESS_EXAMPLES = [
    p["Address"] for p in person_profiles if "Address" in p
]

SEXES = ["male", "female"]

# Alias mapping for all possible field keys
FIELD_ALIASES = {
    # Category tick
    "general sc st obc permanently disabled": "category",
    # Syllabus
    "1. old / new syllabus": "syllabus",
    # Regular/Suplimentary
    "2. regular / suplimentary": "regularity",
    # Exam fees
    "exam fees rs": "exam_fees",
    "received rs": "exam_fees",
    "receipt no": "receipt_no",
    # Dates (handled by position)
    # Exam name
    "examination": "exam_name",
    "20": "exam_year",
    "examination roll no": "exam_roll",
    "to be held in": "exam_month",
    "the requisite fee of rs": "exam_fees",
    "(rupees": "rupees_words",
    # Application date
    # Full signature
    "full signature of the candidate": "signature",
    # Name
    "1.name in full": "full_name",
    "first": "first_name",
    "middle": "middle_name",
    "surname": "surname",
    "sex": "sex",
    "2.son/daughter of": "father",
    "3.address for all correspondence in future": "address",
    "4.phone no": "phone",
    "mob. no.": "mob",
    "5.present class": "present_class",
    "department": "department",
    "6.class roll no": "class_roll",
    "of": "of",  # handled by position
    "7.university regn. no": "university_regn",
    # Enclo, Theoretical, Practicals
    "enclo": "enclo",
    "theoritical paper": "theoretical",
    "practicals / sessionals": "practicals",
    # Admit card section
    "exmination roll no": "exam_roll",
    "admit sri/smt": "admit_name",
    "having examination roll no": "admit_exam_roll",
    "registration no": "admit_regn",
    "checked by": "admit_checked_by",
    "issued by": "admit_issued_by",
    "asstt. cont. 0 f examinations": "admit_asst_cont",
    "signature of candidate": "admit_signature",
}

def extract_keys_with_lines(form_text):
    field_pattern = re.compile(r"^([0-9A-Za-z&/()' .\-]+):", re.MULTILINE)
    keys = []
    for idx, line in enumerate(form_text.splitlines()):
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append((key, idx))
    print(keys)
    return keys

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    first_name = person["Full Name"].split()[0]
    middle_name = person["Full Name"].split()[1] if len(person["Full Name"].split()) > 2 else ""
    surname = person["Full Name"].split()[-1]
    full_name = person["Full Name"]
    father = random.choice(["Rajesh Kumar", "Suresh Singh", "Amitabh Das", "Prakash Chandra", "Rameshwar Sharma", "Sanjay Patel", "Vijay Menon", "Anil Reddy", "Subhash Ghosh", "Manoj Joshi"])
    sex = person.get("Gender", random.choice(SEXES))
    address = person.get("Address", random.choice(ADDRESS_EXAMPLES))
    phone = person.get("Phone", "+91-9" + str(random.randint(100000000, 999999999)))
    mob = "+91-9" + str(random.randint(100000000, 999999999))
    present_class = random.choice(["B.Sc. 2nd Year", "B.A. 3rd Year", "M.Sc. 1st Year", "B.Tech 4th Year", "M.A. 2nd Year"])
    department = random.choice(DEPARTMENTS)
    class_roll = str(random.randint(1, 120))
    class_of = random.choice(["2023", "2024", "2025"])
    university_regn = f"JU{random.randint(201700000, 202399999)}"
    regn_of = random.choice(["2021", "2022", "2023"])
    exam_fees = random.choice(["200", "300", "150", "400", "500"])
    exam_name = random.choice(EXAM_NAMES)
    exam_year = str(random.randint(2023, 2025))
    exam_month = random.choice(["May", "December", "June", "November"])
    exam_roll = f"EX{random.randint(100000, 999999)}"
    receipt_no = str(random.randint(100000, 999999))
    today = datetime.date.today().strftime("%d-%m-%Y")
    rupees_words = random.choice(RUPEES_WORDS)
    signature = full_name
    admit_name = f"Sri/Smt: {full_name}"
    admit_regn = university_regn
    admit_of = regn_of
    admit_exam = exam_name
    admit_subjects = ", ".join(random.sample(PAPERS, 2))
    admit_checked_by = random.choice(FACULTY_NAMES)
    admit_issued_by = random.choice(FACULTY_NAMES)
    # Tick marks
    tick_category = random.choice(CATEGORIES)
    tick_syllabus = random.choice(SYLLABUS)
    tick_regularity = random.choice(REGULARITY)
    # Subject fields
    theoretical = ", ".join(random.sample(PAPERS, 3))
    practicals = ", ".join(random.sample(PRACTICALS, 1))
    # Track repeated fields by order
    date_fields = [i for i, (k, _) in enumerate(keys_with_lines) if k.strip().lower() == "date"]
    filled_dates = {}
    if len(date_fields) >= 3:
        filled_dates[date_fields[0]] = today  # Cash section date
        filled_dates[date_fields[1]] = today  # Application date
        filled_dates[date_fields[2]] = today  # Admit card date
    elif len(date_fields) == 2:
        filled_dates[date_fields[0]] = today
        filled_dates[date_fields[1]] = today
    elif len(date_fields) == 1:
        filled_dates[date_fields[0]] = today
    # For ambiguous 'of' fields, assign by order
    of_counter = 0
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        key_norm = key.strip().lower().replace(" ","").replace("_","").replace("/","").replace(",","").replace(".","").replace("'","")
        alias = FIELD_ALIASES.get(key.strip().lower(), None)
        # Tick mark fields and mapped fields
        if alias == "category":
            form_data[key] = tick_category
        elif alias == "syllabus":
            form_data[key] = tick_syllabus
        elif alias == "regularity":
            form_data[key] = tick_regularity
        elif alias == "exam_fees":
            form_data[key] = exam_fees
        elif alias == "receipt_no":
            form_data[key] = receipt_no
        elif idx in filled_dates:
            form_data[key] = today
        elif alias == "exam_name":
            form_data[key] = exam_name
        elif alias == "exam_year":
            form_data[key] = exam_year
        elif alias == "exam_roll":
            form_data[key] = exam_roll
        elif alias == "exam_month":
            form_data[key] = exam_month
        elif alias == "rupees_words":
            form_data[key] = rupees_words
        elif alias == "signature":
            form_data[key] = signature
        elif alias == "full_name":
            form_data[key] = full_name
        elif alias == "first_name":
            form_data[key] = first_name
        elif alias == "middle_name":
            form_data[key] = middle_name
        elif alias == "surname":
            form_data[key] = surname
        elif alias == "sex":
            form_data[key] = sex
        elif alias == "father":
            form_data[key] = father
        elif alias == "address":
            form_data[key] = address
        elif alias == "phone":
            form_data[key] = phone
        elif alias == "mob":
            form_data[key] = mob
        elif alias == "present_class":
            form_data[key] = present_class
        elif alias == "department":
            form_data[key] = department
        elif alias == "class_roll":
            form_data[key] = class_roll
        elif alias == "university_regn":
            form_data[key] = university_regn
        elif alias == "enclo":
            form_data[key] = "1) Xerox Copy of Money Receipt (Must), 2) Xerox Copy of Latest Grade Card (Must)"
        elif alias == "theoretical":
            form_data[key] = theoretical
        elif alias == "practicals":
            form_data[key] = practicals
        elif alias == "admit_name":
            form_data[key] = admit_name
        elif alias == "admit_exam_roll":
            form_data[key] = exam_roll
        elif alias == "admit_regn":
            form_data[key] = admit_regn
        elif alias == "admit_checked_by":
            form_data[key] = admit_checked_by
        elif alias == "admit_issued_by":
            form_data[key] = admit_issued_by
        elif alias == "admit_signature":
            form_data[key] = signature
        elif alias == "admit_asst_cont":
            form_data[key] = admit_issued_by
        elif key_norm == "of":
            # Assign by order: 1st 'of' is class_of, 2nd is regn_of, 3rd is admit_of
            of_counter += 1
            if of_counter == 1:
                form_data[key] = class_of
            elif of_counter == 2:
                form_data[key] = regn_of
            elif of_counter == 3:
                form_data[key] = admit_of
            else:
                form_data[key] = ""
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_10.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_10_filled.txt')
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
