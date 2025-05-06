# scraper.py
import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_program_page(url: str) -> Optional[str]:
    """
    Fetches and parses a university program page to extract relevant text content.

    Args:
        url: The URL of the program page.

    Returns:
        A string containing the main text content of the page, or None if fetching/parsing fails.
    """
    logging.info(f"Attempting to scrape URL: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        logging.info(
            f"Successfully fetched URL: {url} with status code {response.status_code}"
        )

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during fetching {url}: {e}")
        return None

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        main_content_area = soup.find("main", {"id": "main"})
        if not main_content_area:
            main_content_area = soup.find(
                "div", class_="content-area"
            )  # Example fallback

        if main_content_area:
            raw_text = main_content_area.get_text(separator=" ", strip=True)
            logging.info(
                f"Successfully extracted text content (length: {len(raw_text)} chars)."
            )
            return raw_text
        else:
            logging.warning(
                "Could not find specific main content area, extracting text from body."
            )
            body_text = (
                soup.body.get_text(separator=" ", strip=True) if soup.body else ""
            )  # Handle case where body might be None
            return body_text

    except Exception as e:
        logging.error(f"Error parsing HTML content from {url}: {e}")
        return None


# --- Example Usage (for testing this module directly) ---
if __name__ == "__main__":
    test_url = "https://web.archive.org/web/20240314085048/https://www.uva.nl/en/programmes/masters/information-studies/information-studies.html"
    print(f"Testing scraper with URL: {test_url}")
    extracted_text = scrape_program_page(test_url)
    if extracted_text:
        print("\n--- Extracted Text (First 500 chars) ---")
        print(extracted_text[:500])
        print("\n----------------------------------------")
        print(f"(Total length: {len(extracted_text)} characters)")
    else:
        print("\nFailed to extract text.")
