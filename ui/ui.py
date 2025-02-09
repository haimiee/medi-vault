from nicegui import ui
import asyncio
from datetime import date, datetime

from db.lib import init_db
from db.models import Patient, Drug
from api.drug import add_drug, get_all_drugs, get_drug_by_id, update_drug, delete_drug
from api.patient import add_patient, get_all_patients, get_patient_by_id, update_patient, delete_patient
from api.prescription import add_prescription, get_all_prescriptions, get_prescription_id, update_prescription, delete_prescription

def run_ui():

    # Main Page Setup
    @ui.page("/")
    async def main_page():
        ui.label("MediVault").classes("text-4xl font-bold text-center w-full mt-10")

        # Tabs UI
        with ui.tabs().classes('w-full') as tabs:
            patients_tab = ui.tab('Patients')
            drugs_tab = ui.tab('Drugs')
            prescriptions_tab = ui.tab('Prescriptions')
        
        # Tab Panels
        with ui.tab_panels(tabs, value=patients_tab).classes('w-full'):
            
            # Patients Tab
            with ui.tab_panel(patients_tab):
                await view_patients_table()
                ui.button("Add Patient", on_click=add_patient_popup)

            # Drugs Tab
            with ui.tab_panel(drugs_tab):
                await view_drugs_table()
                ui.button("Add Test Drugs", on_click=add_test_drugs)
            
            # Prescriptions Tab
            with ui.tab_panel(prescriptions_tab):
                await view_prescriptions_table()
                ui.button("Add Test Prescriptions", on_click=add_test_prescriptions)

# UI dialog to input new patient info
async def add_patient_popup():
    with ui.dialog() as dialog:
        with ui.card():
            ui.label("Add New Patient").classes("text-lg font-bold text-center w-full")
            
            # Input fields for patient data
            first_name = ui.input("First name").classes("w-full")
            last_name = ui.input("Last name").classes("w-full")
            ui.label("Date of birth").classes("text-gray-300 text-base")
            dob = ui.date().classes("w-1/2 text-sm")
            email = ui.input("Email").classes("w-full")
            
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
        ui.notify("All fields are required!", type="negative")
        return

    try:
        patient = await add_patient(first_name, last_name, dob, email)  

        ui.notify(f"Patient '{first_name} {last_name}' added successfully", type="positive")

        view_patients_table.refresh() # Refresh patients table
        dialog.close() # Close dialog UI after successfully saving
        
    except Exception as e:
        ui.notify(str(e), type="negative")


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

    # Function to handle changes in cells in the grid (inspired by NiceGUI)
    pending_changes = {} # Stores changes that haven't been saved yet
    
    async def handle_cell_value_change(e):
        new_row = e.args['data']
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        # pending_changes[new_row['ID']] = new_row
        # ui.notify(f"Editing Patient with ID '{new_row['ID']}' (Not saved yet)")

        new_date = datetime.strptime(new_row['Date of Birth'], '%Y-%m-%d').date()
        try:
            await update_patient(new_row['ID'], new_row['First Name'], new_row['Last Name'], new_date, new_row['Email'])
            ui.notify(f'Updated row to: {e.args["data"]}')
        except Exception as e:
            ui.notify(f"{e}", color="red")

    # async def add_row():
    #     new_id = max((dx['id'] for dx in rows), default=-1) + 1
    #     rows.append({'ID': new_id, 'First Name': 'Patient First', 'Last Name': 'Patient Last', 'Date of Birth': date, 'Email': 'Email'})
    #     ui.notify(f'Added row with ID {new_id}')
    #     aggrid.update()

    # async def delete_selected():
    #     selected_id = [row['id'] for row in await aggrid.get_selected_rows()]
    #     rows[:] = [row for row in rows if row['id'] not in selected_id]
    #     ui.notify(f'Deleted row with ID {selected_id}')
    #     aggrid.update()

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add="ag-theme-balham-dark") # Dark theme for grid

    # ui.button('Delete selected', on_click=delete_selected)
    # ui.button('New row', on_click=add_row)

# Adding patients test
# async def add_test_patients():
#     try: 
#         patient1 = await add_patient("Haimie", "Nguyen", date(2001, 9, 15), "hn@mail.com")
#         patient2 = await add_patient("Tyler", "Mcfam", date(2001, 9, 11), "tler@mail.com")
#         ui.notify("Test patients added successfully!")
#         view_patients_table.refresh() # Refresh table after adding
#     except ValueError as ve:
#         ui.notify(f"Error: {ve}", color="red")
#     except Exception as e:
#         ui.notify(f"Unexpected Error: {e}", color="red")

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
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        await update_drug(new_row['ID'], new_row['Drug Name'])

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add="ag-theme-balham-dark") # Dark theme for grid

    # ui.button('Delete selected', on_click=delete_selected)
    # ui.button('New row', on_click=add_row)

# Adding drugs test
async def add_test_drugs():
    try: 
        drug1 = await add_drug("Adderall")
        ui.notify("Test drugs added successfully!")
        view_drugs_table.refresh()
    except ValueError as ve:
        ui.notify(f"Error: {ve}", color="red")
    except Exception as e:
        ui.notify(f"Unexpected Error: {e}", color="red")

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
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        new_date = datetime.strptime(new_row['Refill Date'], '%Y-%m-%d').date()
        await update_prescription(new_row['ID'], new_row['Patient'], new_row['Drug'], new_row['Dosage'], new_date)

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add="ag-theme-balham-dark") # Dark theme for grid

    # ui.button('Delete selected', on_click=delete_selected)
    # ui.button('New row', on_click=add_row)

# Adding prescriptions test
async def add_test_prescriptions():
    # try: 
    #     prescription1 = await add_prescription("hn@mail.com", "Adderall", "20mg", date(2025, 2, 5))
    #     ui.notify("Test prescription added successfully!")
    #     view_prescriptions_table.refresh()
    # except ValueError as ve:
    #     ui.notify(f"Error: {ve}", color="red")
    # except Exception as e:
    #     ui.notify(f"Unexpected Error: {e}", color="red")

    try: 
        prescription = await add_prescription("tler@mail.com", "Adderall", "20mg", date(2025, 2, 6))
        ui.notify("Test prescription added successfully!")
        view_prescriptions_table.refresh()  # ✅ Correct table refresh
    except ValueError as ve:
        ui.notify(f"Error: {ve}", color="red")
    except Exception as e:
        ui.notify(f"Unexpected Error: {e}", color="red")

    # try: 
    #     prescription3 = await add_prescription("jujujabajo@mail.com", "Adderall", "20mg", date(2025, 2, 5))
    #     ui.notify("Test prescription added successfully!")
    #     view_drugs_table.refresh()
    # except ValueError as ve:
    #     ui.notify(f"Error: {ve}", color="red")
    # except Exception as e:
    #     ui.notify(f"Unexpected Error: {e}", color="red")

ui.run(dark=True)
