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

EXAMS = [
    "B.A. 2nd Year", "B.Sc. 1st Year", "M.A. English", "M.Sc. Physics", "B.Com. 3rd Year", "Ph.D. Chemistry"
]
COLLEGES = [
    "DAV College, Chandigarh", "GGDSD College, Sector 32", "Panjab University Campus", "Govt. College, Ludhiana"
]
DISTRICTS = ["Chandigarh", "Ludhiana", "Amritsar", "Patiala", "Jalandhar"]
REASONS = [
    "Medical grounds", "Transfer of parent", "Marriage", "Personal reasons", "Other"
]
OFFICIALS = ["Dr. S. Ghosh", "Ms. P. Roy", "Dr. A. Banerjee", "Mr. R. Dutta", "Ms. N. Sen"]


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
    applicant = random.choice([p for p in person_profiles if p.get('Gender', '').lower() in ['male', 'female']])
    name = applicant["Full Name"].upper()
    father_name = f"Mr. {random.choice(['Ashok','Raj','Sumit','Amitabha','Tapash'])} {name.split()[-1]}"
    roll_no = f"PU{random.randint(100000,999999)}"
    fee_amt = str(random.randint(100, 1000))
    fee_words = f"Rupees {fee_amt} only"
    receipt_no = f"R{random.randint(10000,99999)}"
    receipt_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d/%m/%Y")
    exam = random.choice(EXAMS)
    college = random.choice(COLLEGES)
    district = random.choice(DISTRICTS)
    change_from = random.choice(["Chandigarh", "Ludhiana", "Amritsar"])
    change_to = random.choice([d for d in DISTRICTS if d != change_from])
    reason = random.choice(REASONS)
    address = ', '.join([
        applicant.get("Flat/Door/Block No", ""),
        applicant.get("Premises", ""),
        applicant.get("Road/Street/Lane", ""),
        applicant.get("Area/Locality", ""),
        applicant.get("Town/City/District", "")
    ])
    today = datetime.date.today().strftime("%d/%m/%Y")
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "rollnoifreceived":
            value = roll_no
        elif k == "anameincapitals":
            value = name
        elif k == "fathersname":
            value = father_name
        elif k == "bfeeremittedrs":
            value = fee_amt
        elif k == "rupees":
            value = fee_words
        elif k == "bankdraftipouniversityreceiptno":
            value = receipt_no
        elif k == "dated":
            value = receipt_date
        elif k == "canameofexamination":
            value = exam
        elif k == "bnameofthecollegedistrictforprivatecandidates":
            value = f"{college}, {district}"
        elif k == "thechangeofcentrefrom":
            value = change_from
        elif k == "to":
            value = change_to
        elif k == "dreasonsforchange":
            value = reason
        elif k == "daddressforcorrespondence":
            value = address
        elif k == "signatureoftheapplicant":
            value = name
        elif k == "dated":
            value = today
        # elif k == "principalattestingauthoritywhohadattestedtheadmissionformin caseofprivatecandidate":
        #     value = random.choice(OFFICIALS)
        elif k == "sealofoffice":
            value = "Panjab University"
        elif k == "d.r.e.a.r.e":
            value = random.choice(OFFICIALS)
        elif k == "superintendent":
            value = random.choice(OFFICIALS)
        elif k == "assistantclerk":
            value = random.choice(OFFICIALS)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_47.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_47_filled.txt')
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