# main.py
import json
import logging
import argparse  # <--- ADD THIS IMPORT
from typing import Optional, Dict, Any
from scraper import scrape_program_page
from llm_extractor import extract_structured_data_mocked

# Configure basic logging for the main script
# Set level to DEBUG to see more info, or keep INFO for less verbosity
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - [Main] %(message)s"
)


# --- Function Definition (Remains the same) ---
def run_extraction_pipeline(url: str, university: str) -> Optional[Dict[str, Any]]:
    """
    Runs the full pipeline: scrape -> extract (mocked).

    Args:
        url: The target URL to scrape.
        university: The name of the university.

    Returns:
        A dictionary with the extracted structured data, or None if pipeline fails.
    """
    logging.info(f"Starting extraction pipeline for URL: {url}")
    raw_text = scrape_program_page(url)
    if not raw_text:
        logging.error("Scraping failed or returned no text. Aborting pipeline.")
        return None
    logging.info("Scraping successful. Proceeding to mock LLM extraction.")
    structured_data = extract_structured_data_mocked(
        raw_text, university_name=university
    )
    if not structured_data:
        logging.error("Mocked extraction failed to produce data.")
        return None
    logging.info("Mocked extraction successful.")
    return structured_data


# --- Main execution ---
if __name__ == "__main__":
    logging.info("=" * 30)
    logging.info(" Starting AI-Enhanced Program Data Extractor PoC ")
    logging.info("=" * 30)

    # --- Argument Parsing ---vvv
    parser = argparse.ArgumentParser(
        description="Scrape a university program page and extract structured data (mocked AI)."
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="The full URL of the university program page to scrape.",
    )
    parser.add_argument(
        "--university",
        type=str,
        default="University specified by user",
        help="The name of the university (optional, defaults to generic string).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional file path to save the extracted JSON data.",
    )

    args = parser.parse_args()
    logging.info(
        f"Running with arguments: URL='{args.url}', University='{args.university}', Output file='{args.output}'"
    )
    # --- Argument Parsing ---^^^

    # Execute the pipeline using arguments
    result_data = run_extraction_pipeline(args.url, args.university)

    # Display the result
    if result_data:
        print("\n--- Final Extracted Data (Mocked) ---")
        # Pretty print to console
        print(json.dumps(result_data, indent=2))
        print("------------------------------------")

        # --- Save to File (if specified) ---vvv
        if args.output:
            logging.info(f"Attempting to save output to file: {args.output}")
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result_data, f, indent=2, ensure_ascii=False)
                logging.info(f"Successfully saved output to {args.output}")
            except IOError as e:
                logging.error(f"Failed to write output to file {args.output}: {e}")
            except Exception as e:
                logging.error(
                    f"An unexpected error occurred while writing to file {args.output}: {e}"
                )
        # --- Save to File (if specified) ---^^^

    else:
        print("\n--- Extraction Pipeline Failed ---")
        logging.warning("Pipeline finished without extracting data.")

    logging.info("=" * 30)
    logging.info(" Execution Finished ")
    logging.info("=" * 30)
