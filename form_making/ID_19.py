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
CITIES = ["Port Blair", "Diglipur", "Mayabunder", "Rangat", "Havelock", "Neil Island", "Car Nicobar", "Campbell Bay"]
REASONS = [
    "Increased usage of electrical appliances",
    "Installation of new equipment",
    "Business expansion",
    "Reduced requirement",
    "Energy saving initiative",
    "Seasonal demand change"
]
EQUIPMENT = [
    ("Lighting", random.randint(1, 20)),
    ("Motive Power", random.randint(1, 10)),
    ("Agricultural", random.randint(0, 5)),
    ("Other", random.randint(0, 3))
]

def normalize_key(key):
    return re.sub(r"[\s_/,\.\(\)'0-9]", "", key.strip().lower())

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
    last = random.choice(["Das", "Roy", "Singh", "Kumar", "Paul", "Nair", "Rao", "Sharma", "Patel", "Reddy"])
    return f"{first} {last}"

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    applicant_name = random_name()
    org_name = random.choice([applicant_name, "ABC Enterprises", "XYZ Pvt Ltd", "Sunrise Traders", "Green Energy Solutions"])
    service_conn_no = f"SCN{random.randint(100000,999999)}"
    address = person.get("Address", random.choice(CITIES) + ", Andaman & Nicobar Islands, 744101")
    mobile = f"+91 {random.randint(7000000000, 9999999999)}"
    today = datetime.date.today().strftime("%d-%m-%Y")
    # Load enhancement/reduction
    is_enhancement = random.choice([True, False])
    existing_load = round(random.uniform(2.0, 10.0), 2)
    if is_enhancement:
        requested_load = existing_load + round(random.uniform(1.0, 5.0), 2)
        reduced_load = ""
    else:
        requested_load = ""
        reduced_load = max(0.5, existing_load - round(random.uniform(0.5, 3.0), 2))
    reason = random.choice(REASONS)
    # Equipment details
    lighting = random.randint(1, 20)
    motive_power = random.randint(1, 10)
    agricultural = random.randint(0, 5)
    other = random.randint(0, 3)
    place = random.choice(CITIES)
    contact_no = mobile[-10:]
    email = f"{applicant_name.split()[0].lower()}@gmail.com"
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        # print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "nameofapplicantorganization":
            value = org_name
        elif k == "serviceconnectionnumber":
            value = service_conn_no
        elif k == "addressofpremisestowhichelectricityisbeingsupplied":
            value = address
        elif k == "mobileno":
            value = mobile
        elif k == "existingsanctionedloadinkwkva":
            value = existing_load
        elif k == "enhancedloadrequestedinkwkva":
            # print("Pass")
            value = requested_load
        elif k == "reducedloadrequestedinkwkva":
            value = reduced_load
        elif k == "reasonforloadenhancementlreduction":
            value = reason
        elif k == "detailsofloadaddeddisconnectedfromsupplyifapplicable":
            value = "See below"
        elif k == "alighting":
            value = lighting
        elif k == "bmotivepower":
            value = motive_power
        elif k == "cagricultural":
            value = agricultural
        elif k == "otherpleasespecify":
            value = other
        elif k == "date":
            value = today
        elif k == "signatureofconsumer":
            value = applicant_name
        elif k == "place":
            value = place
        elif k == "name":
            value = applicant_name
        elif k == "contactno":
            value = contact_no
        elif k == "email":
            value = email
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_19.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_19_filled.txt')
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