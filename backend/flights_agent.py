from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace, function_tool
from flights_api import GETFlightsRequest, Flight, get_flights_api_call
from search_agent import run as search_agent_run, AnswerFormat, Suggestion
import json

def get_flights(origin: str, destination: str, departure_date: str, return_date: str, non_stop: bool, adults: int, max_price: int):
    print("[debug] get_flights called", origin, destination, departure_date, return_date, non_stop, adults, max_price)
    return get_flights_api_call(GETFlightsRequest(origin, destination, departure_date, return_date, non_stop, adults, max_price))

@function_tool
def get_flights_from_msg(msg: str) -> AnswerFormat:
    answer = search_agent_run(msg)
    print("[debug] answer", answer)
    return answer

flights_agent = Agent(
    name="Flights",
    instructions=(
        "You are an flights agent that will find the best flights for the user."
        "You will be given a message from the user about the flights."
        "you always use the provided tools."
    ),
    tools=[get_flights_from_msg]
)

format_agent = Agent(
    name="Format",
    instructions=(
        "You are an format agent that will format the flights for the user."
        "You will be given a message from the user about the flights."
        "you always use the provided tools."
        "Extract the origin, destination, departure date, return date, non stop, adults, max price from the message."
    ),
)

async def run(msg):
    with trace(flights_agent):
        agent_result = await Runner.run(flights_agent, msg)
        flights = agent_result.final_output
        print("[debug] flights", flights)

        return flights
        # with trace(format_agent):
        #     return await Runner.run(format_agent, str(flights))

        # suggestion = flights[0]

        # return await get_flights(suggestion.origin, suggestion.destination, suggestion.departure_date, suggestion.return_date, suggestion.non_stop, suggestion.adults, suggestion.max_price)