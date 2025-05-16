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

PROGRAMS = [
    "Science Stream", "Commerce Stream", "Arts Stream", "Computer Science", "Mathematics", "Biology"
]
SOURCES = [
    "Newspaper", "Friend/Relative", "School Website", "Social Media", "Advertisement", "Alumni"
]
ALLERGIES = [
    "None", "Peanuts", "Dust", "Pollen", "Milk", "Eggs", "Seafood"
]
MEDICAL_CONDITIONS = [
    "None", "Asthma", "Diabetes", "Epilepsy", "Heart Condition", "Allergies"
]

# For parent/guardian names
FATHER_NAMES = ["Ashok", "Raj", "Sumit", "Amitabha", "Tapash", "Suresh", "Ramesh", "Sanjay", "Vikram"]
MOTHER_NAMES = ["Sunita", "Anita", "Kavita", "Meena", "Lata", "Shobha", "Poonam", "Neeta", "Rekha"]
GUARDIAN_REL = ["Uncle", "Aunt", "Grandfather", "Grandmother", "Family Friend"]

# For academic records
YEARS = [str(y) for y in range(datetime.date.today().year-2, datetime.date.today().year)]
GRADES = ["A+", "A", "B+", "B", "C", "9.8 CGPA", "8.7 CGPA", "92%", "85%", "78%"]


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
    # Gender distribution: 60% male, 40% female
    gender_choice = random.choices(['male', 'female'], weights=[60, 40])[0]
    candidates = [p for p in person_profiles if p.get('Gender', '').lower() == gender_choice]
    if not candidates:
        candidates = person_profiles
    applicant = random.choice(candidates)
    name = applicant["Full Name"].upper()
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(5000, 7000))).strftime("%d/%m/%Y")
    pob = applicant.get("Town/City/District", applicant.get("City", ""))
    gender = applicant.get("Gender", gender_choice.title())
    nationality = "Indian"
    address = ', '.join(filter(None, [
        applicant.get("Flat/Door/Block No", ""),
        applicant.get("Premises", ""),
        applicant.get("Road/Street/Lane", ""),
        applicant.get("Area/Locality", ""),
        applicant.get("Town/City/District", "")
    ]))
    city = applicant.get("Town/City/District", applicant.get("City", ""))
    pin = applicant.get("PIN", "")
    phone = applicant.get("Phone", "")
    email = applicant.get("Email", "")

    # Academic
    grade_level = random.choice(["11", "12", "10", "9", "8"])
    program = random.choice(PROGRAMS)
    prev_school = random.choice([
        "St. Xaviers School", "Delhi Public School", "Kendriya Vidyalaya", "Loreto Convent", "Don Bosco School"
    ])
    prev_years = YEARS
    prev_grades = random.sample(GRADES, 2)

    # Parent/Guardian
    surname = name.split()[-1]
    father = f"Mr. {random.choice(FATHER_NAMES)} {surname}"
    mother = f"Mrs. {random.choice(MOTHER_NAMES)} {surname}"
    guardian = f"{random.choice(FATHER_NAMES+MOTHER_NAMES)} {surname}" if random.random() < 0.1 else ""
    guardian_rel = random.choice(GUARDIAN_REL) if guardian else ""
    parent_phone = "+91-9{}".format(random.randint(100000000, 999999999))
    # Emergency
    emergency_name = random.choice([father, mother, guardian]) if guardian else random.choice([father, mother])
    emergency_rel = "Father" if emergency_name == father else ("Mother" if emergency_name == mother else guardian_rel)
    emergency_phone = "+91-8{}".format(random.randint(100000000, 999999999))

    # Medical
    med_cond = random.choice(MEDICAL_CONDITIONS)
    allergy = random.choice(ALLERGIES)

    # Additional
    source = random.choice(SOURCES)
    achievements = random.choice(["State-level Chess Champion", "School Topper", "Debate Winner", "None", "District-level Athlete"])

    today = datetime.date.today().strftime("%d/%m/%Y")

    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "fullname":
            value = name
        elif k == "dateofbirth":
            value = dob
        elif k == "placeofbirth":
            value = pob
        elif k == "gender":
            value = gender.title()
        elif k == "nationality":
            value = nationality
        elif k == "address":
            # Sort address components and join with commas, removing duplicates
            addr_parts = []
            seen = set()
            for part in [
                applicant.get("Flat/Door/Block No", ""),
                applicant.get("Premises", ""),
                applicant.get("Road/Street/Lane", ""),
                applicant.get("Area/Locality", ""),
                applicant.get("Town/City/District", "")
            ]:
                if part and part not in seen:
                    addr_parts.append(part)
                    seen.add(part)
            value = ", ".join(part for part in addr_parts if part)
        elif k == "city":
            value = city
        elif k == "postalcode":
            value = pin
        elif k == "phonenumber":
            value = phone
        elif k == "emailaddress":
            value = email
        elif k == "applyingforgradelevel":
            value = grade_level
        elif k == "preferredprogram":
            value = program
        elif k == "previousschoolname":
            value = prev_school
        elif k == "year":
            # Academic records (two years)
            value = prev_years[0] if idx == 0 or (idx > 0 and keys_with_lines[idx-1][0].lower() != "year") else prev_years[1]
        elif k == "gradescore":
            value = prev_grades[0] if idx == 0 or (idx > 0 and keys_with_lines[idx-1][0].lower() != "grade/score") else prev_grades[1]
        elif k == "signatureofparentguardian":
            value = father if random.random() < 0.5 else mother
        elif k == "fathersname":
            value = father
        elif k == "occupation":
            value = random.choice(["Engineer", "Teacher", "Doctor", "Businessman", "Homemaker", "Accountant", "Manager", "Professor"]) 
        elif k == "contactnumber":
            value = parent_phone if idx < 3 else emergency_phone
        elif k == "mothersname":
            value = mother
        elif k == "date":
            value = today
        elif k == "guardiansnameifapplicable":
            value = guardian
        elif k == "relationshipwithstudent":
            value = guardian_rel
        elif k == "name":
            value = emergency_name
        elif k == "relationship":
            value = emergency_rel
        elif k == "conditions?":
            value = med_cond
        elif k == "allergiesifany":
            value = allergy
        elif k == "howdidyoulearnaboutourinstitution?":
            value = source
        elif k == "achievementsifany":
            value = achievements
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_48.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_48_filled.txt')
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