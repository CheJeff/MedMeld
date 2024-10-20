from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from messages import *
ia_addr = "agent1qvt36c3f90rmp2v2ycw8z6hmgcz3pjk66pvxksgmecspdel2pz9hzakrmgq"

agent = Agent(
    seed = "Test Agent",
    name = "Test Agent",
    port = 8005,
    endpoint = ["http://127.0.0.1:8005/submit"]
)

fund_agent_if_low(agent.wallet.address())  # type: ignore

async def run_test_stage(ctx: Context):
    stage = ctx.storage.get("stage")
    if stage == "signin":
        ctx.logger.info("Signing In")
        await ctx.send(ia_addr, ReqSignIn(name="Jone Doe", password="hello"))
    elif stage == "add":
        ctx.logger.info("Adding Provider")
        await ctx.send(ia_addr, ReqAddProvider(token=ctx.storage.get("token"), providers=["Health Primary"]))
    else:
        raise ValueError()

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Starting Tests")
    ctx.storage.set("stage", "signin")
    await run_test_stage(ctx)

@agent.on_message(model=ResSignIn)
async def signed_in(ctx: Context, sender: str, msg: ResSignIn):
    ctx.logger.info("Recieved Message: SignIn")
    ctx.logger.info(f"\tstatus: {msg.status}")
    ctx.logger.info(f"\ttoken : {msg.token}")
    ctx.storage.set("token", msg.token)
    ctx.storage.set("stage", "add")
    await run_test_stage(ctx)

@agent.on_message(model=ResAddProvider)
async def provider_added(ctx: Context, sender: str, msg: ResAddProvider):
    ctx.logger.info("Recieved Message: AddProviders")
    ctx.logger.info(f"\tstatus: {msg.status}")
    ctx.logger.info(f"\ttoken : {msg.token}")
    ctx.storage.set("token", msg.token)



if __name__ == "__main__":
    agent.run()

