import sqlite3
from faker import Faker
import random

fake = Faker()
Faker.seed(329)

conn = sqlite3.connect('databases/hospital1_records.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS hospital1_patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        dob DATE NOT NULL,
        gender TEXT,
        address TEXT,
        phone_number TEXT,
        email TEXT,
        diagnosis TEXT, -- Comma-separated list of diagnoses
        procedures TEXT, -- Comma-separated list of procedures
        prescriptions TEXT, -- Comma-separated list of prescriptions
        treatments TEXT, -- Comma-separated list of treatments
        tests TEXT -- Comma-separated list of tests
    )
''')

cursor.execute('DELETE FROM hospital1_patients')

hardcoded_data = [
    ('John', 'Doe', '1951-02-04', 'Male', '71777 Brown Plains Suite 229, Strongborough, NE 29414', '272-337-8973x15193', 'benjamin95@example.org', 'Flu, Asthma, Migraine', 'X-ray, Blood test', 'Metformin, Amoxicillin, Lisinopril', 'Physical therapy', 'Thyroid test'),
    ('Jane', 'Smith', '1937-10-07', 'Female', 'Unit 7456 Box 9274, DPO AP 30435', '520-493-1321', 'xrodriguez@example.org', 'Hypertension', 'Ultrasound', 'Metformin, Ibuprofen, Insulin', 'Radiation therapy, Dialysis', 'Allergy test'),
    ('Alice', 'Johnson', '1957-10-18', 'Male', '8262 Cabrera Manor, Dorseyfurt, RI 74980', '3457958563', 'andersonwilliam@example.com', 'Arthritis', 'MRI, X-ray', 'Metformin, Lisinopril, Amoxicillin', 'Radiation therapy, Dialysis', 'Cholesterol test, Blood sugar test'),
    ('Chris', 'Evans', '1944-02-20', 'Male', '886 Ashley Islands, New Timothy, AR 53429', '001-569-799-1205x0603', 'rvargas@example.net', 'Diabetes', 'Ultrasound', 'Ibuprofen', 'Radiation therapy', 'Cholesterol test, Thyroid test'),
    ('Tony', 'Stark', '2022-10-20', 'Female', '157 Ortiz Mountains, West Robertside, PW 02183', '717-960-3529x3531', 'terryveronica@example.com', 'Migraine', 'Ultrasound, Blood test', 'Amoxicillin', 'Dialysis', 'Allergy test, Thyroid test'),
    ('Natasha', 'Romanoff', '1936-07-31', 'Male', '668 Wesley Mission Apt. 104, Dorseyfort, NY 12749', '234-555-1234', 'natasha@example.com', 'Hypertension, Migraine', 'Blood test, Ultrasound', 'Amoxicillin', 'Dialysis, Radiation therapy', 'Thyroid test'),
    ('Shuri', 'Black Panther', '1975-11-11', 'Male', 'Unit 4758 Box 9335, DPO AA 96852', '312.675.4489', 'juan40@example.net', 'Arthritis, Flu', 'MRI', 'Ibuprofen', 'Dialysis, Physical therapy', 'Allergy test'),
    ('Clint', 'Barton', '1999-12-04', 'Male', '099 Doyle Crest, Brandonmouth, OK 36754', '+1-735-468-5345', 'gbeasley@example.com', 'Diabetes', 'ECG, MRI', 'Lisinopril', 'Chemotherapy, Radiation therapy', 'Blood sugar test'),
    ('Groot', 'Tree', '1943-08-14', 'Male', '095 Garcia Row, Cynthiatown, MH 26747', '001-457-781-9015x75538', 'tracyrodriguez@example.com', 'Flu', 'X-ray, MRI', 'Metformin', 'Physical therapy', 'Thyroid test'),
    ('Rocket', 'Raccoon', '1935-11-05', 'Male', '59787 April Roads Apt. 106, East David, MS 68741', '(905)881-8911x27538', 'sandy10@example.net', 'Diabetes, Flu, Arthritis', 'MRI', 'Lisinopril, Metformin, Amoxicillin', 'Physical therapy, Chemotherapy', 'Cholesterol test'),
    ('Drax', 'Destroyer', '1946-09-23', 'Female', '66621 Megan Shores Suite 280, New Tanyaport, IA 07132', '612.722.8762', 'ohurst@example.net', 'Migraine, Asthma', 'ECG', 'Amoxicillin, Lisinopril', 'Radiation therapy', 'Thyroid test'),
    ('Gamora', 'Zen-Whoberi', '1934-10-19', 'Male', '6797 Melissa Drive Suite 994, North Christinahaven, ID 24192', '313-734-5563x4085', 'fjohnson@example.org', 'Diabetes', 'X-ray, ECG', 'Amoxicillin', 'Chemotherapy, Radiation therapy', 'Thyroid test'),
    ('Carol', 'Danvers', '2008-07-02', 'Male', '89860 Henderson Lights, Lake Mark, PA 94760', '+1-299-838-4043', 'parkstacey@example.net', 'Migraine, Hypertension, Flu', 'MRI, Ultrasound', 'Lisinopril', 'Chemotherapy, Radiation therapy', 'Thyroid test'),
    ('Wanda', 'Maximoff', '1974-06-22', 'Male', '526 Roy Place, Barkerfurt, AZ 82030', '791-865-7725x8900', 'eddiefowler@example.com', 'Asthma, Diabetes', 'Blood test, ECG', 'Amoxicillin, Insulin', 'Physical therapy', 'Cholesterol test'),
    ('Vision', 'Synthetic', '1967-03-18', 'Male', '455 Williams Brook Suite 258, Rodriguezmouth, LA 77673', '001-542-974-0813x178', 'gregorykevin@example.org', 'Flu', 'Blood test', 'Lisinopril', 'Radiation therapy', 'Allergy test'),
    ('Thor', 'Odinson', '1987-01-05', 'Male', 'USNS Mccoy, FPO AA 15676', '+1-278-775-7803x557', 'ryanhickman@example.org', 'Migraine, Hypertension', 'X-ray, Blood test', 'Amoxicillin, Insulin', 'Chemotherapy', 'Thyroid test, Allergy test'),
    ('Loki', 'Laufeyson', '1948-07-19', 'Male', 'PSC 7088, Box 6661, APO AE 99245', '736-231-3714', 'cassandra06@example.com', 'Diabetes, Arthritis, Migraine', 'MRI, Ultrasound', 'Lisinopril', 'Physical therapy, Chemotherapy', 'Allergy test'),
    ('Sam', 'Wilson', '1937-04-26', 'Male', '71147 Jason Manors, West Allenburgh, NH 38178', '+1-957-675-4908x12713', 'clintonhunt@example.com', 'Hypertension, Diabetes, Asthma', 'MRI, Ultrasound', 'Metformin, Insulin, Lisinopril', 'Radiation therapy, Chemotherapy', 'Thyroid test'),
    ('Bucky', 'Barnes', '2022-12-19', 'Female', '14626 Jessica Point Suite 971, Marcusfort, KS 36288', '(238)789-0176x36697', 'lori71@example.com', 'Flu', 'Blood test', 'Amoxicillin', 'Chemotherapy, Physical therapy', 'Cholesterol test, Thyroid test'),
    ('Scott', 'Lang', '1942-09-30', 'Male', '502 Watson Locks, Kevinview, MT 31039', '(761)657-9827x3534', 'john77@example.net', 'Flu, Diabetes, Asthma', 'Ultrasound, Blood test', 'Lisinopril', 'Dialysis', 'Blood sugar test'),
    ('Hope', 'Van Dyne', '1976-06-08', 'Female', '17059 Lindsey Stream, Lake Charles, FM 76651', '001-770-399-1471x40739', 'zjohnson@example.net', 'Arthritis', 'Blood test, X-ray', 'Lisinopril', 'Physical therapy', 'Blood sugar test'),
    ('TChalla', 'Black Panther', '1972-01-27', 'Female', '4240 Steven Flat, East Charlesborough, CT 18243', '+1-616-360-1943x172', 'millsbeth@example.net', 'Hypertension, Migraine', 'Blood test, Ultrasound', 'Amoxicillin', 'Dialysis, Radiation therapy', 'Thyroid test'),
    ('Shuri', 'Black Panther', '1975-11-11', 'Male', 'Unit 4758 Box 9335, DPO AA 96852', '312.675.4489', 'juan40@example.net', 'Arthritis, Flu', 'MRI', 'Ibuprofen', 'Dialysis, Physical therapy', 'Allergy test'),
    ('Bruce', 'Banner', '1996-12-05', 'Female', '257 Robinson Ridge Suite 968, Yatesborough, OR 10596', '667-863-6263', 'williamsondeborah@example.com', 'Asthma', 'X-ray', 'Ibuprofen', 'Radiation therapy', 'Thyroid test'),
    ('Steve', 'Rogers', '2009-04-04', 'Male', '75652 Jason Meadows, Lake Michael, WV 79574', '451.340.4591x51009', 'ryan36@example.net', 'Flu', 'X-ray', 'Ibuprofen, Lisinopril', 'Chemotherapy, Radiation therapy', 'Thyroid test, Cholesterol test')
]


for patient in hardcoded_data:
    cursor.execute('''
        INSERT INTO hospital1_patients (
            first_name, last_name, dob, gender, address, phone_number, email, diagnosis, procedures, prescriptions, treatments, tests
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', patient)

for _ in range(500):
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=0, maximum_age=90)
    gender = fake.random_element(elements=('Male', 'Female'))
    address = fake.address().replace('\n', ', ')
    phone_number = fake.phone_number()
    email = fake.email()

    diagnosis = ', '.join(random.sample(['Hypertension', 'Diabetes', 'Asthma', 'Arthritis', 'Flu', 'Migraine'], k=random.randint(1, 3)))
    procedure = ', '.join(random.sample(['Blood test', 'X-ray', 'MRI', 'Ultrasound', 'ECG'], k=random.randint(1, 2)))
    prescription = ', '.join(random.sample(['Ibuprofen', 'Metformin', 'Lisinopril', 'Amoxicillin', 'Insulin'], k=random.randint(1, 3)))
    treatment = ', '.join(random.sample(['Physical therapy', 'Chemotherapy', 'Radiation therapy', 'Dialysis'], k=random.randint(1, 2)))
    test = ', '.join(random.sample(['Blood sugar test', 'Cholesterol test', 'Thyroid test', 'Allergy test'], k=random.randint(1, 2)))

    cursor.execute('''
        INSERT INTO hospital1_patients (
            first_name, last_name, dob, gender, address, phone_number, email, diagnosis, procedures, prescriptions, treatments, tests
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, dob, gender, address, phone_number, email, diagnosis, procedure, prescription, treatment, test))

conn.commit()
conn.close()

print("Hardcoded patients and 500 random patients inserted into hospital1_patients table!")