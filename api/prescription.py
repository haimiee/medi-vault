from db.models import Prescription, Patient
from api.drug import get_drug_by_name
from api.patient import validate_email
from datetime import date

async def add_prescription(patient_email: str, drug_name: str, dosage: str, refill_date: date):
    patient = await Patient.get_or_none(email=patient_email)
    drug = await get_drug_by_name(drug_name)

    if not patient:
        raise ValueError(f"No patient found with the email '{patient_email}'.")

    if not drug:
        raise ValueError(f"Drug {drug_name} does not exist in the database.")

    existing_prescription = await Prescription.get_or_none(
        patient=patient, drug=drug, dosage=dosage, refill_date=refill_date
    )

    if existing_prescription:
        raise ValueError("That prescription for already exists.")

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
async def update_prescription(
    prescription_id: int, 
    patient_email: str = None, 
    drug: str = None, 
    dosage: str = None, 
    refill_date: date = None
):
    # Fetch existing prescription
    prescription = await get_prescription_id(prescription_id)
    if not prescription:
        raise ValueError("Prescription not found.")

    # Updating if valid 
    if patient_email:
        if not validate_email(patient_email):
            raise ValueError("Invalid email format. Example: example@mail.com")
        
        patient = await Patient.get(email=patient_email)
    
        if not patient:
            raise ValueError(f"No patient found with email {patient_email}.")
        prescription.patient = patient 

    if drug:
        drug_obj = await get_drug_by_name(drug)
        
        if not drug_obj:
            raise ValueError(f"Drug '{drug}' does not exist in the database.")
        prescription.drug = drug_obj

    if dosage:
        prescription.dosage = dosage

    if refill_date:
        if refill_date < date.today():
            raise ValueError("Updated refill date cannot be in the past.")

        prescription.refill_date = refill_date

    await prescription.save()
    return prescription

async def delete_prescription(prescription_id: int):
    prescription = await get_prescription_id(prescription_id)
    
    if not prescription:
        raise ValueError(f"No prescription found with ID '{prescription_id}'.")
    
    await prescription.delete()

    return prescription


