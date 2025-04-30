# llm_extractor.py
import logging
import re
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIConnectionError,
    RateLimitError,
    APIStatusError,
)

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Load Environment Variables ---
load_dotenv()

# Define the target schema structure we expect
TARGET_SCHEMA = {
    "program_name": "string",
    "university_name": "string",
    "tuition_fee": "string",
    "application_deadline": "string",
    "entry_requirement_summary": "string",
}

# --- Mock Function
def extract_structured_data_mocked(
    raw_text: str, university_name: str = "University specified elsewhere"
) -> Dict[str, Any]:
    """
    MOCK FUNCTION: Simulates extracting structured data from raw text using an LLM.
    Uses simple keyword searching to provide plausible mock data.

    Args:
        raw_text: The raw text content scraped from the webpage.
        university_name: The name of the university (can be passed in or hardcoded).

    Returns:
        A dictionary containing the 'extracted' data, conforming to TARGET_SCHEMA.
    """
    logging.info("Starting mocked LLM data extraction.")
    extracted_data = {key: "Not found" for key in TARGET_SCHEMA}
    extracted_data["university_name"] = university_name  # Use provided name

    # Convert raw_text to lower case for case-insensitive matching
    text_lower = raw_text.lower() if raw_text else ""

    # --- Mock Logic using keyword spotting ---

    # 1. Program Name (Very basic mock: try finding common header patterns or default)
    match = re.search(
        r"(master(?:.s)?\s*(?:programme|program)?\s*in\s*[\w\s]+)", text_lower
    )
    if match:
        # Basic cleaning: capitalize words, strip extra spaces
        potential_name = " ".join(word.capitalize() for word in match.group(1).split())
        extracted_data["program_name"] = f"Mock Program: {potential_name}"
    elif "information studies" in text_lower:  # Fallback specific to our example
        extracted_data["program_name"] = "Mock Program: Information Studies"
    else:
        extracted_data["program_name"] = "Mock Program: Check official page title"

    # 2. Tuition Fee
    fee_keywords = ["tuition", "fee", "cost", "€", "eur", "usd", "$", "gbp", "£"]
    if any(keyword in text_lower for keyword in fee_keywords):
        extracted_data["tuition_fee"] = (
            "Mock Fee: Approx. €XX,XXX / year (Non-EU). Verify on official page."
        )
        logging.info("Found keywords suggesting tuition fee information.")
    else:
        logging.info("No clear keywords found for tuition fee.")

    # 3. Application Deadline
    deadline_keywords = ["deadline", "apply by", "application period", "closes on"]
    month_names = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    if any(keyword in text_lower for keyword in deadline_keywords) or any(
        month in text_lower for month in month_names
    ):
        extracted_data["application_deadline"] = (
            "Mock Deadline: e.g., 1 March (Non-EU) / 1 May (EU). Verify on official page."
        )
        logging.info("Found keywords suggesting application deadline information.")
    else:
        logging.info("No clear keywords found for application deadline.")

    # 4. Entry Requirements
    req_keywords = [
        "requirement",
        "admission",
        "entry",
        "eligibility",
        "qualification",
        "prerequisite",
        "ielts",
        "toefl",
    ]
    if any(keyword in text_lower for keyword in req_keywords):
        extracted_data["entry_requirement_summary"] = (
            "Mock Requirements: Typically Bachelor's degree + English proficiency (e.g., IELTS/TOEFL). Check specifics on official page."
        )
        logging.info("Found keywords suggesting entry requirement information.")
    else:
        logging.info("No clear keywords found for entry requirements.")

    logging.info(f"Mocked extraction complete.")
    return extracted_data

