from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from messages import PatientQuery, PatientData
import sqlite3
import json

# Hospital 1 Agent
HospitalAgent = Agent(
    name="hospital1_agent",
    seed="HospitalOneAgent",
    port=7701,
    endpoint=["http://127.0.0.1:7701/submit"]
)

fund_agent_if_low(HospitalAgent.wallet.address())  # type: ignore

# Function to read data from hospital1 database
def read_hospital1_data(patient_name: str):
    conn = sqlite3.connect('databases/hospital1_records.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT first_name, last_name, dob, gender, address, phone_number, email, 
               diagnosis, procedures, prescriptions, treatments, tests 
        FROM hospital1_patients 
        WHERE first_name || " " || last_name = ?
    ''', (patient_name,))
    patient_data = cursor.fetchall()

    common_data = []
    for patient in patient_data:
        full_name = f"{patient[0]} {patient[1]}"  # First and last name
        dob = patient[2]  # Date of birth
        gender = patient[3]  # Gender
        address = patient[4]  # Address
        phone_number = patient[5]  # Phone number
        email = patient[6]  # Email
        medical_history = {
            "diagnoses": patient[7].split(", ") if patient[7] else [],  # Diagnosis
            "procedures": patient[8].split(", ") if patient[8] else [],  # Procedures
            "prescriptions": patient[9].split(", ") if patient[9] else [],  # Prescriptions
            "treatments": patient[10].split(", ") if patient[10] else [],  # Treatments
            "tests": patient[11].split(", ") if patient[11] else []  # Tests
        }
        common_data.append(PatientData(
            full_name=full_name,
            dob=dob,
            gender=gender,
            address=address,
            phone_number=phone_number,
            email=email,
            medical_history=medical_history  # type: ignore
        ))

    conn.close()
    return common_data[0]

# Hospital 1 handles queries
@HospitalAgent.on_message(model=PatientQuery)
async def handle_hospital1_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital1_data(patient_name)
    await ctx.send(sender, patient_data)

if __name__ == "__main__":
    print(f"Hospital1Agent Address: {HospitalAgent.address}")
    HospitalAgent.run()
