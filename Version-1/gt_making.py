import os
from PIL import Image
import img2pdf
from docx import Document
from docx.shared import Inches
import easyocr
from pdf2image import convert_from_path
import numpy

import random



# Names Dictionary
indian_names = {
    'male_names': [
        'Amit', 'Rahul', 'Vikram', 'Arjun', 'Raj', 'Sanjay', 'Vijay', 'Kamal', 
        'Suresh', 'Ramesh', 'Anil', 'Vikas', 'Mohit', 'Deepak', 'Ankit',

        # Additional North Indian Names
        'Aarav', 'Rohan', 'Karan', 'Varun', 'Nikhil', 'Sachin', 'Akash', 'Gaurav', 
        'Harsh', 'Kartik', 'Mehul', 'Nakul', 'Parag', 'Sameer', 'Vishal',
        
        # South Indian Names
        'Arun', 'Krishna', 'Ravi', 'Murali', 'Srinivas', 'Rajesh', 'Prakash', 
        'Shankar', 'Mahesh', 'Naresh', 'Girish', 'Dinesh', 'Sunil', 'Mohan',
        
        # East Indian Names
        'Pranab', 'Sourav', 'Biswajit', 'Subrata', 'Animesh', 'Dilip', 'Tapas', 
        'Suman', 'Probir', 'Chiranjit', 'Nirmal', 'Uttam', 'Samir', 'Swapan',
        
        # West Indian Names
        'Hitesh', 'Chirag', 'Jignesh', 'Ketan', 'Nilesh', 'Pravin', 'Rakesh', 
        'Manish', 'Vinod', 'Dharmesh', 'Jayesh', 'Navin', 'Pankaj', 'Rajiv'
    ],
    'female_names': [
        'Priya', 'Asha', 'Kavita', 'Neha', 'Anjali', 'Deepa', 'Sonia', 'Rekha', 
        'Meera', 'Geeta', 'Sunita', 'Ritu', 'Divya', 'Pooja', 'Shanti',

        # Additional North Indian Names
        'Anita', 'Madhu', 'Nisha', 'Archana', 'Pallavi', 'Kiran', 'Preeti', 
        'Rashmi', 'Aarti', 'Veena', 'Jyoti', 'Mamta', 'Sarita', 'Usha', 'Reena',
        
        # South Indian Names
        'Lakshmi', 'Padma', 'Gayatri', 'Sudha', 'Revathi', 'Indira', 'Geetha', 
        'Saroja', 'Sarojini', 'Malathi', 'Uma', 'Radha', 'Chitra', 'Vijaya',
        
        # East Indian Names
        'Dipti', 'Susmita', 'Sutapa', 'Aparajita', 'Mamoni', 'Bratati', 'Indrani', 
        'Kaberi', 'Sangita', 'Sikha', 'Arunima', 'Bornali', 'Rituparna', 'Soma',
        
        # West Indian Names
        'Hetal', 'Kiran', 'Minal', 'Nita', 'Poonam', 'Rajal', 'Seema', 
        'Tejal', 'Vaishali', 'Ami', 'Avani', 'Disha', 'Foram', 'Janvi'
    ]
}


# Surnames Dictionary
indian_surnames = {
    'surnames': [
        'Sharma', 'Kumar', 'Singh', 'Patel', 'Gupta', 'Agarwal', 'Verma', 'Malhotra', 
        'Rao', 'Reddy', 'Desai', 'Mehta', 'Chopra', 'Bose', 'Iyer', 'Chatterjee', 'Banerjee', 
        'Mukhopadhyay', 'Bhattacharyya', 'Ghosh', 
        'Das', 'Roy', 'Dutta', 'Dey', 'Mukherjee', 'Chakraborty', 'Sen', 
        'Bose', 'Kundu', 'Paul', 'Sarkar', 'Majumdar', 'Mondal', 'Chowdhury', 
        'Ganguly', 'Haldar', 'Mitra', 'Pal', 'Guha', 'Lahiri', 'Maity', 
        'Biswas', 'Basak', 'Nandi', 'Saha', 'Roychowdhury' 
    ]
}

# Date, Month, Year Dictionary
date_month_year = {
    'days': list(range(1, 32)),  # 1-31
    'months': list(range(1, 13)),  # 1-12
    'years': list(range(1950, 2025))  # 1950-2024
}

# Religion Dictionary
religions = {
    'religions': [
        'Hinduism', 'Islam', 'Christianity', 'Sikhism', 'Buddhism', 
        'Jainism', 'Judaism'
    ]
}

# Gender Dictionary
genders = {
    'genders': [
        'Male', 'Female', 'Transgender', 'Non-Binary', 'Other'
    ]
}

# Caste Dictionary
castes = {
    'general_categories': [
        'General', 'SC', 'ST', 'OBC'
    ],
    'traditional_varnas': [
        'Brahmin', 'Kshatriya', 'Vaishya', 'Shudra'
    ],
    'category': [
        'General', 'SC', 'ST', 'OBC'
    ]
}

# Occupation Dictionary
occupations = {
    'professional': [
        'Engineer', 'Doctor', 'Teacher', 'Software Developer', 'Lawyer', 
        'Architect', 'Scientist', 'Journalist', 'Banker', 'Researcher'
    ],
    'traditional': [
        'Farmer', 'Carpenter', 'Potter', 'Weaver', 'Blacksmith', 
        'Shopkeeper', 'Driver', 'Cook'
    ],
    'positions': [
        'Manager', 'Director', 'Head', 'Chief', 'Officer',
        'Executive', 'Supervisor', 'Coordinator', 'Assistant',
        'Associate', 'Specialist', 'Consultant', 'Advisor'
    ],
    'designations': [
        'Senior', 'Junior', 'Lead', 'Principal', 'Vice',
        'Deputy', 'Assistant', 'Associate', 'Chief', 'Head'
    ]
}

