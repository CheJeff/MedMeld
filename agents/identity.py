from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from os import environ
import hashlib
import psycopg
from psycopg.rows import dict_row
import random
import base64
from messages import *

agent = Agent(
    seed = "identity agent string",
    name = "MedMeld Identity Agent",
    port = 8004,
    endpoint = ["http://127.0.0.1:8004/submit"]
)

fund_agent_if_low(agent.wallet.address())  # type: ignore

def hashpass(passwd: str) -> str:
    # generate salt
    bts = random.randbytes(256)
    return base64.encodebytes(bts + hashlib.sha256(bts + passwd.encode()).digest()).decode()

def verifypass(passwd: str, hash: str) -> bool:
    hashbts = base64.decodebytes(hash.encode())
    return hashbts[256:] == hashlib.sha256(hashbts[:256] + passwd.encode()).digest()

@agent.on_message(model=ReqCreateAccount)  #, replies=ResCreateAccount)
async def create_account(ctx: Context, sender: str, msg: ReqCreateAccount):
    try:
        ctx.logger.info("Identity Agent Create Account")
        ctx.logger.info(f"\t{sender}")
        ctx.logger.info(f"\t{msg}")
        pid: int | None = None
        with psycopg.connect(environ["PGSQL_CONSTR"], row_factory=dict_row) as connection:
            er = connection.execute("INSERT INTO Patients (name, password) VALUES (%s, %s) RETURNING id;", (msg.name, hashpass(msg.password)))
            for row in er:
                pid = int(row["id"])
        if pid is None:
            raise ValueError("")
        await ctx.send(sender, ResCreateAccount(token=Token(pid).to_str(), status="ok"))
        return
    except Exception as e:
        raise e
        ctx.logger.error("CreateAccount Failed")
        await ctx.send(sender, ResCreateAccount(token=Token(0).to_str(), status="ok"))

@agent.on_message(model=ReqSignIn)
async def sign_in(ctx: Context, sender: str, msg: ReqSignIn):
    print("Identity Agent Sign In")
    print("\t",sender)
    print("\t",msg)
    with psycopg.connect(environ["PGSQL_CONSTR"], row_factory=dict_row) as connection:
        er = connection.execute("SELECT password FROM Patients WHERE name = %s;", (msg.name,))
        pswd: bytes | None = None
        for row in er:
            pswd = row["password"]
        if pswd is None or not verifypass(msg.password, pswd):
            await ctx.send(sender, ResSignIn(token="", status="credentials rejected"))
            return
        await ctx.send(sender, ResSignIn(token=f"{msg.name}", status="ok"))
        return

@agent.on_message(model=ReqAddProvider)
async def add_providers(ctx: Context, sender: str, msg: ReqAddProvider):
    print("Identity Agent Add Providers")
    print("\t",sender)
    print("\t",msg)
    with psycopg.connect(environ["PGSQL_CONSTR"]) as connection:
        connection.execute("INSERT INTO PatientProviders (patient_id, provider_id) SELECT %s, id FROM Provider WHERE name = ANY(%s);", (msg.providers,))
        await ctx.send(sender, ResAddProvider(token=msg.token, status="ok"))

@agent.on_message(model=ReqNameToken)
async def name_from_token(ctx: Context, sender: str, msg: ReqNameToken):
    print("Identity Agent Name Token")
    print("\t",sender)
    print("\t",msg)
    name: str | None = None
    with psycopg.connect(environ["PGSQL_CONSTR"]) as connection:
        er = connection.execute("SELECT name FROM Patients WHERE id = %s;", (Token.from_str(msg.token).patient_id,))
        for row in er:
            name = str(row["name"])
    if name is None:
        raise ValueError()
    await ctx.send(sender, ResNameToken(token=msg.token, name=name, status="ok"))
    return

if __name__ == "__main__":
    print("Identity Agent Address:", agent.address)
    agent.run()
