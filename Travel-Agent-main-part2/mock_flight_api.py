from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime, timedelta
import random

app = FastAPI(title="Mock Flight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AIRLINES = ["Delta", "American Airlines", "United", "Southwest", "JetBlue"]
FLIGHT_NUMBERS = [f"{random.randint(100, 9999)}" for _ in range(50)]

MOCK_FLIGHTS_DB = {}

def generate_flight_id():
    return f"FL{random.randint(10000, 99999)}"

def get_mock_flights(origin: str, destination: str, date: str):
    """Generate realistic mock flight data."""
    cache_key = f"{origin}-{destination}-{date}"
    
    if cache_key in MOCK_FLIGHTS_DB:
        return MOCK_FLIGHTS_DB[cache_key]
    
    # Seed random for consistent results per route/date
    seed = hash(cache_key) % (2**32)
    random.seed(seed)
    
    num_flights = random.randint(3, 6)
    flights = []
    base_date = datetime.strptime(date, "%Y-%m-%d")
    
    for i in range(num_flights):
        airline = random.choice(AIRLINES)
        flight_num = f"{airline[:2].upper()}{random.randint(100, 9999)}"
        departure = base_date + timedelta(hours=random.randint(5, 22), minutes=random.choice([0, 15, 30, 45]))
        duration_hours = random.randint(2, 6) + random.choice([0, 0.5])
        arrival = departure + timedelta(hours=duration_hours)
        price = random.randint(150, 800)
        
        flights.append({
            "flight_id": generate_flight_id(),
            "airline": airline,
            "flight_number": flight_num,
            "origin": origin.upper(),
            "destination": destination.upper(),
            "departure_time": departure.isoformat(),
            "arrival_time": arrival.isoformat(),
            "price_usd": price,
            "duration_hours": duration_hours,
            "available_seats": random.randint(5, 50)
        })
    
    # Sort by price
    flights.sort(key=lambda x: x["price_usd"])
    MOCK_FLIGHTS_DB[cache_key] = flights
    return flights

@app.get("/flights")
def search_flights(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    date: str = Query(..., description="Flight date (YYYY-MM-DD)")
):
    flights = get_mock_flights(origin, destination, date)
    return {
        "search_params": {"origin": origin, "destination": destination, "date": date},
        "results_count": len(flights),
        "flights": flights
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "mock-flight-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)