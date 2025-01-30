import datetime
from db.models import Patient

async def lookup_patient(last_name, dob_input):
    patient = await Patient.filter(last_name=last_name).all()
    return patient

async def add_patient(first_name, last_name, date_of_birth):