# Ollama LLM Extraction ---
def extract_structured_data_ollama(
    raw_text: str, university_name: str = "University specified elsewhere"
) -> Optional[Dict[str, Any]]:
    """
    Uses a locally running Ollama model (via OpenAI compatible API) to extract structured data.

    Args:
        raw_text: The raw text content scraped from the webpage.
        university_name: The name of the university.

    Returns:
        A dictionary containing the extracted data conforming to TARGET_SCHEMA,
        or None if extraction fails.
    """
    logging.info("Attempting structured data extraction using Ollama.")

    # 1. Get Ollama configuration from environment variables
    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    ollama_model = os.getenv("OLLAMA_MODEL")

    if not ollama_base_url or not ollama_model:
        logging.error(
            "Ollama base URL or model not configured in environment variables (.env file)."
        )
        return None

    # 2. Initialize OpenAI client to point to Ollama server
    try:
        client = OpenAI(
            base_url=ollama_base_url,
            api_key="ollama",  # Required by library, ignored by Ollama server
        )
        logging.info(f"Initialized OpenAI client for Ollama at {ollama_base_url}")
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client: {e}")
        return None

    # 3. Construct the Prompt
    schema_json_string = json.dumps(TARGET_SCHEMA, indent=2)
    system_prompt = (
        "You are an expert assistant specialized in extracting structured information from "
        "university program webpages. Your task is to extract the information according to "
        "the following JSON schema. Respond ONLY with the JSON object containing the "
        "extracted data. Do not include any explanations or introductory text. If a value "
        'cannot be found in the text, use the string "Not found".\n\n'
        f"Schema:\n```json\n{schema_json_string}\n```"
    )
    user_prompt = (
        f"Please extract the information from the following text extracted from the webpage "
        f'for the university "{university_name}".\n\n'
        f"Webpage Text:\n{raw_text}\n\n"
        f"Respond only with the JSON object:"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # 4. Make the API Call to Ollama
    try:
        logging.info(f"Sending request to Ollama model: {ollama_model}")
        response = client.chat.completions.create(
            model=ollama_model,
            messages=messages,
            temperature=0.1,
        )

        raw_response_content = response.choices[0].message.content
        logging.info("Received response from Ollama.")
        logging.debug(f"Raw Ollama response content: {raw_response_content}")

        # --- Attempt basic JSON parsing ---
        try:
            match = re.search(
                r"```json\s*(\{.*?\})\s*```", raw_response_content, re.DOTALL
            )
            json_str = match.group(1) if match else raw_response_content.strip()

            extracted_data = json.loads(json_str)
            if isinstance(extracted_data, dict) and all(
                key in extracted_data for key in TARGET_SCHEMA
            ):
                logging.info("Successfully parsed JSON response matching schema keys.")
                return extracted_data
            elif isinstance(extracted_data, dict):
                logging.warning(
                    "Parsed JSON but missing some schema keys; filling with placeholders."
                )
                for key in TARGET_SCHEMA:
                    extracted_data.setdefault(key, "Not found (parsing)")
                return extracted_data
            else:
                logging.error(f"Parsed content is not a dict: {type(extracted_data)}")
                return None

        except json.JSONDecodeError as json_err:
            logging.error(f"Failed to parse JSON response: {json_err}")
            logging.error(f"LLM Raw Response was: {raw_response_content}")
            return None

    except APIConnectionError as e:
        logging.error(f"Failed to connect to Ollama server at {ollama_base_url}: {e}")
        print(
            f"\nERROR: Could not connect to Ollama server at {ollama_base_url}. Is Ollama running?"
        )
        return None
    except RateLimitError as e:
        logging.error(f"Rate limit error (unexpected with local Ollama): {e}")
        return None
    except APIStatusError as e:
        logging.error(
            f"Ollama API error: Status Code={e.status_code}, Response={e.response}"
        )
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during Ollama API call: {e}")
        return None

if __name__ == '__main__':
    # Ensure Ollama server is running and you have pulled a model (e.g., llama3:8b)
    print("--- Testing Mock LLM Extractor ---")
    sample_text_mock = """
    Welcome to the Mock Master's Programme. Deadline is soon. Requirements are tough. Fee is high.
    """
    mock_result = extract_structured_data_mocked(sample_text_mock, university_name="Mock University")
    print("Mock Result (for comparison):")
    print(json.dumps(mock_result, indent=2))

    print("\n--- Testing Ollama LLM Extractor ---")
    # Make sure Ollama server is running with the model specified in .env
    sample_text_ollama = """
    Master's Programme: Advanced Web Systems at Test University
    Duration: 2 years. Apply by 1 April for international students. Deadline is June 1st for EU.
    Tuition fees are EUR 20,000 per annum for non-EU/EEA nationals. EU students pay EUR 2,500.
    Entry requirements: A solid Bachelor's degree in Computer Science or related field. English B2 level needed. IELTS 7.0 overall required.
    Contact admissions for details.
    """
    ollama_result = extract_structured_data_ollama(sample_text_ollama, university_name="Test University")

    if ollama_result:
        print("\n--- Ollama Extracted Data (Attempted Parse) ---")
        print(json.dumps(ollama_result, indent=2))
        print("---------------------------------------------")
    else:
        print("\n--- Ollama Extraction Failed ---")
        print("Check logs, ensure Ollama server is running, model in .env is pulled & compatible.")