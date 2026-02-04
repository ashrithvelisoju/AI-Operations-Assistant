# AI Operations Assistant

An AI-powered operations assistant that accepts natural-language tasks, plans steps, calls tools (APIs), and returns structured answers. Built with a multi-agent architecture using Gemini 3 Flash.

## 🏗️ Architecture

```
ai_ops_assistant/
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py    # Converts user input into step-by-step plan
│   ├── executor_agent.py   # Executes steps and calls APIs
│   └── verifier_agent.py   # Validates results and synthesizes output
├── tools/
│   ├── __init__.py
│   ├── weather_tool.py     # OpenWeatherMap API integration
│   └── news_tool.py        # NewsAPI.org integration
├── llm/
│   ├── __init__.py
│   └── gemini_client.py    # Gemini 3 Flash LLM client
├── main.py                 # Main orchestrator
├── streamlit_app.py        # Streamlit UI
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

## 🤖 Multi-Agent System

### Planner Agent
- Analyzes user requests
- Creates structured execution plans
- Selects appropriate tools for each step

### Executor Agent
- Executes plan steps sequentially
- Calls external APIs (Weather, News)
- Handles tool execution and error recovery

### Verifier Agent
- Validates execution results
- Identifies missing or incorrect information
- Synthesizes final response for user

## 🛠️ Tools

### Weather Tool
- **API:** OpenWeatherMap
- **Capabilities:** Current weather data for any city
- **Data:** Temperature, humidity, wind speed, conditions

### News Tool
- **API:** NewsAPI.org
- **Capabilities:** Search news by topic or get top headlines
- **Data:** Article title, source, description, URL

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Streamlit UI
```bash
streamlit run streamlit_app.py --server.port 8501
```

### 3. Run Streamlit UI
```bash
streamlit run streamlit_app.py --server.port 8501
```

### 4. Or Use CLI
```bash
python main.py "What is the weather in London?"
```

## 📋 Example Tasks

- "What's the weather in New York?"
- "Get me the latest technology news"
- "Weather in Tokyo and top headlines"
- "Compare weather in London and Paris"

## ⚙️ Configuration

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key |
| `WEATHER_API_KEY` | OpenWeatherMap API key |
| `NEWS_API_KEY` | NewsAPI.org API key |
| `MONGO_URL` | MongoDB connection string |

## 🔧 LLM Integration

Uses **Gemini 3 Flash** 
- Natural language understanding
- Plan generation with structured JSON output
- Reasoning steps without tool calls
- Result verification and synthesis

## 📊 Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Agent Design | 25% |
| LLM Usage | 20% |
| API Integration | 20% |
| Code Clarity | 15% |
| Working Demo | 10% |
| Documentation | 10% |

## 📝 License

MIT License
