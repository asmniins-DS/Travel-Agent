#!/usr/bin/env python3
"""
Simple AI Travel Agent - Part 1
Searches and discusses flights using mock data with LLM assistance
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client (will be created in run_agent if API key exists)
client = None

# Mock flight data
MOCK_FLIGHTS = [
    {"id": 1, "origin": "NYC", "destination": "LAX", "date": "2025-06-01", "price": 199, "airline": "Delta", "departure": "08:00", "arrival": "11:30"},
    {"id": 2, "origin": "NYC", "destination": "LAX", "date": "2025-06-01", "price": 250, "airline": "United", "departure": "10:00", "arrival": "13:45"},
    {"id": 3, "origin": "NYC", "destination": "LAX", "date": "2025-06-02", "price": 175, "airline": "Southwest", "departure": "06:30", "arrival": "10:15"},
    {"id": 4, "origin": "NYC", "destination": "LAX", "date": "2025-06-02", "price": 280, "airline": "American", "departure": "14:00", "arrival": "17:30"},
    {"id": 5, "origin": "NYC", "destination": "LAX", "date": "2025-06-03", "price": 220, "airline": "JetBlue", "departure": "07:15", "arrival": "10:45"},
    {"id": 6, "origin": "LAX", "destination": "NYC", "date": "2025-06-05", "price": 220, "airline": "American", "departure": "09:00", "arrival": "17:30"},
    {"id": 7, "origin": "LAX", "destination": "NYC", "date": "2025-06-05", "price": 189, "airline": "Southwest", "departure": "12:00", "arrival": "20:15"},
    {"id": 8, "origin": "LAX", "destination": "NYC", "date": "2025-06-06", "price": 260, "airline": "Delta", "departure": "08:30", "arrival": "16:45"},
    {"id": 9, "origin": "SFO", "destination": "MIA", "date": "2025-07-01", "price": 310, "airline": "United", "departure": "11:00", "arrival": "19:30"},
    {"id": 10, "origin": "SFO", "destination": "MIA", "date": "2025-07-02", "price": 285, "airline": "JetBlue", "departure": "10:30", "arrival": "19:00"},
]

def search_flights(origin: str, destination: str, date: str = None) -> list:
    """
    Search for flights matching the given criteria.
    
    Args:
        origin: City code (e.g., 'NYC')
        destination: City code (e.g., 'LAX')
        date: Optional date in format 'YYYY-MM-DD'
    
    Returns:
        List of matching flight dictionaries
    """
    results = []
    origin = origin.upper().strip()
    destination = destination.upper().strip()
    
    for flight in MOCK_FLIGHTS:
        # Check origin and destination
        if flight["origin"].upper() != origin or flight["destination"].upper() != destination:
            continue
        
        # Check date if provided
        if date and flight["date"] != date:
            continue
        
        results.append(flight)
    
    return results

def detect_flight_search(user_message: str) -> tuple[bool, dict]:
    """
    Detect if user is asking about flights and extract parameters.
    Uses simple keyword matching for Part 1.
    
    Returns:
        Tuple of (is_flight_query, search_params)
    """
    message_lower = user_message.lower()
    
    # Keywords that indicate a flight search
    flight_keywords = ["flight", "flights", "fly", "flying", "travel", "trip", "from", "to", "cheapest", "price", "airline"]
    
    # Check if message contains flight-related keywords
    if not any(keyword in message_lower for keyword in flight_keywords):
        return False, {}
    
    # Simple extraction of origin and destination
    search_params = {"origin": None, "destination": None, "date": None}
    
    # Look for common city pairs in the message
    words = message_lower.split()
    
    # Find "from" or detect origin cities
    city_codes = ["nyc", "lax", "sfo", "mia"]
    for word in words:
        if word.strip(",.!?") in city_codes:
            if search_params["origin"] is None:
                search_params["origin"] = word.strip(",.!?").upper()
            elif search_params["destination"] is None:
                search_params["destination"] = word.strip(",.!?").upper()
    
    # Return True only if we found both origin and destination
    if search_params["origin"] and search_params["destination"]:
        return True, search_params
    
    return False, {}

def format_flights_for_display(flights: list) -> str:
    """Format flight data as a readable string."""
    if not flights:
        return "No flights found matching your criteria."
    
    output = f"Found {len(flights)} flight(s):\n\n"
    for flight in flights:
        output += (
            f"Flight {flight['id']}: {flight['airline']}\n"
            f"  Date: {flight['date']} | {flight['departure']} → {flight['arrival']}\n"
            f"  Price: ${flight['price']}\n"
            f"  Route: {flight['origin']} → {flight['destination']}\n\n"
        )
    return output

def run_agent():
    """
    Main conversation loop for the travel agent.
    """
    # Initialize OpenAI client
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key to .env")
        print("  3. Run the script again")
        return
    
    client = OpenAI(api_key=api_key)
    
    print("=" * 60)
    print("Welcome to the AI Travel Agent!")
    print("Ask me about flights, prices, airlines, and travel options.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("=" * 60)
    print()
    
    # System prompt for the LLM
    system_prompt = """
You are a helpful travel agent assistant. Your role is to help users find flights and discuss travel options.
You have access to a database of flights and can help users:
- Search for flights between cities
- Compare prices and airlines
- Discuss travel dates and options
- Answer questions about flights

When flight results are provided to you, summarize them in a friendly way and help the user choose the best option.
Keep responses concise and helpful.
"""
    
    messages = [{"role": "system", "content": system_prompt}]
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nAssistant: Thank you for using the Travel Agent! Have a great trip!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Check if user is asking about flights
            is_flight_query, search_params = detect_flight_search(user_input)
            flight_results = ""
            
            if is_flight_query and search_params["origin"] and search_params["destination"]:
                flights = search_flights(
                    search_params["origin"],
                    search_params["destination"],
                    search_params.get("date")
                )
                flight_results = format_flights_for_display(flights)
                
                # Add flight data to the context
                user_input += f"\n\n[FLIGHT SEARCH RESULTS:\n{flight_results}]"
            
            # Add user message to conversation
            messages.append({"role": "user", "content": user_input})
            
            # Call LLM API
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Using gpt-3.5-turbo for cost efficiency
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                assistant_message = response.choices[0].message.content
                
                # Add assistant response to conversation history
                messages.append({"role": "assistant", "content": assistant_message})
                
                # Print the response
                print(f"\nAssistant: {assistant_message}")
                
            except Exception as api_error:
                print(f"\nError communicating with LLM: {api_error}")
                print("Make sure your OPENAI_API_KEY is set correctly in the .env file")
                # Remove the user message since we couldn't get a response
                messages.pop()
        
        except KeyboardInterrupt:
            print("\n\nAssistant: Goodbye! Thank you for using the Travel Agent.")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    run_agent()
