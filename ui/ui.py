from nicegui import ui
import asyncio
from datetime import date, datetime

from db.lib import init_db
from api.drug import add_drug, get_all_drugs, get_drug_by_id, update_drug, delete_drug
from api.patient import add_patient, get_all_patients, get_patient_by_id, update_patient, delete_patient
from api.prescription import add_prescription, get_all_prescriptions, get_prescription_id, update_refill_date, delete_prescription

def run_ui():

    # Main Page Setup
    @ui.page("/")
    async def main_page():
        ui.label("Hi! Welcome to Medivault")

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
                ui.button("Add Test Patients", on_click=add_test_patients)

            # Drugs Tab
            with ui.tab_panel(drugs_tab):
                ui.label('Second tab')
            
            # Prescriptions Tab
            with ui.tab_panel(prescriptions_tab):
                ui.label('Third tab')


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
            {'ID': patient.id, 'First Name': patient.first_name, 'Last Name': patient.last_name, 'Date of Birth': str(patient.date_of_birth), 'Email': patient.email}
        )

    # Function to handle changes in cells in the grid (inspired by NiceGUI)
    async def handle_cell_value_change(e):
        new_row = e.args['data']
        ui.notify(f'Updated row to: {e.args["data"]}')
        rows[:] = [row | new_row if row['ID'] == new_row['ID'] else row for row in rows]

        new_date = datetime.strptime(new_row['Date of Birth'], '%Y-%m-%d').date()
        await update_patient(new_row['ID'], new_row['First Name'], new_row['Last Name'], new_date, new_row['Email'])

        print(type(new_row['Date of Birth']))

    aggrid = ui.aggrid({
        'columnDefs': columns,
        'rowData': rows,
        'rowSelection': 'multiple',
        'stopEditingWhenCellsLoseFocus': True,
    }).on('cellValueChanged', handle_cell_value_change)

    aggrid.classes(add="ag-theme-balham-dark") # Dark theme for grid

# Adding patients test
async def add_test_patients():
    try: 
        patient1 = await add_patient("Haimie", "Nguyen", date(2001, 9, 15), "hn@mail.com")
        patient2 = await add_patient("Tyler", "Mcfam", date(2001, 9, 11), "tler@mail.com")
        ui.notify("Test patients added successfully!")
        view_patients_table.refresh() # Refresh table after adding
    except ValueError as ve:
        ui.notify(f"Error: {ve}", color="red")
    except Exception as e:
        ui.notify(f"Unexpected Error: {e}", color="red")

ui.run(dark=True)
