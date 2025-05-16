import os
import re
import random
import datetime

FORMS_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_text'
FORMS_FILL_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_filled'

# Define some person profiles
person_profiles = [
    {
        "Name": "Amit Sharma",
        "Email": "amit.sharma@gmail.com",
        "Phone No": "+91-9876543210",
        "City": "Delhi",
        "Address": "Flat No. 12B, 3rd Floor, Metro Heights Apartments, Connaught Place, New Delhi - 110001"
    },
    {
        "Name": "Priya Singh",
        "Email": "priya.singh@gmail.com",
        "Phone No": "+91-9123456789",
        "City": "Mumbai",
        "Address": "Apt 403, Sea View Residency, Near Girgaon Chowpatty, Marine Drive, Mumbai, Maharashtra - 400002"
    },
    {
        "Name": "Rahul Verma",
        "Email": "rahul.verma@gmail.com",
        "Phone No": "+91-9988776655",
        "City": "Bengaluru",
        "Address": "House No. 25, 2nd Cross, Church Street, MG Road, Shivajinagar, Bengaluru, Karnataka - 560001"
    },
    {
        "Name": "Sneha Patel",
        "Email": "sneha.patel@gmail.com",
        "Phone No": "+91-9001122334",
        "City": "Ahmedabad",
        "Address": "Bungalow No. 17, Sunrise Villas, Near Swastik Cross Road, CG Road, Navrangpura, Ahmedabad, Gujarat - 380009"
    },

    {
        "Name": "Meera Iyer",
        "Email": "meera.iyer@gmail.com",
        "Phone No": "+91-9445566778",
        "City": "Chennai",
        "Address": "Plot No. 18, 2nd Street, Besant Nagar, Chennai, Tamil Nadu - 600090"
    },
    {
        "Name": "Arjun Deshmukh",
        "Email": "arjun.deshmukh@gmail.com",
        "Phone No": "+91-9823456781",
        "City": "Pune",
        "Address": "Row House 12, Green Meadows Society, Baner Road, Pune, Maharashtra - 411045"
    },

    {
        "Name": "Naveen Reddy",
        "Email": "naveen.reddy@gmail.com",
        "Phone No": "+91-9988123456",
        "City": "Hyderabad",
        "Address": "Villa No. 9, Pearl City Villas, Jubilee Hills, Hyderabad, Telangana - 500033"
    },
    {
        "Name": "Farah Khan",
        "Email": "farah.khan@gmail.com",
        "Phone No": "+91-9911223344",
        "City": "Lucknow",
        "Address": "H.No. 23, Gulmohar Colony, Near Hazratganj Market, Lucknow, Uttar Pradesh - 226001"
    },

    {
        "Name": "Anirban Ghosh",
        "Gender": "Male",
        "Email": "anirban.ghosh@gmail.com",
        "Phone No": "+91-9830011223",
        "City": "Kolkata",
        "Address": "Flat 5C, Shantiniketan Residency, 45 Gariahat Road, Ballygunge, Kolkata, West Bengal - 700019"
    },
    {
        "Name": "Sourav Sen",
        "Gender": "Male",
        "Email": "sourav.sen@gmail.com",
        "Phone No": "+91-9800011223",
        "City": "Kolkata",
        "Address": "House No. 7, Lake Gardens Housing Complex, Prince Anwar Shah Road, Kolkata, West Bengal - 700045"
    },
    {
        "Name": "Arka Dutta",
        "Gender": "Male",
        "Email": "arka.dutta@gmail.com",
        "Phone No": "+91-9900990088",
        "City": "Kolkata",
        "Address": "B-102, Orchid Tower, Rajarhat Main Road, Near City Centre 2, Kolkata, West Bengal - 700136"
    },
    {
        "Name": "Debdeep Mukherjee",
        "Gender": "Male",
        "Email": "debdeep.mukherjee@gmail.com",
        "Phone No": "+91-9900112233",
        "City": "Kolkata",
        "Address": "Block C, Flat 203, South City Residency, Prince Anwar Shah Road, Kolkata, West Bengal - 700068"
    },
    {
        "Name": "Ritoban Bhattacharya",
        "Gender": "Male",
        "Email": "ritoban.bhattacharya@gmail.com",
        "Phone No": "+91-9812345678",
        "City": "Kolkata",
        "Address": "Flat 2B, Saptarshi Apartments, 102 Jodhpur Park, Kolkata, West Bengal - 700068"
    },
    {
        "Name": "Mainak Sarkar",
        "Gender": "Male",
        "Email": "mainak.sarkar@gmail.com",
        "Phone No": "+91-9876567890",
        "City": "Kolkata",
        "Address": "House No. 28, Deshapriya Park East, Near Rashbehari Avenue, Kolkata, West Bengal - 700029"
    },
    {
        "Name": "Saptarshi Roy",
        "Gender": "Male",
        "Email": "saptarshi.roy@gmail.com",
        "Phone No": "+91-9800456123",
        "City": "Kolkata",
        "Address": "Flat 4D, Krishna Enclave, 88A Naktala Road, Garia, Kolkata, West Bengal - 700047"
    },
    {
        "Name": "Dipayan Das",
        "Gender": "Male",
        "Email": "dipayan.das@gmail.com",
        "Phone No": "+91-9832154896",
        "City": "Kolkata",
        "Address": "House No. 50, Shibpur Road, Near Howrah AC Market, Kolkata, West Bengal - 711102"
    },
    {
        "Name": "Animesh Chatterjee",
        "Gender": "Male",
        "Email": "animesh.chatterjee@gmail.com",
        "Phone No": "+91-9887788990",
        "City": "Kolkata",
        "Address": "1st Floor, Gitanjali Apartments, 7A Beliaghata Main Road, Kolkata, West Bengal - 700085"
    },
    {
        "Name": "Niladri Sinha",
        "Gender": "Male",
        "Email": "niladri.sinha@gmail.com",
        "Phone No": "+91-9876543221",
        "City": "Kolkata",
        "Address": "Flat No. 12, Sukriti Residency, Behala Chowrasta, Kolkata, West Bengal - 700034"
    },

    {
        "Name": "Ritika Basu",
        "Gender": "Female",
        "Email": "ritika.basu@gmail.com",
        "Phone No": "+91-9870012345",
        "City": "Kolkata",
        "Address": "3rd Floor, Siddharth Apartments, 22 Park Circus, Beck Bagan, Kolkata, West Bengal - 700017"
    },

    {
        "Name": "Moumita Roy",
        "Gender": "Female",
        "Email": "moumita.roy@gmail.com",
        "Phone No": "+91-9831122334",
        "City": "Kolkata",
        "Address": "Flat 9B, Ujjwala Apartments, Salt Lake Sector V, Near Wipro Campus, Kolkata, West Bengal - 700091"
    },

    {
        "Name": "Sraboni Chatterjee",
        "Gender": "Female",
        "Email": "sraboni.chatterjee@gmail.com",
        "Phone No": "+91-9876543212",
        "City": "Kolkata",
        "Address": "Flat 3A, Ananya Apartment, Hazra Road, Kalighat, Kolkata, West Bengal - 700026"
    },

    {
        "Name": "Tiyasha Saha",
        "Gender": "Female",
        "Email": "tiyasha.saha@gmail.com",
        "Phone No": "+91-9745678912",
        "City": "Kolkata",
        "Address": "House 14, Subhas Pally, Dum Dum Road, Near Nagerbazar, Kolkata, West Bengal - 700028"
    }

    ]

