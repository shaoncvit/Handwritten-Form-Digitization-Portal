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
BERTH_CHOICES = ["Lower", "Upper", "Middle", "Side Lower", "Side Upper"]
CLASSES = ["1A", "2A", "3A", "SL", "2S"]
VEG_CHOICES = ["Veg", "Non-Veg"]
STATIONS = ["Hyderabad", "Secunderabad", "Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Pune", "Lucknow", "Patna"]
TRAIN_NAMES = [
    ("12723", "Telangana Express"),
    ("12627", "Karnataka Express"),
    ("12951", "Mumbai Rajdhani"),
    ("12295", "Sanghamitra Express"),
    ("12863", "Howrah Express"),
    ("12615", "Grand Trunk Express"),
    ("12760", "Charminar Express"),
    ("12025", "Shatabdi Express"),
    ("12425", "Kerala Express"),
    ("12621", "Tamil Nadu Express")
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

OCCUPATIONS = [
    "Teacher", "Engineer", "Doctor", "Businessman", "Government Employee", "Farmer", "Shopkeeper", "Accountant", "Manager", "Clerk"
]

CITIES = ["Hyderabad", "Secunderabad", "Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Pune", "Lucknow", "Patna"]


def normalize_key(key):
    return re.sub(r"[\s_/,.\(\)']", "", key.strip().lower())

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
    last = random.choice(["Sharma", "Patel", "Reddy", "Singh", "Kumar", "Das", "Gupta", "Nair", "Chatterjee", "Yadav"])
    return f"{first} {last}"

def fill_form(keys_with_lines):
    # Main applicant
    person = random.choice(person_profiles)
    full_name = person["Full Name"]
    surname = full_name.split()[-1]
    first_name = full_name.split()[0]
    if "Gender" in person:
        gender = person["Gender"]
    elif first_name in FATHER_FIRST_NAMES:
        gender = "Male"
    elif first_name in MOTHER_FIRST_NAMES:
        gender = "Female"
    else:
        gender = random.choice(GENDERS)
    address = person.get("Address", "123 Main Road, City, State, 123456")
    phone = person.get("Phone", f"+91-{random.randint(7000000000, 9999999999)}")
    today = datetime.date.today()
    # Train details
    train_no, train_name = random.choice(TRAIN_NAMES)
    date_of_journey = (today + datetime.timedelta(days=random.randint(1, 30))).strftime("%d-%m-%Y")
    train_class = random.choice(CLASSES)
    num_berths = random.randint(1, 6)
    station_from = random.choice(STATIONS)
    station_to = random.choice([s for s in STATIONS if s != station_from])
    boarding_at = station_from
    reservation_upto = station_to
    # Passenger details
    passengers = []
    for i in range(num_berths):
        p_gender = random.choice(GENDERS)
        p_name = random_name(p_gender)
        p_age = random.randint(18, 65)
        p_berth = random.choice(BERTH_CHOICES)
        p_concession = "TRV-2025-{:02d}".format(random.randint(1, 9))  # Could be filled with logic if needed
        p_veg = random.choice(VEG_CHOICES)
        passengers.append({
            "name": p_name,
            "gender": p_gender[0],
            "age": p_age,
            "berth": p_berth,
            "concession": p_concession,
            "veg": p_veg
        })
    # Children (optional, 0-2)
    num_children = random.randint(0, 2)
    children = []
    for i in range(num_children):
        c_gender = random.choice(GENDERS)
        c_name = random_name(c_gender)
        c_age = random.randint(1, 4)
        children.append({
            "name": c_name,
            "gender": c_gender[0],
            "age": c_age
        })
    # Onward/Return journey
    onward_train_no, onward_train_name = random.choice(TRAIN_NAMES)
    onward_date = (today + datetime.timedelta(days=random.randint(31, 60))).strftime("%d-%m-%Y")
    onward_class = random.choice(CLASSES)
    onward_berths = random.randint(1, 6)
    onward_from = random.choice(STATIONS)
    onward_to = random.choice([s for s in STATIONS if s != onward_from])
    # Applicant
    applicant_name = full_name
    applicant_address = address
    applicant_phone = phone
    # Misc
    med_practitioner = random.choice(["Yes", "No"])
    sr_citizen = random.choice(["Yes", "No"])
    upgrade = random.choice(["Yes", "No"])
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        print(k)
        is_block = "blockletter" in k or "capitalletter" in k
        value = ""
        if k == "ifyouareamedicalpractitionerpleasetickinboxyoucouldbeofhelpinanemergency":
            value = med_practitioner
        elif k == "ifyouwantsrcitizenconcessionpleasewriteyesnoinboxifyespleasecarryaproofofageduringthejourneytoavoidinconvenienceofpenalchartingunderexantrailwayrulesyesno":
            value = sr_citizen
        elif k == "doyouwanttobeupgradedwithoutanyextrachargewriteyesnointheboxifthisoptionisnotexercisefullfarepayingpassengersmaybeupgradedautomaticallyyesno":
            value = upgrade
        elif k == "trainno&name":
            value = f"{train_no} {train_name}"
        elif k == "dateofjourney":
            value = date_of_journey
        elif k == "class":
            value = train_class
        elif k == "noofberthseats":
            value = num_berths
        elif k == "stationfrom":
            value = station_from
        elif k == "to":
            value = station_to
        elif k == "boardingat":
            value = boarding_at
        elif k == "reservationupto":
            value = reservation_upto
        elif k == "nameinblocklettersnotmorethan15characters":
            # Fill all passenger names, comma separated, max 15 chars each
            value = ", ".join([p["name"][:15].upper() for p in passengers])
        elif k == "gendermf":
            value = ", ".join([p["gender"] for p in passengers])
        elif k == "age":
            value = ", ".join([str(p["age"]) for p in passengers])
        elif k == "concessiontravelauthorityno":
            value = ", ".join([p["concession"] for p in passengers])
        elif k == "berthchoicelowerupper":
            value = ", ".join([p["berth"] for p in passengers])
        elif k == "vegnon-vegforrajdhanishatabiexponly":
            value = ", ".join([p["veg"] for p in passengers])
        elif k == "childrenbelow5yearsfowhomticketisnottobeissued":
            value = num_children
        elif k == "nameinblockletters":
            value = ", ".join([c["name"][:15].upper() for c in children])
        elif k == "gendermf":
            value = ", ".join([c["gender"] for c in children])
        elif k == "age":
            value = ", ".join([str(c["age"]) for c in children if c["age"] < 5])
        elif k == "onwardreturnjourneydetails":
            value = f"{onward_train_no} {onward_train_name}, {onward_date}, {onward_class}, {onward_berths}, {onward_from} to {onward_to}"
        elif k == "nameofapplicant":
            value = applicant_name
        elif k == "fulladdress":
            value = applicant_address
        elif k == "signatureoftheapplicantrepresentative":
            value = applicant_name
        elif k == "telmobnoifany":
            value = applicant_phone
        elif k == "date":
            value = today.strftime("%d-%m-%Y")
        elif k == "time":
            value = datetime.datetime.now().strftime("%H:%M")
        elif k == "snorequisition":
            value = f"REQ-2025-{random.randint(10000, 99999)}"
        elif k == "pnrno":
            value = str(random.randint(10**9, 10**10 - 1))
        elif k == "amountcollected":
            value = str(random.randint(100, 999))
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_17.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_17_filled.txt')
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