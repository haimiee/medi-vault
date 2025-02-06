from db.models import Prescription, Patient
from api.drug import get_drug_by_name
from datetime import date

async def add_prescription(patient_email: str, drug_name: str, dosage: str, refill_date: date):
    patient = await Patient.get(email=patient_email)

    if not patient:
        raise ValueError(f"No patient found with the email '{patient_email}'.")

    drug = await get_drug_by_name(drug_name)

    if not drug:
        raise ValueError(f"Drug {drug_name} does not exist in the database.")

    prescription = await Prescription.create(
        patient=patient, drug=drug, dosage=dosage, refill_date=refill_date
    )
    
    return prescription

async def get_all_prescriptions():
    return await Prescription.all()

async def get_prescription_id(prescription_id: int):
    prescription = await Prescription.filter(id=prescription_id).first()  # ✅ Returns a single object
    if not prescription:
        raise ValueError("No prescription found with this ID.")
    return prescription

# Function to update refill date 
async def update_prescription(prescription_id: int, new_refill_date: date):
    prescription = await get_prescription_id(prescription_id)

    if new_refill_date < date.today():
        raise ValueError(f"Updated refill date cannot be in the past.")

    prescription.refill_date = new_refill_date

    await prescription.save()
    return prescription


async def delete_prescription(prescription_id: int):
    prescription = await get_prescription_id(prescription_id)
    await prescription.delete()
    return f"Prescription for '{prescription.drug.drug_name}' deleted successfully."



