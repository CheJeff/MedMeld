import asyncio
from uagents import Agent, Bureau, Context, Model
import sqlite3
import json

class PatientQuery(Model):
    patient_name: str

class PatientData(Model):
    data: str

TestAgent = Agent(
    name="test_agent_hospital2",
    seed="TestAgentHospital2 secret phrase",  
)

Hospital2Agent = Agent(
    name="hospital2_agent",
    seed="HospitalTwoAgent secret phrase",  
)

def read_hospital2_data(patient_name):
    conn = sqlite3.connect('hospital2_records.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT full_name, dob, gender, contact_info, email, medical_history 
        FROM hospital2_patients 
        WHERE full_name = ?
    ''', (patient_name,))
    patient_data = cursor.fetchall()

    # Define common data format
    common_data = []
    for patient in patient_data:
        full_name = patient[0]  # Full name already combined
        dob = patient[1]  # Date of birth as text
        gender = patient[2]  # Gender
        contact_info = patient[3].split(", ")  # Contact info (split into address and phone number)
        address = contact_info[0] if len(contact_info) > 0 else ""
        phone_number = contact_info[1] if len(contact_info) > 1 else ""
        email = patient[4]  # Email
        medical_history = json.loads(patient[5])  # Parse JSON-like medical history field

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

@Hospital2Agent.on_message(model=PatientQuery)
async def handle_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital2_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    await ctx.send(sender, PatientData(data=patient_data_json))

# @TestAgent.on_event("start")
@TestAgent.on_interval(period=3.0)
async def send_query(ctx: Context):
    patient_name = "Steve Rogers"
    await ctx.send(Hospital2Agent.address, PatientQuery(patient_name=patient_name))

@TestAgent.on_message(model=PatientData)
async def handle_response(ctx: Context, sender: str, msg: PatientData):
    print(f"Received medical data from {sender}: {msg.data}")

bureau = Bureau()
bureau.add(TestAgent)
bureau.add(Hospital2Agent)

if __name__ == "__main__":
    bureau.run() 
