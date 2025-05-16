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

FATHER_FIRST_NAMES = [
    "Rajesh", "Amit", "Suresh", "Anil", "Vijay", "Sanjay", "Rakesh", "Manoj", "Prakash", "Sunil", "Arun", "Ravi", "Deepak", "Ajay", "Ashok"
]
MOTHER_FIRST_NAMES = [
    "Sunita", "Anita", "Suman", "Kavita", "Neeta", "Poonam", "Rekha", "Seema", "Shobha", "Meena", "Renu", "Geeta", "Anjali", "Neelam", "Priya"
]
GENDERS = ["Male", "Female"]
CITIES = ["Jammu", "Srinagar", "Udhampur", "Baramulla", "Kathua", "Poonch", "Rajouri", "Anantnag", "Pulwama", "Doda"]
EXAMS = ["B.A.", "B.Sc.", "B.Com.", "M.A.", "M.Sc.", "M.Com.", "B.Ed.", "M.Ed.", "Ph.D.", "Diploma"]
MEDALS = ["Gold Medal", "Silver Medal", "Bronze Medal", "Merit Certificate"]


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

def random_name():
    first = random.choice(FATHER_FIRST_NAMES + MOTHER_FIRST_NAMES)
    last = random.choice(["Sharma", "Singh", "Gupta", "Raina", "Koul", "Choudhary", "Rathore", "Verma", "Kumar", "Pandit"])
    return f"{first} {last}"

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    candidate_name = random_name()
    parent_name = f"{random.choice(FATHER_FIRST_NAMES + MOTHER_FIRST_NAMES)} {candidate_name.split()[-1]}"
    exam = random.choice(EXAMS)
    year = random.randint(2015, 2023)
    marks = random.randint(400, 500)
    medal = random.choice(MEDALS)
    dd_no = f"DD{random.randint(10000,99999)}"
    dd_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y")
    ph_no = f"+91 {random.randint(7000000000, 9999999999)}"
    alt_no = f"+91 {random.randint(7000000000, 9999999999)}"
    today = datetime.date.today().strftime("%d-%m-%Y")
    department_head = random_name()
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "sno":
            value = str(random.randint(1, 1000))
        elif k == "i":
            value = candidate_name
        elif k == "sodo":
            value = parent_name
        elif k == "havequalified":
            value = exam
        elif k == "examinationsduring":
            value = year
        elif k == "yearandhavestood":
            value = random.randint(1, 10)
        elif k == "securing":
            value = marks
        elif k == "marks":
            value = marks
        elif k == "iameligibletoreceivemedalmeritcertificatefortheyear":
            value = f"{medal}, {year}"
        elif k == "didno":
            value = dd_no
        elif k == "jammuon":
            value = today
        elif k == "dated":
            value = dd_date
        elif k == "phnomobile":
            value = ph_no
        elif k == "alternateno":
            value = alt_no
        elif k == "signatureofthecandidate":
            value = candidate_name
        elif k == "dated":
            value = today
        elif k == "headoftheconcerneddepartment":
            value = department_head
        elif k == "receivedanapplicationfrom":
            value = candidate_name
        elif k == "sodo":
            value = parent_name
        elif k == "alongwithddno":
            value = dd_no
        elif k == "dated":
            value = dd_date
        elif k == "forrs-forattendingtheconvocationon":
            value = today
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_23.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_23_filled.txt')
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