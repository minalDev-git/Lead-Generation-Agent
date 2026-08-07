# Leads Generation Agent

An intelligent automation tool designed to discover, extract, and compile business leads from online directories and map services using natural language prompts.

By simply inputting a conversational search query (such as "coffee shops in America"), the agent automates browser navigation, parses relevant business listings, handles missing data gracefully, and exports the gathered information into a clean, organized Excel spreadsheet for immediate use.

## Agent Architecture & ReAct Loop

The agent uses a ReAct-style loop to alternate between reasoning and tool execution. It asks the LLM to return only structured JSON actions, either calling a tool or returning a final answer. The loop continues until the task is complete.

Implemented in:

- `backend/app/agent/chat.py` — ReAct loop and tool orchestration
- `backend/app/agent/prompt.py` — system prompt with tool instructions, valid JSON action formats, and workflow rules
- `backend/app/agent/tool_registry.py` — tool registration, tool schemas, and handler lookup
- `backend/app/agent/llm.py` — LLM interface that returns JSON actions for each reasoning step

Tool implementations currently include:

- `backend/app/tools/scraper.py` — searches and scrapes business leads
- the Excel export tool defined via `backend/app/agent/tool_registry.py` for saving data to `.xlsx`

## How It Works

The Leads Generation Agent automates the entire process of discovering and compiling business leads from a simple natural-language prompt. The workflow is structured into three main phases:

### 1. Prompt Processing & Intent Extraction

**Natural Language Input:** The user provides a descriptive prompt specifying the target audience and geographic location (e.g., "coffee shops in America").

**Entity Extraction:** The agent parses the prompt to accurately isolate and identify two core components:

- Business Category (e.g., "coffee shops")
- Target Location (e.g., "America")

### 2. Browser Automation & Lead Scraping

**Automated Navigation:** Utilizing a browser automation tool, the agent navigates to business listing and map platforms (such as Google Maps or Bing Maps).

**Targeted Search:** It dynamically enters the extracted business category and location into the platform's search bar.

**Data Extraction:** The agent iterates through the search results, collecting multiple leads and capturing vital details for each business:

- Business Name
- Email Address
- Phone Number
- Website Link
- Location / Address

**Fault Tolerance:** If specific information (like an email or phone number) is unavailable for a listing, the agent gracefully leaves the field blank and continues execution without crashing.

### 3. Data Export & Execution Summary

**Structured Storage:** All successfully gathered leads are compiled and saved into a structured Excel (.xlsx) file.

**Meaningful Naming:** The file is automatically saved with a descriptive filename tailored to the search (e.g., `leads_coffee_shops_america.xlsx`).

**Terminal Reporting:** Upon completion, a clear execution summary is printed directly to the terminal, detailing the search query used and the total number of leads successfully collected and saved.

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
cd /home/user/Desktop/python/aiseason/session_4/LeadsGenerationAgent/backend
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` and configure the following variables:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Browser Automation
BROWSER_TYPE=chromium
HEADLESS_MODE=true

# Output Configuration
EXCEL_OUTPUT_DIR=./outputs
```

**Environment Variables Explanation:**

| Variable           | Description                                        | Example     |
| ------------------ | -------------------------------------------------- | ----------- |
| `OPENAI_API_KEY`   | Your OpenAI API key for LLM                        | `sk-...`    |
| `BROWSER_TYPE`     | Browser for automation (chromium, firefox, webkit) | `chromium`  |
| `HEADLESS_MODE`    | Run browser in headless mode (true/false)          | `true`      |
| `EXCEL_OUTPUT_DIR` | Directory to save Excel files                      | `./outputs` |

## Running the Agent

### Start the CLI Agent

```bash
python -m app.main
```

### Example Interaction

```
You: Find me 10 coffee shops in New York
⏳ Processing scrape_leads...
Agent: I've found 10 coffee shops in New York and saved them to leads_coffee_shops_new_york.xlsx

You: quit
Bye
```

## Providing a Search Prompt

The agent accepts natural language queries. Format your prompt as follows:

**Basic Format:**

```
[Business Type] in [Location]
```

**Examples:**

- "pizza restaurants in Los Angeles"
- "software development companies in London"
- "dentists near San Francisco"
- "hotels in Tokyo"

The agent will automatically extract the business category and location, then scrape relevant leads.

## Locating Generated Excel Files

### Output Directory

All generated Excel files are saved to: `./outputs/`

### File Naming Convention

Files are named descriptively based on your search:

```
leads_[business_type]_[location].xlsx
```

**Examples:**

- `leads_coffee_shops_new_york.xlsx`
- `leads_pizza_restaurants_los_angeles.xlsx`
- `leads_software_companies_london.xlsx`

### Access Generated Files

```bash
# List all generated files
ls -la outputs/

# Open specific file (on Linux)
libreoffice outputs/leads_coffee_shops_new_york.xlsx
```

## Project Structure

```
backend/
├── app/
│   ├── agent/
│   │   ├── chat.py           # CLI chat loop
│   │   ├── llm.py            # LLM integration
│   │   ├── memory.py         # Conversation history
│   │   ├── prompt.py         # System prompts
│   │   └── tool_registry.py  # Tool handlers
│   ├── tools/
│   │   └── scraper.py        # Web scraping logic
│   └── main.py               # FastAPI app & CLI entry
├── .env.example              # Environment variables template
├── .env                       # Environment variables (create from .env.example)
├── requirements.txt          # Python dependencies
├── outputs/                  # Generated Excel files
└── README.md                 # This file
```

## Troubleshooting

### "asyncio.run() cannot be called from a running event loop"

Ensure you're running the CLI directly:

```bash
python -m app.main
```

### Missing API Key

Check that `OPENAI_API_KEY` is set in `.env`:

```bash
echo $OPENAI_API_KEY
```

### No Excel Files Generated

Verify the `outputs/` directory exists:

```bash
mkdir -p outputs/
```

### Browser Automation Issues

Ensure browser dependencies are installed:

```bash
pip install playwright
playwright install chromium
```

## Dependencies

Key dependencies (see `requirements.txt`):

- `langchain-groq` - LLM
- `pydantic` - Data validation
- `openai` - LLM API
- `playwright` - Browser automation
- `openpyxl` - Excel file generation
- `python-dotenv` - Environment configuration

## License

This project is provided as-is for educational purposes.
