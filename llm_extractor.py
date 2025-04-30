# llm_extractor.py
import logging
import re
import json
from typing import Dict, Any

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the target schema structure we expect
TARGET_SCHEMA = {
    "program_name": "string",
    "university_name": "string",
    "tuition_fee": "string",
    "application_deadline": "string",
    "entry_requirement_summary": "string",
}


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
    # A real LLM would understand context better.
    # Try to find a plausible title-like string early in the text
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
    # Also look for month names which often appear near deadlines
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

    logging.info(
        f"Mocked extraction complete. Data: {json.dumps(extracted_data, indent=2)}"
    )
    return extracted_data


# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    # Sample raw text (simulating output from scraper.py)
    sample_text = """
    Welcome to the Master's Programme in Information Studies at the University of Amsterdam!
    This program dives deep into data science and systems.
    Application deadline is 1 March for non-EU students. The tuition fee is approximately EUR 18,720 per year for non-EU.
    Admission requirements include a relevant Bachelor's degree and proof of English proficiency like IELTS score 6.5.
    Explore the curriculum and apply now! Costs may vary. Check eligibility criteria carefully. Apply by May 1st if EU student.
    """

    print("--- Testing Mock LLM Extractor ---")
    # Use the specific university name for our example
    mock_result = extract_structured_data_mocked(
        sample_text, university_name="University of Amsterdam"
    )

    print("\n--- Mock Extracted Data ---")
    print(json.dumps(mock_result, indent=2))
    print("---------------------------")

    print("\n--- Testing with Empty Text ---")
    mock_result_empty = extract_structured_data_mocked(
        "", university_name="University of Amsterdam"
    )
    print(json.dumps(mock_result_empty, indent=2))
    print("----------------------------")
