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

PROGRAMMES = [
    "B.Stat.", "B.Math.", "M.Stat.", "M.Math.", "MSQE", "MSCS", "MSQMS", "Ph.D. Statistics", "Ph.D. Mathematics", "Ph.D. Computer Science"
]
HOSTELS = ["R.N. Tagore Hostel", "Ramanujan Hostel", "Nivedita Hostel", "S.N. Bose Hostel", "C.V. Raman Hostel"]
RELATIONSHIPS = ["Brother", "Sister", "Uncle", "Aunt", "Guardian"]
MEDICAL_ISSUES = ["None", "Asthma", "Diabetes", "Allergy", "Hypertension", "None"]
INSURANCE_COMPANIES = ["LIC", "ICICI Lombard", "HDFC Ergo", "Star Health", "New India Assurance"]


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
    name = person["Full Name"]
    roll_no = f"ISI{random.randint(1000,9999)}"
    gender = person.get("Gender", random.choice(["Male", "Female"]))
    programme = random.choice(PROGRAMMES)
    academic_year = f"{random.randint(2021,2023)}-{random.randint(2024,2025)}"
    id_no = f"ID{random.randint(100000,999999)}"
    passport_no = f"P{random.randint(1000000,9999999)}"
    aadhaar_no = f"{random.randint(100000000000,999999999999)}"
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(7000, 9000))).strftime("%d-%m-%Y")
    nationality = "Indian"
    phone = person["Phone"].replace("-", " ")
    email = person["Email"]
    perm_addr = person["Address"]
    res_addr = person["Address"]
    medical_illness = random.choice(MEDICAL_ISSUES)
    insurance_type = random.choice(["ISI", "Others"])
    ins_comp = random.choice(INSURANCE_COMPANIES) if insurance_type == "Others" else ""
    policy_no = f"POL{random.randint(100000,999999)}" if insurance_type == "Others" else ""
    expiry_date = (datetime.date.today() + datetime.timedelta(days=random.randint(100, 1000))).strftime("%d-%m-%Y") if insurance_type == "Others" else ""
    # Emergency contact
    em_name = random.choice(["Rajesh Sharma", "Sunita Singh", "Amit Verma", "Priya Das"])
    em_relation = random.choice(RELATIONSHIPS)
    em_phone_mob = f"+91 {random.randint(7000000000, 9999999999)}"
    em_phone_land = f"033-{random.randint(20000000,29999999)}"
    em_addr = perm_addr if random.random() < 0.5 else "Flat 12, Lake Town, Kolkata-700089"
    today = datetime.date.today().strftime("%d-%m-%Y")
    warden_comment = random.choice(["Recommended", "No objection", "Room available", "Room not available"])
    ao_comment = random.choice(["Room is available", "Room not available"])
    hostel_name = random.choice(HOSTELS)
    room_no = str(random.randint(101, 599))
    dean_comment = random.choice(["Approved", "Pending", "Rejected"])
    hostel_rent = random.choice(["2000", "2500", "3000"])
    rent_from = "01-07-2023"
    rent_to = "30-06-2024"
    total_amt = str(1000 + int(hostel_rent))
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "name":
            value = name
        elif k == "rollno":
            value = roll_no
        elif k == "malefemale":
            value = gender
        elif k == "programme":
            value = programme
        elif k == "academicyear":
            value = academic_year
        elif k == "idno":
            value = id_no
        elif k == "passportno":
            value = passport_no
        elif k == "aadhaarno":
            value = aadhaar_no
        elif k == "dateofbirth":
            value = dob
        elif k == "nationality":
            value = nationality
        elif k == "phoneno":
            value = phone
        elif k == "emailid":
            value = email
        elif k == "permanentaddress":
            value = perm_addr
        elif k == "residentialaddress":
            value = res_addr
        elif k == "medicalillnessifany":
            value = medical_illness
        elif k == "medicalinsurancepolicydetailsincludeasmanyasapplicableisiothers":
            value = insurance_type
        elif k == "ifotherscompname":
            value = ins_comp
        elif k == "policyno":
            value = policy_no
        elif k == "expirydate":
            value = expiry_date
        elif k == "name1":
            value = em_name
        elif k == "relationship":
            value = em_relation
        elif k == "phonenomob":
            value = em_phone_mob
        elif k == "phonenolandline":
            value = em_phone_land
        elif k == "addressincasedifferentthanpermanentaddressgivenabove":
            value = em_addr
        elif k == "date":
            value = today
        elif k == "signatureoftheapplicant":
            value = name
        elif k == "warden'scomment":
            value = warden_comment
        elif k == "roomisavailablenotavailable":
            value = ao_comment
        elif k == "nameofhostel":
            value = hostel_name
        elif k == "roomno":
            value = room_no
        elif k == "hostelroomrentfrom":
            value = rent_from
        elif k == "to":
            value = rent_to
        elif k == "totalrs":
            value = total_amt
        elif k == "dean'scomment":
            value = dean_comment
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_28.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_28_filled.txt')
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