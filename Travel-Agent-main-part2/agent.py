import os
import json
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
MOCK_API_BASE = os.getenv("MOCK_API_BASE", "http://localhost:8000")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")  # or gpt-4o, claude, etc.

client = OpenAI(api_key=OPENAI_API_KEY)

# ============================================================
# TOOL SCHEMA
# ============================================================
SEARCH_FLIGHTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "Search for available flights between two airports on a specific date. Use this when the user asks about flights, travel, or airfare.",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Origin airport code or city (e.g., 'NYC', 'LAX', 'JFK')"
                },
                "destination": {
                    "type": "string",
                    "description": "Destination airport code or city (e.g., 'LAX', 'NYC', 'SFO')"
                },
                "date": {
                    "type": "string",
                    "description": "Flight date in YYYY-MM-DD format"
                }
            },
            "required": ["origin", "destination", "date"]
        }
    }
}

TOOLS = [SEARCH_FLIGHTS_TOOL]

# ============================================================
# TOOL EXECUTION
# ============================================================
def execute_search_flights(origin: str, destination: str, date: str) -> dict:
    """Call the mock flight API."""
    try:
        response = httpx.get(
            f"{MOCK_API_BASE}/flights",
            params={"origin": origin, "destination": destination, "date": date},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        
        # Format for LLM consumption
        flights = data.get("flights", [])
        if not flights:
            return {"status": "no_results", "message": f"No flights found from {origin} to {destination} on {date}."}
        
        formatted = []
        for i, f in enumerate(flights, 1):
            dep = f["departure_time"].split("T")[1][:5]
            arr = f["arrival_time"].split("T")[1][:5]
            formatted.append({
                "option_number": i,
                "flight_id": f["flight_id"],
                "airline": f["airline"],
                "flight_number": f["flight_number"],
                "departure": dep,
                "arrival": arr,
                "duration_hours": f["duration_hours"],
                "price_usd": f["price_usd"],
                "available_seats": f["available_seats"]
            })
        
        return {
            "status": "success",
            "search_summary": f"Found {len(flights)} flights from {origin} to {destination} on {date}.",
            "flights": formatted
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_tool(tool_name: str, tool_args: dict) -> dict:
    """Route tool calls to the appropriate handler."""
    if tool_name == "search_flights":
        return execute_search_flights(**tool_args)
    return {"status": "error", "message": f"Unknown tool: {tool_name}"}

# ============================================================
# TOOL-CALLING LOOP
# ============================================================
def run_agent(user_input: str, conversation_history: list = None) -> tuple[str, list]:
    """
    Run the agent with tool-calling loop.
    Returns: (final_response, updated_conversation_history)
    """
    if conversation_history is None:
        system_prompt = """You are a helpful travel agent assistant. Your job is to help users find and book domestic direct flights.

When the user asks about flights, you MUST use the search_flights tool to look up real flight data.

After showing flight options, if the user selects one, ask for their full name to complete the booking. Then return a structured booking confirmation including:
- Passenger name
- Flight details (airline, flight number, departure/arrival times, date)
- Price paid

Keep responses concise but friendly. Only search for domestic direct flights."""
        
        conversation_history = [
            {"role": "system", "content": system_prompt}
        ]
    
    # Add user message
    conversation_history.append({"role": "user", "content": user_input})
    
    # Tool-calling loop
    max_iterations = 5
    for iteration in range(max_iterations):
        # Call LLM with tools
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=conversation_history,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        # Check if LLM wants to call a tool
        if message.tool_calls:
            # Append assistant's tool call request to history
            conversation_history.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in message.tool_calls
                ]
            })
            
            # Execute each tool call and append results
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Tool Call: {tool_name}({json.dumps(tool_args)})")
                
                result = execute_tool(tool_name, tool_args)
                
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })
            
            # Loop back to LLM with tool results
            continue
        
        # No tool calls — we have the final response
        conversation_history.append({
            "role": "assistant",
            "content": message.content
        })
        return message.content, conversation_history
    
    return "I apologize, but I got stuck in a loop. Please try again.", conversation_history

# ============================================================
# INTERACTIVE MODE
# ============================================================
def main():
    print("=" * 60)
    print("✈️  Travel Agent — Part 2 (Tool-Calling Edition)")
    print("=" * 60)
    print("Type 'quit' to exit.\n")
    
    history = None
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Agent: Thank you for using our service! Safe travels! ✈️")
            break
        
        if not user_input:
            continue
        
        response, history = run_agent(user_input, history)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()