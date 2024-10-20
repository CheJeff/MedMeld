from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
# from ..identity import ReqCreateAccount, ResCreateAccount, ReqNameToken, ReqAddProvider
ia_addr = "agent1qvt36c3f90rmp2v2ycw8z6hmgcz3pjk66pvxksgmecspdel2pz9hzakrmgq"

class ReqCreateAccount(Model):
    name: str
    password: str

class ResCreateAccount(Model):
    token: str
    status: str


agent = Agent(
    seed = "Test Agent",
    name = "Test Agent",
    port = 8005,
    endpoint = ["http://127.0.0.1:8005/submit"]
)

fund_agent_if_low(agent.wallet.address())  # type: ignore

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Test Agent Sending Message")
    await ctx.send(ia_addr, ReqCreateAccount(name="Steve Rogers", password="IamCaptain4."))

@agent.on_message(model=ResCreateAccount)
async def account_created(ctx: Context, sender: str, msg: ResCreateAccount):
    ctx.logger.info("Test Agent Recieved Message: CreateAccount")
    ctx.logger.info(f"\tstatus: {msg.status}")
    ctx.logger.info(f"\ttoken : {msg.token}")


if __name__ == "__main__":
    agent.run()

