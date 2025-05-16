import os
import re
import random
import json
import datetime

# Directory containing your form .txt files
FORMS_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_text'
FORMS_FILL_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_filled'

# Define some person profiles
person_profiles = [
    {
        "Full Name": "Amit Sharma",
        "Email": "amit.sharma@gmail.com",
        "Phone": "+91-9876543210",
        "City": "Delhi",
        "Address": "Flat No. 12B, 3rd Floor, Metro Heights Apartments, Connaught Place, New Delhi - 110001"
    },
    {
        "Full Name": "Priya Singh",
        "Email": "priya.singh@gmail.com",
        "Phone": "+91-9123456789",
        "City": "Mumbai",
        "Address": "Apt 403, Sea View Residency, Near Girgaon Chowpatty, Marine Drive, Mumbai, Maharashtra - 400002"
    },
    {
        "Full Name": "Rahul Verma",
        "Email": "rahul.verma@gmail.com",
        "Phone": "+91-9988776655",
        "City": "Bengaluru",
        "Address": "House No. 25, 2nd Cross, Church Street, MG Road, Shivajinagar, Bengaluru, Karnataka - 560001"
    },
    {
        "Full Name": "Sneha Patel",
        "Email": "sneha.patel@gmail.com",
        "Phone": "+91-9001122334",
        "City": "Ahmedabad",
        "Address": "Bungalow No. 17, Sunrise Villas, Near Swastik Cross Road, CG Road, Navrangpura, Ahmedabad, Gujarat - 380009"
    },

    {
        "Full Name": "Meera Iyer",
        "Email": "meera.iyer@gmail.com",
        "Phone": "+91-9445566778",
        "City": "Chennai",
        "Address": "Plot No. 18, 2nd Street, Besant Nagar, Chennai, Tamil Nadu - 600090"
    },
    {
        "Full Name": "Arjun Deshmukh",
        "Email": "arjun.deshmukh@gmail.com",
        "Phone": "+91-9823456781",
        "City": "Pune",
        "Address": "Row House 12, Green Meadows Society, Baner Road, Pune, Maharashtra - 411045"
    },

    {
        "Full Name": "Naveen Reddy",
        "Email": "naveen.reddy@gmail.com",
        "Phone": "+91-9988123456",
        "City": "Hyderabad",
        "Address": "Villa No. 9, Pearl City Villas, Jubilee Hills, Hyderabad, Telangana - 500033"
    },
    {
        "Full Name": "Farah Khan",
        "Email": "farah.khan@gmail.com",
        "Phone": "+91-9911223344",
        "City": "Lucknow",
        "Address": "H.No. 23, Gulmohar Colony, Near Hazratganj Market, Lucknow, Uttar Pradesh - 226001"
    },

    {
        "Full Name": "Anirban Ghosh",
        "Gender": "Male",
        "Email": "anirban.ghosh@gmail.com",
        "Phone": "+91-9830011223",
        "City": "Kolkata",
        "Address": "Flat 5C, Shantiniketan Residency, 45 Gariahat Road, Ballygunge, Kolkata, West Bengal - 700019"
    },
    {
        "Full Name": "Sourav Sen",
        "Gender": "Male",
        "Email": "sourav.sen@gmail.com",
        "Phone": "+91-9800011223",
        "City": "Kolkata",
        "Address": "House No. 7, Lake Gardens Housing Complex, Prince Anwar Shah Road, Kolkata, West Bengal - 700045"
    },
    {
        "Full Name": "Arka Dutta",
        "Gender": "Male",
        "Email": "arka.dutta@gmail.com",
        "Phone": "+91-9900990088",
        "City": "Kolkata",
        "Address": "B-102, Orchid Tower, Rajarhat Main Road, Near City Centre 2, Kolkata, West Bengal - 700136"
    },
    {
        "Full Name": "Debdeep Mukherjee",
        "Gender": "Male",
        "Email": "debdeep.mukherjee@gmail.com",
        "Phone": "+91-9900112233",
        "City": "Kolkata",
        "Address": "Block C, Flat 203, South City Residency, Prince Anwar Shah Road, Kolkata, West Bengal - 700068"
    },
    {
        "Full Name": "Ritoban Bhattacharya",
        "Gender": "Male",
        "Email": "ritoban.bhattacharya@gmail.com",
        "Phone": "+91-9812345678",
        "City": "Kolkata",
        "Address": "Flat 2B, Saptarshi Apartments, 102 Jodhpur Park, Kolkata, West Bengal - 700068"
    },
    {
        "Full Name": "Mainak Sarkar",
        "Gender": "Male",
        "Email": "mainak.sarkar@gmail.com",
        "Phone": "+91-9876567890",
        "City": "Kolkata",
        "Address": "House No. 28, Deshapriya Park East, Near Rashbehari Avenue, Kolkata, West Bengal - 700029"
    },
    {
        "Full Name": "Saptarshi Roy",
        "Gender": "Male",
        "Email": "saptarshi.roy@gmail.com",
        "Phone": "+91-9800456123",
        "City": "Kolkata",
        "Address": "Flat 4D, Krishna Enclave, 88A Naktala Road, Garia, Kolkata, West Bengal - 700047"
    },
    {
        "Full Name": "Dipayan Das",
        "Gender": "Male",
        "Email": "dipayan.das@gmail.com",
        "Phone": "+91-9832154896",
        "City": "Kolkata",
        "Address": "House No. 50, Shibpur Road, Near Howrah AC Market, Kolkata, West Bengal - 711102"
    },
    {
        "Full Name": "Animesh Chatterjee",
        "Gender": "Male",
        "Email": "animesh.chatterjee@gmail.com",
        "Phone": "+91-9887788990",
        "City": "Kolkata",
        "Address": "1st Floor, Gitanjali Apartments, 7A Beliaghata Main Road, Kolkata, West Bengal - 700085"
    },
    {
        "Full Name": "Niladri Sinha",
        "Gender": "Male",
        "Email": "niladri.sinha@gmail.com",
        "Phone": "+91-9876543221",
        "City": "Kolkata",
        "Address": "Flat No. 12, Sukriti Residency, Behala Chowrasta, Kolkata, West Bengal - 700034"
    },

    {
        "Full Name": "Ritika Basu",
        "Gender": "Female",
        "Email": "ritika.basu@gmail.com",
        "Phone": "+91-9870012345",
        "City": "Kolkata",
        "Address": "3rd Floor, Siddharth Apartments, 22 Park Circus, Beck Bagan, Kolkata, West Bengal - 700017"
    },

    {
        "Full Name": "Moumita Roy",
        "Gender": "Female",
        "Email": "moumita.roy@gmail.com",
        "Phone": "+91-9831122334",
        "City": "Kolkata",
        "Address": "Flat 9B, Ujjwala Apartments, Salt Lake Sector V, Near Wipro Campus, Kolkata, West Bengal - 700091"
    },

    {
        "Full Name": "Sraboni Chatterjee",
        "Gender": "Female",
        "Email": "sraboni.chatterjee@gmail.com",
        "Phone": "+91-9876543212",
        "City": "Kolkata",
        "Address": "Flat 3A, Ananya Apartment, Hazra Road, Kalighat, Kolkata, West Bengal - 700026"
    },

    {
        "Full Name": "Tiyasha Saha",
        "Gender": "Female",
        "Email": "tiyasha.saha@gmail.com",
        "Phone": "+91-9745678912",
        "City": "Kolkata",
        "Address": "House 14, Subhas Pally, Dum Dum Road, Near Nagerbazar, Kolkata, West Bengal - 700028"
    }

    ]

