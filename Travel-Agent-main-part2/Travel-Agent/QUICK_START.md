# Quick Start Guide

## 30-Second Setup

### 1. Get API Key
- Go to https://platform.openai.com/api-keys
- Sign up or log in
- Create a new API key
- Copy it

### 2. Set Up Environment
```bash
# Create .env from example
cp .env.example .env

# Edit .env and paste your API key
# OPENAI_API_KEY=sk-...your-key-here...
```

### 3. Run the Agent
```bash
source venv/bin/activate  # macOS/Linux
python travel_agent.py
```

## Example Conversation

```
You: Find flights from NYC to LAX
Assistant: I found 5 flights from New York to Los Angeles. The cheapest option is Southwest at $175 with a departure at 6:30 AM on June 2nd...

You: What about return flights?
Assistant: For return flights from LAX to NYC, I have 3 options ranging from $189 to $260...

You: Show me the Delta flight details
Assistant: The Delta flight departs LAX on June 6th at 8:30 AM and arrives in NYC at 4:45 PM, priced at $260...

You: exit
Assistant: Thank you for using the Travel Agent! Have a great trip!
```

## Test Without API Key

Run the component test to verify everything works:
```bash
python test_components.py
```

This tests flight search and intent detection without needing an API key.

## Troubleshooting

**Error: OPENAI_API_KEY not found**
- Create `.env` file from `.env.example`
- Add your API key: `OPENAI_API_KEY=sk-...`
- Restart the script

**Error: Invalid API key**
- Check your key at https://platform.openai.com/api-keys
- Make sure there are no extra spaces in `.env`

**No flights found**
- Try these city codes: NYC, LAX, SFO, MIA
- Example: "flights from NYC to LAX"
