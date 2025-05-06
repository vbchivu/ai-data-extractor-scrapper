# llm_extractor.py
import logging
import re
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, RateLimitError, APIStatusError

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

# --- Target Schema Definition ---
TARGET_SCHEMA = {
    "program_name": "string",
    "university_name": "string",
    "tuition_fee": "string",
    "application_deadline": "string",
    "entry_requirement_summary": "string",
}

# --- Prompt Templates ---
SYSTEM_PROMPT_TEMPLATE = """
You are an expert assistant specialized in extracting structured information from university program webpages.
Your task is to analyze the provided text and extract information matching the fields in the following JSON schema.
You MUST respond ONLY with a single, valid JSON object containing the extracted data.
Do NOT include any explanations, markdown formatting (like ```json), or introductory/concluding text outside the JSON object itself.
If a specific piece of information cannot be found in the text, use the exact string "Not found" as the value for that field in the JSON output.

JSON Schema:
{schema_json_string}
"""

USER_PROMPT_TEMPLATE = """
Analyze the following text scraped from the webpage of "{university_name}" and extract the required information based on the schema provided in the system prompt.

Webpage Text:
\"\"\"
{raw_text}
\"\"\"

Respond ONLY with the valid JSON object:
"""


# --- Mock Function ---
def extract_structured_data_mocked(
    raw_text: str, university_name: str = "University specified elsewhere"
) -> Dict[str, Any]:
    """MOCK FUNCTION: Simulates extracting structured data..."""
    logging.info("Starting mocked LLM data extraction.")
    extracted_data = {key: "Not found" for key in TARGET_SCHEMA}
    extracted_data["university_name"] = university_name
    text_lower = raw_text.lower() if raw_text else ""

    # Mock Logic using keyword spotting
    match = re.search(
        r"(master(?:.s)?\s*(?:programme|program)?\s*in\s*[\w\s]+)", text_lower
    )
    if match:
        potential_name = " ".join(word.capitalize() for word in match.group(1).split())
        extracted_data["program_name"] = f"Mock Program: {potential_name}"
    elif "information studies" in text_lower:
        extracted_data["program_name"] = "Mock Program: Information Studies"
    else:
        extracted_data["program_name"] = "Mock Program: Check official page title"

    fee_keywords = ["tuition", "fee", "cost", "€", "eur", "usd", "$", "gbp", "£"]
    if any(keyword in text_lower for keyword in fee_keywords):
        extracted_data["tuition_fee"] = (
            "Mock Fee: Approx. €XX,XXX / year (Non-EU). Verify on official page."
        )

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

    logging.info(f"Mocked extraction complete.")
    return extracted_data