# Company and position pairs
company_positions = [
    ("Tata Consultancy Services", "Software Engineer"),
    ("Infosys", "Data Scientist"),
    ("Wipro", "Manager"),
    ("Reliance Industries", "Analyst"),
    ("HDFC Bank", "Consultant")
]

# Degree and university pairs
degree_university = [
    ("B.Tech Computer Science", "IIT Delhi"),
    ("MBA", "IIM Ahmedabad"),
    ("B.Com", "Delhi University"),
    ("M.Sc Physics", "Anna University"),
    ("B.A. Economics", "Jadavpur University")
]

# Other fields
sample_data = {
    "Nationality": ["Indian"],
    "DoB": ["1992-05-14", "1988-11-23", "1995-07-30", "1990-01-01"],
    "Driving License": ["Yes", "No"],
    "Years of work": ["2", "5", "10", "7", "3", "8"],
    "Marital Status": ["Single", "Married"],
    "number of dependent(s)": ["0", "1", "2", "3"],
    "Year of Graduate": ["2012", "2015", "2018", "2020", "2016", "2019", "2013"],
    "Grade": ["A", "B", "C", "First Class", "Distinction"],
    "Reason for Leaving": [
        "Career growth", "Relocation", "Better opportunity", "Personal reasons", "Higher studies", "Family commitment"
    ],
    "Skill & Training Achievement(s)": [
        "Python", "Data Analysis", "Project Management", "Machine Learning", "Java", "Cloud Computing", "Digital Marketing",
        "Financial Analysis", "Public Speaking"
    ],
    "Level": ["Beginner", "Intermediate", "Expert"],
    "Institute": [
        "NIIT", "Aptech", "Coursera", "Udemy", "UpGrad", "Simplilearn", "Edureka", "Great Learning", "IIT Bombay", "IIM Bangalore"
    ]
}

