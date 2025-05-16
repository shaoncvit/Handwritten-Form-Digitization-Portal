import re

person_profiles = [
    {
        "Full Name": "Amit Sharma",
        "Email": "amit.sharma@gmail.com",
        "Phone": "+91-9876543210",
        "City": "New Delhi",
        "State/Province": "Delhi",
        "Country": "India",
        "Address": "Flat No. 12B, 3rd Floor, Metro Heights Apartments, Connaught Place, New Delhi - 110001"
    },
    {
        "Full Name": "Priya Singh",
        "Email": "priya.singh@gmail.com",
        "Phone": "+91-9123456789",
        "City": "Mumbai",
        "State/Province": "Maharashtra",
        "Country": "India",
        "Address": "Apt 403, Sea View Residency, Near Girgaon Chowpatty, Marine Drive, Mumbai, Maharashtra - 400002"
    },
    {
        "Full Name": "Rahul Verma",
        "Email": "rahul.verma@gmail.com",
        "Phone": "+91-9988776655",
        "City": "Bengaluru",
        "State/Province": "Karnataka",
        "Country": "India",
        "Address": "House No. 25, 2nd Cross, Church Street, MG Road, Shivajinagar, Bengaluru, Karnataka - 560001"
    },
    {
        "Full Name": "Sneha Patel",
        "Email": "sneha.patel@gmail.com",
        "Phone": "+91-9001122334",
        "City": "Ahmedabad",
        "State/Province": "Gujarat",
        "Country": "India",
        "Address": "Bungalow No. 17, Sunrise Villas, Near Swastik Cross Road, CG Road, Navrangpura, Ahmedabad, Gujarat - 380009"
    },

    {
        "Full Name": "Meera Iyer",
        "Email": "meera.iyer@gmail.com",
        "Phone": "+91-9445566778",
        "City": "Chennai",
        "State/Province": "Tamil Nadu",
        "Country": "India",
        "Address": "Plot No. 18, 2nd Street, Besant Nagar, Chennai, Tamil Nadu - 600090"
    },
    {
        "Full Name": "Arjun Deshmukh",
        "Email": "arjun.deshmukh@gmail.com",
        "Phone": "+91-9823456781",
        "City": "Pune",
        "State/Province": "Maharashtra",
        "Country": "India",
        "Address": "Row House 12, Green Meadows Society, Baner Road, Pune, Maharashtra - 411045"
    },

    {
        "Full Name": "Naveen Reddy",
        "Email": "naveen.reddy@gmail.com",
        "Phone": "+91-9988123456",
        "City": "Hyderabad",
        "State/Province": "Telangana",
        "Country": "India",
        "Address": "Villa No. 9, Pearl City Villas, Jubilee Hills, Hyderabad, Telangana - 500033"
    },
    {
        "Full Name": "Farah Khan",
        "Email": "farah.khan@gmail.com",
        "Phone": "+91-9911223344",
        "City": "Lucknow",
        "State/Province": "Uttar Pradesh",
        "Country": "India",
        "Address": "H.No. 23, Gulmohar Colony, Near Hazratganj Market, Lucknow, Uttar Pradesh - 226001"
    },

    {
        "Full Name": "Anirban Ghosh",
        "Gender": "Male",
        "Email": "anirban.ghosh@gmail.com",
        "Phone": "+91-9830011223",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Flat 5C, Shantiniketan Residency, 45 Gariahat Road, Ballygunge, Kolkata, West Bengal - 700019"
    },
    {
        "Full Name": "Sourav Sen",
        "Gender": "Male",
        "Email": "sourav.sen@gmail.com",
        "Phone": "+91-9800011223",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "House No. 7, Lake Gardens Housing Complex, Prince Anwar Shah Road, Kolkata, West Bengal - 700045"
    },
    {
        "Full Name": "Arka Dutta",
        "Gender": "Male",
        "Email": "arka.dutta@gmail.com",
        "Phone": "+91-9900990088",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "B-102, Orchid Tower, Rajarhat Main Road, Near City Centre 2, Kolkata, West Bengal - 700136"
    },
    {
        "Full Name": "Debdeep Mukherjee",
        "Gender": "Male",
        "Email": "debdeep.mukherjee@gmail.com",
        "Phone": "+91-9900112233",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Block C, Flat 203, South City Residency, Prince Anwar Shah Road, Kolkata, West Bengal - 700068"
    },
    {
        "Full Name": "Ritoban Bhattacharya",
        "Gender": "Male",
        "Email": "ritoban.bhattacharya@gmail.com",
        "Phone": "+91-9812345678",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Flat 2B, Saptarshi Apartments, 102 Jodhpur Park, Kolkata, West Bengal - 700068"
    },
    {
        "Full Name": "Mainak Sarkar",
        "Gender": "Male",
        "Email": "mainak.sarkar@gmail.com",
        "Phone": "+91-9876567890",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "House No. 28, Deshapriya Park East, Near Rashbehari Avenue, Kolkata, West Bengal - 700029"
    },
    {
        "Full Name": "Saptarshi Roy",
        "Gender": "Male",
        "Email": "saptarshi.roy@gmail.com",
        "Phone": "+91-9800456123",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Flat 4D, Krishna Enclave, 88A Naktala Road, Garia, Kolkata, West Bengal - 700047"
    },
    {
        "Full Name": "Dipayan Das",
        "Gender": "Male",
        "Email": "dipayan.das@gmail.com",
        "Phone": "+91-9832154896",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "House No. 50, Shibpur Road, Near Howrah AC Market, Kolkata, West Bengal - 711102"
    },
    {
        "Full Name": "Animesh Chatterjee",
        "Gender": "Male",
        "Email": "animesh.chatterjee@gmail.com",
        "Phone": "+91-9887788990",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "1st Floor, Gitanjali Apartments, 7A Beliaghata Main Road, Kolkata, West Bengal - 700085"
    },
    {
        "Full Name": "Niladri Sinha",
        "Gender": "Male",
        "Email": "niladri.sinha@gmail.com",
        "Phone": "+91-9876543221",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Flat No. 12, Sukriti Residency, Behala Chowrasta, Kolkata, West Bengal - 700034"
    },

    {
        "Full Name": "Ritika Basu",
        "Gender": "Female",
        "Email": "ritika.basu@gmail.com",
        "Phone": "+91-9870012345",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "3rd Floor, Siddharth Apartments, 22 Park Circus, Beck Bagan, Kolkata, West Bengal - 700017"
    },

    {
        "Full Name": "Moumita Roy",
        "Gender": "Female",
        "Email": "moumita.roy@gmail.com",
        "Phone": "+91-9831122334",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Flat 9B, Ujjwala Apartments, Salt Lake Sector V, Near Wipro Campus, Kolkata, West Bengal - 700091"
    },

    {
        "Full Name": "Sraboni Chatterjee",
        "Gender": "Female",
        "Email": "sraboni.chatterjee@gmail.com",
        "Phone": "+91-9876543212",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "Flat 3A, Ananya Apartment, Hazra Road, Kalighat, Kolkata, West Bengal - 700026"
    },

    {
        "Full Name": "Tiyasha Saha",
        "Gender": "Female",
        "Email": "tiyasha.saha@gmail.com",
        "Phone": "+91-9745678912",
        "City": "Kolkata",
        "State/Province": "West Bengal",
        "Country": "India",
        "Address": "House 14, Subhas Pally, Dum Dum Road, Near Nagerbazar, Kolkata, West Bengal - 700028"
    }

    ]

