import sqlite3
from faker import Faker
import random
import json

fake = Faker()
Faker.seed(12345)

conn = sqlite3.connect('hospital2_records.db')
cursor = conn.cursor()

def drop_table():
    cursor.execute('''
        DROP TABLE IF EXISTS hospital2_patients;
    ''')


def create_table():
    cursor.execute('''
        CREATE TABLE hospital2_patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT,
            contact_info TEXT,
            email TEXT,
            medical_history TEXT
        );
    ''')

def insert_hardcoded_patients():
    patients = [
        ("John Doe", "1951-02-04", "Male", "71777 Brown Plains Suite 229, Strongborough, NE 29414, 272-337-8973x15193", "benjamin95@example.org", '{"diagnoses": ["Asthma", "Kidney Stones"], "procedures": ["Knee Surgery", "Gallbladder Removal"], "prescriptions": ["Insulin 10 units before meals", "Aspirin 81mg daily"], "treatments": ["Physical therapy for 3 months"], "tests": ["Blood test", "MRI scan"]}'),
        ("Jane Smith", "1937-10-07", "Female", "Unit 7456 Box 9274, DPO AP 30435, 520-493-1321", "xrodriguez@example.org", '{"diagnoses": ["Pneumonia"], "procedures": ["Angioplasty"], "prescriptions": ["Albuterol inhaler", "Aspirin 81mg daily"], "treatments": ["Chemotherapy for 6 months"], "tests": ["CT scan"]}'),
        ("Alice Johnson", "1957-10-18", "Male", "8262 Cabrera Manor, Dorseyfurt, RI 74980, 3457958563", "andersonwilliam@example.com", '{"diagnoses": ["Bronchitis"], "procedures": ["Hip Replacement"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Blood pressure monitoring"], "tests": ["X-ray"]}'),
        ("Chris Evans", "1944-02-20", "Male", "886 Ashley Islands, New Timothy, AR 53429, 001-569-799-1205x0603", "rvargas@example.net", '{"diagnoses": ["Heart disease", "Hypertension"], "procedures": ["Angioplasty"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Radiation therapy"], "tests": ["Blood test"]}'),
        ("Tony Stark", "2022-10-20", "Female", "157 Ortiz Mountains, West Robertside, PW 02183, 717-960-3529x3531", "terryveronica@example.com", '{"diagnoses": ["Migraines", "Diabetes"], "procedures": ["Knee Surgery"], "prescriptions": ["Insulin 10 units before meals"], "treatments": ["Blood pressure monitoring"], "tests": ["MRI scan", "CT scan"]}'),
        ("Natasha Romanoff", "1936-07-31", "Male", "668 Wesley Mission Apt. 507, Jocelynburgh, WI 95373, 587-426-7226x63792", "amy89@example.com", '{"diagnoses": ["Asthma"], "procedures": ["Appendectomy"], "prescriptions": ["Albuterol inhaler"], "treatments": ["Physical therapy for 3 months"], "tests": ["X-ray", "CT scan"]}'),
        ("Bruce Banner", "1996-12-05", "Female", "257 Robinson Ridge Suite 968, Yatesborough, OR 10596, 667-863-6263", "williamsondeborah@example.com", '{"diagnoses": ["Broken leg"], "procedures": ["Hip Replacement"], "prescriptions": ["Aspirin 81mg daily"], "treatments": ["Radiation therapy"], "tests": ["Blood test"]}'),
        ("Steve Rogers", "2009-04-04", "Male", "75652 Jason Meadows, Lake Michael, WV 79574, 451.340.4591x51009", "ryan36@example.net", '{"diagnoses": ["Pneumonia"], "procedures": ["Knee Surgery"], "prescriptions": ["Insulin 10 units before meals"], "treatments": ["Chemotherapy for 6 months"], "tests": ["MRI scan", "CT scan"]}'),
        ("Peter Parker", "2013-07-28", "Female", "707 Yang Courts Apt. 719, Port Kyleside, VI 02020, (483)409-6991x1430", "christopherhampton@example.org", '{"diagnoses": ["Diabetes"], "procedures": ["Angioplasty"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Blood pressure monitoring"], "tests": ["CT scan"]}'),
        ("Carol Danvers", "2008-07-02", "Male", "89860 Henderson Lights, Lake Mark, PA 94760, +1-299-838-4043", "parkstacey@example.net", '{"diagnoses": ["Allergies", "Bronchitis"], "procedures": ["Appendectomy"], "prescriptions": ["Albuterol inhaler", "Aspirin 81mg daily"], "treatments": ["Chemotherapy for 6 months"], "tests": ["X-ray"]}'),
        ("Wanda Maximoff", "1974-06-22", "Male", "526 Roy Place, Barkerfurt, AZ 82030, 791-865-7725x8900", "eddiefowler@example.com", '{"diagnoses": ["Kidney Stones"], "procedures": ["Angioplasty"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Blood pressure monitoring"], "tests": ["Blood test"]}'),
        ("Vision Synthetic", "1967-03-18", "Male", "455 Williams Brook Suite 258, Rodriguezmouth, LA 77673, 001-542-974-0813x178", "gregorykevin@example.org", '{"diagnoses": ["Asthma", "Heart disease"], "procedures": ["Appendectomy"], "prescriptions": ["Albuterol inhaler"], "treatments": ["Radiation therapy"], "tests": ["X-ray"]}'),
        ("Thor Odinson", "1987-01-05", "Male", "USNS Mccoy, FPO AA 15676, +1-278-775-7803x557", "ryanhickman@example.org", '{"diagnoses": ["Bronchitis"], "procedures": ["Gallbladder Removal"], "prescriptions": ["Aspirin 81mg daily"], "treatments": ["Physical therapy for 3 months"], "tests": ["MRI scan"]}'),
        ("Loki Laufeyson", "1948-07-19", "Male", "PSC 7088, Box 6661, APO AE 99245, 736-231-3714", "cassandra06@example.com", '{"diagnoses": ["Hypertension", "Heart disease"], "procedures": ["Hip Replacement"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Chemotherapy for 6 months"], "tests": ["CT scan"]}'),
        ("Sam Wilson", "1937-04-26", "Male", "71147 Jason Manors, West Allenburgh, NH 38178, +1-957-675-4908x12713", "clintonhunt@example.com", '{"diagnoses": ["Pneumonia", "Diabetes"], "procedures": ["Angioplasty"], "prescriptions": ["Insulin 10 units before meals"], "treatments": ["Blood pressure monitoring"], "tests": ["MRI scan", "CT scan"]}'),
        ("Bucky Barnes", "2022-12-19", "Female", "14626 Jessica Point Suite 971, Marcusfort, KS 36288, (238)789-0176x36697", "lori71@example.com", '{"diagnoses": ["Asthma"], "procedures": ["Knee Surgery"], "prescriptions": ["Albuterol inhaler"], "treatments": ["Chemotherapy for 6 months"], "tests": ["Blood test"]}'),
        ("Scott Lang", "1942-09-30", "Male", "502 Watson Locks, Kevinview, MT 31039, (761)657-9827x3534", "john77@example.net", '{"diagnoses": ["Hypertension", "Migraines"], "procedures": ["Gallbladder Removal"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Blood pressure monitoring"], "tests": ["X-ray"]}'),
        ("Hope Van Dyne", "1976-06-08", "Female", "17059 Lindsey Stream, Lake Charles, FM 76651, 001-770-399-1471x40739", "zjohnson@example.net", '{"diagnoses": ["Kidney Stones", "Asthma"], "procedures": ["Hip Replacement"], "prescriptions": ["Albuterol inhaler"], "treatments": ["Radiation therapy"], "tests": ["MRI scan"]}'),
        ("TChalla Black Panther", "1972-01-27", "Female", "4240 Steven Flat, East Charlesborough, CT 18243, +1-616-360-1943x172", "millsbeth@example.net", '{"diagnoses": ["Hypertension"], "procedures": ["Knee Surgery"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Physical therapy for 3 months"], "tests": ["CT scan"]}'),
        ("Shuri Black Panther", "1975-11-11", "Male", "Unit 4758 Box 9335, DPO AA 96852, 312.675.4489", "juan40@example.net", '{"diagnoses": ["Diabetes", "Pneumonia"], "procedures": ["Hip Replacement"], "prescriptions": ["Insulin 10 units before meals"], "treatments": ["Chemotherapy for 6 months"], "tests": ["Blood test", "X-ray"]}'),
        ("Clint Barton", "1999-12-04", "Male", "099 Doyle Crest, Brandonmouth, OK 36754, +1-735-468-5345", "gbeasley@example.com", '{"diagnoses": ["Asthma"], "procedures": ["Angioplasty"], "prescriptions": ["Albuterol inhaler"], "treatments": ["Radiation therapy"], "tests": ["CT scan"]}'),
        ("Groot Tree", "1943-08-14", "Male", "095 Garcia Row, Cynthiatown, MH 26747, 001-457-781-9015x75538", "tracyrodriguez@example.com", '{"diagnoses": ["Allergies"], "procedures": ["Appendectomy"], "prescriptions": ["Aspirin 81mg daily"], "treatments": ["Physical therapy for 3 months"], "tests": ["MRI scan"]}'),
        ("Rocket Raccoon", "1935-11-05", "Male", "59787 April Roads Apt. 106, East David, MS 68741, (905)881-8911x27538", "sandy10@example.net", '{"diagnoses": ["Migraines", "Kidney Stones"], "procedures": ["Knee Surgery"], "prescriptions": ["Insulin 10 units before meals"], "treatments": ["Blood pressure monitoring"], "tests": ["Blood test"]}'),
        ("Drax Destroyer", "1946-09-23", "Female", "66621 Megan Shores Suite 280, New Tanyaport, IA 07132, 612.722.8762", "ohurst@example.net", '{"diagnoses": ["Diabetes", "Asthma"], "procedures": ["Gallbladder Removal"], "prescriptions": ["Albuterol inhaler"], "treatments": ["Radiation therapy"], "tests": ["X-ray"]}'),
        ("Gamora Zen-Whoberi", "1934-10-19", "Male", "6797 Melissa Drive Suite 994, North Christinahaven, ID 24192, 313-734-5563x4085", "fjohnson@example.org", '{"diagnoses": ["Hypertension"], "procedures": ["Angioplasty"], "prescriptions": ["Metoprolol 50mg daily"], "treatments": ["Blood pressure monitoring"], "tests": ["Blood test", "CT scan"]}')
    ]

    
    for patient in patients:
        cursor.execute('''
            INSERT INTO hospital2_patients (full_name, dob, gender, contact_info, email, medical_history)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', patient)

def generate_hospital2_medical_history():
    conditions = [
        'Hypertension', 'Diabetes', 'Asthma', 'Broken leg', 'Migraines',
        'Allergies', 'Bronchitis', 'Kidney Stones', 'Pneumonia', 'Heart disease'
    ]
    
    procedures = [
        'Appendectomy', 'Knee Surgery', 'Angioplasty', 
        'Gallbladder Removal', 'Hip Replacement'
    ]
    
    prescriptions = [
        'Metoprolol 50mg daily', 'Insulin 10 units before meals', 
        'Aspirin 81mg daily', 'Albuterol inhaler'
    ]
    
    treatments = [
        'Physical therapy for 3 months', 'Chemotherapy for 6 months', 
        'Radiation therapy', 'Blood pressure monitoring'
    ]
    
    tests = [
        'Blood test', 'MRI scan', 'X-ray', 'CT scan'
    ]

    medical_history = {
        "diagnoses": random.choices(conditions, k=random.randint(1, 3)),
        "procedures": random.choices(procedures, k=random.randint(0, 2)),
        "prescriptions": random.choices(prescriptions, k=random.randint(1, 3)),
        "treatments": random.choices(treatments, k=random.randint(0, 2)),
        "tests": random.choices(tests, k=random.randint(0, 3))
    }
    
    return json.dumps(medical_history)

def insert_into_hospital2(num_records=500):
    for _ in range(num_records):
        full_name = fake.first_name() + ' ' + fake.last_name()  
        dob = str(fake.date_of_birth(minimum_age=20, maximum_age=90))
        gender = random.choice(['Male', 'Female', 'Other'])
        contact_info = fake.address() + ', ' + fake.phone_number()  
        email = fake.email()

        medical_history = generate_hospital2_medical_history()

        cursor.execute('''
            INSERT INTO hospital2_patients (full_name, dob, gender, contact_info, email, medical_history)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (full_name, dob, gender, contact_info, email, medical_history))

drop_table()
create_table()
insert_hardcoded_patients()
insert_into_hospital2(500)

conn.commit()
conn.close()



"""
CREATE TABLE hospital2_patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL, -- Full name instead of separate first/last names
    dob TEXT NOT NULL, -- Date of birth stored as TEXT
    gender TEXT,
    contact_info TEXT, -- Address and phone number combined into a single text field
    email TEXT,
    medical_history TEXT -- JSON-like text storing all medical history
);
"""