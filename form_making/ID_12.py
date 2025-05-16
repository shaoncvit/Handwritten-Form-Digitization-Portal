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

DEGREE_SUBJECTS = {
    "M.Sc.": ["Physics", "Chemistry", "Mathematics", "Computer Science", "Electronics", "Life Sciences"],
    "M.A.": ["English", "History", "Political Science", "Economics"],
    "M.Tech": ["Computer Science", "Electronics"],
    "M.Phil": ["Physics", "Chemistry", "Mathematics", "English", "History", "Electronics", "Life Sciences", "Economics"],
    "Ph.D.": ["Physics", "Chemistry", "Mathematics", "English", "History", "Political Science", "Computer Science", "Electronics", "Life Sciences", "Economics"],
    "MBA": ["Economics"],
    "MCA": ["Computer Science"],
}

POSITIONS = [
    "Research Scholar", "Assistant Professor", "Software Engineer", "Project Fellow", "Lecturer", "Manager", "Consultant", "Analyst"
]
OCCUPATIONS = [
    "Academics", "Industry", "Government Service", "Research", "Teaching", "Business", "Consultancy"
]
SUPERVISORS = [
    "Dr. Anil Kumar", "Dr. Priya Sharma", "Dr. Suresh Reddy", "Dr. Meena Iyer", "Dr. Rajiv Menon", "Dr. Kavita Das", "Dr. Arvind Joshi", "Dr. Sunita Rao", "Dr. Manoj Singh", "Dr. Neha Gupta"
]
THESIS_TITLES = [
    "Studies on Quantum Dots in Nanostructures",
    "A Comparative Study of Modern Indian Literature",
    "Design and Analysis of Algorithms for Big Data",
    "Synthesis of Organic Compounds for Drug Discovery",
    "Impact of Climate Change on Indian Agriculture",
    "Wireless Sensor Networks for Smart Cities",
    "Political Movements in Postcolonial India",
    "Machine Learning Approaches in Bioinformatics"
]
BANKS = [
    "State Bank of India", "Punjab National Bank", "ICICI Bank", "HDFC Bank", "Axis Bank", "Bank of Baroda"
]
PLACES = [
    "Hyderabad", "Kolkata", "Mumbai", "Delhi", "Bangalore", "Chennai", "Pune"
]

THESIS_TITLES_MAP = {
    "Physics": [
        "Studies on Quantum Dots in Nanostructures",
        "Impact of Climate Change on Indian Agriculture",
        "Optical Properties of Semiconductor Nanowires",
        "Magnetic Resonance Studies in Solid State Physics",
        "Experimental Analysis of Superconducting Materials"
    ],
    "Chemistry": [
        "Synthesis of Organic Compounds for Drug Discovery",
        "Catalytic Activity of Transition Metal Complexes",
        "Green Chemistry Approaches in Pesticide Synthesis",
        "Electrochemical Studies of Corrosion Inhibitors",
        "Photocatalytic Degradation of Industrial Dyes"
    ],
    "Mathematics": [
        "Numerical Solutions to Partial Differential Equations",
        "Graph Theory Applications in Social Networks",
        "Mathematical Modelling of Infectious Diseases",
        "Optimization Techniques in Operations Research",
        "Algebraic Structures and Their Applications"
    ],
    "English": [
        "A Comparative Study of Modern Indian Literature",
        "Postcolonial Narratives in Indian English Fiction",
        "Feminist Perspectives in Contemporary Poetry",
        "Translation and Identity in Indian Literature",
        "The Role of Myth in Indian Drama"
    ],
    "History": [
        "Political Movements in Postcolonial India",
        "Socio-Economic Impact of the Green Revolution",
        "Women's Participation in Indian Freedom Struggle",
        "Urbanization and Social Change in Medieval India",
        "Trade and Commerce in Ancient South India"
    ],
    "Political Science": [
        "Electoral Reforms in Indian Democracy",
        "Federalism and Centre-State Relations in India",
        "Role of Media in Indian Politics",
        "Public Policy and Rural Development",
        "Human Rights Movements in South Asia"
    ],
    "Computer Science": [
        "Design and Analysis of Algorithms for Big Data",
        "Machine Learning Approaches in Bioinformatics",
        "Blockchain Technology and Its Applications",
        "Natural Language Processing for Indian Languages",
        "Cybersecurity Challenges in E-Governance"
    ],
    "Electronics": [
        "Wireless Sensor Networks for Smart Cities",
        "VLSI Design for Low Power Applications",
        "Embedded Systems in Healthcare Monitoring",
        "IoT Solutions for Rural India",
        "Signal Processing Techniques in Communication"
    ],
    "Life Sciences": [
        "Genetic Diversity in Indian Medicinal Plants",
        "Microbial Bioremediation of Polluted Soils",
        "Stem Cell Research in Regenerative Medicine",
        "Ecological Impact of Deforestation in Western Ghats",
        "Bioinformatics Analysis of Plant Genomes"
    ],
    "Economics": [
        "Microfinance and Women Empowerment in Rural India",
        "Impact of GST on Indian Small Businesses",
        "Agricultural Subsidies and Farmer Welfare",
        "Foreign Direct Investment Trends in India",
        "Poverty Alleviation Programmes: A Critical Review"
    ],
}

# For Hindi name, just use the English name for demo

