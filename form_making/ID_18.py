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
CITIES = ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha", "Kannur", "Kottayam", "Palakkad", "Malappuram"]


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

def random_name(gender):
    if gender == "Male":
        first = random.choice(FATHER_FIRST_NAMES)
    else:
        first = random.choice(MOTHER_FIRST_NAMES)
    last = random.choice(["Nair", "Menon", "Pillai", "Kurian", "Varma", "Pillai", "Panicker", "Warrier", "Chacko", "Thomas"])
    return f"{first} {last}"

def fill_form(keys_with_lines):
    # Pensioner
    gender = random.choice(GENDERS)
    pensioner_name = random_name(gender)
    ppo_number = f"KSEB{random.randint(100000,999999)}"
    pension_type = random.choice(["Service Pension", "Family Pension"])
    mobile = f"+91 {random.randint(7000000000, 9999999999)}"
    aadhar = str(random.randint(100000000000, 999999999999))
    email = f"{pensioner_name.split()[0].lower()}@gmail.com"
    aru = random.choice(["TVM", "KLM", "EKM", "KZD", "TSR", "ALP", "KNR", "KTM", "PLK", "MLP"])
    place = random.choice(CITIES)
    today = datetime.date.today().strftime("%d/%m/%Y")
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "pponumber":
            value = ppo_number
        elif k == "pensionername":
            value = pensioner_name
        elif k == "pensiontype":
            value = pension_type
        elif k == "personalmobilenumber":
            value = mobile
        elif k == "aadharnumbercopyrequired":
            value = aadhar
        elif k == "email":
            value = email
        elif k == "pensionaru":
            value = aru
        elif k == "place":
            value = place
        elif k == "signatureofpensioner":
            value = pensioner_name
        elif k == "date":
            value = today
        elif k == "nameofpensioner":
            value = pensioner_name
        elif k == "verified&entereddate":
            value = today
        elif k == "employeecodesignature":
            value = f"EMP{random.randint(1000,9999)} / {random.choice(FATHER_FIRST_NAMES)}"
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_18.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_18_filled.txt')
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