# --- Ollama LLM Extraction Function ---
def extract_structured_data_ollama(
    raw_text: str, university_name: str = "University specified elsewhere"
) -> Optional[Dict[str, Any]]:
    """
    Uses a locally running Ollama model (via OpenAI compatible API) to extract structured data.
    Refactored prompts, attempts JSON mode, includes robust parsing and validation.

    Args:
        raw_text: The raw text content scraped from the webpage.
        university_name: The name of the university.

    Returns:
        A dictionary containing the extracted data conforming to TARGET_SCHEMA,
        or None if extraction fails.
    """
    logging.info(
        "Attempting structured data extraction using Ollama (Synced & Refactored)."
    )

    # 1. Get Ollama configuration
    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    ollama_model = os.getenv("OLLAMA_MODEL")
    if not ollama_base_url or not ollama_model:
        logging.error(
            "Ollama base URL or model not configured in environment variables (.env file)."
        )
        return None

    # 2. Initialize OpenAI client
    try:
        client = OpenAI(base_url=ollama_base_url, api_key="ollama")
        logging.info(f"Initialized OpenAI client for Ollama at {ollama_base_url}")
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client: {e}")
        return None

    # 3. Format Prompts using Templates
    try:
        schema_json_string = json.dumps(TARGET_SCHEMA, indent=2)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            schema_json_string=schema_json_string
        )
        user_prompt = USER_PROMPT_TEMPLATE.format(
            university_name=university_name, raw_text=raw_text
        )
    except KeyError as e:
        logging.error(f"Failed to format prompt template. Missing key: {e}")
        return None

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # 4. Make the API Call - Attempting JSON Mode
    try:
        logging.info(
            f"Sending request to Ollama model: {ollama_model} (attempting JSON mode)"
        )
        response = client.chat.completions.create(
            model=ollama_model,
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},  # Attempt to force JSON output
        )
        raw_response_content = response.choices[0].message.content
        logging.info("Received response from Ollama (JSON mode attempted).")
        logging.debug(f"Raw Ollama response content:\n{raw_response_content}")

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
        # Check if the error indicates JSON mode is unsupported
        err_content = str(e.response.content).lower()
        if (
            "json_object type is not supported" in err_content
            or "response_format" in err_content
        ):
            logging.warning(
                f"Ollama model '{ollama_model}' or server version might not support JSON mode. Consider updating Ollama/model or removing 'response_format'. Error: {e}"
            )
            # Potentially retry without JSON mode here if needed, but for PoC we'll fail.
        else:
            logging.error(
                f"Ollama API error: Status Code={e.status_code}, Response={e.response}"
            )
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during Ollama API call: {e}")
        return None

    # 5. Robust Parsing and Validation
    try:
        logging.debug("Attempting to parse LLM response as JSON.")
        # Attempt to strip markdown fences first, as models might still add them even with JSON mode
        match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```", raw_response_content, re.DOTALL
        )
        if match:
            logging.debug("Found JSON within markdown fences. Extracting.")
            json_str = match.group(1)
        else:
            # Otherwise, assume the whole string is the JSON (after stripping whitespace)
            json_str = raw_response_content.strip()

        extracted_data = json.loads(json_str)

        if not isinstance(extracted_data, dict):
            logging.error(
                f"LLM response parsed, but is not a dictionary (Type: {type(extracted_data)}). Response: {json_str}"
            )
            return None

        # Validate keys and fill missing ones
        validated_data = {}
        missing_keys = []
        extra_keys = []

        # Check for expected keys
        for key in TARGET_SCHEMA:
            if key in extracted_data:
                validated_data[key] = extracted_data[key]
            else:
                validated_data[key] = "Not found (missing in LLM output)"
                missing_keys.append(key)

        # Check for unexpected extra keys
        for key in extracted_data:
            if key not in TARGET_SCHEMA:
                extra_keys.append(key)
                # Optionally include extra keys if desired:
                # validated_data[key] = extracted_data[key]

        if missing_keys:
            logging.warning(
                f"Ollama response JSON was missing expected keys: {missing_keys}. Filled with 'Not found'."
            )
        if extra_keys:
            logging.warning(
                f"Ollama response JSON included unexpected extra keys: {extra_keys}."
            )

        logging.info("Successfully parsed and validated JSON response from Ollama.")
        return validated_data

    except json.JSONDecodeError as json_err:
        logging.error(f"Failed to parse JSON response from Ollama: {json_err}")
        logging.error(f"LLM Raw Response content was:\n{raw_response_content}")
        return None
    except Exception as e:
        logging.error(f"Error during JSON parsing/validation: {e}")
        return None


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Testing Mock LLM Extractor ---")
    sample_text_mock = "..."
    mock_result = extract_structured_data_mocked(
        sample_text_mock, university_name="Mock University"
    )
    # print(json.dumps(mock_result, indent=2))

    print("\n--- Testing Ollama LLM Extractor ---")
    # Make sure Ollama server is running with the model specified in .env
    sample_text_ollama = """
    Master's Programme: Advanced Web Systems at Test University
    Duration: 2 years. Apply by 1 April for international students. Deadline is June 1st for EU.
    Tuition fees are EUR 20,000 per annum for non-EU/EEA nationals. EU students pay EUR 2,500.
    Entry requirements: A solid Bachelor's degree in Computer Science or related field. English B2 level needed. IELTS 7.0 overall required.
    Contact admissions for details.
    """
    ollama_result = extract_structured_data_ollama(
        sample_text_ollama, university_name="Test University"
    )

    if ollama_result:
        print("\n--- Ollama Extracted Data (Parsed & Validated) ---")
        print(json.dumps(ollama_result, indent=2))
        print("-------------------------------------------------")
    else:
        print("\n--- Ollama Extraction Failed ---")
        print(
            "Check logs, ensure Ollama server is running, model in .env is pulled & compatible."
        )
