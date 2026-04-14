#!/usr/bin/env python3
"""
Quick test of the Travel Agent components (without LLM)
Run this to verify search_flights() and intent detection work correctly
"""

import sys
sys.path.insert(0, '/workspaces/Travel-Agent')

from travel_agent import search_flights, detect_flight_search, format_flights_for_display

print("=" * 60)
print("TRAVEL AGENT - COMPONENT TEST")
print("=" * 60)

# Test 1: Search for NYC to LAX flights
print("\n[TEST 1] Search NYC → LAX flights")
print("-" * 60)
results = search_flights("NYC", "LAX")
print(format_flights_for_display(results))

# Test 2: Search for LAX to NYC flights  
print("\n[TEST 2] Search LAX → NYC flights")
print("-" * 60)
results = search_flights("LAX", "NYC")
print(format_flights_for_display(results))

# Test 3: Search for non-existent route
print("\n[TEST 3] Search for non-existent route (NYC → SFO)")
print("-" * 60)
results = search_flights("NYC", "SFO")
print(format_flights_for_display(results))

# Test 4: Intent detection - flight question
print("\n[TEST 4] Intent Detection - 'Find me flights from NYC to LAX'")
print("-" * 60)
is_flight, params = detect_flight_search("Find me flights from NYC to LAX")
print(f"Is flight query: {is_flight}")
print(f"Search params: {params}")

# Test 5: Intent detection - non-flight question
print("\n[TEST 5] Intent Detection - 'What's the weather today?'")
print("-" * 60)
is_flight, params = detect_flight_search("What's the weather today?")
print(f"Is flight query: {is_flight}")
print(f"Search params: {params}")

# Test 6: Intent detection - natural language
print("\n[TEST 6] Intent Detection - 'I want to fly from LAX to MIA'")
print("-" * 60)
is_flight, params = detect_flight_search("I want to fly from LAX to MIA")
print(f"Is flight query: {is_flight}")
print(f"Search params: {params}")

print("\n" + "=" * 60)
print("✅ All component tests completed!")
print("=" * 60)
