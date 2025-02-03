from db.models import Patient
from datetime import date

# CRUD Functions for patients

# Create a new patient
async def add_patient(first_name: str, last_name: str, dob: date, email: str):
    # Checking for existing patient
    existing_patient = await Patient.filter(
        first_name=first_name, last_name=last_name, date_of_birth=dob, email=email
    ).first()

    if existing_patient:
        raise ValueError("A patient with this information already exists. Try again.")

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
    """Updates a patient's information if they exist."""
    patient = await get_patient_by_id(patient_id)

    if first_name:
        patient.first_name = first_name
    if last_name:
        patient.last_name = last_name
    if dob:
        patient.date_of_birth = dob
    if email:
        patient.email = email

    await patient.save()
    return patient  # Successfully updated

# Delete a patient
async def delete_patient(patient_id: int):
    patient = await get_patient_by_id(patient_id)
    await patient.delete()
    return f"Patient {patient.first_name} {patient.last_name} deleted successfully."


    
