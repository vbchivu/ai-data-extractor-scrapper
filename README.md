
# AI-Enhanced Program Data Extractor PoC

## Overview

This project is a Proof-of-Concept (PoC) demonstrating an approach to automatically extracting structured information (like tuition fees, application deadlines, and entry requirements) from university program webpages.

It simulates a workflow relevant to Studyportals' goal of enhancing study data collection through automation and AI. The core idea is to scrape relevant text content and then use a (currently mocked) AI component (like an LLM) to parse this unstructured text into a predefined structured format (JSON).

This PoC aims to showcase skills in:

* Python programming
* Web scraping (`requests`, `BeautifulSoup`)
* Understanding data structuring (JSON)
* Conceptualizing AI/LLM integration for data extraction
* Command-line interface design (`argparse`)
* Proactive thinking about automation challenges in data collection

**Disclaimer:** This is a simplified PoC and is **not** production-ready. It uses a *mocked* AI component and basic scraping techniques.

## Features

* Scrapes HTML content from a given university program URL.
* Extracts relevant text blocks from the page.
* Simulates (mocks) using an LLM to extract predefined structured data points (program name, university, fee, deadline, requirements) from the text.
* Provides a command-line interface (CLI) to specify the target URL, university name, and an optional output file.
* Outputs the extracted structured data as JSON to the console.
* Optionally saves the JSON output to a specified file.

## Technology Stack

* Python 3 (tested on 3.8+, requires >= 3.8 for `typing.Optional`)
* Libraries:
  * `requests`: For fetching web page content.
  * `beautifulsoup4`: For parsing HTML content.
  * `argparse`: For handling command-line arguments.
  * Standard libraries: `json`, `logging`, `typing`, `re`

## Setup

1. **Prerequisites:**
    * Python 3.8 or higher installed.
    * `pip` (Python package installer).

2. **Get the Code:**
    * Clone this repository or download the source code files (`main.py`, `scraper.py`, `llm_extractor.py`).

3. **Install Dependencies:**
    * Navigate to the project directory in your terminal.
    * Create a `requirements.txt` file (if not already present) with the following content:

        ```txt
        requests
        beautifulsoup4
        ```

    * Install the required libraries:

        ```bash
        pip install -r requirements.txt
        ```

## Usage

Run the main script from your terminal using `python3 main.py`.

**Arguments:**

* `--url URL`: (Required) The full URL of the university program page to scrape.
* `--university UNIVERSITY`: (Optional) The name of the university. Defaults to "University specified by user".
* `--output FILEPATH`: (Optional) Path to a file where the extracted JSON data should be saved.

**Examples:**

1. **Scrape a URL and print to console:**

    ```bash
    python3 main.py --url "YOUR_TARGET_PROGRAM_URL"
    ```

2. **Scrape, specify university, and print:**

    ```bash
    python3 main.py --url "YOUR_TARGET_PROGRAM_URL" --university "Example University Name"
    ```

3. **Scrape, specify university, and save output to a file:**

    ```bash
    python3 main.py --url "YOUR_TARGET_PROGRAM_URL" --university "Example University Name" --output program_data.json
    ```

4. **Scrape a specific UvA program page and save output:**

    ```bash
    python3 main.py --url "https://web.archive.org/web/20240314085048/https://www.uva.nl/en/programmes/masters/information-studies/information-studies.html" --university "University of Amsterdam" --output program_data.json
    ```

## Project Structure

.
├── main.py           # Main orchestrator script, handles CLI args  
├── scraper.py        # Module for fetching and parsing webpage HTML  
├── llm_extractor.py  # Module with the mocked AI data extraction logic  
└── README.md         # This documentation file  
└── requirements.txt  # List of Python dependencies (You need to create this)

## How it Works

1. `main.py` parses the command-line arguments (`url`, `university`, `output`).
2. It calls the `scrape_program_page` function in `scraper.py`.
3. `scraper.py` uses `requests` to fetch the HTML from the target URL and `BeautifulSoup` to parse it. It attempts to find the main content area and extracts the raw text.
4. If scraping is successful, `main.py` passes the raw text and university name to the `extract_structured_data_mocked` function in `llm_extractor.py`.
5. `llm_extractor.py` *simulates* an LLM call by performing basic keyword searches on the raw text to find indicators for tuition fees, deadlines, and requirements. It populates a dictionary based on these findings using predefined mock strings.
6. `main.py` receives the structured dictionary (JSON) back from the mock extractor.
7. The resulting JSON is printed to the console.
8. If an `--output` file was specified, the JSON data is also saved to that file.

## Limitations

* **Mocked AI:** The core extraction logic does *not* use a real Language Model. It relies on simple keyword spotting, which is not robust or accurate for real-world variable text.
* **Scraper Fragility:** The HTML selectors in `scraper.py` are likely specific to the example UvA page structure. They will break if the website layout changes or if used on different university sites. Real-world scraping requires more robust and adaptable selectors.
* **Limited Scope:** Only extracts a few predefined fields.
* **Basic Error Handling:** Error handling is minimal; many edge cases are not covered.
* **No Database:** Extracted data is only printed or saved to a file, not stored in a structured database like PostgreSQL.
* **No Change Detection:** The script only performs a one-time extraction.
* **Not Production-Ready:** This PoC lacks the robustness, scalability, monitoring, and testing required for production use.

## Future Enhancements & Proactive Ideas (Relevant for Studyportals)

This PoC provides a foundation. Here's how it could be evolved into a more robust solution, aligning with Studyportals' goals:

1. **Real LLM Integration:**
    * Replace the mock function in `llm_extractor.py` with actual calls to an LLM API.
    * Develop effective **prompt engineering** strategies.
    * Implement secure **API key management**.
    * Monitor **costs** and **rate limits**.
    * Consider **Retrieval-Augmented Generation (RAG)** if needing to combine LLM reasoning with verified internal data.

2. **Robust & Scalable Scraping:**
    * Utilize more advanced scraping frameworks like **Scrapy**.
    * Implement robust **CSS/XPath selectors**.
    * Handle **JavaScript-rendered content** using tools like Selenium or Playwright.
    * Incorporate **politeness measures** and **anti-scraping countermeasures**.

3. **Structured Data Storage:**
    * Integrate with a **PostgreSQL database**.
    * Define a proper schema and use an ORM like SQLAlchemy or `psycopg2`.

4. **Change Detection & Monitoring:**
    * Store previous scrapes.
    * Compare new scrapes to detect changes.
    * Set up **monitoring and alerting**.

5. **Cloud Deployment & Scalability (AWS):**
    * Deploy via **AWS Lambda**, store files in **Amazon S3**, manage tasks via **SQS**, and orchestrate with **Step Functions**.

6. **Workflow Optimization & Orchestration:**
    * Use **Apache Airflow** or **AWS Step Functions**.

7. **Testing & Validation:**
    * Add **unit and integration tests**.
    * Validate extracted data quality.

8. **UI/Dashboard:**
    * Create a dashboard using **Flask**, **Django**, or **Streamlit**.

By addressing these areas, this PoC could evolve into a robust system that aligns with Studyportals' automation and scalability goals.
