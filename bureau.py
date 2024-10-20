import asyncio
import sys
from uagents import Agent, Bureau, Context, Model
import sqlite3
import json

# Define models
class PatientQuery(Model):
    patient_name: str

class PatientData(Model):
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

# Hospital 1 handles queries
@HospitalAgent.on_message(model=PatientQuery)
async def handle_hospital1_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital1_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    await ctx.send(sender, PatientData(data=patient_data_json))

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

# Hospital 2 handles queries
@Hospital2Agent.on_message(model=PatientQuery)
async def handle_hospital2_query(ctx: Context, sender: str, msg: PatientQuery):
    patient_name = msg.patient_name
    patient_data = read_hospital2_data(patient_name)
    patient_data_json = json.dumps(patient_data, indent=4)
    await ctx.send(sender, PatientData(data=patient_data_json))

# Store the responses
patient_data_responses = {}

# Test agent handles responses from hospitals
@TestAgent.on_message(model=PatientData)
async def handle_response(ctx: Context, sender: str, msg: PatientData):
    global patient_data_responses
    patient_data_responses[sender] = json.loads(msg.data)

# Function to get combined patient data from both hospitals
async def get_combined_patient_data(patient_name, ctx: Context):
    global patient_data_responses
    # Clear previous responses
    patient_data_responses = {}

    # Send query to both hospitals using the passed context
    await ctx.send(HospitalAgent.address, PatientQuery(patient_name=patient_name))
    await ctx.send(Hospital2Agent.address, PatientQuery(patient_name=patient_name))

    # Wait for both responses to be collected
    while len(patient_data_responses) < 2:
        await asyncio.sleep(0.1)  # Allow event loop to continue processing

    # Get hospital 1 data (handle case where it may have no data)
    hospital1_data = patient_data_responses.get(HospitalAgent.address, "No data found in Hospital 1")
    
    # Get hospital 2 data (handle case where it may have no data)
    hospital2_data = patient_data_responses.get(Hospital2Agent.address, "No data found in Hospital 2")
    
    # Format the output as a single string
    combined_data = f"--- Hospital 1 Data ---\n{json.dumps(hospital1_data, indent=4)}\n\n" \
                    f"--- Hospital 2 Data ---\n{json.dumps(hospital2_data, indent=4)}"
    
    return combined_data

# Async input function
async def async_input(prompt):
    print(prompt, end='', flush=True)
    loop = asyncio.get_event_loop()
    return (await loop.run_in_executor(None, sys.stdin.readline)).rstrip('\n')

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
            
            # Get the combined data and print it
            combined_data = await get_combined_patient_data(patient_name, ctx)
            print(f"\nCombined medical data:\n{combined_data}\n")
    
    # Schedule the input loop as a background task
    asyncio.create_task(input_loop())

# Create a bureau that contains all agents
bureau = Bureau(port=8000)  # Single bureau to manage all agents
bureau.add(TestAgent)
bureau.add(HospitalAgent)
bureau.add(Hospital2Agent)

if __name__ == "__main__":
    print(f"Hospital1Agent Address: {HospitalAgent.address}")
    print(f"Hospital2Agent Address: {Hospital2Agent.address}")
    bureau.run()
