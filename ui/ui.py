from typing import List, Dict
from nicegui import ui, app
import asyncio

# from api.patient import add_patient, lookup_patient
# from api.prescription import add_prescription, get_prescriptions, update_prescription, delete_prescription
# from api.drug import add_drug, get_all_drugs

# Test! 

def run_ui():
    @ui.page("/")
    def main_page():
        ui.label("Select Your Birthdate")

        months = [str(i) for i in range(1, 13)]
        days = [str(i) for i in range(1, 32)]
        years = [str(i) for i in range(1900, 2025)]

        month_dropdown = ui.select(months, value=None, label="Month")
        day_dropdown = ui.select(days, value=None, label="Day")
        year_dropdown = ui.select(years, value=None, label="Year")

        output_label = ui.label("").style("font-size: 18px; color: blue;")

        def update_output():
            selected_month = month_dropdown.value
            selected_day = day_dropdown.value
            selected_year = year_dropdown.value

            if selected_month and selected_day and selected_year:
                output_label.set_text(f"Selected Date: {selected_month}-{selected_day}-{selected_year}")
            else:
                output_label.set_text("Please select Month, Day, and Year.")

        ui.button("Submit", on_click=update_output)
