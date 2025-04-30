# AI-Enhanced Program Data Extractor PoC

## Overview

This project is a Proof-of-Concept (PoC) demonstrating an approach to automatically extracting structured information (like tuition fees, application deadlines, and entry requirements) from university program webpages.

It implements a workflow relevant to Studyportals' goal of enhancing study data collection through automation and AI. The core idea is to scrape relevant text content and then use an AI component (LLM) to parse this unstructured text into a predefined structured format (JSON).

This version allows using either:

* A **mock extractor** (simulating AI with keyword spotting).
* A **real LLM running locally via Ollama** (interacting through its OpenAI-compatible API).

This PoC aims to showcase skills in:

* Python programming
* Web scraping (`requests`, `BeautifulSoup`)
* Understanding data structuring (JSON)
* Implementing and conceptualizing AI/LLM integration (OpenAI library, local Ollama)
* Command-line interface design (`argparse`)
* Secure configuration management (`dotenv`)
* Proactive thinking about automation challenges in data collection

**Disclaimer:** This is a simplified PoC and is **not** production-ready. The scraping is fragile, and while it can use a real local LLM via Ollama, the accuracy depends heavily on the chosen model and prompt engineering.

## Features

* Scrapes HTML content from a given university program URL.
* Extracts relevant text blocks from the page.
* Provides two extraction methods selectable via CLI:
  * **Mock:** Simulates LLM extraction using keyword spotting.
  * **Ollama:** Uses a locally running LLM via Ollama (OpenAI-compatible API) for actual data extraction, attempting to enforce JSON output.
* Provides a command-line interface (CLI) to specify the target URL, university name, extractor type, and an optional output file.
* Outputs the extracted structured data as JSON to the console.
* Optionally saves the JSON output to a specified file.

## Technology Stack

* Python 3 (tested on 3.8+, requires >= 3.8 for `typing.Optional`)
* **Libraries:**
  * `requests`: For fetching web page content.
  * `beautifulsoup4`: For parsing HTML content.
  * `openai`: For interacting with the Ollama server (OpenAI-compatible API).
  * `python-dotenv`: For managing environment variables (e.g., Ollama configuration).
  * `argparse`: For handling command-line arguments.
  * Standard libraries: `json`, `logging`, `typing`, `re`, `os`
* **External Tools:**
  * `Ollama`: Required for running the local LLM (Needs separate installation).

## Setup

1. **Prerequisites:**
    * Python 3.8 or higher installed.
    * `pip` (Python package installer).
    * **Ollama Installed:** Download and install Ollama from [https://ollama.com/](https://ollama.com/) and ensure it's running.

2. **Download an Ollama Model:**
    * Pull a model suitable for instruction following and JSON output. `llama3:8b` is recommended. Open your terminal and run:

        ```bash
        ollama pull llama3:8b
        ```

3. **Get the Code:**
    * Clone this repository or download the source code files (`main.py`, `scraper.py`, `llm_extractor.py`).

4. **Configure Environment Variables:**
    * Create a file named `.env` in the project's root directory.
    * Add the following lines, adjusting `OLLAMA_MODEL` if you pulled a different model:

        ```dotenv
        OLLAMA_BASE_URL="http://localhost:11434/v1"
        OLLAMA_MODEL="llama3:8b"
        ```

5. **Install Python Dependencies:**
    * Navigate to the project directory in your terminal.
    * *(Optional but recommended)* Create and activate a virtual environment:

        ```bash
        python3 -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
        ```

    * Ensure your `requirements.txt` file has the following content:

        ```txt
        requests
        beautifulsoup4
        openai
        python-dotenv
        ```

    * Install the required libraries:

        ```bash
        pip install -r requirements.txt
        ```

## Usage

Run the main script from your terminal using `python3 main.py`.

**Arguments:**

* `--url URL`: (Required) The full URL of the university program page to scrape.
* `--university UNIVERSITY`: (Optional) The name of the university.
* `--extractor {mock,ollama}`: (Optional) Choose the extraction method.
* `--output FILEPATH`: (Optional) Path to a file where the extracted JSON data should be saved.

**Examples:**

```bash
python3 main.py --url "YOUR_TARGET_PROGRAM_URL"
python3 main.py --url "YOUR_TARGET_PROGRAM_URL" --extractor ollama
python3 main.py --url "YOUR_TARGET_PROGRAM_URL" --university "Example University Name" --extractor ollama --output program_data_ollama.json
python3 main.py --url "https://web.archive.org/web/20240314085048/https://www.uva.nl/en/programmes/masters/information-studies/information-studies.html" --university "University of Amsterdam" --extractor ollama --output uva_is_ollama.json
```

## Project Structure

```
.
├── main.py           # Main orchestrator script
├── scraper.py        # Fetch and parse HTML
├── llm_extractor.py  # Mock and Ollama extraction logic
├── .env              # Ollama configuration (secret)
├── requirements.txt  # Python dependencies
├── README.md         # Documentation
└── .gitignore        # Should ignore .env
```

## How it Works

1. `main.py` parses CLI arguments.
2. Calls `scrape_program_page` in `scraper.py`.
3. Depending on extractor, calls `extract_structured_data_mocked` or `extract_structured_data_ollama`.
4. The extractor returns structured JSON.
5. Prints or optionally saves the JSON.

## Limitations

* **LLM Dependency:** Ollama must be running, and model pulled.
* **Scraper Fragility:** Selectors are basic and site-specific.
* **Limited Scope:** Only extracts a few fields.
* **No DB or Persistence.**
* **Not Production-Ready.**

## Future Enhancements

1. Retry logic, better prompts, API flexibility, fine-tuning
2. More robust scraping
3. Add structured storage (PostgreSQL)
4. Add change detection and monitoring
5. Deploy to AWS (Lambda, S3, etc.)
6. Add orchestration (Airflow)
7. Add tests
8. Build a dashboard (Flask or Streamlit)

## requirements.txt Confirmation

```txt
requests
beautifulsoup4
openai
python-dotenv
```

## Code Files Confirmation

Ensure `main.py`, `llm_extractor.py`, and `scraper.py` match the latest version with Ollama logic.
