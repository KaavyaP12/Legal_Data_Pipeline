# Fetch legislation XML from legislation.gov.uk.
import requests


class FetcherError(Exception):
    # Raised when fetching or normalizing a URL fails.
    pass


def normalize_url(url):
    # Convert any legislation URL to /data.xml endpoint.
    if not url or "legislation.gov.uk" not in url:
        raise FetcherError("Invalid legislation.gov.uk URL")
    
    url = url.rstrip("/")
    if not url.endswith("/data.xml"):
        url += "/data.xml"
    return url


def fetch_xml(url):
    # Fetch XML content from the legislation URL.
    try:
        response = requests.get(normalize_url(url), timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        raise FetcherError("Request timed out")
    except requests.exceptions.HTTPError:
        raise FetcherError(f"HTTP error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise FetcherError(f"Failed to fetch: {e}")