def extract_keys(form_text):
    # Regex to find lines that look like fields (ending with ':', or with options)
    field_pattern = re.compile(r'^([A-Za-z &/()]+):')
    keys = []
    for line in form_text.splitlines():
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append(key)
    return keys

def fill_form(keys, date_format):
    person = random.choice(person_profiles)
    company, position = random.choice(company_positions)
    degree, university = random.choice(degree_university)
    city = person["City"]

    form_data = {}
    for key in keys:
        if key == "Full Name":
            form_data[key] = person["Full Name"]
        elif key == "Email":
            form_data[key] = person["Email"]
        elif key == "Phone":
            form_data[key] = person["Phone"]
        elif key == "City":
            form_data[key] = city
        elif key == "Address":
            form_data[key] = person["Address"]
        elif key == "Company":
            form_data[key] = company
        elif key == "Position":
            form_data[key] = position
        elif key == "Degree/Course":
            form_data[key] = degree
        elif key == "University/Institute":
            form_data[key] = university
        elif key == "DoB":
            # Use a random date from sample_data, but format it
            dob_str = random.choice(sample_data["DoB"])
            dob_obj = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date()
            form_data[key] = format_date(dob_obj, date_format)
        elif key in sample_data:
            form_data[key] = random.choice(sample_data[key])
        else:
            form_data[key] = "Sample Value"
    return form_data

def fill_form_text(form_text, form_data, date_format):
    def replacer(match):
        key = match.group(1).strip()
        # Special handling for Date of Application
        if key == "Date of Application":
            today = datetime.date.today()
            random_days = random.randint(0, 30)
            date_obj = today - datetime.timedelta(days=random_days)
            value = format_date(date_obj, date_format)
            return f"{key}: {value}"
        # Special handling for fields with options (comma or multiple choices)
        line = match.group(0)
        after_colon = line.split(":", 1)[1].strip()
        # If comma-separated options (e.g., Employment Type)
        if "," in after_colon and not after_colon.startswith(" "):
            options = [opt.strip() for opt in after_colon.split(",")]
            value = random.choice(options)
            return f"{key}: {value}"
        # If space-separated options (e.g., Driving License: No  Yes)
        if key == "Driving License" and ("No" in after_colon and "Yes" in after_colon):
            options = [opt.strip() for opt in after_colon.split() if opt.strip()]
            value = random.choice(options)
            return f"{key}: {value}"
        # If the key is "Year" and value is "Sample Value", pick a realistic year
        if key == "Year":
            value = random.choice(["2018", "2019", "2020", "2021", "2022", "2023","2024","2025"])
            return f"{key}: {value}"
        # Default: use form_data
        value = form_data.get(key, "")
        return f"{key}: {value}"
    field_pattern = re.compile(r'^([A-Za-z &/()]+):.*$', re.MULTILINE)
    filled_text = field_pattern.sub(replacer, form_text)
    return filled_text

def format_date(date_obj, fmt):
    if fmt == "DD-MM-YYYY":
        return date_obj.strftime("%d-%m-%Y")
    elif fmt == "YYYY-MM-DD":
        return date_obj.strftime("%Y-%m-%d")
    elif fmt == "MM-DD-YYYY":
        return date_obj.strftime("%m-%d-%Y")
    else:
        return date_obj.strftime("%Y-%m-%d")  # default

def main():
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_1.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_1_filled.txt')
    with open(FORM_PATH, 'r') as f:
        form_text = f.read()
    keys = extract_keys(form_text)
    # Pick a random date format for this form
    date_format = random.choice(["DD-MM-YYYY", "YYYY-MM-DD", "MM-DD-YYYY"])
    form_data = fill_form(keys, date_format)
    filled_text = fill_form_text(form_text, form_data, date_format)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(filled_text)
    print(f"Filled form saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
