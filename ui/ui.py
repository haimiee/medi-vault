from nicegui import ui
import asyncio
from datetime import date, datetime

from db.models import Patient, Drug
from api.patient import add_patient, get_all_patients, get_patient_by_id, update_patient, delete_patient
from api.drug import add_drug, get_all_drugs, get_drug_by_id, update_drug, delete_drug
from api.prescription import add_prescription, get_all_prescriptions, get_prescription_id, update_prescription, delete_prescription

# UI dialog to input new patient info
async def add_patient_popup():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Add New Patient").classes('ext-lg font-bold text-center w-full')
            
            # Input fields for patient data
            first_name = ui.input("First name").classes('w-full')
            last_name = ui.input("Last name").classes('w-full')
            ui.label("Date of birth").classes('text-gray-300 text-base')
            dob = ui.date().classes('w-1/2 text-sm')
            email = ui.input("Email").classes('w-full')
            
            with ui.row():
                ui.button("Save", on_click=lambda: save_patient_info(
                    dialog, first_name.value, last_name.value, dob.value, email.value
                    )
                )
                ui.button("Cancel", on_click=dialog.close)

    dialog.open()

# Save new patient info from popup function to db
async def save_patient_info(dialog, first_name, last_name, dob, email):
    if not first_name or not last_name or not dob or not email:
        ui.notify("Please enter all fields", type='negative')
        return

    try:
        patient = await add_patient(first_name, last_name, dob, email)  

        ui.notify(f"Patient '{first_name} {last_name}' added successfully", type='positive')

        view_patients_table.refresh() # Refresh patients table
        dialog.close() # Close dialog UI after successfully saving

    except Exception as e:
        ui.notify(str(e), type='negative')

# Function to delete patients in the database
async def handle_delete_patients(selected_ids):
    for patient in selected_ids:
        try:
            await delete_patient(patient)
            view_patients_table.refresh()
        except Exception as e:
            ui.notify(e, type='negative')

# Function for refreshable patients table/grid
@ui.refreshable
async def view_patients_table():    
    patients = await get_all_patients()

    # Column Setup
    columns = [
        {'field': 'ID', 'sortable': True},
        {'field': 'First Name', 'editable': True},
        {'field': 'Last Name', 'editable': True},
        {'field': 'Date of Birth', 'editable': True},
        {'field': 'Email', 'editable': True}
    ]

    # Row Setup
    rows = []

    for patient in patients:
        rows.append(
            {'ID': patient.id, 'First Name': patient.first_name, 'Last Name': patient.last_name, 'Date of Birth': patient.date_of_birth, 'Email': patient.email}
        )
    
    async def handle_cell_value_change(e):
        new_row = e.args['data']
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        new_date = datetime.strptime(new_row['Date of Birth'], '%Y-%m-%d').date()
        try:
            await update_patient(new_row['ID'], new_row['First Name'], new_row['Last Name'], new_date, new_row['Email'])
            ui.notify(f"Updated row to: {e.args['data']}")
        except Exception as e:
            ui.notify(f"{e}", type='negative')

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add='ag-theme-balham-dark') # Dark theme for grid

    # Function to delete selected UI row(s) (inspired by NiceGUI)
    async def delete_selected():
        selected_rows = await aggrid.get_selected_rows()  # Get selected rows

        if not selected_rows:
            ui.notify("No patient selected!", type="negative")
            return

        selected_ids = [row["ID"] for row in selected_rows]  # Extract selected IDs
        new_rows = [row for row in aggrid.options['rowData'] if row["ID"] not in selected_ids]

        aggrid.options['rowData'] = new_rows  # Update grid data
        await handle_delete_patients(selected_ids)
        ui.notify(f"Deleted patient(s) with ID(s): {selected_ids}", type="positive")

    ui.button('Delete selected', on_click=delete_selected)

# UI dialog to input new drug info
async def add_drug_popup():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Add New Drug").classes('ext-lg font-bold text-center w-full')
            
            # Input fields for patient data
            drug_name = ui.input("Drug name").classes('w-full')
            
            with ui.row():
                ui.button("Save", on_click=lambda: save_drug_info(dialog, drug_name.value))
                ui.button("Cancel", on_click=dialog.close)

    dialog.open()

# Save new drug name from popup function to db
async def save_drug_info(dialog, drug_name):
    if not drug_name:
        ui.notify("Please enter the drug name", type='negative')
        return

    try:
        patient = await add_drug(drug_name)  

        ui.notify(f"Drug '{drug_name}' added successfully", type='positive')

        view_drugs_table.refresh() # Refresh drugs table
        dialog.close() # Close dialog UI after successfully saving

    except Exception as e:
        ui.notify(str(e), type='negative')

# Function to delete drugs in the database
async def handle_delete_drugs(selected_ids):
    for drug in selected_ids:
        try:
            await delete_drug(drug)
            view_drugs_table.refresh()
        except Exception as e:
            ui.notify(e, type='negative')

# Function for refreshable drugs table/grid
@ui.refreshable
async def view_drugs_table():    
    drugs = await get_all_drugs()

    # Column Setup
    columns = [
        {'field': 'ID', 'sortable': True},
        {'field': 'Drug Name', 'editable': True, 'sortable': True},
    ]

    # Row Setup
    rows = []

    for drug in drugs:
        rows.append(
            {'ID': drug.id, 'Drug Name': drug.drug_name}
        )

    # Function to handle changes in cells in the grid (inspired by NiceGUI)
    async def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f"Updated row to: {e.args['data']}")
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        await update_drug(new_row['ID'], new_row['Drug Name'])

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add='ag-theme-balham-dark') # Dark theme for grid

    # Function to delete selected UI row(s) (inspired by NiceGUI)
    async def delete_selected():
        selected_rows = await aggrid.get_selected_rows()  # Get selected rows

        if not selected_rows:
            ui.notify("No drug selected!", type="negative")
            return

        selected_ids = [row["ID"] for row in selected_rows]  # Extract selected IDs
        new_rows = [row for row in aggrid.options['rowData'] if row["ID"] not in selected_ids]

        aggrid.options['rowData'] = new_rows  # Update grid data
        await handle_delete_drugs(selected_ids)
        ui.notify(f"Deleted drug(s) with ID(s): {selected_ids}", type="positive")

    ui.button('Delete selected', on_click=delete_selected)

