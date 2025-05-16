import os
import re
import random
import datetime

FORMS_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_text'
FORMS_FILL_DIR = '/home/shaon/Handwritten-Form-Digitization-Portal/final_selected_filled'

# Example person profiles (expand as needed)
person_profiles = [
    {
        "Name": "Amit Sharma",
        "Email": "amit.sharma@gmail.com",
        "Contact Number": "+91-9876543210",
        "Address": "Flat No. 12B, 3rd Floor, Metro Heights Apartments, Connaught Place, New Delhi - 110001",
        "Gender": "Male",
        "Father's Name": "Rajesh Sharma",
        "Mother's Name": "Sunita Sharma",
        "Person to contact in case of emergency": "Priya Sharma",
        "Emergency Contact Number": "+91-9123456789"
    },
    {
        "Name": "Priya Singh",
        "Email": "priya.singh@gmail.com",
        "Contact Number": "+91-9123456789",
        "Address": "Apt 403, Sea View Residency, Near Girgaon Chowpatty, Marine Drive, Mumbai, Maharashtra - 400002",
        "Gender": "Female",
        "Father's Name": "Ramesh Singh",
        "Mother's Name": "Kavita Singh",
        "Person to contact in case of emergency": "Amit Singh",
        "Emergency Contact Number": "+91-9876543210"
    },
    {
        "Name": "Rahul Verma",
        "Email": "rahul.verma@gmail.com",
        "Contact Number": "+91-9988776655",
        "Address": "House No. 25, 2nd Cross, Church Street, MG Road, Shivajinagar, Bengaluru, Karnataka - 560001",
        "Gender": "Male",
        "Father's Name": "Suresh Verma",
        "Mother's Name": "Meena Verma",
        "Person to contact in case of emergency": "Sneha Verma",
        "Emergency Contact Number": "+91-9001122334"
    },
    {
        "Name": "Sneha Patel",
        "Email": "sneha.patel@gmail.com",
        "Contact Number": "+91-9001122334",
        "Address": "Bungalow No. 17, Sunrise Villas, Near Swastik Cross Road, CG Road, Navrangpura, Ahmedabad, Gujarat - 380009",
        "Gender": "Female",
        "Father's Name": "Mahesh Patel",
        "Mother's Name": "Nita Patel",
        "Person to contact in case of emergency": "Rohit Patel",
        "Emergency Contact Number": "+91-9988776655"
    }
]

sample_data = {
    "Occupation": ["Student", "Engineer", "Doctor", "Teacher", "Business Analyst", "Accountant", "Software Developer"],
    "Civil Status": ["Single", "Married", "Divorced", "Widowed"],
    "Citizenship": ["Indian"],
    "Religion": ["Hindu", "Muslim", "Christian", "Sikh", "Jain", "Buddhist"],
    "Language": ["Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Gujarati", "Punjabi", "English"],
    "Father's Occupation": ["Engineer", "Teacher", "Businessman", "Doctor", "Retired"],
    "Mother's Occupation": ["Homemaker", "Teacher", "Doctor", "Businesswoman", "Retired"],
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
    age = datetime.date.today().year - dob.year
    height = random.randint(150, 190)  # cm
    weight = random.randint(45, 95)    # kg

    # Shorten address: just city and state
    address_parts = person["Address"].split(",")
    if len(address_parts) >= 2:
        short_address = address_parts[-3].strip() + ", " + address_parts[-2].strip()  # e.g., "Ahmedabad, Gujarat"
    else:
        short_address = person["Address"]

    form_data = {}
    # Track last key for parent occupation logic
    last_key = ""
    for key in keys:
        if key == "Name":
            form_data[key] = person["Name"]
        elif key == "Date of Birth":
            form_data[key] = format_date(dob, date_format)
        elif key == "Address":
            form_data[key] = short_address
        elif key == "Contact Number":
            # If this is the emergency contact, use that, else main
            if "emergency" in last_key.lower():
                form_data[key] = person.get("Emergency Contact Number", person["Contact Number"])
            else:
                form_data[key] = person["Contact Number"]
        elif key == "Email":
            form_data[key] = person["Email"]
        elif key == "Occupation":
            # If previous key was Father's Name or Mother's Name, use parent occupation
            if last_key == "Father's Name":
                form_data[key] = random.choice(sample_data["Father's Occupation"])
            elif last_key == "Mother's Name":
                form_data[key] = random.choice(sample_data["Mother's Occupation"])
            else:
                form_data[key] = random.choice(sample_data["Occupation"])
        elif key == "Age":
            form_data[key] = str(age)
        elif key == "Gender":
            form_data[key] = person["Gender"]
        elif key == "Civil Status":
            form_data[key] = random.choice(sample_data["Civil Status"])
        elif key == "Citizenship":
            form_data[key] = random.choice(sample_data["Citizenship"])
        elif key == "Height":
            form_data[key] = f"{height} cm"
        elif key == "Weight":
            form_data[key] = f"{weight} kg"
        elif key == "Religion":
            form_data[key] = random.choice(sample_data["Religion"])
        elif key == "Language":
            form_data[key] = random.choice(sample_data["Language"])
        elif key == "Father's Name":
            form_data[key] = person["Father's Name"]
        elif key == "Mother's Name":
            form_data[key] = person["Mother's Name"]
        elif key == "Person to contact in case of emergency":
            form_data[key] = person["Person to contact in case of emergency"]
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_2.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_2_filled.txt')
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