sample_data = {
    "Position": ["Software Engineer", "Data Analyst", "Teacher", "Accountant", "HR Executive", "Marketing Manager"],
    "Available for Work": ["Yes", "No", "Immediately", "Within 1 Month"],
    "Level of Education": ["Bachelor's", "Master's", "PhD", "Diploma"],
    "Major": ["Computer Science", "Business Administration", "Physics", "Mathematics", "English", "Economics"],
    "Graduate Year": [str(y) for y in range(2010, 2024)],
    "Company Name": ["Tata Consultancy Services", "Infosys", "Wipro", "Reliance Industries", "HDFC Bank"],
    "Work Position": ["Software Engineer", "Analyst", "Manager", "Consultant", "Developer"],
    "Period": ["2018-2020", "2020-2022", "2019-2023", "2015-2018"],
    "Certification Title": ["Data Science Professional", "Project Management", "AWS Certified", "Digital Marketing"],
    "Organization": ["Coursera", "NIIT", "Udemy", "IIT Bombay", "IIM Bangalore"],
    "Completion Date": ["2020", "2021", "2022", "2023"]
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
    dob = datetime.date(1980, 1, 1) + datetime.timedelta(days=random.randint(0, 15000))
    form_data = {}
    last_key = ""
    for key in keys:
        if key == "Name":
            form_data[key] = person["Name"]
        elif key == "Address":
            form_data[key] = person["Address"]
        elif key == "ZIP Code":
            match = re.search(r'(\d{6})', person["Address"])
            form_data[key] = match.group(1) if match else "000000"
        elif key == "Date of Birth":
            form_data[key] = format_date(dob, date_format)
        elif key == "Phone No":
            form_data[key] = person["Phone No"]
        elif key == "Email":
            form_data[key] = person["Email"]
        elif key == "Position":
            form_data[key] = random.choice(sample_data["Position"])
        elif key == "Available for Work":
            form_data[key] = random.choice(sample_data["Available for Work"])
        elif key == "Level of Education":
            form_data[key] = random.choice(sample_data["Level of Education"])
        elif key == "Major":
            form_data[key] = random.choice(sample_data["Major"])
        elif key == "Graduate Year":
            form_data[key] = random.choice(sample_data["Graduate Year"])
        elif key == "Company Name":
            form_data[key] = random.choice(sample_data["Company Name"])
        elif key == "Position":
            form_data[key] = random.choice(sample_data["Work Position"])
        elif key == "Period":
            form_data[key] = random.choice(sample_data["Period"])
        elif key == "Certification Title":
            form_data[key] = random.choice(sample_data["Certification Title"])
        elif key == "Organization":
            form_data[key] = random.choice(sample_data["Organization"])
        elif key == "Completion Date":
            form_data[key] = random.choice(sample_data["Completion Date"])
        else:
            form_data[key] = "Sample Value"
        last_key = key
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_3.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_3_filled.txt')
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