# Add parsed address components to each profile for reusability
for person in person_profiles:
    addr = person.get("Address", "")
    # Try to parse components from the address string
    # Example: 'Flat No. 12B, 3rd Floor, Metro Heights Apartments, Connaught Place, New Delhi - 110001'
    parts = [p.strip() for p in addr.split(',')]
    # Flat/Door/Block No
    flat = next((p for p in parts if re.search(r'(Flat|House|Apt|Plot|Row House|Villa|Bungalow|Block|Floor|H.No\.|House No\.|Plot No\.|B-\d+|1st Floor|2nd Floor|3rd Floor|\d+)', p, re.I)), "")
    # Premises (apartment/building/society)
    premises = next((p for p in parts if re.search(r'(Apartments|Residency|Villas|Society|Tower|Enclave|Complex|Bungalow|Row House|Pearl City|Sunrise Villas|Residency|Heights|Hostel|Villa|Pearl City|Block|Floor)', p, re.I)), "")
    # Road/Street/Lane
    road = next((p for p in parts if re.search(r'(Road|Street|Lane|Cross|Avenue|Main Road|MG Road|Shivajinagar|CG Road|Prince Anwar Shah Road|Park|Sector|Circle|Chowrasta|Chowpatty|Market|Near|Besant Nagar|Baner Road|Jubilee Hills|Salt Lake|Sector)', p, re.I)), "")
    # Area/Locality
    area = next((p for p in parts if re.search(r'(Place|Nagar|Colony|Park|Garden|Chowrasta|Chowpatty|Navrangpura|Ballygunge|Behala|Kalighat|Lake Town|Salt Lake|Sector|Cross Road|Circle|Chowrasta|Chowpatty|Market|Near|Besant Nagar|Baner Road|Jubilee Hills|Salt Lake|Sector)', p, re.I)), "")
    # Town/City/District
    city = person.get("City", "")
    # State
    state = person.get("State/Province", "")
    # PIN
    pin_match = re.search(r'(\d{6})', addr)
    pin = pin_match.group(1) if pin_match else ""
    person["Flat/Door/Block No"] = flat
    person["Premises"] = premises
    person["Road/Street/Lane"] = road
    person["Area/Locality"] = area
    person["Town/City/District"] = city
    person["State/Province"] = state
    person["PIN"] = pin