# Educational Courses Dictionary
courses = {
    'undergraduate': [
        'B.Tech', 'B.Sc', 'B.Com', 'BA', 'BBA', 'BCA', 'MBBS'
    ],
    'postgraduate': [
        'M.Tech', 'M.Sc', 'M.Com', 'MA', 'MBA', 'MCA', 'MD'
    ],
    'professional': [
        'CA', 'CS', 'UPSC', 'GATE', 'NET'
    ],
    'departments': [
        'Computer Science', 'Electronics', 'Mechanical', 'Civil',
        'Electrical', 'Information Technology', 'Business Administration',
        'Commerce', 'Arts', 'Science', 'Engineering', 'Medical',
        'Law', 'Management', 'Finance'
    ]
}

# Medium of Education Dictionary
education_medium = {
    'languages': [
        'English', 'Hindi', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 
        'Gujarati', 'Kannada', 'Malayalam', 'Punjabi'
    ]
}

# Marital Status Dictionary
marital_status = {
    'status': [
        'Single', 'Married', 'Divorced', 'Widowed', 'Separated'
    ]
}

# Class Dictionary
class_levels = {
    'school': [
        'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5',
        'Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10'
    ],
    'college': [
        'First Year', 'Second Year', 'Third Year', 'Fourth Year',
        'Final Year', 'Post Graduate Year 1', 'Post Graduate Year 2'
    ],
    'university': [
        'Semester 1', 'Semester 2', 'Semester 3', 'Semester 4',
        'Year 1', 'Year 2', 'Year 3', 'Year 4'
    ]
}

# Subjects Dictionary
subjects = {
    'school': [
        'Mathematics', 'Science', 'English', 'Hindi', 'Social Studies',
        'Computer Science', 'Sanskrit', 'Bengali', 'History', 'Geography',
        'Physics', 'Chemistry', 'Biology', 'Economics', 'Political Science'
    ],
    'college': [
        'Computer Science', 'Electronics', 'Mechanical', 'Civil',
        'Electrical', 'Information Technology', 'Business Administration',
        'Commerce', 'Arts', 'Science', 'Engineering', 'Medical',
        'Law', 'Management', 'Finance'
    ],
    'university': [
        'Computer Science', 'Data Science', 'Artificial Intelligence',
        'Machine Learning', 'Business Analytics', 'Finance',
        'International Business', 'Human Resource Management',
        'Marketing', 'Operations Management', 'Economics',
        'Public Policy', 'Law', 'Medicine', 'Engineering'
    ]
}

# Reasons for Leaving Dictionary
reasons_for_leaving = {
    'academic': [
        'Higher Studies', 'Change of Course', 'Transfer to Another Institution',
        'Academic Performance', 'Course Completion', 'Discontinued Studies'
    ],
    'personal': [
        'Family Circumstances', 'Health Issues', 'Financial Constraints',
        'Personal Choice', 'Relocation', 'Marriage'
    ],
    'professional': [
        'Job Opportunity', 'Career Change', 'Business Venture',
        'Professional Training', 'Work Commitments'
    ]
}

