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
    "Degree/Course": ["B.Tech Computer Science", "MBA", "B.Com", "M.Sc Physics", "B.A. Economics"],
    "University/Institute": ["IIT Delhi", "IIM Ahmedabad", "Delhi University", "Anna University", "Jadavpur University"],
    "Year of Graduate": [str(y) for y in range(2010, 2024)],
    "Grade": ["A", "B", "C", "First Class", "Distinction"],
    "Employee": ["Tata Consultancy Services", "Infosys", "Wipro", "Reliance Industries", "HDFC Bank"],
    "Job Title": ["Software Engineer", "Data Analyst", "Manager", "Consultant", "Developer"],
    "Responsibilities": ["Software Development", "Data Analysis", "Team Management", "Client Communication", "Project Planning"],
    "Why I Quit": ["Career growth", "Relocation", "Better opportunity", "Personal reasons", "Higher studies"],
    "Skill & Training Achievement(s)": ["Python", "Data Analysis", "Project Management", "Machine Learning", "Java", "Cloud Computing"],
    "Level": ["Beginner", "Intermediate", "Expert"],
    "Institute": ["NIIT", "Aptech", "Coursera", "Udemy", "IIT Bombay", "IIM Bangalore"]
}

company_addresses = {
    "Tata Consultancy Services": "TCS House, Raveline Street, Fort, Mumbai, Maharashtra - 400001",
    "Infosys": "Electronics City, Hosur Road, Bengaluru, Karnataka - 560100",
    "Wipro": "Sarjapur Road, Doddakannelli, Bengaluru, Karnataka - 560035",
    "Reliance Industries": "Maker Chambers IV, Nariman Point, Mumbai, Maharashtra - 400021",
    "HDFC Bank": "HDFC Bank House, Senapati Bapat Marg, Lower Parel, Mumbai, Maharashtra - 400013"
}

university_city = {
    "IIT Delhi": "Delhi",
    "IIM Ahmedabad": "Ahmedabad",
    "Delhi University": "Delhi",
    "Jadavpur University": "Kolkata",
    "IIT Khargapur": "Khargapur",
    "IIT Bombay": "Mumbai",
    "IIM Bangalore": "Bangalore"
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
    return keys

def fill_form(keys, date_format):
    person = random.choice(person_profiles)
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
    match_zip = re.search(r'(\d{6})', person.get("Address", ""))
    zip_code = match_zip.group(1) if match_zip else "000000"
    today = datetime.date.today()
    # Education
    university = random.choice(sample_data["University/Institute"])
    edu_city = university_city.get(university, "Sample City")
    # Employment
    company = random.choice(sample_data["Employee"])
    company_address = company_addresses.get(company, "Sample Company Address")
    job_title = random.choice(sample_data["Job Title"])
    # Employment dates
    start_year = random.randint(2010, today.year - 1)
    start_month = random.randint(1, 12)
    start_day = random.randint(1, 28)
    start_date_obj = datetime.date(start_year, start_month, start_day)
    duration_years = random.randint(1, 5)
    end_year = min(start_year + duration_years, today.year)
    end_month = random.randint(1, 12)
    end_day = random.randint(1, 28)
    end_date_obj = datetime.date(end_year, end_month, end_day)
    if end_date_obj <= start_date_obj:
        end_date_obj = start_date_obj + datetime.timedelta(days=365 * duration_years)
    form_data = {}
    section = None
    for key in keys:
        key_lower = key.replace(" ", "").replace("_", "").replace("/", "").lower()
        # Section detection
        if key_lower in ["educationalbackground"]:
            section = "education"
            continue
        elif key_lower in ["employmenthistory"]:
            section = "employment"
            continue
        elif key_lower in ["skills&training", "skillsandtraining"]:
            section = "skills"
            continue
        elif key_lower in ["personalinformation"]:
            section = "personal"
            continue
        matched = False
        for pkey in person:
            pkey_lower = pkey.replace(" ", "").replace("_", "").replace("/", "").lower()
            if key_lower == pkey_lower:
                if key_lower in ["dateofbirth", "dob"]:
                    form_data[key] = format_date(dob_obj, date_format)
                else:
                    form_data[key] = person[pkey]
                matched = True
                break
        if matched:
            continue
        # Section-aware filling
        if section == "education":
            if key_lower == "universityinstitute":
                form_data[key] = university
            elif key_lower == "city":
                form_data[key] = edu_city
            elif key in sample_data:
                form_data[key] = random.choice(sample_data[key])
            else:
                form_data[key] = ""
        elif section == "employment":
            if key_lower == "employee":
                form_data[key] = company
            elif key_lower == "address":
                form_data[key] = company_address
            elif key_lower == "jobtitle":
                form_data[key] = job_title
            elif key_lower == "startdate":
                form_data[key] = format_date(start_date_obj, date_format)
            elif key_lower == "enddate":
                form_data[key] = format_date(end_date_obj, date_format)
            elif key in sample_data:
                form_data[key] = random.choice(sample_data[key])
            else:
                form_data[key] = ""
        elif section == "skills":
            if key in sample_data:
                form_data[key] = random.choice(sample_data[key])
            elif key_lower == "year":
                form_data[key] = str(random.randint(2015, today.year))
            else:
                form_data[key] = ""
        else:  # personal or unknown section
            if key_lower in ["phonenumber", "phoneno", "phone"]:
                form_data[key] = person.get("Phone") or person.get("Phone Number") or person.get("Phone No") or ""
            elif key_lower in ["emailaddress", "email"]:
                form_data[key] = person.get("Email") or person.get("Email Address") or ""
            elif key_lower in ["stateprovince", "state"]:
                form_data[key] = person.get("State/Province") or person.get("State") or ""
            elif key_lower in ["zippostalcode", "zipcode", "postalcode"]:
                form_data[key] = zip_code
            elif key_lower == "country":
                form_data[key] = person.get("Country", "India")
            elif key_lower == "city":
                form_data[key] = person.get("City", "")
            elif key_lower == "date":
                form_data[key] = format_date(today, date_format)
            elif key_lower == "year":
                form_data[key] = str(random.randint(2015, today.year))
            elif key_lower == "signature":
                form_data[key] = person.get("Full Name", "")
            elif key in sample_data:
                form_data[key] = random.choice(sample_data[key])
            else:
                form_data[key] = ""
    # Fill any missing critical fields
    for key in keys:
        key_lower = key.replace(" ", "").replace("_", "").replace("/", "").lower()
        if key_lower in ["dateofbirth", "dob"] and not form_data.get(key):
            form_data[key] = format_date(dob_obj, date_format)
        elif key_lower == "startdate" and not form_data.get(key):
            form_data[key] = format_date(start_date_obj, date_format)
        elif key_lower == "enddate" and not form_data.get(key):
            form_data[key] = format_date(end_date_obj, date_format)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_4.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_4_filled.txt')
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
