from db.models import Prescription, Patient
from api.drug import get_drug_by_name
from datetime import date

async def add_prescription(patient_email: str, drug_name: str, dosage: str, refill_date: date):
    patient = await Patient.filter(email=patient_email)

    if not patient:
        raise ValueError(f"No patient found with the email '{patient_email}'.")

    drug = await get_drug_by_name(drug_name)

    if not drug:
        raise ValueError(f"Drug {drug_name} does not exist in the database.")

    prescription = Prescription.create(
        patient=patient, drug=drug, dosage=dosage, refill_date=refill_date
    )
    
    return prescription

    

