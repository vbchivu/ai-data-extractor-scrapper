# main.py
import json
import logging
import argparse
from typing import Optional, Dict, Any
# --- Import necessary functions ---
from scraper import scrape_program_page
# Import both extractor functions
from llm_extractor import (
    extract_structured_data_mocked,
    extract_structured_data_ollama
)
# --- --- --- --- --- --- --- ---

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [Main] %(message)s')

# --- Updated Pipeline Function ---
def run_extraction_pipeline(url: str, university: str, extractor_type: str) -> Optional[Dict[str, Any]]:
    """
    Runs the full pipeline: scrape -> extract (using specified method).

    Args:
        url: The target URL to scrape.
        university: The name of the university.
        extractor_type: The type of extractor to use ('mock' or 'ollama').

    Returns:
        A dictionary with the extracted structured data, or None if pipeline fails.
    """
    logging.info(f"Starting extraction pipeline for URL: {url} using '{extractor_type}' extractor.")

    # Step 1: Scrape the webpage (remains the same)
    raw_text = scrape_program_page(url)
    if not raw_text:
        logging.error("Scraping failed or returned no text. Aborting pipeline.")
        return None
    logging.info(f"Scraping successful (extracted {len(raw_text)} chars).")

    # Step 2: Extract structured data using the selected method
    structured_data: Optional[Dict[str, Any]] = None
    if extractor_type == 'ollama':
        logging.info("Using Ollama extractor.")
        structured_data = extract_structured_data_ollama(raw_text, university_name=university)
    elif extractor_type == 'mock':
        logging.info("Using Mock extractor.")
        structured_data = extract_structured_data_mocked(raw_text, university_name=university)
    else:
        # This case should be prevented by argparse 'choices'
        logging.error(f"Invalid extractor type specified: {extractor_type}")
        return None

    # Step 3: Check result and return
    if not structured_data:
        logging.error(f"Extractor '{extractor_type}' failed to produce data.")
        return None

    logging.info(f"Extractor '{extractor_type}' successful.")
    return structured_data
# --- --- --- --- --- --- --- ---


# --- Main execution ---
if __name__ == '__main__':
    logging.info("="*30)
    logging.info(" Starting AI-Enhanced Program Data Extractor PoC ")
    logging.info("="*30)

    # --- Argument Parsing (Updated) ---vvv
    parser = argparse.ArgumentParser(description='Scrape a university program page and extract structured data using Mock or Ollama LLM.')
    parser.add_argument('--url', type=str, required=True,
                        help='The full URL of the university program page to scrape.')
    parser.add_argument('--university', type=str, default="University specified by user",
                        help='The name of the university (optional).')
    # --- NEW ARGUMENT ---
    parser.add_argument('--extractor', type=str, default='mock', choices=['mock', 'ollama'],
                        help='Choose the extraction method: "mock" (default) or "ollama" (requires running Ollama server).')
    # --- -------------- ---
    parser.add_argument('--output', type=str, default=None,
                        help='Optional file path to save the extracted JSON data.')

    args = parser.parse_args()
    logging.info(f"Running with arguments: URL='{args.url}', University='{args.university}', Extractor='{args.extractor}', Output file='{args.output}'")
    # --- Argument Parsing (Updated) ---^^^


    # Execute the pipeline using arguments, including the extractor type
    result_data = run_extraction_pipeline(args.url, args.university, args.extractor)

    # Display the result (remains the same)
    if result_data:
        print(f"\n--- Final Extracted Data (Using: {args.extractor}) ---")
        print(json.dumps(result_data, indent=2))
        print("-------------------------------------------------")

        # Save to File (remains the same)
        if args.output:
            logging.info(f"Attempting to save output to file: {args.output}")
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result_data, f, indent=2, ensure_ascii=False)
                logging.info(f"Successfully saved output to {args.output}")
            except IOError as e:
                logging.error(f"Failed to write output to file {args.output}: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred while writing to file {args.output}: {e}")

    else:
        print("\n--- Extraction Pipeline Failed ---")
        logging.warning("Pipeline finished without extracting data. Check logs.")

    logging.info("="*30)
    logging.info(" Execution Finished ")
    logging.info("="*30)