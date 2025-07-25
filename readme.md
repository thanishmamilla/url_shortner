# Setup Instructions

Before running the application or tests, install the required dependencies:

```sh
pip install -r requirements.txt
```

## Overview
This document describes the implementation approach for the URL Shortener Service, covering architecture, design decisions, and testing.

---

## Architecture & Design

- **Framework:** Python 3.8+ with Flask for the web API.
- **Structure:**
  - `app/models.py`: In-memory, thread-safe storage for URL mappings and metadata.
  - `app/utils.py`: Utility functions for URL validation and short code generation.
  - `app/main.py`: Flask app with all API endpoints.
  - `tests/test_basic.py`: Pytest-based tests for core functionality and error cases.

### In-Memory Storage
- Implemented via the `URLStore` class in `app/models.py`.
- Uses a `threading.Lock` to ensure thread safety for concurrent requests.
- Stores each short code with its original URL, click count, and creation timestamp.

### Utilities
- `is_valid_url(url)`: Validates URLs using a regex pattern.
- `generate_short_code(length=6)`: Generates a random 6-character alphanumeric code.

---

## API Endpoints

### 1. Shorten URL
- **Endpoint:** `POST /api/shorten`
- **Input:** JSON with a `url` field.
- **Output:** JSON with `short_code` and `short_url`.
- **Validation:** Checks for valid URL and unique code generation.

### 2. Redirect
- **Endpoint:** `GET /<short_code>`
- **Behavior:** Redirects to the original URL if found (HTTP 302), increments click count. Returns 404 if not found.

### 3. Analytics
- **Endpoint:** `GET /api/stats/<short_code>`
- **Output:** JSON with the original URL, click count, and creation timestamp. Returns 404 if not found.

---

## Error Handling
- Returns 400 for invalid or missing input.
- Returns 404 for unknown short codes.
- Returns 500 if a unique code cannot be generated (very rare).

---

## Testing
- Tests are located in `tests/test_basic.py` and use `pytest`.
- **Coverage:**
  - Health check endpoint
  - URL shortening (valid and invalid input)
  - Redirection and click counting
  - Analytics endpoint
  - Error cases (missing fields, unknown codes)
- All tests pass, confirming correct implementation and error handling.

---

## Notes
- No external database is used; all data is in-memory and will be lost on restart.
- No authentication, rate limiting, or custom short codes, as per requirements.
