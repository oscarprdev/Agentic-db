from fastapi import FastAPI
from pydantic import BaseModel
import agents_tools

app = FastAPI()

class MessageRequest(BaseModel):
    message: str
    session_id: str = None

class MessageResponse(BaseModel):
    message: str
    agent: str = None
    response_data: dict = None

@app.post("/chat", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    result = await agents_tools.main(request.message)
    
    response_text = result.final_output
    agent_name = result.current_agent.name if hasattr(result, 'current_agent') else "Orchestrator"
    
    return MessageResponse(
        message=response_text,
        agent=agent_name,
        response_data=result.to_dict() if hasattr(result, 'to_dict') else {}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 