def extract_keys_with_lines(form_text):
    field_pattern = re.compile(r"^(.+?):", re.MULTILINE)
    keys = []
    for idx, line in enumerate(form_text.splitlines()):
        line = line.strip()
        match = field_pattern.match(line)
        if match:
            key = match.group(1).strip()
            keys.append((key, idx))

    # print(keys)
    return keys

def fill_form(keys_with_lines):
    person = random.choice(person_profiles)
    full_name = person["Full Name"]
    reg_no = f"UH{random.randint(201700000, 202399999)}"
    convocation_no = str(random.randint(1000, 9999))
    name_hindi = full_name  # For demo, same as English
    degree = random.choice(list(DEGREE_SUBJECTS.keys()))
    subject = random.choice(DEGREE_SUBJECTS[degree])
    year = str(random.randint(2018, 2024))
    receive_in_person = random.choice(["Yes", "No"])
    thesis_titles = THESIS_TITLES_MAP.get(subject, ["General Thesis Title"])
    thesis_title = random.choice(thesis_titles)
    supervisor = random.choice(SUPERVISORS)
    # Address
    address_lines = person.get("Address", "Hostel Block A, University of Hyderabad, Hyderabad").split(", ")
    mailing_name = full_name
    mailing_address = ", ".join(address_lines[:-1]) if len(address_lines) > 1 else address_lines[0]
    mailing_pin = re.search(r"(\d{6})", person.get("Address", ""))
    mailing_pin = mailing_pin.group(1) if mailing_pin else "500046"
    permanent_address = person.get("Address", "Hostel Block A, University of Hyderabad, Hyderabad")
    permanent_pin = re.search(r"(\d{6})", permanent_address)
    permanent_pin = permanent_pin.group(1) if permanent_pin else "500046"
    mobile = person.get("Phone", "+91-9" + str(random.randint(100000000, 999999999)))
    email = person.get("Email", f"user{random.randint(1000,9999)}@gmail.com")
    occupation = random.choice(OCCUPATIONS)
    position = random.choice(POSITIONS)
    office_address = random.choice([
        "Infosys Ltd, Hyderabad", "IIT Hyderabad, Kandi", "TCS, Gachibowli", "University of Hyderabad, Hyderabad", "Wipro, Bangalore"
    ])
    # Bank draft
    draft_no = str(random.randint(100000, 999999))
    draft_date = (datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))).strftime("%d/%m/%Y")
    draft_amount = random.choice(["500", "1000", "1500", "2000"])
    issuing_bank = random.choice(BANKS)
    place = random.choice(PLACES)
    today = datetime.date.today().strftime("%d-%m-%Y")
    signature = full_name
    form_data = {}
    for idx, (key, line_no) in enumerate(keys_with_lines):
        key_lower = key.strip().lower().replace(" ","").replace("_","").replace("/","").replace(",","").replace(".","").replace("'","")
        # print(key_lower)
        if key_lower == "regno":
            form_data[key] = reg_no
        elif key_lower == "convocationnumber":
            form_data[key] = convocation_no
        # elif key_lower == "nameofthecandidateinfull(inblocklettersaswaswritteninmatriculationssccbsehsccertificates)":
        #     form_data[key] = full_name
        elif key_lower == "inenglish":
            form_data[key] = full_name
        elif key_lower == "inhindi":
            form_data[key] = name_hindi
        elif key_lower == "2a)nameofthedegree":
            form_data[key] = degree
        elif key_lower == "b)subject":
            form_data[key] = subject
        elif key_lower == "c)yearofpassing":
            form_data[key] = year
        elif key_lower == "3whethertoreceivethedegreeinpersonattheconvocation(yesno)":
            
            form_data[key] = receive_in_person
        elif key_lower == "4ifapplyingformphilmtechphddegreefurnishbelowthetitleofthedissertationprojectthesis":
            form_data[key] = thesis_title
        elif key_lower == "nameofthesupervisors":
            form_data[key] = supervisor
        elif key_lower == "name":
            form_data[key] = mailing_name
        elif key_lower == "address":
            form_data[key] = mailing_address
        elif key_lower == "pincode":
            form_data[key] = mailing_pin
        elif key_lower == "permanentaddresswithpincode":
            form_data[key] = permanent_address
        elif key_lower == "whichthedegreeistobedispatched(pleasewriteclearly)":
            form_data[key] = full_name + ", " + mailing_address
        elif key_lower == "pincode":
            form_data[key] = permanent_pin
        elif key_lower == "mobileno":
            form_data[key] = mobile
        elif key_lower == "e-mail":
            form_data[key] = email
        elif key_lower == "a)occupation":
            form_data[key] = occupation
        elif key_lower == "b)position":
            form_data[key] = position
        elif key_lower == "c)officeaddress":
            form_data[key] = office_address
        elif key_lower == "bankdraftno":
            form_data[key] = draft_no
        elif key_lower == "date(ddmmyyyy)":
            form_data[key] = draft_date
        elif key_lower == "amountrs":
            form_data[key] = draft_amount
        elif key_lower == "issuingbank":
            form_data[key] = issuing_bank
        elif key_lower == "place":
            form_data[key] = place
        elif key_lower == "signatureofthecandidate":
            form_data[key] = signature
        elif key_lower == "date":
            form_data[key] = today
        else:
            form_data[key] = ""
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_12.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_12_filled.txt')
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
