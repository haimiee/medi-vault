from db.models import Patient
from datetime import date
import re

# Function to validate email format using regex
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

""" CRUD Functions for patients """

# Create a new patient
async def add_patient(first_name: str, last_name: str, dob: date, email: str):
    # Check if valid email format
    if not validate_email(email):
        raise ValueError(f"Invalid email format. Example: example@mail.com")

    # Checking for existing email
    existing_email = await Patient.filter(email=email).first()
    
    if existing_email:
        raise ValueError(f"{email} email is in use.")

    patient = await Patient.create(
        first_name=first_name, last_name=last_name, date_of_birth=dob, email=email
    )
    return patient  # Successfully created

# Get all patients
async def get_all_patients():
    return await Patient.all()

# Get a single patient by ID
async def get_patient_by_id(patient_id: int):
    patient = await Patient.filter(id=patient_id).first()
    
    if not patient:
        raise ValueError("No patient found with this ID.")

    return patient

# Update a patient's information
async def update_patient(patient_id: int, first_name: str=None, last_name: str=None, dob: date=None, email: str=None):
    patient = await get_patient_by_id(patient_id)

    if email:
        if not validate_email(email):
            raise ValueError(f"Invalid email format. Example: example@mail.com")
        else:
            patient.email = email
    if first_name:
        patient.first_name = first_name
    if last_name:
        patient.last_name = last_name
    if dob:
        patient.date_of_birth = dob

    await patient.save()
    return patient  # Successfully updated

# Delete a patient
async def delete_patient(patient_id: int):
    patient = await Patient.get_or_none(patient_id=patient_id)
    
    if not patient:
        raise ValueError(f"No patient found with ID '{patient_id}'.")
    
    return patient