indian_locations = {
    'West Bengal': {
        'cities': [
            'Kolkata', 'Howrah', 'Siliguri', 'Durgapur', 'Asansol'
        ],
        'post_offices': {
            'Kolkata': [
                'Kolkata GPO', 'Bhawanipur PO', 'Salt Lake City PO', 
                'Park Street PO', 'Gariahat PO', 'Sudder Street PO', 
                'Ballygunge PO', 'College Street PO', 'Sealdah PO', 
                'Jadavpur PO', 'Tollygunge PO', 'Kyd Street PO', 
                'Mullick Bazar PO', 'Wellington PO'
            ],
            'Howrah': [
                'Howrah Junction PO', 'Shibpur PO', 'Santragachi PO', 
                'Golabari PO', 'Ramrajatala PO', 'Dasnagar PO', 
                'Bally PO', 'Howrah Maidan PO', 'Liluah PO'
            ],
            'Siliguri': [
                'Siliguri Main PO', 'Hill Cart Road PO', 'Darjeeling Road PO', 
                'Bidhan Nagar PO', 'Matigara PO', 'Sevoke Road PO', 
                'Pradhan Nagar PO', 'Sukna PO'
            ],
            'Durgapur': [
                'Durgapur Steel Town PO', 'Durgapur City Centre PO', 
                'Bidhannagar PO', 'Purnendu Sekhar Road PO', 
                'Damoda PO', 'Muchipara PO'
            ],
            'Asansol': [
                'Asansol Main PO', 'Asansol City PO', 'Burnpur PO', 
                'Kulti PO', 'Hirapur PO', 'Pandaveswar PO', 
                'Salanpur PO'
            ]
        },
        'police_stations': {
            'Kolkata': [
                'Kolkata Police HQ', 'Bhawanipur PS', 'Gariahat PS', 
                'Salt Lake PS', 'Park Street PS', 'Kalighat PS', 
                'Jadavpur PS', 'Tollygunge PS', 'Jorasanko PS', 
                'Bowbazar PS', 'Entally PS', 'Loudon Street PS', 
                'Shakespeare Sarani PS', 'Muchipara PS'
            ],
            'Howrah': [
                'Howrah Police Commissionerate', 'Shibpur PS', 'Santragachi PS', 
                'Bally PS', 'Golabari PS', 'Ramrajatala PS', 
                'Dasnagar PS', 'Liluah PS', 'Howrah Maidan PS'
            ],
            'Siliguri': [
                'Siliguri Police Station', 'Hill Cart Road PS', 'Matigara PS', 
                'Sevoke Road PS', 'Pradhan Nagar PS', 'Sukna PS', 
                'Bidhan Nagar PS'
            ],
            'Durgapur': [
                'Durgapur Steel Town PS', 'Durgapur City Centre PS', 
                'Bidhannagar PS', 'Muchipara PS', 'Damoda PS', 
                'Purnendu Sekhar Road PS'
            ],
            'Asansol': [
                'Asansol Main PS', 'Asansol City PS', 'Burnpur PS', 
                'Kulti PS', 'Hirapur PS', 'Pandaveswar PS', 
                'Salanpur PS'
            ]
        }
    },
    'Maharashtra': {
        'cities': [
            'Mumbai', 'Pune', 'Nagpur', 'Thane', 'Nashik'
        ],
        'post_offices': {
            'Mumbai': [
                'Mumbai GPO', 'Andheri PO', 'Bandra PO', 'Colaba PO', 
                'Marine Lines PO', 'Churchgate PO', 'Fort PO', 
                'Juhu PO', 'Santacruz PO', 'Vile Parle PO', 
                'Dadar PO', 'Goregaon PO', 'Malad PO', 'Borivali PO', 
                'Kandivali PO', 'Chembur PO', 'Khar PO'
            ],
            'Pune': [
                'Pune Head PO', 'Koregaon Park PO', 'Camp PO', 
                'Model Colony PO', 'Deccan Gymkhana PO', 'Shivajinagar PO', 
                'Kothrud PO', 'Hadapsar PO', 'Katraj PO', 'Warje PO', 
                'Baner PO', 'Aundh PO'
            ],
            'Nagpur': [
                'Nagpur GPO', 'Empress City PO', 'Civil Lines PO', 
                'Dharampeth PO', 'Congress Nagar PO', 'Sadar PO', 
                'Itwari PO', 'Sitabuldi PO', 'Neri PO', 'Gandhibagh PO'
            ],
            'Thane': [
                'Thane Head PO', 'Thane West PO', 'Thane East PO', 
                'Vartak Nagar PO', 'Kalwa PO', 'Wagle Estate PO', 
                'Ghodbunder Road PO'
            ],
            'Nashik': [
                'Nashik Head PO', 'Nashik Road PO', 'Cidco PO', 
                'College Road PO', 'Gangapur Road PO', 'Satpur PO', 
                'Deolali PO'
            ]
        },
        'police_stations': {
            'Mumbai': [
                'Mumbai Police Headquarters', 'Andheri PS', 'Bandra PS', 
                'Colaba PS', 'Marine Drive PS', 'Churchgate PS', 
                'Fort PS', 'Juhu PS', 'Santacruz PS', 'Vile Parle PS', 
                'Dadar PS', 'Goregaon PS', 'Malad PS', 'Borivali PS', 
                'Kandivali PS', 'Chembur PS', 'Khar PS'
            ],
            'Pune': [
                'Pune Police Commissionerate', 'Koregaon Park PS', 'Camp PS', 
                'Model Colony PS', 'Deccan Gymkhana PS', 'Shivajinagar PS', 
                'Kothrud PS', 'Hadapsar PS', 'Katraj PS', 'Warje PS', 
                'Baner PS', 'Aundh PS'
            ],
            'Nagpur': [
                'Nagpur City Police', 'Civil Lines PS', 'Sitabuldi PS', 
                'Dharampeth PS', 'Congress Nagar PS', 'Sadar PS', 
                'Itwari PS', 'Neri PS', 'Gandhibagh PS'
            ],
            'Thane': [
                'Thane Police Commissionerate', 'Thane West PS', 'Thane East PS', 
                'Vartak Nagar PS', 'Kalwa PS', 'Wagle Estate PS', 
                'Ghodbunder Road PS'
            ],
            'Nashik': [
                'Nashik City Police', 'Nashik Road PS', 'Cidco PS', 
                'College Road PS', 'Gangapur Road PS', 'Satpur PS', 
                'Deolali PS'
            ]
        }
    },
    'Karnataka': {
        'cities': [
            'Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum'
        ],
        'post_offices': {
            'Bangalore': [
                'Bangalore GPO', 'Indiranagar PO', 'Koramangala PO', 
                'Whitefield PO', 'Electronic City PO', 'Jayanagar PO', 
                'Malleswaram PO', 'Rajajinagar PO', 'RT Nagar PO', 
                'Marathahalli PO', 'HSR Layout PO', 'Hebbal PO'
            ],
            'Mysore': [
                'Mysore Head PO', 'Chamaraja Nagar PO', 'Saraswathipuram PO', 
                'Jayalakshmipuram PO', 'Kuvempunagar PO', 'Vijayanagar PO', 
                'Bannimantap PO', 'Metropolitan PO'
            ],
            'Hubli': [
                'Hubli Main PO', 'Dharwad PO', 'University Campus PO', 
                'Vidyanagar PO', 'Unkal PO', 'Navanagar PO'
            ],
            'Mangalore': [
                'Mangalore Head PO', 'Bunder PO', 'Hampankatta PO', 
                'Kadri PO', 'Mannagudda PO', 'Kavoor PO'
            ],
            'Belgaum': [
                'Belgaum Head PO', 'Cantonment PO', 'City PO', 
                'Tilakwadi PO', 'Vadgaon PO'
            ]
        },
        'police_stations': {
            'Bangalore': [
                'Bangalore Police Headquarters', 'Indiranagar PS', 
                'Koramangala PS', 'Whitefield PS', 'Electronic City PS', 
                'Jayanagar PS', 'Malleswaram PS', 'Rajajinagar PS', 
                'RT Nagar PS', 'Marathahalli PS', 'HSR Layout PS', 'Hebbal PS'
            ],
            'Mysore': [
                'Mysore City Police', 'Chamaraja Nagar PS', 'Saraswathipuram PS', 
                'Jayalakshmipuram PS', 'Kuvempunagar PS', 'Vijayanagar PS', 
                'Bannimantap PS', 'Metropolitan PS'
            ],
            'Hubli': [
                'Hubli Police Station', 'Dharwad PS', 'University Campus PS', 
                'Vidyanagar PS', 'Unkal PS', 'Navanagar PS'
            ],
            'Mangalore': [
                'Mangalore City Police', 'Bunder PS', 'Hampankatta PS', 
                'Kadri PS', 'Mannagudda PS', 'Kavoor PS'
            ],
            'Belgaum': [
                'Belgaum City Police', 'Cantonment PS', 'City PS', 
                'Tilakwadi PS', 'Vadgaon PS'
            ]
        }
    },
    'Tamil Nadu': {
        'cities': [
            'Chennai', 'Coimbatore', 'Madurai', 'Trichy', 'Salem'
        ],
        'post_offices': {
            'Chennai': [
                'Chennai GPO', 'Anna Nagar PO', 'Mylapore PO', 
                'T. Nagar PO', 'Egmore PO', 'Tambaram PO', 
                'Adyar PO', 'Velachery PO', 'Guindy PO', 
                'Kodambakkam PO', 'Saidapet PO', 'Nungambakkam PO'
            ],
            'Coimbatore': [
                'Coimbatore Main PO', 'RS Puram PO', 'Gandhipuram PO', 
                'Peelamedu PO', 'Saibaba Colony PO', 'Race Course PO', 
                'Ukkadam PO', 'Civil Supplies PO'
            ],
            'Madurai': [
                'Madurai GPO', 'Meenakshi Nagar PO', 'Anna Nagar PO', 
                'Villapuram PO', 'Arasaradi PO', 'Tallakulam PO', 
                'Avaraipatti PO'
            ],
            'Trichy': [
                'Trichy Head PO', 'Srirangam PO', 'Thillai Nagar PO', 
                'K. Syndicate PO', 'Woraiyur PO', 'Cantonment PO'
            ],
            'Salem': [
                'Salem Head PO', 'Fairlands PO', 'Attur Road PO', 
                'Gugai PO', 'SIDCO PO', 'Colony PO'
            ]
        },
        'police_stations': {
            'Chennai': [
                'Chennai Police Headquarters', 'Anna Nagar PS', 
                'Mylapore PS', 'T. Nagar PS', 'Egmore PS', 
                'Tambaram PS', 'Adyar PS', 'Velachery PS', 
                'Guindy PS', 'Kodambakkam PS', 'Saidapet PS', 'Nungambakkam PS'
            ],
            'Coimbatore': [
                'Coimbatore City Police', 'RS Puram PS', 'Gandhipuram PS', 
                'Peelamedu PS', 'Saibaba Colony PS', 'Race Course PS', 
                'Ukkadam PS', 'Civil Supplies PS'
            ],
            'Madurai': [
                'Madurai Police Commissionerate', 'Meenakshi Nagar PS', 
                'Anna Nagar PS', 'Villapuram PS', 'Arasaradi PS', 
                'Tallakulam PS', 'Avaraipatti PS'
            ],
            'Trichy': [
                'Trichy City Police', 'Srirangam PS', 'Thillai Nagar PS', 
                'K. Syndicate PS', 'Woraiyur PS', 'Cantonment PS'
            ],
            'Salem': [
                'Salem City Police', 'Fairlands PS', 'Attur Road PS', 
                'Gugai PS', 'SIDCO PS', 'Colony PS'
            ]
        }
    },
    'Uttar Pradesh': {
        'cities': [
            'Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Allahabad'
        ],
        'post_offices': {
            'Lucknow': [
                'Lucknow GPO', 'Hazratganj PO', 'Gomti Nagar PO', 
                'Charbagh PO', 'Civil Lines PO', 'Alambagh PO', 
                'Kaiserbagh PO', 'Mahanagar PO'
            ],
            'Kanpur': [
                'Kanpur GPO', 'Civil Lines PO', 'Yashoda Nagar PO', 
                'Kidwai Nagar PO', 'Swaroop Nagar PO', 'Kakadeo PO'
            ],
            'Varanasi': [
                'Varanasi Head PO', 'Cantonment PO', 'Banaras Hindu University PO', 
                'Lanka PO', 'Sigra PO', 'Nadesar PO'
            ],
            'Agra': [
                'Agra Head PO', 'Civil Lines PO', 'Taj Ganj PO', 
                'Sadar Bazaar PO', 'Sikandra PO', 'Ashok Nagar PO'
            ],
            'Allahabad': [
                'Allahabad Head PO', 'Civil Lines PO', 'Chowk PO', 
                'Katra PO', 'Meerganj PO', 'Colonelganj PO'
            ]
        },
        'police_stations': {
            'Lucknow': [
                'Lucknow Police Commissionerate', 'Hazratganj PS', 
                'Gomti Nagar PS', 'Charbagh PS', 'Civil Lines PS', 
                'Alambagh PS', 'Kaiserbagh PS', 'Mahanagar PS'
            ],
            'Kanpur': [
                'Kanpur Police Commissionerate', 'Civil Lines PS', 
                'Yashoda Nagar PS', 'Kidwai Nagar PS', 'Swaroop Nagar PS', 
                'Kakadeo PS'
            ],
            'Varanasi': [
                'Varanasi City Police', 'Cantonment PS', 
                'Banaras Hindu University PS', 'Lanka PS', 'Sigra PS', 
                'Nadesar PS'
            ],
            'Agra': [
                'Agra City Police', 'Civil Lines PS', 'Taj Ganj PS', 
                'Sadar Bazaar PS', 'Sikandra PS', 'Ashok Nagar PS'
            ],
            'Allahabad': [
                'Allahabad City Police', 'Civil Lines PS', 'Chowk PS', 
                'Katra PS', 'Meerganj PS', 'Colonelganj PS'
            ]
        }
    },
    'Punjab': {
        'cities': [
            'Chandigarh', 'Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala'
        ],
        'post_offices': {
            'Chandigarh': [
                'Chandigarh Head PO', 'Sector 17 PO', 'Sector 22 PO', 
                'Sector 34 PO', 'IT Park PO', 'University PO'
            ],
            'Ludhiana': [
                'Ludhiana Head PO', 'Civil Lines PO', 'Model Town PO', 
                'Pakhowal Road PO', 'Gurdev Nagar PO', 'Sarabha Nagar PO'
            ],
            'Amritsar': [
                'Amritsar Head PO', 'Golden Temple PO', 'Lawrence Road PO', 
                'Katra Ahluwalia PO', 'Ranjit Avenue PO', 'Sultanwind PO'
            ],
            'Jalandhar': [
                'Jalandhar Head PO', 'Civil Lines PO', 'Model Town PO', 
                'Defence Colony PO', 'Kakowal Road PO', 'Patel Nagar PO'
            ],
            'Patiala': [
                'Patiala Head PO', 'Bahadur Garh PO', 'Qila Mubarak PO', 
                'New Lal Bagh PO', 'Sheranwala Bagh PO'
            ]
        },
        'police_stations': {
            'Chandigarh': [
                'Chandigarh Police Headquarters', 'Sector 17 PS', 
                'Sector 22 PS', 'Sector 34 PS', 'IT Park PS', 'University PS'
            ],
            'Ludhiana': [
                'Ludhiana Police Commissionerate', 'Civil Lines PS', 
                'Model Town PS', 'Pakhowal Road PS', 'Gurdev Nagar PS', 
                'Sarabha Nagar PS'
            ],
            'Amritsar': [
                'Amritsar City Police', 'Golden Temple PS', 'Lawrence Road PS', 
                'Katra Ahluwalia PS', 'Ranjit Avenue PS', 'Sultanwind PS'
            ],
            'Jalandhar': [
                'Jalandhar City Police', 'Civil Lines PS', 'Model Town PS', 
                'Defence Colony PS', 'Kakowal Road PS', 'Patel Nagar PS'
            ],
            'Patiala': [
                'Patiala City Police', 'Bahadur Garh PS', 'Qila Mubarak PS', 
                'New Lal Bagh PS', 'Sheranwala Bagh PS'
            ]
        }
    },
    'Gujarat': {
        'cities': [
            'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar'
        ],
        'post_offices': {
            'Ahmedabad': [
                'Ahmedabad GPO', 'Satellite PO', 'Navrangpura PO', 
                'C.G. Road PO', 'Bopal PO', 'Thaltej PO', 
                'Maninagar PO', 'Isanpur PO'
            ],
            'Surat': [
                'Surat Head PO', 'Varachha Road PO', 'Adajan PO', 
                'Althan PO', 'Magob PO', 'Katargam PO'
            ],
            'Vadodara': [
                'Vadodara Head PO', 'Alkapuri PO', 'Sayajigunj PO', 
                'Akota PO', 'Race Course PO', 'Fatehgunj PO'
            ],
            'Rajkot': [
                'Rajkot Head PO', 'Race Course PO', 'Kalawad Road PO', 
                '150 Feet Ring Road PO', 'Mavdi PO', 'University Road PO'
            ],
            'Gandhinagar': [
                'Gandhinagar Head PO', 'Sector 10 PO', 'Sector 21 PO', 
                'Kudasan PO', 'Capital Complex PO'
            ]
        },
        'police_stations': {
            'Ahmedabad': [
                'Ahmedabad Police Commissionerate', 'Satellite PS', 
                'Navrangpura PS', 'C.G. Road PS', 'Bopal PS', 
                'Thaltej PS', 'Maninagar PS', 'Isanpur PS'
            ],
            'Surat': [
                'Surat City Police', 'Varachha Road PS', 'Adajan PS', 
                'Althan PS', 'Magob PS', 'Katargam PS'
            ],
            'Vadodara': [
                'Vadodara City Police', 'Alkapuri PS', 'Sayajigunj PS', 
                'Akota PS', 'Race Course PS', 'Fatehgunj PS'
            ],
            'Rajkot': [
                'Rajkot City Police', 'Race Course PS', 'Kalawad Road PS', 
                '150 Feet Ring Road PS', 'Mavdi PS', 'University Road PS'
            ],
            'Gandhinagar': [
                'Gandhinagar Police', 'Sector 10 PS', 'Sector 21 PS', 
                'Kudasan PS', 'Capital Complex PS'
            ]
        }
    }
}

