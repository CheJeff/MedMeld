import asyncio
from uagents import Agent, Bureau, Context, Model
import sqlite3
import json

class PatientQuery(Model):
    patient_name: str

class PatientData(Model):
    data: str

TestAgent = Agent(
    name="test_agent",
    seed="TestAgent secret phrase",  
)

HospitalAgent = Agent(
    name="hospital1_agent",
    seed="HospitalOneAgent",  
)

def read_hospital1_data(patient_name):
    conn = sqlite3.connect('hospital1_records.db')
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
        common_data.append({
            "full_name": full_name,
            "dob": dob,
            "gender": gender,
            "address": address,
            "phone_number": phone_number,
            "email": email,
            "medical_history": medical_history
        })

    conn.close()
    return common_data

@HospitalAgent.on_message(model=PatientQuery)
async def handle_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    print(f"[hospital1_agent] Received query for: {patient_name}")
    patient_data = read_hospital1_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    print(f"[hospital1_agent] Sending patient data: {patient_data_json}")
    await ctx.send(sender, PatientData(data=patient_data_json))

# @TestAgent.on_event("start")
@TestAgent.on_interval(period=3.0)
async def send_query(ctx: Context):
    patient_name = "Steve Rogers"
    print(f"[test_agent] Sending query for {patient_name}")
    await ctx.send(HospitalAgent.address, PatientQuery(patient_name=patient_name))

@TestAgent.on_message(model=PatientData)
async def handle_response(ctx: Context, sender: str, msg: PatientData):
    print(f"Received medical data from {sender}: {msg.data}")

bureau = Bureau()
bureau.add(TestAgent)
bureau.add(HospitalAgent)

if __name__ == "__main__":
    bureau.run()  
