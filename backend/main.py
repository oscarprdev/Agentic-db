from fastapi import FastAPI
from pydantic import BaseModel
import search_agent
import flights_agent
from search_agent import AnswerFormat
from flights_api import get_flights_api_call, GETFlightsRequest
import json
import re

app = FastAPI()

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    message: str

@app.post("/chat", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    search_result = search_agent.run(request.message)
    print("[debug] search_result", search_result)
    
    # Extract the JSON content from the string that contains markdown code block
    json_match = re.search(r'```json\s*(.*?)\s*```', search_result, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
        # Parse the JSON string into a Python dictionary
        parsed_data = json.loads(json_str)
        
        # Now you can access suggestions
        suggestions = parsed_data.get('suggestions', [])
        print(f"[debug] Found {len(suggestions)} suggestions")
        
        all_flight_results = []
        
        if suggestions:
            # Loop through all suggestions
            for i, suggestion in enumerate(suggestions):
                print(f"[debug] Processing suggestion {i+1}:", suggestion)
                    
                try:                    
                    suggestion_mapped = GETFlightsRequest(
                        origin=suggestion['departureAirport'],
                        destination=suggestion['arrivalAirport'],
                        departure_date=suggestion['departureDate'],
                        return_date=suggestion['returnDate'],
                        adults=1,
                    )
                    
                    # Call flights API with the mapped suggestion
                    flights_result = get_flights_api_call(suggestion_mapped)
                    print("[debug] flights_result", flights_result)
                    
                    all_flight_results.append(flights_result)
                except Exception as e:
                    print(f"[error] Failed to process suggestion {i+1}: {str(e)}")
                    # Add error info to results
                    all_flight_results.append({
                        "error": str(e)
                    })
            
            # Return all results as a JSON array
            return MessageResponse(message=json.dumps({
                "original_query": request.message,
                "results": all_flight_results,
            }))
    
    # Return the original search result if parsing fails or no suggestions found
    return MessageResponse(
        message=search_result,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 