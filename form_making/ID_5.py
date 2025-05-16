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

sample_data = {
    "JOB TITLE": ["Software Engineer", "Manager", "Data Analyst", "Consultant", "Developer"],
    "COMPANY NAME": ["Tata Consultancy Services", "Infosys", "Wipro", "Reliance Industries", "HDFC Bank"],
    "BUSINESS TYPE": ["IT", "Finance", "Manufacturing", "Consulting", "Education"],
    "SINGLE/MULTI MEMBERSHIP": ["Single", "Multi"],
    "WORK HOURS": ["9am-5pm", "10am-6pm", "Flexible", "Night Shift"],
}

company_addresses = {
    "Tata Consultancy Services": "TCS House, Raveline Street, Fort, Mumbai, Maharashtra - 400001",
    "Infosys": "Electronics City, Hosur Road, Bengaluru, Karnataka - 560100",
    "Wipro": "Sarjapur Road, Doddakannelli, Bengaluru, Karnataka - 560035",
    "Reliance Industries": "Maker Chambers IV, Nariman Point, Mumbai, Maharashtra - 400021",
    "HDFC Bank": "HDFC Bank House, Senapati Bapat Marg, Lower Parel, Mumbai, Maharashtra - 400013"
}

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
    # print(keys)
    return keys

def fill_form(keys, date_format):
    person = random.choice(person_profiles)
    # Names
    full_name = person.get("Full Name", "")
    print(full_name)
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
    mobile_phone = person.get("Phone", "")
    home_phone = "+91-" + str(random.randint(7000000000, 9999999999))
    # Address, State, Zip
    address = person.get("Address", "")
    state = person.get("State/Province", "")
    match_zip = re.search(r'(\d{6})', address)
    zipcode = match_zip.group(1) if match_zip else "000000"
    # Company/job
    company = random.choice(sample_data["COMPANY NAME"])
    job_title = random.choice(sample_data["JOB TITLE"])
    company_address = company_addresses.get(company, "Sample Company Address")
    work_email = first_name.lower() + "." + last_name.lower() + "@" + company.replace(" ", "").lower() + ".com"
    business_type = random.choice(sample_data["BUSINESS TYPE"])
    work_hours = random.choice(sample_data["WORK HOURS"])
    # Membership
    membership = random.choice(sample_data["SINGLE/MULTI MEMBERSHIP"])
    # Membership start date
    today = datetime.date.today()
    start_date_obj = today - datetime.timedelta(days=random.randint(0, 365*5))
    start_date_str = format_date(start_date_obj, date_format)
    # Previous membership period
    prev_start_year = random.randint(2000, today.year - 2)
    prev_start = datetime.date(prev_start_year, random.randint(1, 12), random.randint(1, 28))
    prev_end = prev_start + datetime.timedelta(days=365*random.randint(1, 5))
    prev_start_str = format_date(prev_start, date_format)
    prev_end_str = format_date(prev_end, date_format)
    # Ref/family/friend
    ref_name1 = random.choice([p["Full Name"] for p in person_profiles if p["Full Name"] != full_name])
    print(ref_name1)
    ref_id1 = str(random.randint(10000, 99999))
    ref_name2 = random.choice([p["Full Name"] for p in person_profiles if p["Full Name"] not in [full_name, ref_name1]])
    print(ref_name2)
    ref_id2 = str(random.randint(10000, 99999))
    form_number = str(random.randint(100000, 999999))
    ref_number = str(random.randint(100000, 999999))
    form_data = {}
    for key in keys:
        key_lower = key.replace(" ", "").replace("_", "").replace("/", "").replace(".", "").lower()
        print(key_lower)
        if key_lower == "formnumber":
            form_data[key] = form_number
        elif key_lower in ["dateofbirth(ddmmyyyy)"]:
            form_data[key] = dob_obj.strftime("%d/%m/%Y")
        elif key_lower in ["refnumber"]:
            form_data[key] = ref_number
        elif key_lower in ["mrmrmsmiss"]:
            form_data[key] = random.choice(["Mr.", "Ms.", "Miss"]) if person.get("Gender", "Male").lower() == "male" else random.choice(["Ms.", "Miss"]) 
        elif key_lower == "firstname":
            form_data[key] = first_name
        elif key_lower == "lastname":
            form_data[key] = last_name
        elif key_lower in ["dateofbirth", "dob"]:
            form_data[key] = dob_str_formatted
        elif key_lower == "mobilephone":
            form_data[key] = mobile_phone
        elif key_lower == "homephone":
            form_data[key] = home_phone
        elif key_lower == "address":
            form_data[key] = address
        elif key_lower == "state":
            form_data[key] = state
        elif key_lower == "zipcode":
            form_data[key] = zipcode
        elif key_lower == "jobtitle":
            form_data[key] = job_title
        elif key_lower == "companyname":
            form_data[key] = company
        elif key_lower == "jobaddress":
            form_data[key] = company_address
        elif key_lower == "workhours":
            form_data[key] = work_hours
        elif key_lower == "workemail":
            form_data[key] = work_email
        elif key_lower == "businesstype":
            form_data[key] = business_type
        elif key_lower == "contactnumber":
            form_data[key] = mobile_phone
        elif key_lower == "businessaddress":
            form_data[key] = company_address
        elif key_lower == "singlemultimembership":
            form_data[key] = membership
        elif key_lower == "startdate(ddmmyyyy)":
            form_data[key] = start_date_str
        elif key_lower == "startdate":
            form_data[key] = prev_start_str
        elif key_lower == "enddate":
            form_data[key] = prev_end_str
        elif key_lower == "name":
            # For friend/family section, use ref names, for signature use full name
            if not form_data.get("NAME1"):
                form_data[key] = ref_name1
                form_data["NAME1"] = ref_name1
            elif not form_data.get("NAME2"):
                form_data[key] = ref_name2
                form_data["NAME2"] = ref_name2
            else:
                form_data[key] = full_name
        elif key_lower == "memberid1":
            form_data[key] = ref_id1
        elif key_lower == "memberid2":
            form_data[key] = ref_id2
        elif key_lower == "signature":
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_5.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_5_filled.txt')
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
