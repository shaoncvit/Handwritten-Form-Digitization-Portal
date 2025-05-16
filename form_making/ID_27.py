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

COURSES = [
    ("M.Sc.", "Physics"), ("M.Sc.", "Chemistry"), ("M.A.", "English"), ("M.A.", "History"),
    ("M.Tech", "Computer Science"), ("M.Tech", "Biotechnology"), ("MBA", "Business Administration"),
    ("Ph.D.", "Mathematics"), ("Ph.D.", "Economics")
]
HOSTELS = ["Tagore International Hostel", "New Boys Hostel", "New Girls Hostel", "Sarat Chandra Hostel", "Gopichand Hostel"]
PAPER_TITLES = ["Quantum Mechanics", "Organic Chemistry", "Modern Indian History", "Machine Learning", "Financial Management", "Topology", "Microeconomics"]
CORE_ELECTIVE = ["Core", "Elective", "Audited"]
REGULAR_RECOURSE = ["Regular", "Recourse"]

# Define course-to-papers mapping for logical consistency
COURSE_PAPERS = {
    "M.A. in English": [
        ("British Poetry", "British Drama", "Indian Writing in English", "Literary Criticism"),
        ("British Poetry", "British Drama", "Indian Writing in English", "Literary Criticism"),
    ],
    "M.Sc. in Physics": [
        ("Quantum Mechanics", "Electrodynamics", "Statistical Mechanics", "Solid State Physics"),
        ("Quantum Mechanics", "Electrodynamics", "Statistical Mechanics", "Solid State Physics"),
    ],
    "M.Tech in Computer Science": [
        ("Data Structures", "Machine Learning", "Computer Networks", "Operating Systems"),
        ("Data Structures", "Machine Learning", "Computer Networks", "Operating Systems"),
    ],
    "MBA in Business Administration": [
        ("Financial Management", "Marketing Management", "Human Resource Management", "Operations Research"),
        ("Financial Management", "Marketing Management", "Human Resource Management", "Operations Research"),
    ],
    "M.A. in History": [
        ("Modern Indian History", "Ancient Civilizations", "World History", "History of Science"),
        ("Modern Indian History", "Ancient Civilizations", "World History", "History of Science"),
    ],
    "M.Sc. in Chemistry": [
        ("Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry"),
        ("Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry"),
    ],
    "Ph.D. in Mathematics": [
        ("Topology", "Number Theory", "Functional Analysis", "Algebra"),
        ("Topology", "Number Theory", "Functional Analysis", "Algebra"),
    ],
    "Ph.D. in Economics": [
        ("Microeconomics", "Macroeconomics", "Econometrics", "Development Economics"),
        ("Microeconomics", "Macroeconomics", "Econometrics", "Development Economics"),
    ],
    "M.Tech in Biotechnology": [
        ("Biochemistry", "Cell Biology", "Genetics", "Molecular Biology"),
        ("Biochemistry", "Cell Biology", "Genetics", "Molecular Biology"),
    ],
}

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
    person = random.choice(person_profiles)
    student_name = person["Full Name"]
    reg_no = f"UH{random.randint(100000,999999)}"
    course, subject = random.choice(COURSES)
    semester = random.choice(["I", "II", "III", "IV"])
    fees_paid = f"Rs. {random.randint(1000, 5000)}/-"
    sc_st_scholarship = random.choice(["YES", "NO"])
    scholarship_applied = random.choice(["YES", "NO"])
    hostel = random.choice(HOSTELS)
    room_no = str(random.randint(101, 599))
    drc_enclosed = random.choice(["YES", "NO"])
    extension_enclosed = random.choice(["YES", "NO"])
    email = person.get("Email", f"student{random.randint(100,999)}@uohyd.ac.in")
    mobile = person.get("Phone", f"+91 {random.randint(7000000000, 9999999999)}").replace("-", " ")
    # Backlogs
    backlog_courses = [(f"C{random.randint(101,199)}", random.choice(PAPER_TITLES), random.choice(["I", "II", "III", "IV"]), f"{random.randint(2021,2023)}-{random.choice(['Jan','May','Dec'])}") for _ in range(random.randint(0,2))]
    # Registered courses
    registered_courses = [
        {
            "sno": i+1,
            "course_no": f"C{random.randint(201,299)}",
            "title": random.choice(PAPER_TITLES),
            "core_elective": random.choice(CORE_ELECTIVE),
            "credits": random.choice([2,3,4]),
            "regular_recourse": random.choice(REGULAR_RECOURSE)
        } for i in range(random.randint(4,6))
    ]
    today = datetime.date.today().strftime("%d-%m-%Y")
    form_data = {}
    # Compose the course/subject string
    course_subject_str = f"{course} in {subject}"
    # Pick papers for this course/subject
    papers = COURSE_PAPERS.get(course_subject_str, [("Paper1", "Paper2", "Paper3", "Paper4")])[0]
    # For Title of the Paper, use the same as papers (or a different set if needed)
    title_of_paper = COURSE_PAPERS.get(course_subject_str, [("Paper1", "Paper2", "Paper3", "Paper4")])[1]
    for idx, (key, line_no) in enumerate(keys_with_lines):
        k = normalize_key(key)
        # Alias mapping for registered courses section and backlogs
        aliases = {
            'titleofthepaper': 'titleofthepaper',
            'core/elective/audited': 'coreelectiveaudited',
            'coreelectiveaudited': 'coreelectiveaudited',
            'credits': 'credits',
            'regular/recourse': 'regularrecourse',
            'regularrecourse': 'regularrecourse',
            'semester': 'backlog_semester',
            'year&monthofexamination': 'backlog_yearmonth',
            'yearmonthofexamination': 'backlog_yearmonth',
        }
        k_alias = aliases.get(k, k)
        value = ""
        if k_alias == "registrationno":
            value = reg_no
        elif k_alias == "name":
            value = student_name
        elif k_alias == "coursesubjectofstudy":
            value = course_subject_str
        elif k_alias == "semesterforwhichregistrationissought":
            value = semester
        elif k_alias == "feespaidpleaseencloseofpaymentoffees":
            value = fees_paid
        elif k_alias == "inthecaseofscstscholarshipholdergovt":
            value = sc_st_scholarship
        elif k_alias == "hostelandroomno":
            value = f"{hostel}, Room {room_no}"
        elif k_alias == "whetheracopyofthelatestdrcreportisenclosedforphdscholarsonly":
            value = drc_enclosed
        elif k_alias == "whetheracopyoftheextensionorderisenclosedincaseofmphil&phdscholarsoughtextension":
            value = extension_enclosed
        elif k_alias == "email":
            value = email
        elif k_alias == "mobilenumber":
            value = mobile
        elif k_alias == "courseno":
            course_nums = [f"C27{i+1}" for i in range(4)]
            value = ", ".join(course_nums)
        elif k_alias == "coursetitle":
            value = ", ".join(papers)
        elif k_alias == "titleofthepaper":
            value = ", ".join(title_of_paper)
        elif k_alias == "coreelectiveaudited":
            core_elec = ["Core", "Elective", "Elective", "Audited"]
            value = ", ".join(core_elec[:4])
        elif k_alias == "credits":
            credit_vals = ["3", "2", "3", "3"]
            value = ", ".join(credit_vals[:4])
        elif k_alias == "regularrecourse":
            reg_rec = ["Regular", "Regular", "Recourse", "Regular"]
            value = ", ".join(reg_rec[:4])
        elif k_alias == "backlog_semester":
            value = "III" if backlog_courses else "None"
        elif k_alias == "backlog_yearmonth":
            value = "2022-Jan" if backlog_courses else "None"
        elif k_alias == "date":
            value = today
        elif k_alias == "signatureofthestudent":
            value = student_name
        elif k_alias == "forwardingremarks":
            value = random.choice(["Recommended", "No objection", "Eligible for registration"])
        elif k_alias == "deanheaddirectorcoordinator":
            value = random.choice(["Dr. S. Rao", "Prof. A. Singh", "Dr. M. Iyer"])
        elif k_alias == "warden":
            value = random.choice(["Mr. P. Kumar", "Ms. R. Das"])
        elif k_alias == "chiefwarden":
            value = random.choice(["Dr. S. Banerjee", "Dr. T. Roy"])
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_27.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_27_filled.txt')
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