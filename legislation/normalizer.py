# Normalize and standardize extracted legislation data.
from datetime import datetime


def normalize_date(date_str):
    # Convert date string to YYYY-MM-DD format.
    if not date_str or not isinstance(date_str, str):
        return None
    
    formats = ["%d %B %Y", "%d %b %Y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return None


def normalize_legislation_data(data):
    # Normalize extracted data to consistent format.
    fields = [
        "title", "type", "year", "number", "status", "isbn", "extent",
        "document_uri", "id_uri", "xml_url", "html_url", "pdf_url",
        "rdf_url", "csv_url", "akn_url", "introduction_url", "body_url",
        "schedules_url", "contents_url"
    ]
    
    normalized = {field: data.get(field) for field in fields}
    
    # Normalize dates
    normalized["enactment_date"] = normalize_date(data.get("enactment_date"))
    normalized["last_modified"] = normalize_date(data.get("last_modified"))
    normalized["valid_from"] = normalize_date(data.get("valid_from"))
    
    # Complex fields
    normalized["versions"] = data.get("versions", [])
    normalized["unapplied_effects"] = data.get("unapplied_effects", [])
    
    return normalized
