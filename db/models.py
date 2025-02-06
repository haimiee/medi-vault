from tortoise import fields, models

class Patient(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    date_of_birth = fields.DateField()  # Stores YYYY-MM-DD format
    email = fields.CharField(max_length=100, unique=True)  # Ensures email uniqueness

class Drug(models.Model):
    id = fields.IntField(pk=True)
    drug_name = fields.CharField(max_length=50)

class Prescription(models.Model):
    id = fields.IntField(pk=True)  # Primary Key
    patient = fields.ForeignKeyField("models.Patient")  # Link to Patient
    drug = fields.ForeignKeyField("models.Drug")  # Link to Drug
    dosage = fields.CharField(max_length=100)
    refill_date = fields.DateField(null=True)  # User inputs when is next refill