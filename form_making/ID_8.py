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

GENDERS = ["Male", "Female", "Other"]
MARITAL_STATUSES = ["Single", "Married", "Divorced", "Widowed", "Separated"]
OCCUPATIONS = [
    "Software Engineer", "Teacher", "Accountant", "Business Owner", "Student", "Homemaker", "Retired", "Doctor", "Nurse", "Sales Executive", "Artist", "Journalist", "Civil Servant", "Lawyer", "Engineer", "Banker", "Shopkeeper", "Driver", "Farmer", "Police Officer"
]
SEVERITIES = ["Mild", "Moderate", "Severe"]
DURATIONS = ["2 weeks", "1 month", "3 months", "6 months", "1 year", "2 years", "5 years", "Since childhood"]

PRESENTING_ISSUES = [
    "Low mood, lack of interest, and fatigue",
    "Persistent anxiety and restlessness",
    "Difficulty sleeping and irritability",
    "Hearing voices and suspiciousness",
    "Repetitive thoughts and compulsive behaviors",
    "Excessive worry about health",
    "Social withdrawal and poor self-care",
    "Memory loss and confusion",
    "Mood swings and impulsivity",
    "Difficulty concentrating at work"
]

PAST_PSYCH_HISTORY = [
    "No prior psychiatric illness",
    "History of depression treated with medication",
    "Previous episode of anxiety disorder",
    "Hospitalized for psychosis 2 years ago",
    "History of substance use disorder, now abstinent"
]

MEDICAL_CONDITIONS = [
    "No significant medical history",
    "Diabetes mellitus",
    "Hypertension",
    "Hypothyroidism",
    "Asthma",
    "Migraine",
    "Epilepsy",
    "Coronary artery disease"
]

SUBSTANCE_USES = [
    "No substance use",
    "Occasional alcohol use",
    "Tobacco chewing for 5 years",
    "Smokes 5 cigarettes/day",
    "History of cannabis use, now abstinent"
]

FAMILY_HISTORY = [
    "No family history of psychiatric illness",
    "Father had depression",
    "Mother has anxiety disorder",
    "Sibling with schizophrenia",
    "Uncle with alcohol dependence"
]

FAMILY_SUBSTANCE = [
    "No substance use in family",
    "Father smokes tobacco",
    "Brother drinks alcohol occasionally",
    "Mother chews betel nut"
]

LIVING_SITUATIONS = [
    "Lives with spouse and children",
    "Lives alone",
    "Lives with parents",
    "Lives in joint family",
    "Lives in hostel"
]

EDUCATIONS = [
    "Graduate",
    "Postgraduate",
    "12th Pass",
    "10th Pass",
    "Diploma",
    "PhD",
    "Illiterate"
]

SOCIAL_SUPPORTS = [
    "Good support from family and friends",
    "Limited social support",
    "Active in community groups",
    "Isolated, no close friends"
]

LEGAL_ISSUES = [
    "No legal issues",
    "Pending divorce case",
    "Involved in property dispute",
    "History of minor traffic violations"
]

EMPLOYMENT_STATUSES = [
    "Employed full-time",
    "Unemployed",
    "Part-time job",
    "Retired",
    "Student",
    "Homemaker"
]

RELATIONSHIPS = [
    "Supportive relationship with spouse",
    "Frequent arguments with family",
    "Estranged from parents",
    "Good relationship with children",
    "Single, no current relationship"
]

DAILY_ACTIVITIES = [
    "Able to manage daily activities independently",
    "Needs assistance for daily tasks",
    "Neglects self-care",
    "Active in sports and hobbies"
]

CURRENT_MEDICATIONS = [
    "None",
    "Escitalopram 10mg daily",
    "Olanzapine 5mg at night",
    "Sertraline 50mg daily",
    "Risperidone 2mg daily",
    "Lithium 300mg twice daily",
    "Clonazepam 0.5mg as needed"
]

PREVIOUS_TREATMENTS = [
    "No previous treatment",
    "Cognitive Behavioral Therapy for 6 months",
    "Electroconvulsive therapy (ECT) in 2020",
    "Hospital admission for 2 weeks",
    "Ayurvedic treatment tried previously"
]

PRIMARY_DIAGNOSES = [
    "Major Depressive Disorder",
    "Generalized Anxiety Disorder",
    "Schizophrenia",
    "Bipolar Affective Disorder",
    "Obsessive Compulsive Disorder",
    "Alcohol Dependence Syndrome",
    "Panic Disorder"
]

