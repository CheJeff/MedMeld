from uagents import Model

class Token:
    patient_id: int
    def __init__(self, pid: int) -> None:
        self.patient_id = pid

    @classmethod
    def from_str(cls, parse: str):
        return cls(int(parse))

    def to_str(self) -> str:
        return str(self.patient_id).rjust(9, "0")

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
