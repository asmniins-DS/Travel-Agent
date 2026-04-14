# Travel Agent - Part 1

A simple AI-powered travel agent that helps users search for flights and discuss travel options using mock flight data and an LLM (Large Language Model).

## 🎯 Project Overview

This is a **Part 1** project demonstrating a conversational travel agent that:
- ✅ Searches mock flight data based on user queries
- ✅ Uses OpenAI's GPT API for natural conversations
- ✅ Maintains conversation history for context-aware responses
- ✅ Detects flight search intent and injects data into prompts
- ❌ Does NOT use real flight APIs, function calling, or complex features

## 📋 Features

- **Mock Flight Database**: 10 pre-populated flights across multiple routes
- **Intelligent Flight Detection**: Parses user messages to extract origin/destination
- **Conversation History**: Maintains message context for multi-turn conversations
- **Simple Architecture**: No complex routing, databases, or external APIs
- **Terminal-Based UI**: Easy-to-use command-line interface

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- OpenAI API key (get one at https://platform.openai.com/api-keys)

### 2. Environment Setup

```bash
# Clone or navigate to the project
cd Travel-Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install openai python-dotenv
```

### 3. Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-...your-key-here...
```

⚠️ **Important**: Never commit your `.env` file to version control!

### 4. Run the Agent

```bash
python travel_agent.py
```

## 💬 Usage Examples

Once the script is running, try these queries:

```
You: Find me flights from NYC to LAX
Assistant: [Lists available flights and provides recommendations]

You: What's the cheapest flight to Los Angeles?
Assistant: [Shows budget options and highlights the best deals]

You: Tell me about the Southwest flight
Assistant: [Provides details about Southwest flights]

You: When are the flights from NYC to LAX?
Assistant: [Lists departure times and dates]

You: Exit
Assistant: Thank you for using the Travel Agent! Have a great trip!
```

## 📁 Project Structure

```
Travel-Agent/
├── travel_agent.py       # Main agent script
├── .env.example          # Example environment configuration
├── .gitignore            # Git ignore file
├── README.md             # This file
└── venv/                 # Virtual environment (auto-created)
```

## 🔧 How It Works

### Architecture Flow

```
User Input
    ↓
Detect Flight Intent (origin + destination)
    ↓
    ├─→ If flight query detected → search_flights()
    │                                     ↓
    │                            Get matching flights
    │                                     ↓
    │                            Format results
    │                                     ↓
    │                            Inject into user message
    │
    ├─→ Add to message history
    │
    ↓
Call OpenAI API with full conversation context
    ↓
Display Assistant Response
    ↓
Add to conversation history
    ↓
Loop back for next input
```

### Key Functions

#### `search_flights(origin, destination, date=None)`
- Filters mock flight database by origin and destination
- Optional date filtering
- Returns list of matching flight dictionaries

#### `detect_flight_search(user_message)`
- Analyzes user input for flight-related keywords
- Extracts origin and destination city codes
- Returns search parameters if flight query detected

#### `format_flights_for_display(flights)`
- Converts flight data to readable string format
- Shows flight ID, airline, date, time, and price
- Used when injecting flight results into LLM context

#### `run_agent()`
- Main conversation loop
- Handles user input and exit commands
- Manages message history for conversation context
- Calls OpenAI API and prints responses

## 📊 Mock Flight Data

The database includes 10 flights across these routes:
- **NYC ↔ LAX** (6 flights)
- **SFO → MIA** (2 flights)

Flights include: ID, origin, destination, date, price, airline, departure, and arrival times.

## ⚙️ Configuration

### Model Used
- **Model**: `gpt-3.5-turbo` (efficient and cost-effective)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 500 (suitable for conversational responses)

### Supported City Codes
- NYC (New York City)
- LAX (Los Angeles)
- SFO (San Francisco)
- MIA (Miami)

## 🎓 Learning Points

This project demonstrates:
1. **LLM Integration**: Using OpenAI's API in Python
2. **Conversation Management**: Maintaining message history
3. **Intent Detection**: Simple pattern matching for user queries
4. **Context Injection**: Adding data to prompts dynamically
5. **Error Handling**: Graceful API failure management

## 📝 Part 1 Constraints (Intentional Simplifications)

| Feature | Status | Why |
|---------|--------|-----|
| Real Flight APIs | ❌ Not implemented | Using mock data for simplicity |
| Function Calling | ❌ Not implemented | Data injected manually into prompts |
| RAG/Vector DB | ❌ Not implemented | Small dataset doesn't require it |
| Hotels/Cars | ❌ Not implemented | Flights only for Part 1 |
| User Accounts | ❌ Not implemented | In-memory state sufficient |
| Database | ❌ Not implemented | Mock Python list is enough |

## 🔐 Security Notes

- Never share your API key
- Never commit `.env` to version control
- Keep your API key secret in your environment
- Delete or rotate keys if accidentally exposed

## 💡 Tips for Testing

1. **Test flight search**: "Find flights from NYC to LAX"
2. **Test price comparison**: "Which flight is cheapest?"
3. **Test conversation context**: First ask about flights, then ask follow-up questions
4. **Test exit**: Type "exit", "quit", or "bye"
5. **Test invalid routes**: Ask about flights that don't exist in the database

## 🤖 LLM Enhancement Ideas (Future Parts)

- Implement function calling with OpenAI API
- Add hotel and rental car services
- Connect to real flight APIs (Skyscanner, Kayak)
- Add user accounts and booking history
- Implement RAG for detailed flight information
- Add voice input/output
- Multi-language support

## 📚 References

- [OpenAI Python API Reference](https://platform.openai.com/docs/api-reference)
- [Chat Completions API](https://platform.openai.com/docs/guides/gpt)
- [Environment Variables in Python](https://docs.python.org/3/library/os.html)

## 📄 License

This project is provided as-is for educational purposes.