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

BANKS = [
    "HDFC Bank", "State Bank of India", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Bank of Baroda", "Canara Bank"
]
ACCOUNT_TYPES = ["Resident", "Non Resident"]
IFSC_CODES = [
    "HDFC0001234", "SBIN0005678", "ICIC0004321", "UTIB0008765", "PUNB0123456", "BARB0KOLKAT", "CNRB0001111"
]
OFFICIAL_NAMES = ["Mr. S. Ghosh", "Ms. P. Roy", "Dr. A. Banerjee", "Mr. R. Dutta", "Ms. N. Sen"]

PURPOSES = ["Family Maintenance", "Retirement Fund", "Pension Fund", "Others"]


def normalize_key(key):
    return re.sub(r"[\s_/,.:;\\(\\)'0-9]", "", key.strip().lower())

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
    # 60% male, 40% female profile selection for remitter
    males = [p for p in person_profiles if p.get('Gender', '').lower() == 'male']
    females = [p for p in person_profiles if p.get('Gender', '').lower() == 'female']
    if random.random() < 0.6 and males:
        remitter = random.choice(males)
    elif females:
        remitter = random.choice(females)
    else:
        remitter = random.choice(person_profiles)
    # Beneficiary: random Indian name and plausible account
    beneficiary_name = random.choice([
        "Amit Sharma", "Priya Singh", "Rahul Verma", "Sneha Patel", "Meera Iyer", "Arjun Deshmukh", "Naveen Reddy", "Farah Khan"
    ])
    beneficiary_acc = f"{random.randint(10000000000,99999999999)}"
    beneficiary_bank = random.choice(BANKS)
    beneficiary_branch = f"{random.choice(['Park Street', 'Salt Lake', 'Andheri', 'MG Road', 'Jubilee Hills'])}, {random.choice(['Kolkata', 'Mumbai', 'Delhi', 'Hyderabad'])}"
    beneficiary_ifsc = random.choice(IFSC_CODES)
    beneficiary_acc_type = random.choice(ACCOUNT_TYPES)
    beneficiary_address = f"{random.randint(1, 100)}, {random.choice(['MG Road', 'Park Street', 'Salt Lake', 'Andheri', 'Jubilee Hills'])}, {random.choice(['Kolkata', 'Mumbai', 'Delhi', 'Hyderabad'])}"
    # Remitter details
    remitter_name = remitter["Full Name"]
    remitter_acc = f"{random.randint(10000000000,99999999999)}"
    remitter_email = remitter.get("Email", "")
    remitter_mobile = remitter.get("Phone", "").replace("-", " ")
    remitter_address = remitter.get("Address", "")
    remitter_lei = f"{random.randint(1000000000000000,9999999999999999)}" if random.random() < 0.2 else ""
    remitter_lei_expiry = (datetime.date.today() + datetime.timedelta(days=random.randint(30, 365*3))).strftime("%d/%m/%Y") if remitter_lei else ""
    # Amount
    amount = random.randint(1000, 200000)
    amount_words = f"{amount} Rupees Only"
    # Cheque/cash
    chq_no = f"{random.randint(100000,999999)}" if random.random() < 0.7 else ""
    cash_deposit = str(amount) if random.random() < 0.2 else ""
    # Dates
    today = datetime.date.today().strftime("%d/%m/%Y")
    # Purpose
    purpose = random.choice(PURPOSES)
    # Official signatories
    signatories = random.sample(OFFICIAL_NAMES, 3)
    # Form data mapping
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "customersname":
            value = remitter_name
        elif k == "accountno":
            value = remitter_acc
        elif k == "chqno":
            value = chq_no
        elif k == "mobileno":
            value = remitter_mobile
        elif k == "telno":
            value = remitter_mobile
        elif k == "remitterlegalentityidentifiercodelei":
            value = remitter_lei
        elif k == "leiexpirydate":
            value = remitter_lei_expiry
        elif k == "addressofremittermandatoryfornonhdfcbankcustomer":
            value = remitter_address
        elif k == "emailid":
            value = remitter_email
        elif k == "incaseofnonhdfcbankcustomeramountofcashdeposited":
            value = cash_deposit
        elif k == "name":
            value = beneficiary_name
        elif k == "address":
            value = beneficiary_address
        elif k == "accountno":
            value = beneficiary_acc
        elif k == "re-confirmaccountno":
            value = beneficiary_acc
        elif k == "bankname&branch":
            value = f"{beneficiary_bank}, {beneficiary_branch}"
        elif k == "ifsccode":
            value = beneficiary_ifsc
            if not value:
                value = "SBIN0005678"  # Default IFSC code from filled form
        elif k == "actype":
            value = beneficiary_acc_type
        elif k == "beneficiarylegalentityidentifiercodelei":
            # LEI is only required for transactions >= 50 crores for non-individual accounts
            # For this sample data we'll leave it empty since we're dealing with smaller amounts
            value = ""
        elif k == "leiexpirydate":
            # LEI expiry date is only needed if LEI is provided
            # Empty since we're not generating LEI codes for these sample transactions
            value = ""
        elif k == "amounttobecreditedinfigures":
            value = str(amount)
        elif k == "inwords":
            value = amount_words
        elif k == "remarks":
            value = purpose
        elif k == "time":
            value = today
        elif k == "purposeofremittancetonepaltickone":
            value = purpose
        elif k == "signatureofauthorizedsignatory":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "stsignatory":
            value = signatories[0]
        elif k == "ndsignatory":
            value = signatories[1]
        elif k == "rdsignatory":
            value = signatories[2]
        elif k == "processedbyempcodeandsign":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "authorizedbyempcodeandsign":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "dd/mc/utr-norefno":
            value = f"UTR{random.randint(10000000,99999999)}"
        elif k == "chargesrecoveredrsapplicableonlyfornoncustomer":
            value = str(random.randint(10, 500))
        elif k == "dayendcheckedby":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "transactionauthorizedbyndlevelforamount>lacs":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "kycdocumentationdonebyonlyfornon-hdfcbankcustomers":
            value = random.choice(OFFICIAL_NAMES)
        elif k == "receivedapplicalionforrtgsneftforanamountofrs":
            value = str(amount)
        elif k == "videcashchequenumber":
            value = chq_no if chq_no else "Cash"
        elif k == "tobecreditedtoaccountnumber":
            value = beneficiary_acc
        elif k == "of":
            value = beneficiary_name
        elif k == "bankwithifsccode":
            value = beneficiary_ifsc
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_36.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_36_filled.txt')
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