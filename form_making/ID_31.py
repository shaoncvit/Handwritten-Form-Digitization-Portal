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
INCOME_NATURES = ["Interest on FD", "Interest on RD", "Dividend", "Savings Account Interest", "PPF Interest"]
SECTIONS = ["194A", "194DA", "194EE", "194K"]


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

def random_pan():
    return f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000,9999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"

def fill_form(keys_with_lines):
    # Select person profile with 60% male, 40% female probability
    males = [p for p in person_profiles if p.get('Gender', '').lower() == 'male']
    females = [p for p in person_profiles if p.get('Gender', '').lower() == 'female']
    if random.random() < 0.6 and males:
        person = random.choice(males)
    elif females:
        person = random.choice(females)
    else:
        person = random.choice(person_profiles)
    name = person["Full Name"]
    pan = random_pan()
    status = random.choice(["Individual", "HUF", "Trust", "AOP", "BOI"])
    prev_year = f"{datetime.date.today().year-1}-{datetime.date.today().year}"
    res_status = "Resident"
    addr = person["Address"]
    city = person["City"]
    state = person.get("State/Province", random.choice(STATES))
    pin = re.findall(r"\d{6}", addr)
    pin = pin[0] if pin else f"7{random.randint(10000,99999)}"
    email = person["Email"]
    phone = person["Phone"].replace("-", " ")
    assessed_tax = random.choice(["Yes", "No"])
    assess_year = str(datetime.date.today().year-1) if assessed_tax == "Yes" else ""
    est_income = random.randint(10000, 200000)
    est_total_income = est_income + random.randint(10000, 50000)
    prev_forms = random.randint(0, 2)
    prev_forms_amt = prev_forms * random.randint(5000, 20000)
    # Income details
    inv_count = random.randint(1, 3)
    inv_ids = [f"INV{random.randint(10000,99999)}" for _ in range(inv_count)]
    inv_natures = random.choices(INCOME_NATURES, k=inv_count)
    inv_sections = random.choices(SECTIONS, k=inv_count)
    inv_amts = [random.randint(5000, 50000) for _ in range(inv_count)]
    today = datetime.date.today().strftime("%d/%m/%Y")
    place = city
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "nameofassesseedeclarant":
            value = name
        elif k == "panoftheassessee":
            value = pan
        elif k == "status":
            value = status
        elif k == "previousyearpyforwhichdeclarationisbeingmade":
            value = prev_year
        elif k == "residentialstatus":
            value = res_status
        elif k == "flatdoorblockno":
            value = person.get('Flat/Door/Block No', '')
        elif k == "nameofpremises":
            value = person.get('Premises', '')
        elif k == "roadstreetlane":
            value = person.get('Road/Street/Lane', '')
        elif k == "arealocality":
            value = person.get('Area/Locality', '')
        elif k == "towncitydistrict":
            value = person.get('Town/City/District', city)
        elif k == "state":
            value = person.get('State/Province', state)
        elif k == "pin":
            value = person.get('PIN', pin)
        elif k == "email":
            value = email
        elif k == "telephonenowithstdcodeandmobileno":
            value = phone
        elif k == "awhetherassessedtotaxundertheincome-taxact":
            value = assessed_tax
        elif k == "bifyeslatestassessmentyearforwhichassessed":
            value = assess_year
        elif k == "estimatedincomeforwhichthisdeclarationismade":
            value = est_income
        elif k == "estimatedtotalincomeofthepyinwhichincomementionedincolumntobeincluded":
            value = est_total_income
        elif k == "detailsofformnogotherthanthisformfiledduringthepreviousyearifany":
            value = prev_forms
        elif k == "totalnoofformnogfiled":
            value = prev_forms
        elif k == "aggregateamountofincomeforwhichformnogfiled":
            value = prev_forms_amt
        elif k == "identificationnumberofrelevantinvestmentaccountetc":
            value = ", ".join(inv_ids)
        elif k == "natureofincome":
            value = ", ".join(inv_natures)
        elif k == "sectionunderwhichtaxisdeductible":
            value = ", ".join(inv_sections)
        elif k == "amountofincome":
            value = ", ".join(str(a) for a in inv_amts)
        elif k == "signatureofthedeclarant":
            value = name
        elif k == "place":
            value = place
        elif k == "date":
            value = today
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_31.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_31_filled.txt')
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