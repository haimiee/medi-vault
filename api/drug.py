from db.models import Drug

# CRUD functions for drugs

# Creating a new drug
async def add_drug(drug_name: str):
    if not drug_name:
        raise ValueError("Drug name cannot be empty.")

    existing_drug = await Drug.filter(drug_name=drug_name).first()

    if existing_drug:
        raise ValueError("This drug already exists.")

    drug = await Drug.create(drug_name=drug_name)
    return drug

# Get all drugs
async def get_all_drugs():
    return await Drug.all()

# Get a single drug by ID
async def get_drug_by_id(drug_id: int):
    drug = await Drug.filter(id=drug_id).first()
    
    if not drug:
        raise ValueError("No drug found with this ID.")

    return drug

# Update a drug's name
async def update_drug(drug_id: int, new_name: str):
    """Updates a drug's name if it exists."""
    if not new_name:
        raise ValueError("Drug name cannot be empty.")

    drug = await get_drug_by_id(drug_id)
    drug.drug_name = new_name
    await drug.save()
    return drug

# Delete a drug
async def delete_drug(drug_id: int):
    drug = await get_drug_by_id(drug_id)
    await drug.delete()
    return f"Drug '{drug.drug_name}' deleted successfully."