# UI dialog to input new drug info
async def add_prescription_popup():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Add New Prescription").classes('ext-lg font-bold text-center w-full')
            
            # Input fields for prescription data
            patient_email = ui.input("Patient email").classes('w-full')
            drug_name = ui.input("Drug name").classes('w-full')
            dosage = ui.input("Dosage").classes('w-full')
            ui.label("Refill date").classes('text-gray-300 text-base')
            refill_date = ui.date().classes('w-1/2 text-sm')
            
            with ui.row():
                ui.button("Save", on_click=lambda: save_prescription_info(
                    dialog, patient_email.value, drug_name.value, dosage.value, refill_date.value
                    )
                )
                ui.button("Cancel", on_click=dialog.close)

    dialog.open()

# Save new prescription name from popup function to db
async def save_prescription_info(dialog, patient_email, drug_name, dosage, refill_date):
    if not patient_email or not drug_name or not dosage or not refill_date:
        ui.notify("Please enter all fields", type='negative')
        return

    try:
        prescription = await add_prescription(patient_email, drug_name, dosage, refill_date)  

        ui.notify(f"Prescription for '{patient_email}' added successfully", type='positive')

        view_prescriptions_table.refresh() # Refresh prescriptions table
        dialog.close() # Close dialog UI after successfully saving

    except Exception as e:
        ui.notify(str(e), type='negative')

# Function to delete prescriptions in the database
async def handle_delete_prescriptions(selected_ids):
    for p in selected_ids:
        try:
            await delete_prescription(p)
            view_prescriptions_table.refresh()
        except Exception as e:
            ui.notify(e, type='negative')

# Function for refreshable prescriptions table/grid
@ui.refreshable
async def view_prescriptions_table():    
    prescriptions = await get_all_prescriptions()

    # Column Setup
    columns = [
        {'field': 'ID', 'sortable': True},
        {'field': 'Patient Email', 'sortable': True},
        {'field': 'Drug', 'sortable': True},
        {'field': 'Dosage', 'editable': True},
        {'field': 'Refill Date', 'editable': True, 'sortable': True},

    ]

    # Row Setup
    rows = []

    for prescription in prescriptions:
        patient = await Patient.get_or_none(id=prescription.patient_id)  # Fetch patient directly

        drug = await Drug.get_or_none(id=prescription.drug_id)  # Fetch drug directly

        rows.append(
            {
                'ID': prescription.id, 
                'Patient Email': patient.email if patient else "Unknown",  # Extract email safely
                'Drug': drug.drug_name if drug else "Unknown",  # Extract drug name safely
                'Dosage': prescription.dosage, 
                'Refill Date': prescription.refill_date
            }
        )

    # Function to handle changes in cells in the grid (inspired by NiceGUI)
    async def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f"Updated row to: {e.args['data']}")
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        new_date = datetime.strptime(new_row['Refill Date'], '%Y-%m-%d').date()
        await update_prescription(new_row['ID'], new_row['Patient'], new_row['Drug'], new_row['Dosage'], new_date)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add='ag-theme-balham-dark') # Dark theme for grid

    # Function to delete selected UI row(s) (inspired by NiceGUI)
    async def delete_selected():
        selected_rows = await aggrid.get_selected_rows()  # Get selected rows

        if not selected_rows:
            ui.notify("No prescription selected!", type="negative")
            return

        selected_ids = [row["ID"] for row in selected_rows]  # Extract selected IDs
        new_rows = [row for row in aggrid.options['rowData'] if row["ID"] not in selected_ids]

        aggrid.options['rowData'] = new_rows  # Update grid data
        await handle_delete_prescriptions(selected_ids)
        ui.notify(f"Deleted prescription(s) with ID(s): {selected_ids}", type="positive")

    ui.button('Delete selected', on_click=delete_selected)

def run_ui():

    # Main Page Setup
    @ui.page("/")
    async def main_page():
        ui.label("MediVault").classes('text-4xl font-bold text-center w-full mt-10')

        # Tabs UI
        with ui.tabs().classes('w-full') as tabs:
            patients_tab = ui.tab('Patients')
            drugs_tab = ui.tab('Drugs')
            prescriptions_tab = ui.tab('Prescriptions')
        
        # Tab Panels
        with ui.tab_panels(tabs, value=patients_tab).classes('w-full'):
            
            # Patients Tab
            with ui.tab_panel(patients_tab):
                
                with ui.row().classes('items-center justify-between w-full mt-2'): # Single row of button to allow justify

                    ui.button("+", on_click=add_patient_popup).classes('ml-auto') # Justify + button to the right
                
                await view_patients_table()

            # Drugs Tab
            with ui.tab_panel(drugs_tab):

                with ui.row().classes('items-center justify-between w-full mt-2'):
                    ui.button("+", on_click=add_drug_popup).classes('ml-auto')
                
                await view_drugs_table()
            
            # Prescriptions Tab
            with ui.tab_panel(prescriptions_tab):
                
                with ui.row().classes('items-center justify-between w-full mt-2'):
                    ui.button("+", on_click=add_prescription_popup).classes('ml-auto')
                
                await view_prescriptions_table()

ui.run(dark=True)