SECONDARY_DIAGNOSES = [
    "None",
    "Hypertension",
    "Diabetes Mellitus",
    "Social Phobia",
    "Personality Disorder"
]

TREATMENT_GOALS = [
    "Achieve symptom remission",
    "Improve social and occupational functioning",
    "Prevent relapse",
    "Enhance medication adherence",
    "Reduce substance use"
]

PROPOSED_INTERVENTIONS = [
    "Pharmacotherapy",
    "Cognitive Behavioral Therapy",
    "Family counseling",
    "Psychoeducation",
    "Motivational enhancement therapy",
    "Group therapy"
]

def extract_keys(form_text):
    field_pattern = re.compile(r"^([A-Za-z0-9&/()' .\-]+):", re.MULTILINE)
    keys = []
    for line in form_text.splitlines():
        match = field_pattern.match(line.strip())
        if match:
            key = match.group(1).strip()
            keys.append(key)
    return keys

def fill_form(keys):
    person = random.choice(person_profiles)
    full_name = person.get("Full Name", "")
    gender = person.get("Gender", random.choice(GENDERS))
    age = str(random.randint(18, 70))
    occupation = random.choice(OCCUPATIONS)
    marital_status = random.choice(MARITAL_STATUSES)
    education = random.choice(EDUCATIONS)
    form_data = {}
    for key in keys:
        key_lower = key.replace(" ","").replace("_","").replace("/","").replace(",","").lower()
        if key_lower == "name":
            form_data[key] = full_name
        elif key_lower == "age":
            form_data[key] = age
        elif key_lower == "gender":
            form_data[key] = gender
        elif key_lower == "occupation":
            form_data[key] = occupation
        elif key_lower == "maritalstatus":
            form_data[key] = marital_status
        elif key_lower == "presentingissue":
            form_data[key] = random.choice(PRESENTING_ISSUES)
        elif key_lower == "durationofsymptoms":
            form_data[key] = random.choice(DURATIONS)
        elif key_lower == "severity":
            form_data[key] = random.choice(SEVERITIES)
        elif key_lower == "pastpsychiatrichistory":
            form_data[key] = random.choice(PAST_PSYCH_HISTORY)
        elif key_lower == "medicalconditions":
            form_data[key] = random.choice(MEDICAL_CONDITIONS)
        elif key_lower == "substanceuse":
            form_data[key] = random.choice(SUBSTANCE_USES)
        elif key_lower == "familyhistory":
            form_data[key] = random.choice(FAMILY_HISTORY)
        elif key_lower == "substanceuseinfamily":
            form_data[key] = random.choice(FAMILY_SUBSTANCE)
        elif key_lower == "livingsituation":
            form_data[key] = random.choice(LIVING_SITUATIONS)
        elif key_lower == "education":
            form_data[key] = education
        elif key_lower == "socialsupport":
            form_data[key] = random.choice(SOCIAL_SUPPORTS)
        elif key_lower == "legalissues":
            form_data[key] = random.choice(LEGAL_ISSUES)
        elif key_lower == "employmentstatus":
            form_data[key] = random.choice(EMPLOYMENT_STATUSES)
        elif key_lower == "relationships":
            form_data[key] = random.choice(RELATIONSHIPS)
        elif key_lower == "dailyactivities":
            form_data[key] = random.choice(DAILY_ACTIVITIES)
        elif key_lower == "currentmedications":
            form_data[key] = random.choice(CURRENT_MEDICATIONS)
        elif key_lower == "previoustreatments":
            form_data[key] = random.choice(PREVIOUS_TREATMENTS)
        elif key_lower == "primarydiagnosis":
            form_data[key] = random.choice(PRIMARY_DIAGNOSES)
        elif key_lower == "secondarydiagnosis":
            form_data[key] = random.choice(SECONDARY_DIAGNOSES)
        elif key_lower == "treatmentgoals":
            form_data[key] = random.choice(TREATMENT_GOALS)
        elif key_lower == "proposedinterventions":
            form_data[key] = random.choice(PROPOSED_INTERVENTIONS)
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
    FORM_PATH = os.path.join(FORMS_DIR, 'ID_8.txt')
    OUTPUT_PATH = os.path.join(FORMS_FILL_DIR, 'ID_8_filled.txt')
    with open(FORM_PATH, 'r') as f:
        form_text = f.read()
    keys = extract_keys(form_text)
    form_data = fill_form(keys)
    filled_text = fill_form_text(form_text, form_data)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(filled_text)
    print(f"Filled form saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
