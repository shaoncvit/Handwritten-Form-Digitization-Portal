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

def format_date(date_obj, fmt):
    if fmt == "DD-MM-YYYY":
        return date_obj.strftime("%d-%m-%Y")
    elif fmt == "YYYY-MM-DD":
        return date_obj.strftime("%Y-%m-%d")
    elif fmt == "MM-DD-YYYY":
        return date_obj.strftime("%m-%d-%Y")
    else:
        return date_obj.strftime("%Y-%m-%d")

def extract_keys(form_text):
    field_pattern = re.compile(r"^([A-Za-z0-9&/()' \-]+):", re.MULTILINE)
    keys = []
    for line in form_text.splitlines():
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append(key)
    return keys

def fill_form(keys, date_format):
    person = random.choice(person_profiles)
    # Names
    full_name = person.get("Full Name", "")
    first_name = full_name.split()[0] if full_name else ""
    last_name = full_name.split()[-1] if full_name and len(full_name.split()) > 1 else ""
    # Date of Birth
    dob_str = None
    for dob_key in ["Date of Birth", "DoB", "dob"]:
        if dob_key in person and person[dob_key]:
            dob_str = person[dob_key]
            break
    dob_obj = None
    if dob_str:
        try:
            dob_obj = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
        except Exception:
            dob_obj = None
    if not dob_obj:
        dob_obj = datetime.date(1980, 1, 1) + datetime.timedelta(days=random.randint(0, 15000))
    dob_str_formatted = format_date(dob_obj, date_format)
    # Phones
    cell_phone = person.get("Phone", "")
    # Address, State, Zip
    address = person.get("Address", "")
    city = person.get("City", "")
    state = person.get("State/Province", "")
    match_zip = re.search(r'(\d{6})', address)
    zipcode = match_zip.group(1) if match_zip else "000000"
    # Email
    email = person.get("Email", "")
    # Emergency contact
    emergency_contact = random.choice([p["Full Name"] for p in person_profiles if p["Full Name"] != full_name])
    emergency_phone = "+91-" + str(random.randint(7000000000, 9999999999))
    # Marital Status
    marital_status = random.choice(["Married", "Single", "Divorced", "Widowed", "Other"])
    # Gender
    gender = person.get("Gender", "Male")
    # Previous Dentist, Dental Office
    previous_dentist = random.choice([p["Full Name"] for p in person_profiles if p["Full Name"] != full_name])
    dental_office = random.choice(["Smile Dental", "Bright Teeth Clinic", "Happy Smiles", "Pearl Dental Care"])
    # How did you hear about us?
    hear_about = random.choice(["live/work in area", "I was referred by", "Social media", "Other"])
    # Insurance
    insurance_type = random.choice(["No Dental Insurance", "Primary Insurance"])
    insurance_company = random.choice(["LIC", "ICICI Lombard", "HDFC Ergo", "Star Health", "Bajaj Allianz"])
    policy_holder = random.choice([p["Full Name"] for p in person_profiles])
    policy_holder_birth = format_date(dob_obj, date_format)
    member_id = str(random.randint(10000, 99999))
    group = str(random.randint(100, 999))
    employer = random.choice(["Infosys", "TCS", "Wipro", "Reliance", "HDFC Bank"])
    relationship = random.choice(["Self", "Parent", "Child", "Spouse", "Other"])
    # Today
    today = datetime.date.today()
    today_str = format_date(today, date_format)
    form_data = {}
    for key in keys:
        key_lower = key.replace(" ", "").replace("_", "").replace("/", "").replace(",", "").lower()
        if key_lower == "patient":
            form_data[key] = full_name
        elif key_lower == "date":
            form_data[key] = today_str
        elif key_lower == "firstname":
            form_data[key] = first_name
        elif key_lower == "lastname":
            form_data[key] = last_name
        elif key_lower in ["birthdate", "dateofbirth", "dob"]:
            form_data[key] = dob_str_formatted
        elif key_lower == "gender":
            form_data[key] = gender
        elif key_lower == "address":
            form_data[key] = address
        elif key_lower == "city":
            form_data[key] = city
        elif key_lower == "state":
            form_data[key] = state
        elif key_lower == "zip":
            form_data[key] = zipcode
        elif key_lower == "email":
            form_data[key] = email
        elif key_lower == "cellphone":
            form_data[key] = cell_phone
        elif key_lower == "maritalstatus":
            form_data[key] = marital_status
        elif key_lower == "emergencycontact":
            form_data[key] = emergency_contact
        elif key_lower == "phone":
            form_data[key] = emergency_phone
        elif key_lower == "previousdentist":
            form_data[key] = previous_dentist
        elif key_lower == "dentaloffice":
            form_data[key] = dental_office
        elif key_lower == "howdidyouhearaboutus":
            form_data[key] = hear_about
        elif key_lower == "insuranceinformation":
            form_data[key] = insurance_type
        elif key_lower == "nameofinsurancecompany":
            form_data[key] = insurance_company
        elif key_lower == "policyholdername":
            form_data[key] = policy_holder
        elif key_lower == "birthdate":
            form_data[key] = policy_holder_birth
        elif key_lower == "memberid":
            form_data[key] = member_id
        elif key_lower == "group":
            form_data[key] = group
        elif key_lower == "nameofemployer":
            form_data[key] = employer
        elif key_lower == "relationshiptoinsuranceholder":
            form_data[key] = relationship
        elif key_lower == "patientsignature":
            form_data[key] = full_name
        else:
            form_data[key] = ""
    return form_data

def fill_form_text(form_text, form_data):
    def replacer(match):
        key = match.group(1).strip()
        value = form_data.get(key, "")
        return f"{key}: {value}"
    field_pattern = re.compile(r"^([A-Za-z0-9&/()' \-]+):.*$", re.MULTILINE)
    filled_text = field_pattern.sub(replacer, form_text)
    return filled_text

def main():
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_6.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_6_filled.txt')
    with open(FORM_PATH, 'r') as f:
        form_text = f.read()
    keys = extract_keys(form_text)
    date_format = random.choice(["DD-MM-YYYY", "YYYY-MM-DD", "MM-DD-YYYY"])
    form_data = fill_form(keys, date_format)
    filled_text = fill_form_text(form_text, form_data)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(filled_text)
    print(f"Filled form saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
