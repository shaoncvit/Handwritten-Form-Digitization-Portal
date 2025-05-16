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

ORDER_ITEMS = [
    {"desc": "A4 Printing Paper (500 sheets)", "price": 350},
    {"desc": "Ballpoint Pens (Pack of 10)", "price": 120},
    {"desc": "Stapler Machine", "price": 220},
    {"desc": "Whiteboard Marker (Set of 4)", "price": 180},
    {"desc": "Desk Organizer", "price": 450},
    {"desc": "USB Flash Drive 32GB", "price": 600},
    {"desc": "Notebook (200 pages)", "price": 90},
    {"desc": "Calculator", "price": 300},
    {"desc": "Sticky Notes (Pack of 12)", "price": 80},
    {"desc": "Highlighter Pens (Set of 5)", "price": 150},
]

ORDER_METHODS = ["Online", "Phone", "In-Person", "Email"]
ORDER_STATUS = ["STARTED", "COMPLETED", "DELIVERED"]


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
    field_pattern = re.compile(r"^([A-Za-z0-9&/()' .\-]+):", re.MULTILINE)
    keys = []
    for line in form_text.splitlines():
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append(key)
    return keys

def fill_order_details():
    num_items = random.randint(2, 5)
    items = random.sample(ORDER_ITEMS, num_items)
    order_lines = []
    total = 0
    for idx, item in enumerate(items, 1):
        qty = random.randint(1, 10)
        price = item["price"]
        discount = random.choice([0, 5, 10, 15])  # percent
        line_total = qty * price * (1 - discount/100)
        order_lines.append({
            "NO": str(idx),
            "ITEM DESCRIPTION": item["desc"],
            "QTY": str(qty),
            "PRICE": f"₹{price}",
            "DISCOUNT": f"{discount}%",
            "TOTAL": f"₹{int(line_total)}"
        })
        total += line_total
    tax = int(total * 0.18)  # 18% GST
    shipping = random.choice([0, 50, 100])
    grand_total = int(total + tax + shipping)
    return order_lines, total, tax, shipping, grand_total

def fill_form(keys, date_format):
    person = random.choice(person_profiles)
    full_name = person.get("Full Name", "")
    company = random.choice(["Tata Consultancy Services", "Infosys Ltd.", "Reliance Industries", "HDFC Bank", "Wipro Ltd.", "ITC Limited", "Larsen & Toubro", "Mahindra & Mahindra"])
    phone = person.get("Phone", "")
    email = person.get("Email", "")
    address = person.get("Address", "")
    today = datetime.date.today()
    date_str = format_date(today, date_format)
    order_no = f"ORD{random.randint(10000,99999)}"
    tracking_no = f"TRK{random.randint(100000,999999)}"
    method = random.choice(ORDER_METHODS)
    date_received = format_date(today + datetime.timedelta(days=random.randint(1,7)), date_format)
    status = random.choice(ORDER_STATUS)
    notes = random.choice(["Deliver between 10am-5pm", "Urgent delivery requested", "Gift wrap the items", "Contact before delivery", ""])
    order_lines, subtotal, tax, shipping, grand_total = fill_order_details()

    # Prepare order details fields as comma-separated lists
    order_fields = {
        "NO": ", ".join([str(i+1) for i in range(len(order_lines))]),
        "ITEM DESCRIPTION": ", ".join([l["ITEM DESCRIPTION"] for l in order_lines]),
        "QTY": ", ".join([l["QTY"] for l in order_lines]),
        "PRICE": ", ".join([l["PRICE"] for l in order_lines]),
        "DISCOUNT": ", ".join([l["DISCOUNT"] for l in order_lines]),
        "TOTAL": ", ".join([l["TOTAL"] for l in order_lines]),
    }

    # Map fields
    form_data = {}
    for key in keys:
        key_lower = key.replace(" ","").replace("_","").replace("/","").replace(",","").lower()
        if key_lower == "name":
            form_data[key] = full_name
        elif key_lower == "orderno":
            form_data[key] = order_no
        elif key_lower == "date":
            form_data[key] = date_str
        elif key_lower == "company":
            form_data[key] = company
        elif key_lower == "phoneno":
            form_data[key] = phone
        elif key_lower == "email":
            form_data[key] = email
        elif key_lower == "address":
            form_data[key] = address
        elif key_lower == "method":
            form_data[key] = method
        elif key_lower == "trackingno":
            form_data[key] = tracking_no
        elif key_lower == "datereceived":
            form_data[key] = date_received
        elif key_lower == "orderstatus":
            form_data[key] = status
        elif key_lower == "notes":
            form_data[key] = notes
        elif key_lower == "tax":
            form_data[key] = f"₹{tax}"
        elif key_lower == "shipping":
            form_data[key] = f"₹{shipping}"
        elif key_lower == "total":
            form_data[key] = f"₹{grand_total}"
        elif key in order_fields:
            form_data[key] = order_fields[key]
        else:
            form_data[key] = ""
    return form_data

def fill_form_text(form_text, form_data):
    def replacer(match):
        key = match.group(1).strip()
        value = form_data.get(key, "")
        return f"{key}: {value}"
    field_pattern = re.compile(r"^([A-Za-z0-9&/()' .\-]+):.*$", re.MULTILINE)
    filled_text = field_pattern.sub(replacer, form_text)
    return filled_text

def main():
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_7.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_7_filled.txt')
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
