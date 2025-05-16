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
    ("M.Sc.", "Physics"), ("M.Sc.", "Chemistry"), ("M.A.", "English"), ("M.A.", "History"),
    ("M.Tech", "Computer Science"), ("M.Tech", "Biotechnology"), ("MBA", "Business Administration"),
    ("Ph.D.", "Mathematics"), ("Ph.D.", "Economics")
]
HOSTELS = ["Tagore International Hostel", "New Boys Hostel", "New Girls Hostel", "Sarat Chandra Hostel", "Gopichand Hostel"]
REASONS = [
    "Medical grounds", "Personal reasons", "Academic improvement", "Missed semester due to internship", "Family emergency"
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
    person = random.choice(person_profiles)
    student_name = person["Full Name"]
    reg_no = f"UH{random.randint(100000,999999)}"
    course, subject = random.choice(COURSES)
    semester = random.choice(["I", "II", "III", "IV"])
    academic_year = f"{random.randint(2021,2023)}-{random.randint(2024,2025)}"
    admission_date = (datetime.date.today() - datetime.timedelta(days=random.randint(800, 1200))).strftime("%d-%m-%Y")
    # Passed courses
    passed_courses = [(f"{semester}-{i+1}", f"Course {random.randint(1,10)}") for i in range(3)]
    retain_result = random.choice(["YES", "NO"])
    # To be studied
    to_study_courses = [(f"{course} {semester}-{i+4}", f"Course {i+4}") for i in range(3)]
    reason = random.choice(REASONS)
    tuition_fee_paid = f"{random.randint(2021,2023)}"
    hostel_staying = random.choice(["YES", "NO"])
    hostel_name = random.choice(HOSTELS) if hostel_staying == "YES" else ""
    room_no = str(random.randint(101, 599)) if hostel_staying == "YES" else ""
    hostel_dues_paid = f"{random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}/{random.randint(2023,2025)}" if hostel_staying == "YES" else ""
    today = datetime.date.today().strftime("%d-%m-%Y")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameofthestudent":
            value = student_name
        elif k == "registrationnumber":
            value = reg_no
        elif k == "course&subject":
            value = f"{course} in {subject}"
        elif k == "datemonthyearofadmission":
            value = admission_date
        elif k == "idetailsofcoursesofsemesteralreadypassedcoursenotitleofthecourse":
            value = ", ".join([f"{i+1}: {course} {semester}-{i+1}" for i in range(3)])
        elif k == "optiononceexercisedwillbefinal":
            value = retain_result
        elif k == "detailsofthecoursestobestudiedduringre-admissiontothesemestercoursenotitleofthecourse":
            value = ", ".join([f"{i+1}: {course} {semester}-{i+4}" for i in range(3)])
        elif k == "reasonforre-admission":
            value = reason
        elif k == "tuitionfeepaidupto":
            value = tuition_fee_paid
        elif k == "whetherstayinginthehostelifyesgivethefollowingdetails":
            value = hostel_staying
        elif k == "anameofthehostel":
            value = hostel_name
        elif k == "roomno":
            value = room_no
        elif k == "bhostelduespaidupto":
            value = hostel_dues_paid
        elif k == "date":
            value = today
        elif k == "signatureofthestudent":
            value = student_name
        elif k == "name":
            value = student_name
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_26.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_26_filled.txt')
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