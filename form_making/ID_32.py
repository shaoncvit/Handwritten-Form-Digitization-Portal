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

STATES = [
    "West Bengal", "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Gujarat", "Telangana", "Rajasthan", "Madhya Pradesh"
]
TRANSACTION_MODES = ["Cash", "Cheque", "Card", "Draft/Banker's Cheque", "Online transfer"]
TRANSACTION_TYPES = [
    "05- Investment in time deposit", "06- Deposit in cash", "09- Opening an account (other than savings and time deposit)",
    "10- Account with balance exceeding Rs. 50,000", "11- Purchase of bank drafts or pay orders", "12- Application for issue of a credit or debit card",
    "14- Payment in connection with travel to any foreign country", "15- Payment for purchase, or remittance outside India", "22- Not classified above"
]
DOC_CODES = ["A1", "B2", "C3", "D4"]
DOC_AUTHORITIES = ["UIDAI", "Govt. of India", "Passport Office", "RTO"]


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
    # 60% male, 40% female profile selection
    males = [p for p in person_profiles if p.get('Gender', '').lower() == 'male']
    females = [p for p in person_profiles if p.get('Gender', '').lower() == 'female']
    if random.random() < 0.6 and males:
        person = random.choice(males)
    elif females:
        person = random.choice(females)
    else:
        person = random.choice(person_profiles)
    # Name parsing
    full_name = person["Full Name"]
    name_parts = full_name.split()
    first_name = name_parts[0]
    middle_name = name_parts[1] if len(name_parts) > 2 else ""
    surname = name_parts[-1]
    father_name = random.choice([p["Full Name"] for p in males]) if males else "Rajesh Sharma"
    father_parts = father_name.split()
    father_first = father_parts[0]
    father_middle = father_parts[1] if len(father_parts) > 2 else ""
    father_surname = father_parts[-1]
    dob = (datetime.date.today() - datetime.timedelta(days=random.randint(7000, 9000))).strftime("%d/%m/%Y")
    addr = person.get("Address", "")
    flat = person.get("Flat/Door/Block No", "")
    floor = random.choice(["1st", "2nd", "3rd", "Ground", "4th", "5th"])
    premises = person.get("Premises", "")
    block = random.choice(["A", "B", "C", "D", "E", "F"]) + str(random.randint(1, 10))
    road = person.get("Road/Street/Lane", "")
    area = person.get("Area/Locality", "")
    city = person.get("Town/City/District", person.get("City", ""))
    district = city
    state = person.get("State/Province", random.choice(STATES))
    pin = person.get("PIN", "7{:05d}".format(random.randint(10000,99999)))
    tel = f"033-{random.randint(20000000,29999999)}"
    mobile = person.get("Phone", f"+91 {random.randint(7000000000, 9999999999)}").replace("-", " ")
    transaction_amt = random.randint(1000, 200000)
    transaction_date = datetime.date.today().strftime("%d/%m/%Y")
    joint_count = random.randint(1, 3)
    mode = random.choice(TRANSACTION_MODES)
    mode_other = "" if mode != "Other" else "UPI"
    aadhaar = str(random.randint(100000000000, 999999999999))
    pan_applied = random.choice([True, False])
    pan_app_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 60))).strftime("%d/%m/%Y") if pan_applied else ""
    pan_ack = f"ACK{random.randint(100000,999999)}" if pan_applied else ""
    agri_income = random.randint(0, 10000)
    other_income = random.randint(0, 200000)
    doc_code = random.choice(DOC_CODES)
    doc_id = f"DOC{random.randint(10000,99999)}"
    doc_auth = random.choice(DOC_AUTHORITIES)
    trans_type = random.choice(TRANSACTION_TYPES)
    today = datetime.date.today()
    ver_day = today.day
    ver_month = today.strftime("%B")
    ver_year = today.year
    place = city
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "firstname":
            value = first_name
        elif k == "dateofbirthincorporationofdeclarant":
            value = dob
        elif k == "middlename":
            value = middle_name
        elif k == "sumame":
            value = surname
        elif k == "fathersnameincaseofindividualfirstname":
            value = father_first
        elif k == "middlename":
            value = father_middle
        elif k == "sumame1":
            value = father_surname
        elif k == "flat/roomno":
            value = flat
        elif k == "floorno":
            value = floor
        elif k == "nameofpremises":
            value = premises
        elif k == "blocknameno":
            value = block
        elif k == "roadstreetlane":
            value = road
        elif k == "arealocality":
            value = area
        elif k == "towncity":
            value = city
        elif k == "district":
            value = district
        elif k == "state":
            value = state
        elif k == "pincode":
            value = pin
        elif k == "telephonenumberwthstdcode":
            value = tel
        elif k == "mobileno":
            value = mobile
        elif k == "amountoftansactionrs":
            value = transaction_amt
        elif k == "dateoftransaction":
            value = transaction_date
        elif k == "incaseoftransactioninjointnamesnumberofpersonsinvolvedinthetransaction":
            value = joint_count
        elif k == "modeoftransaction":
            value = mode
        elif k == "other":
            value = mode_other
        elif k == "aadhaarnumberissuedbyuidaiifavailable":
            value = aadhaar
        elif k == "ifappliedforpananditisnotyetgeneratedenterdateofapplicationandacknowedgementnumber":
            value = f"{pan_app_date}, {pan_ack}" if pan_applied else ""
        elif k == "ifpannotapplied,fillestimatedtotalincome(includingincomeofspouse,minorchildetcaspersection64ofincome-taxact,1961)forthefinancialyearinwich theabovetransactionisheld":
            value = agri_income + other_income
        elif k == "aagriculturalincomers":
            value = agri_income
        elif k == "botherthanagriculturalincomers":
            value = other_income
        elif k == "detailsofdocumentbeingproducedinsupportofidentifyincolumn1referinstructionoverleaf":
            value = doc_code
        elif k == "documentidentificationnumber":
            value = doc_id
        elif k == "nameandaddressoftheauthorityissuingthedocument":
            value = doc_auth
        elif k == "documentcode":
            value = doc_code
        elif k == "documentidentificationnumber":
            value = doc_id
        elif k == "nameandaddressoftheauthorityissuingthedocument":
            value = doc_auth
        elif k == "transactiontype":
            value = trans_type
        elif k == "i":
            value = full_name
        elif k == "verifiedtodaythe":
            value = ver_day
        elif k == "dayof":
            value = ver_month
        elif k == "20":
            value = ver_year
        elif k == "place":
            value = place
        elif k == "signatureofdeclarant":
            value = full_name
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_32.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_32_filled.txt')
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