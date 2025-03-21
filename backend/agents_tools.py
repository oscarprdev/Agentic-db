from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace

reader_agent = Agent(
    name="Reader",
    instructions=(
        "You are an database reader agent that will read the database."
        "Say hello to the user."
    ),
)

writer_agent = Agent(
    name="Writer",
    instructions=(
        "You are an database writer agent that will write to the database."
        "Say bye to the user."
    ),
)

orchestrator_agent = Agent(
    name="Orchestrator",
    instructions=(
        "You are an databaseorchestrator agent that will orchestrate the other agents."
        "You will be given a message from the user about the database."
        "you always use the provided tools."
    ),
    tools=[reader_agent.as_tool(
        tool_name="reader",
        tool_description="You are an database reader agent that will read the database."
    ), writer_agent.as_tool(
        tool_name="writer",
        tool_description="You are an database writer agent that will write to the database."
    )],
)

async def main(msg):
    with trace(orchestrator_agent):
        return await Runner.run(orchestrator_agent, msg)

