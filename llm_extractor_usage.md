# Example Usage (for testing this module directly)

```python
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
```

---

## Explanation, Comments, and Usage

- **Purpose:** This script now contains two functions for extracting structured data:
  - `extract_structured_data_mocked`: Simulates extraction using basic keyword spotting (unchanged).
  - `extract_structured_data_ollama`: The new function that attempts extraction using a real LLM running locally via Ollama.

- **Imports:** Added `os`, `dotenv`, `typing`, and `openai` library components.

- **Environment Loading:** `load_dotenv()` is called to load `OLLAMA_BASE_URL` and `OLLAMA_MODEL` from your `.env` file.

- **Ollama Function Logic (`extract_structured_data_ollama`)**:
  1. Reads the Ollama URL and model name from environment variables.
  2. Initializes the `OpenAI` client, setting the `base_url` to your local Ollama server and using `api_key='ollama'`.
  3. Constructs a basic prompt instructing the LLM to act as an expert extractor, providing the target JSON schema and raw text. It asks for JSON only.
  4. Makes the API call with `client.chat.completions.create`, using `temperature=0.1` for determinism.
  5. Includes `try...except` blocks to handle connection, API, and other errors.
  6. **Basic Parsing:** Attempts to extract JSON from markdown-style code fences and parse it.
  7. Returns the parsed dictionary if successful, otherwise `None`.

- **Testing (`if __name__ == '__main__':`)**
  - The example includes a test for `extract_structured_data_ollama`.
  - **To Test:**
    1. Run `ollama serve` or use the Ollama desktop app.
    2. Ensure your `.env` file has the model listed (e.g., `OLLAMA_MODEL=llama3:8b`) and it’s downloaded.
    3. Execute the script: `python3 llm_extractor.py`
    4. Review the output in the terminal.

- **Current Limitations:** The prompt is basic, and the parsing logic is still primitive. Improvements are ongoing.

---

## Next Step

The core connection is established. The next step is:

**Phase 3 (Revised): Prompt Engineering & Response Parsing (Ollama)**

1. Refine the prompt for more consistent JSON.
2. Improve response validation and parsing logic.
3. Explore Ollama model-specific enhancements (if available).
