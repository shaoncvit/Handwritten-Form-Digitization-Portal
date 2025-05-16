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
COLLEGES = [
    "Government College Jammu", "MAM College Jammu", "Science College Jammu", "Women's College Gandhi Nagar", "GGM Science College", "Jammu University", "Jammu Province"
]
REASONS = [
    "Lost original certificate", "Damaged certificate", "Name correction", "Change in particulars", "Certificate not received"
]


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
    applicant_name = random_name()
    father_name = f"{random.choice(FATHER_FIRST_NAMES)} {applicant_name.split()[-1]}"
    exam = random.choice(EXAMS)
    year = random.randint(2000, 2023)
    reg_no = f"REG{random.randint(100000,999999)}"
    roll_no = f"{random.randint(100000,999999)}"
    college = random.choice(COLLEGES)
    reason = random.choice(REASONS)
    fee = random.choice(["500", "1000", "1500"])
    voucher_no = f"VCHR{random.randint(10000,99999)}"
    voucher_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%Y/%m/%d")
    perm_address = person.get("Address", random.choice(CITIES) + ", Jammu & Kashmir, 180001")
    pres_address = person.get("Address", random.choice(CITIES) + ", Jammu & Kashmir, 180001")
    today = datetime.date.today().strftime("%Y/%m/%d")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "name":
            value = applicant_name
        elif k == "fathersname":
            value = father_name
        elif k == "nameoftheexaminationpassed":
            value = exam
        elif k == "yearoftheexaminationdegreelcertificateofpassingwhichisrequired":
            value = year
        elif k == "registrationno":
            value = reg_no
        elif k == "rollnooftheexamination":
            value = roll_no
        elif k == "collegeinthecaseofregularcandidatesorprovinceinthecaseofprivatecandidatefromwhichappeared":
            value = college
        elif k == "reasonswhichhaveledtotheapplicationforduplicatedegreediplomacertificate":
            value = reason
        elif k == "feeofrs":
            value = fee
        elif k == "paidunderuniversityvoucherno":
            value = voucher_no
        elif k == "dated":
            value = voucher_date
        elif k == "parmanentaddressasshownintheadmissionform":
            value = perm_address
        elif k == "presentaddress":
            value = pres_address
        elif k == "signatureoftheapplicant":
            value = applicant_name
        elif k == "date":
            value = today
        elif k == "no":
            value = f"NO{random.randint(1000,9999)}"
        elif k == "20":
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_21.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_21_filled.txt')
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