# Add new dictionary for roll/enrollment numbers
student_numbers = {
    'roll_number_prefixes': ['R', 'RN', 'ROLL', 'RNO'],
    'enrollment_prefixes': ['EN', 'ENR', 'ENRL', 'ENROLL'],
    'number_lengths': [8, 10, 12, 15]
}

# Add Email Domains Dictionary
email_domains = {
    'domains': [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'rediffmail.com',
        'protonmail.com', 'icloud.com', 'aol.com', 'live.com', 'msn.com'
    ]
}

def generate_indian_phone_number():
    """
    Generates a valid Indian mobile phone number
    Starts with 6, 7, 8, or 9 as per current Indian mobile number rules
    """
    start_digits = ['6', '7', '8', '9']
    return ''.join([
        random.choice(start_digits),
        ''.join(random.choices('0123456789', k=9))
    ])

# Example of generating multiple phone numbers
phone_numbers = [generate_indian_phone_number() for _ in range(10)]


def convert_image_to_pdf(image_path, output_pdf_path):
    """
    Convert image file to PDF
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Convert image to PDF
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(image.filename))
        
        print(f"Successfully converted {image_path} to PDF: {output_pdf_path}")
        return True
    except Exception as e:
        print(f"Error converting image to PDF: {str(e)}")
        return False

def convert_pdf_to_text(pdf_path, output_text_path):
    """
    Convert PDF to text format
    """
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path)
        
        # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])
        
        # Create text file
        with open(output_text_path, 'w', encoding='utf-8') as f:
            # Process each page
            for i, image in enumerate(images):
                # Extract text using EasyOCR
                results = reader.readtext(numpy.array(image))
                text = '\n'.join([result[1] for result in results])
                
                # Write text to file
                f.write(text + '\n')
                
                # Add separator between pages
                if i < len(images) - 1:
                    f.write('_' * 50 + '\n\n')
        
        print(f"Successfully converted PDF to text: {output_text_path}")
        return True
    except Exception as e:
        print(f"Error converting PDF to text: {str(e)}")
        return False

def fill_text_with_values(input_text_path, output_text_path):
    """
    Read a text file and fill it with values
    """
    try:
        # Initialize state and city for consistent address
        state = random.choice(list(indian_locations.keys()))
        city = random.choice(indian_locations[state]['cities'])
        
        # Generate different dates for different fields
        birth_date = random.choice(date_month_year['days'])
        birth_month = random.choice(date_month_year['months'])
        birth_year = random.choice(date_month_year['years'])
        
        # Generate different dates for other fields
        promotion_date = random.choice(date_month_year['days'])
        promotion_month = random.choice(date_month_year['months'])
        promotion_year = random.choice(date_month_year['years'])
        
        eligibility_date = random.choice(date_month_year['days'])
        eligibility_month = random.choice(date_month_year['months'])
        eligibility_year = random.choice(date_month_year['years'])
        
        # Track used names to ensure uniqueness
        used_names = set()
        
        # Track student name and gender for consistency
        student_name = None
        student_gender = None
        
        # Generate family surname at the start
        family_surname = random.choice(indian_surnames['surnames'])
        
        # Generate student numbers for consistency
        roll_prefix = random.choice(student_numbers['roll_number_prefixes'])
        enroll_prefix = random.choice(student_numbers['enrollment_prefixes'])
        number_length = random.choice(student_numbers['number_lengths'])
        roll_number = f"{roll_prefix}{''.join(random.choices('0123456789', k=number_length))}"
        enrollment_number = f"{enroll_prefix}{''.join(random.choices('0123456789', k=number_length))}"
        
        # Generate class and subject for consistency
        education_level = random.choice(['school', 'college', 'university'])
        class_level = random.choice(class_levels[education_level])
        subject = random.choice(subjects[education_level])
        
        # Generate department/course for consistency
        department = random.choice(courses['departments'])
        
        # Read the input text file
        with open(input_text_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # First pass: Check if month and year fields exist separately
        has_separate_month = False
        has_separate_year = False
        for line in lines:
            line = line.lower().strip()
            if 'month' in line and not any(keyword in line for keyword in ['date', 'dob', 'birth']):
                has_separate_month = True
            if 'year' in line and not any(keyword in line for keyword in ['date', 'dob', 'birth']):
                has_separate_year = True
        
        # Second pass: Fill values
        filled_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                filled_lines.append(line)
                continue
            
            # Clean up the line by removing double colons and extra spaces
            line = line.replace('::', ':').replace('  ', ' ').strip()
            
            # Handle name fields
            if any(keyword in line.lower() for keyword in ['name', 'student name', 'first name']):
                if 'father' in line.lower():
                    # Handle father's name
                    if 'surname' in line.lower():
                        filled_lines.append(line + ": " + family_surname)
                    else:
                        while True:
                            father_name = random.choice(indian_names['male_names'])
                            if father_name not in used_names:
                                used_names.add(father_name)
                                # Only include first name, not surname
                                filled_lines.append(line + ": " + father_name)
                                break
                elif 'mother' in line.lower():
                    # Handle mother's name
                    if 'surname' in line.lower():
                        filled_lines.append(line + ": " + family_surname)
                    else:
                        while True:
                            mother_name = random.choice(indian_names['female_names'])
                            if mother_name not in used_names:
                                used_names.add(mother_name)
                                # Only include first name, not surname
                                filled_lines.append(line + ": " + mother_name)
                                break
                else:
                    # Handle student name
                    if 'surname' in line.lower():
                        filled_lines.append(line + ": " + family_surname)
                    else:
                        while True:
                            student_name = random.choice(indian_names['male_names'] + indian_names['female_names'])
                            if student_name not in used_names:
                                used_names.add(student_name)
                                # Include full name with surname
                                filled_lines.append(line + ": " + student_name + " " + family_surname)
                                # Set gender based on the name
                                student_gender = 'Male' if student_name in indian_names['male_names'] else 'Female'
                                break
            
            # Handle date fields
            elif any(keyword in line.lower() for keyword in ['date', 'dob', 'birth']):
                if 'last promotion' in line.lower():
                    filled_lines.append(line + ": " + f"{promotion_date:02d}/{promotion_month:02d}/{promotion_year}")
                elif 'eligibility' in line.lower():
                    filled_lines.append(line + ": " + f"{eligibility_date:02d}/{eligibility_month:02d}/{eligibility_year}")
                elif 'birth' in line.lower():
                    filled_lines.append(line + ": " + f"{birth_date:02d}/{birth_month:02d}/{birth_year}")
                elif 'date' in line.lower():
                    # For any other date field, use a new random date
                    new_date = random.choice(date_month_year['days'])
                    new_month = random.choice(date_month_year['months'])
                    new_year = random.choice(date_month_year['years'])
                    filled_lines.append(line + ": " + f"{new_date:02d}/{new_month:02d}/{new_year}")
                else:
                    # Default to birth date if no specific type is mentioned
                    filled_lines.append(line + ": " + f"{birth_date:02d}/{birth_month:02d}/{birth_year}")
            
            # Handle separate month field
            elif 'month' in line.lower() and not any(keyword in line.lower() for keyword in ['date', 'dob', 'birth']):
                filled_lines.append(line + ": " + f"{birth_month:02d}")
            
            # Handle separate year field
            elif 'year' in line.lower() and not any(keyword in line.lower() for keyword in ['date', 'dob', 'birth']):
                filled_lines.append(line + ": " + f"{birth_year}")
            
            # Handle address fields
            elif any(keyword in line.lower() for keyword in ['address', 'city', 'state', 'post office', 'police station', 'po', 'ps']):
                try:
                    if 'po/ps' in line.lower() or 'ps/po' in line.lower():
                        # Get PO and PS from the selected city
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        ps = random.choice(indian_locations[state]['police_stations'][city]).replace(' PS', '')
                        filled_lines.append(line + ": " + f"{po}/{ps}")
                    elif any(keyword in line.lower() for keyword in ['post office', 'po']):
                        # Get PO from the selected city
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        filled_lines.append(line + ": " + po)
                    elif any(keyword in line.lower() for keyword in ['police station', 'ps']):
                        # Get PS from the selected city
                        ps = random.choice(indian_locations[state]['police_stations'][city]).replace(' PS', '')
                        filled_lines.append(line + ": " + ps)
                    elif 'city' in line.lower():
                        # Use the selected city
                        filled_lines.append(line + ": " + city)
                    elif 'state' in line.lower():
                        # Use the selected state
                        filled_lines.append(line + ": " + state)
                    elif any(keyword in line.lower() for keyword in ['correspondence', 'address']):
                        # For correspondence address, use a complete address format with pincode
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        pincode = random.choice(pincodes[state][city])
                        filled_lines.append(line + ": " + f"{po}, {city}, {state} - {pincode}")
                    else:
                        # For general address field, use a complete address format with pincode
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        pincode = random.choice(pincodes[state][city])
                        filled_lines.append(line + ": " + f"{po}, {city}, {state} - {pincode}")
                except KeyError as e:
                    print(f"Warning: Could not find location data for {state} or {city}. Using default values.")
                    filled_lines.append(line + ": " + "Kolkata, West Bengal - 700001")  # Default fallback
            
            # Handle email field
            elif any(keyword in line.lower() for keyword in ['email', 'e-mail']):
                # Generate email based on student name
                if student_name:
                    # Convert name to lowercase and remove spaces
                    email_name = student_name.lower().replace(' ', '')
                    # Add random numbers
                    email_name += ''.join(random.choices('0123456789', k=random.randint(1, 4)))
                    # Add random domain
                    domain = random.choice(email_domains['domains'])
                    filled_lines.append(line + ": " + f"{email_name}@{domain}")
                else:
                    # Fallback if student name hasn't been processed yet
                    filled_lines.append(line + ": " + f"user{random.randint(1000, 9999)}@{random.choice(email_domains['domains'])}")
            
            # Handle gender/sex - use the gender determined from student name
            elif any(keyword in line.lower() for keyword in ['gender', 'sex']):
                if student_gender:
                    filled_lines.append(line + ": " + student_gender)
                else:
                    # Fallback if student name hasn't been processed yet
                    filled_lines.append(line + ": " + random.choice(genders['genders']))
            
            # Handle marital status
            elif any(keyword in line.lower() for keyword in ['marital status', 'marital']):
                filled_lines.append(line + ": " + random.choice(marital_status['status']))
            
            # Handle religion
            elif 'religion' in line.lower():
                filled_lines.append(line + ": " + random.choice(religions['religions']))
            
            # Handle caste/category
            elif any(keyword in line.lower() for keyword in ['caste', 'category']):
                if 'general' in line.lower():
                    filled_lines.append(line + ": " + random.choice(castes['general_categories']))
                else:
                    filled_lines.append(line + ": " + random.choice(castes['category']))
            
            # Handle occupation/position/designation
            elif any(keyword in line.lower() for keyword in ['occupation', 'position', 'designation']):
                if 'position' in line.lower():
                    position = random.choice(occupations['positions'])
                    designation = random.choice(occupations['designations'])
                    filled_lines.append(line + ": " + f"{designation} {position}")
                else:
                    filled_lines.append(line + ": " + random.choice(occupations['professional'] + occupations['traditional']))
            
            # Handle course/department
            elif any(keyword in line.lower() for keyword in ['course', 'program', 'degree', 'department']):
                filled_lines.append(line + ": " + department)
            
            # Handle class
            elif any(keyword in line.lower() for keyword in ['class', 'year', 'semester']):
                filled_lines.append(line + ": " + class_level)
            
            # Handle subject
            elif 'subject' in line.lower():
                filled_lines.append(line + ": " + subject)
            
            # Handle medium
            elif 'medium' in line.lower():
                filled_lines.append(line + ": " + random.choice(education_medium['languages']))
            
            # Handle roll number/enrollment number
            elif any(keyword in line.lower() for keyword in ['roll number', 'roll no', 'roll']):
                filled_lines.append(line + ": " + roll_number)
            elif any(keyword in line.lower() for keyword in ['enrollment number', 'enrollment no', 'enrollment']):
                filled_lines.append(line + ": " + enrollment_number)
            
            # Handle reasons for leaving
            elif any(keyword in line.lower() for keyword in ['reason for leaving', 'reason of leaving', 'leaving reason']):
                category = random.choice(list(reasons_for_leaving.keys()))
                filled_lines.append(line + ": " + random.choice(reasons_for_leaving[category]))
            
            # Handle address fields
            elif any(keyword in line.lower() for keyword in ['address', 'city', 'state', 'post office', 'police station', 'po', 'ps']):
                try:
                    if 'po/ps' in line.lower() or 'ps/po' in line.lower():
                        # Get PO and PS from the selected city
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        ps = random.choice(indian_locations[state]['police_stations'][city]).replace(' PS', '')
                        filled_lines.append(line + ": " + f"{po}/{ps}")
                    elif any(keyword in line.lower() for keyword in ['post office', 'po']):
                        # Get PO from the selected city
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        filled_lines.append(line + ": " + po)
                    elif any(keyword in line.lower() for keyword in ['police station', 'ps']):
                        # Get PS from the selected city
                        ps = random.choice(indian_locations[state]['police_stations'][city]).replace(' PS', '')
                        filled_lines.append(line + ": " + ps)
                    elif 'city' in line.lower():
                        # Use the selected city
                        filled_lines.append(line + ": " + city)
                    elif 'state' in line.lower():
                        # Use the selected state
                        filled_lines.append(line + ": " + state)
                    elif any(keyword in line.lower() for keyword in ['correspondence', 'address']):
                        # For correspondence address, use a complete address format with pincode
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        pincode = random.choice(pincodes[state][city])
                        filled_lines.append(line + ": " + f"{po}, {city}, {state} - {pincode}")
                    else:
                        # For general address field, use a complete address format with pincode
                        po = random.choice(indian_locations[state]['post_offices'][city]).replace(' PO', '')
                        pincode = random.choice(pincodes[state][city])
                        filled_lines.append(line + ": " + f"{po}, {city}, {state} - {pincode}")
                except KeyError as e:
                    print(f"Warning: Could not find location data for {state} or {city}. Using default values.")
                    filled_lines.append(line + ": " + "Kolkata, West Bengal - 700001")  # Default fallback
            
            # Handle phone number
            elif any(keyword in line.lower() for keyword in ['phone', 'mobile', 'contact']):
                filled_lines.append(line + ": " + generate_indian_phone_number())
            
            # Handle nationality
            elif 'nationality' in line.lower():
                filled_lines.append(line + ": " + 'Indian')
            
            else:
                # Keep original line if no matching field is found
                filled_lines.append(line)
        
        # Write filled lines to output file
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(filled_lines))
        
        print(f"Successfully filled and saved text file: {output_text_path}")
        return True
    except Exception as e:
        print(f"Error filling text file: {str(e)}")
        return False

def process_image_to_text(image_path, output_pdf_path, output_text_path, filled_text_path):
    """
    Process image to PDF, then to text, and finally fill the text
    """
    # First convert image to PDF
    if convert_image_to_pdf(image_path, output_pdf_path):
        # Then convert PDF to text
        if convert_pdf_to_text(output_pdf_path, output_text_path):
            # Finally fill the text with values
            fill_text_with_values(output_text_path, filled_text_path)
    else:
        print("Failed to convert image to PDF. Stopping process.")

# Add Pincode Dictionary
pincodes = {
    'West Bengal': {
        'Kolkata': ['700001', '700002', '700003', '700004', '700005', '700006', '700007', '700008', '700009', '700010'],
        'Howrah': ['711101', '711102', '711103', '711104', '711105', '711106', '711107', '711108', '711109'],
        'Siliguri': ['734001', '734002', '734003', '734004', '734005', '734006', '734007', '734008'],
        'Durgapur': ['713201', '713202', '713203', '713204', '713205', '713206'],
        'Asansol': ['713301', '713302', '713303', '713304', '713305', '713306', '713307']
    },
    'Maharashtra': {
        'Mumbai': ['400001', '400002', '400003', '400004', '400005', '400006', '400007', '400008', '400009', '400010'],
        'Pune': ['411001', '411002', '411003', '411004', '411005', '411006', '411007', '411008'],
        'Nagpur': ['440001', '440002', '440003', '440004', '440005', '440006', '440007', '440008', '440009'],
        'Thane': ['400601', '400602', '400603', '400604', '400605', '400606', '400607'],
        'Nashik': ['422001', '422002', '422003', '422004', '422005', '422006', '422007']
    },
    'Gujarat': {
        'Ahmedabad': ['380001', '380002', '380003', '380004', '380005', '380006', '380007', '380008'],
        'Surat': ['395001', '395002', '395003', '395004', '395005', '395006', '395007'],
        'Vadodara': ['390001', '390002', '390003', '390004', '390005', '390006', '390007'],
        'Rajkot': ['360001', '360002', '360003', '360004', '360005', '360006'],
        'Gandhinagar': ['382001', '382002', '382003', '382004', '382005']
    }
}

if __name__ == "__main__":
    # Example usage

    image_path = "form_template_info/template_3/template_3.png"  # Replace with your image path
    output_pdf_path = "form_template_info/template_3/template_3.pdf"
    output_text_path = "form_template_info/template_3/template_3.txt"
    filled_text_path = "form_template_info/template_3/template_3_filled.txt"

    # image_path = "form_template_info/english_test/english_test.png"  # Replace with your image path
    # output_pdf_path = "form_template_info/english_test/english_test.pdf"
    # output_text_path = "form_template_info/english_test/english_test.txt"
    # filled_text_path = "form_template_info/english_test/english_test_filled.txt"
    # Process the image to PDF, then to text, and finally fill it
    process_image_to_text(image_path, output_pdf_path, output_text_path, filled_text_path)
    
    # Print success message
    print(f"\nForm has been filled and saved to: {filled_text_path}")
