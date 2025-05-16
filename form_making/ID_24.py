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
CATEGORIES = ["Open", "OBC", "SC", "ST", "EWS"]
BRANCHES = ["Computer Science", "Electronics & Communication", "Mechanical", "Civil", "Electrical"]
BANKS = ["State Bank of India", "Punjab National Bank", "Jammu & Kashmir Bank", "HDFC Bank", "ICICI Bank"]
DISTRICTS = ["Jammu", "Srinagar", "Udhampur", "Baramulla", "Kathua", "Poonch", "Rajouri", "Anantnag", "Pulwama", "Doda"]
BOARDS = ["CBSE", "JKBOSE", "ICSE"]


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

def random_parent_name(gender, child_last_name):
    if gender == "Male":
        first = random.choice(FATHER_FIRST_NAMES)
    else:
        first = random.choice(MOTHER_FIRST_NAMES)
    return f"{first} {child_last_name}"

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    gender = person.get("Gender", random.choice(GENDERS))
    candidate_name = person["Full Name"]
    last_name = candidate_name.split()[-1]
    father_name = random_parent_name("Male", last_name)
    mother_name = random_parent_name("Female", last_name)
    branch = random.choice(BRANCHES)
    reg_no = f"UIET{random.randint(10000,99999)}"
    jee_score = random.randint(50, 300)
    jkcet_score = random.randint(50, 150)
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(7000, 9000))).strftime("%d-%m-%Y")
    category = random.choice(CATEGORIES)
    income = random.randint(10000, 200000)
    email = person["Email"]
    contact = person["Phone"].replace("-", " ")
    corr_addr = person["Address"]
    perm_addr = person["Address"]
    resident_jk = random.choice(["YES", "NO"])
    dd_no = f"DD{random.randint(10000,99999)}"
    dd_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y")
    bank = random.choice(BANKS)
    amount = random.choice([35000, 40000, 45000])
    studied_pcm = "YES"
    last_exam = "12th (Senior Secondary)"
    marks_phy = random.randint(50, 100)
    marks_chem = random.randint(50, 100)
    marks_math = random.randint(50, 100)
    school_names = ["Kendriya Vidyalaya", "Army Public School", "Delhi Public School", "Presentation Convent"]
    school = f"{random.choice(school_names)} {person['City']}"
    district = person["City"] if person["City"] in DISTRICTS else random.choice(DISTRICTS)
    board_10 = random.choice(BOARDS)
    board_12 = random.choice(BOARDS)
    roll_10 = f"{random.randint(100000,999999)}"
    roll_12 = f"{random.randint(100000,999999)}"
    year_10 = random.randint(2014, 2017)
    year_12 = year_10 + 2
    max_marks = 500
    marks_10 = random.randint(350, 500)
    marks_12 = marks_phy + marks_chem + marks_math + random.randint(50, 100)
    percent_10 = round(marks_10 / max_marks * 100, 2)
    percent_12 = round(marks_12 / max_marks * 100, 2)
    result_10 = "Passed"
    result_12 = "Passed"

    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "programmebtechin":
            value = branch
        elif k == "uietregistrationno":
            value = reg_no
        elif k == "jeescore":
            value = jee_score
        elif k == "of2018":
            value = 2018
        elif k == "jkcetscore":
            value = jkcet_score
        elif k == "candidatesname":
            value = candidate_name
        elif k == "fathersname":
            value = father_name
        elif k == "mothersname":
            value = mother_name
        elif k == "gender":
            value = gender
        elif k == "dateofbirth":
            value = dob
        elif k == "nationality":
            value = "Indian"
        elif k == "categoryasperuietnotification":
            value = category
        elif k == "monthlyincomeofthefatherguardian":
            value = income
        elif k == "e-mailid":
            value = email
        elif k == "contactno":
            value = contact
        elif k == "correspondenceaddress":
            value = corr_addr
        elif k == "permanentaddress":
            value = perm_addr
        elif k == "permanentresidentofj&kifyespleaseattachcopy":
            value = resident_jk
        elif k == "detailsofthefeedepositedbybankdraftno":
            value = dd_no
        elif k == "dated":
            value = dd_date
        elif k == "bankname":
            value = bank
        elif k == "amount":
            value = amount
        elif k == "whetherstudiedat+physicschemistrymath":
            value = studied_pcm
        elif k == "lastqualifyingexamonwhichadmissionisbeingsought":
            value = last_exam
        elif k == "marksobtainedin+classphysics":
            value = marks_phy
        elif k == "chemistry":
            value = marks_chem
        elif k == "math":
            value = marks_math
        elif k == "institutionschoollastattended":
            value = school
        elif k == "districtinwhichinstitutionschoolislocated":
            value = district
        elif k == "board":
            value = f"10th: {board_10}, 12th: {board_12}"
        elif k == "rollno":
            value = f"10th: {roll_10}, 12th: {roll_12}"
        elif k == "year":
            value = f"10th: {year_10}, 12th: {year_12}"
        elif k == "maxmarks":
            value = max_marks
        elif k == "%ageofmarks":
            value = f"10th: {percent_10}%, 12th: {percent_12}%"
        elif k == "resultstatus":
            value = f"10th: {result_10}, 12th: {result_12}"
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_24.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_24_filled.txt')
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