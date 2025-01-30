from db.models import Drug

async def add_drug(drug_name: str):
    drug_name = drug_name.strip()  # Remove extra spaces

    if not drug_name:
        return None, "Drug name cannot be empty."

    # Check if drug already exists
    drug, created = await Drug.get_or_create(drug_name=drug_name)

    return drug, created  # Returns the drug object and whether it was newly created

async def get_all_drugs():
    drugs = await Drug.all()
    return drugs  # Returns a list of all drugs in the database