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

MEMBERSHIP_TYPES = [
    "Regular (3 month)", "Gold (6 month)", "Platinum (12 month)"
]


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
    # Address
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
    address = ", ".join(part for part in addr_parts if part)
    city = applicant.get("Town/City/District", applicant.get("City", ""))
    country = "India"
    email = applicant.get("Email", "")
    phone = applicant.get("Phone", "")
    membership = random.choice(MEMBERSHIP_TYPES)

    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        value = ""
        if k == "fullname":
            value = name
        elif k == "placebirth":
            value = pob
        elif k == "birthofdate":
            value = dob
        elif k == "fulladdress":
            value = address
        elif k == "nationality":
            value = nationality
        elif k == "citycountry":
            value = f"{city}, {country}"
        elif k == "gander":
            value = gender.title()
        elif k == "email":
            value = email
        elif k == "phonenumber":
            value = phone
        elif k == "typeofmembership#chooseyourtypeofmembership":
            value = membership
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_49.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_49_filled.txt')
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