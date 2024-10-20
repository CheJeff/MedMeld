import asyncio
import sys
from uagents import Agent, Bureau, Context, Model
import sqlite3
import json

# Define models
class PatientQuery(Model):
    patient_name: str

class PatientData(Model):
    patient_name: str
    data: str

# Test Agent
TestAgent = Agent(
    name="test_agent",
    seed="TestAgent secret phrase",
)

# Hospital 1 Agent
HospitalAgent = Agent(
    name="hospital1_agent",
    seed="HospitalOneAgent",
    port=8000,
)

# Hospital 2 Agent
Hospital2Agent = Agent(
    name="hospital2_agent",
    seed="HospitalTwoAgent",
    port=8001,
)

# Function to read data from hospital1 database
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
    pass

# Hospital 1 handles queries
@HospitalAgent.on_message(model=PatientQuery)
async def handle_hospital1_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital1_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    await ctx.send(sender, PatientData(data=patient_data_json))
    pass
# Function to read data from hospital2 database
def read_hospital2_data(patient_name):
    conn = sqlite3.connect('hospital2_records.db')
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
    pass

# Hospital 2 handles queries
@Hospital2Agent.on_message(model=PatientQuery)
async def handle_hospital2_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital2_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    await ctx.send(sender, PatientData(data=patient_data_json))
    pass
async def async_input(prompt):
    print(prompt, end='', flush=True)
    loop = asyncio.get_event_loop()
    return (await loop.run_in_executor(None, sys.stdin.readline)).rstrip('\n')

# Test agent handles responses from hospitals
@TestAgent.on_message(model=PatientData)
async def handle_response(ctx: Context, sender: str, msg: PatientData):
    print(f"\nReceived medical data from {sender}:\n{msg.data}\n")

# Test agent waits for user input and sends queries
@TestAgent.on_event("startup")
async def on_startup(ctx: Context):
    async def input_loop():
        while True:
            patient_name = await async_input("Enter patient name (or 'exit' to quit): ")
            if patient_name.lower() == 'exit':
                print("Exiting.")
                sys.exit()
            if not patient_name.strip():
                print("Please enter a valid patient name.")
                continue
            # Send query to hospital 1
            await ctx.send(HospitalAgent.address, PatientQuery(patient_name=patient_name))
            # Send query to hospital 2
            await ctx.send(Hospital2Agent.address, PatientQuery(patient_name=patient_name))
    # Schedule the input loop as a background task
    asyncio.create_task(input_loop())

def combine_patient_data(patient_data_list):
    combined_patient_data = {}
    for data_list in patient_data_list:
        for patient in data_list:
            for key, value in patient.items():
                if key not in combined_patient_data:
                    combined_patient_data[key] = value
                else:
                    if isinstance(value, dict):
                        if not isinstance(combined_patient_data[key], dict):
                            combined_patient_data[key] = {}
                        for subkey, subvalue in value.items():
                            if subkey not in combined_patient_data[key]:
                                combined_patient_data[key][subkey] = subvalue
                            else:
                                if isinstance(subvalue, list):
                                    combined_list = combined_patient_data[key][subkey] + subvalue
                                    combined_list = list(set(combined_list))
                                    combined_patient_data[key][subkey] = combined_list
                    elif isinstance(value, list):
                        if not isinstance(combined_patient_data[key], list):
                            combined_patient_data[key] = []
                        combined_list = combined_patient_data[key] + value
                        combined_list = list(set(combined_list))
                        combined_patient_data[key] = combined_list
    return combined_patient_data


# Create a bureau that contains all agents
bureau = Bureau(port=8000)  # Single bureau to manage all agents
bureau.add(TestAgent)
bureau.add(HospitalAgent)
bureau.add(Hospital2Agent)

if __name__ == "__main__":
    print(f"Hospital1Agent Address: {HospitalAgent.address}")
    print(f"Hospital2Agent Address: {Hospital2Agent.address}")
    bureau.run()
