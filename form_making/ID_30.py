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
    "B.Stat.", "B.Math.", "M.Stat.", "M.Math.", "MSQE", "MSCS", "MSQMS", "Ph.D. Statistics", "Ph.D. Mathematics", "Ph.D. Computer Science"
]
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
CATEGORIES = ["GEN", "SC", "ST", "OBC", "PC"]
HOSTELS = ["R.N. Tagore Hostel", "Ramanujan Hostel", "Nivedita Hostel", "S.N. Bose Hostel", "C.V. Raman Hostel"]
PARENT_NAMES = ["Rajesh Sharma", "Sunita Singh", "Amit Verma", "Priya Das", "Suresh Kumar", "Meena Gupta"]
GUARDIANS = ["Uncle", "Aunt", "Family Friend", "Guardian"]


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
    name = person["Full Name"].upper()
    course = random.choice(COURSES)
    year = random.choice(["1st", "2nd", "3rd", "4th"])
    roll_no = f"ISI{random.randint(1000,9999)}"
    gender = person.get("Gender", random.choice(["Male", "Female"]))
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(7000, 9000))).strftime("%d/%m/%Y")
    today = datetime.date.today()
    dob_date = datetime.datetime.strptime(dob, "%d/%m/%Y")
    age_years = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    blood_group = random.choice(BLOOD_GROUPS)
    category = random.choice(CATEGORIES)
    phone = person["Phone"].replace("-", " ")
    email = person["Email"]
    present_addr = person["Address"]
    perm_addr = person["Address"]
    father = random.choice(PARENT_NAMES)
    mother = random.choice(PARENT_NAMES)
    father_phone = f"+91 {random.randint(7000000000, 9999999999)}"
    mother_phone = f"+91 {random.randint(7000000000, 9999999999)}"
    father_email = f"father.split(' ')[0]{random.randint(100,999)}@gmail.com"
    mother_email = f"mother.split(' ')[0]{random.randint(100,999)}@gmail.com"
    guardian = random.choice(PARENT_NAMES)
    guardian_phone = f"+91 {random.randint(7000000000, 9999999999)}"
    guardian_email = f"guardian{random.randint(100,999)}@gmail.com"
    emergency_name = random.choice(PARENT_NAMES)
    emergency_addr = present_addr
    emergency_phone = f"+91 {random.randint(7000000000, 9999999999)}"
    emergency_email = f"emergency{random.randint(100,999)}@gmail.com"
    hosteller = random.choice(["YES", "NO"])
    hostel_name = random.choice(HOSTELS) if hosteller == "YES" else ""
    hostel_room = str(random.randint(101, 599)) if hosteller == "YES" else ""
    signature = name + " / " + name.split()[0][0] + name.split()[-1][0]
    # Office use
    app_received = (today - datetime.timedelta(days=random.randint(1, 10))).strftime("%d/%m/%Y")
    date_issued = (today + datetime.timedelta(days=random.randint(1, 5))).strftime("%d/%m/%Y")
    id_card_no = f"ID{random.randint(10000,99999)}"
    valid_upto = (today + datetime.timedelta(days=365)).strftime("%d/%m/%Y")
    card_delivered = (today + datetime.timedelta(days=random.randint(6, 10))).strftime("%d/%m/%Y")
    db_id = f"DB{random.randint(10000,99999)}"
    extension = random.choice(["(1)", "(2)", "(3)", "(4)", "(5)", "(6)"])
    validity = valid_upto
    duplicate_issued = random.choice(["YES", "NO"])
    cash_receipt = f"CR{random.randint(10000,99999)} / {today.strftime('%d/%m/%Y')}"
    issuing_officer = random.choice(["Mr. P. Kumar", "Ms. R. Das"])
    verified_by = random.choice(["Ms. S. Ghosh", "Mr. A. Dutta", "Ms. P. Roy"])
    remarks = random.choice(["", "All documents verified", "Photo attached", "Pending signature"])
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "cardcategory":
            value = "Student"
        elif k == "dateofapplication":
            value = today.strftime("%d/%m/%Y")
        elif k == "nameincapital":
            value = name
        elif k == "course":
            value = course
        elif k == "year":
            value = year
        elif k == "rollno":
            value = roll_no
        elif k == "sex":
            value = gender
        elif k == "dateofbirthddmmyyyy":
            value = dob
        elif k == "ageasondate":
            value = age_years
        elif k == "bloodgroup":
            value = blood_group
        elif k == "genscstobcpc":
            value = category
        elif k == "phonemobileno":
            value = phone
        elif k == "e-mailid":
            value = email
        elif k == "presentaddress":
            value = present_addr
        elif k == "permanentaddress":
            value = perm_addr
        elif k == "father":
            surname = name.split()[-1]
            male_names = ["Rajesh", "Suresh", "Ramesh", "Mahesh", "Dinesh", "Mukesh", "Rakesh", "Anil", "Sunil", "Kamal"]
            father_full = f"{random.choice(male_names)} {surname}"
            value = father_full
        elif k == "phone&e-mail":
            # Father's contact
            father_first_name = father_full.split()[0].lower()
            value = f"{father_phone}, {father_first_name}{random.randint(100,999)}@gmail.com"
        elif k == "mother":
            surname = name.split()[-1]
            female_names = ["Priya", "Sunita", "Anita", "Kavita", "Savita", "Meena", "Reena", "Seema", "Neha", "Rita"]
            mother_full = f"{random.choice(female_names)} {surname}"
            value = mother_full
        elif k == "phone&e-mail1":
            # Mother's contact
            mother_first_name = mother_full.split()[0].lower()
            value = f"{mother_phone}, {mother_first_name}{random.randint(100,999)}@gmail.com"
        elif k == "localguardian":
            surname = name.split()[-1]
            male_names = ["Rajesh", "Suresh", "Ramesh", "Mahesh", "Dinesh", "Mukesh", "Rakesh", "Anil", "Sunil", "Kamal"]
            guardian_full = f"{random.choice(male_names)} {surname}"
            value = guardian_full
        elif k == "phone&e-mail2":
            # Guardian's contact
            guardian_first_name = guardian_full.split()[0].lower()
            value = f"{guardian_phone}, {guardian_first_name}{random.randint(100,999)}@gmail.com"
        elif k == "incaseofemergencypersontobecontactpleaseputnameaddressphoneemailetc":
            value = f"{emergency_name}, {emergency_addr}, {emergency_phone}, {emergency_email}"
        elif k == "whetherhosteller":
            value = hosteller
        elif k == "ifyeshostelnameroomno":
            value = f"{hostel_name}, Room {hostel_room}" if hosteller == "YES" else ""
        elif k == "signaturebothfulladinitial":
            value = signature
        elif k == "applicationreceivedon":
            value = app_received
        elif k == "dateofissuance":
            value = date_issued
        elif k == "idcardno":
            value = id_card_no
        elif k == "initialvalidationupto":
            value = valid_upto
        elif k == "carddeliveredon":
            value = card_delivered
        elif k == "databaseidno":
            value = db_id
        elif k == "extension":
            value = extension
        elif k == "validity":
            value = validity
        elif k == "duplicateissued":
            value = duplicate_issued
        elif k == "cashreceiptno&date":
            value = cash_receipt
        elif k == "signatureofissuingofficer":
            value = issuing_officer
        elif k == "verifiedby":
            value = verified_by
        elif k == "notesremarks":
            value = remarks
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_30.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_30_filled.txt')
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