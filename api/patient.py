import datetime
from db.models import Patient

async def add_patient(first_name, last_name, date_of_birth):
    # Validate if the selected date is real (prevents invalid days like Feb 30)
    year, month, day = map(int, date_of_birth.split("-"))
    try:
        dob = datetime.date(year, month, day)  # This raises an error if the date is invalid
    except ValueError:
        return None, "Invalid birthdate. Please select a valid date."

    # Check if a patient already exists with the same name and DOB
    existing_patient = await Patient.filter(first_name=first_name, last_name=last_name, date_of_birth=dob).first()

    if existing_patient:
        return None, "A patient with this name and birthdate already exists."

    # Create a new patient
    new_patient = await Patient.create(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=dob,
    )

    return new_patient, None  # Return the new patient object and no error
    
async def lookup_patient(last_name, dob_input):
    try:
        # Convert user input (string) into a date object
        dob = datetime.datetime.strptime(dob_input, "%Y-%m-%d").date()
    except ValueError:
        return None, "Invalid date format. Use YYYY-MM-DD."

    # Search for a patient with both last name and DOB
    patient = await Patient.filter(last_name=last_name, date_of_birth=dob).first()

    if not patient:
        return None, "No matching patient found with this last name and birthdate. Try again."

    return patient, None


    
