from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import sqlite3
import json

# Define models
class PatientQuery(Model):
    patient_name: str

class PatientData(Model):
    data: str

# Hospital 2 Agent
Hospital2Agent = Agent(
    name="hospital2_agent",
    seed="HospitalTwoAgent",
    port=7702,
    endpoint=["http://127.0.0.1:7702/submit"]
)

fund_agent_if_low(Hospital2Agent)

# Function to read data from hospital2 database
def read_hospital2_data(patient_name):
    conn = sqlite3.connect('databases/hospital2_records.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT full_name, dob, gender, contact_info, email, medical_history 
        FROM hospital2_patients 
        WHERE full_name = ?
    ''', (patient_name,))
    patient_data = cursor.fetchall()

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

# Hospital 2 handles queries
@Hospital2Agent.on_message(model=PatientQuery)
async def handle_hospital2_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital2_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    await ctx.send(sender, PatientData(data=patient_data_json))

if __name__ == "__main__":
    print(f"Hospital2Agent Address: {Hospital2Agent.address}")
    Hospital2Agent.run()
