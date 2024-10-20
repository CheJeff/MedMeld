from uagents import Model
from typing import TypedDict

class Token:
    _patient_id: int
    def __init__(self, pid: int) -> None:
        self._patient_id = pid

    @property
    def patient_id(self) -> str:
        return self._patient_id

    def to_str(self) -> str:
        return str(self._patient_id).rjust(9, "0")

    @classmethod
    def from_str(cls, parse: str):
        return cls(int(parse))


class ReqCreateAccount(Model):
    name: str
    password: str

class ResCreateAccount(Model):
    token: str
    status: str

class ReqSignIn(Model):
    name: str
    password: str

class ResSignIn(Model):
    token: str
    status: str

class ReqAddProvider(Model):
    token: str
    providers: list[str]

class ResAddProvider(Model):
    token: str
    status: str

class ReqNameToken(Model):
    token: str

class ResNameToken(Model):
    token: str
    name: str
    status: str


class MedicalHistory(TypedDict):
    diagnoses: list[str]  # Diagnosis
    procedures: list[str]  # Procedures
    prescriptions: list[str]  # Prescriptions
    treatments: list[str]  # Treatments
    tests: list[str]  # Tests


class PatientQuery(Model):
    patient_name: str

class PatientData(Model):
    full_name: str
    dob: str
    gender: str
    address: str
    phone_number: str
    email: str
    medical_history: MedicalHistory
