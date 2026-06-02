# Parse UK legislation XML and extract structured data.
import xml.etree.ElementTree as ET


class ParserError(Exception):
    # Raised when XML parsing fails.
    pass

def parse_xml(xml_content):
    # Parse XML and extract all legislation data.
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        raise ParserError(f"Failed to parse XML: {e}")
    
    result = {}
    
    # Extract root attributes
    result["document_uri"] = root.get("DocumentURI")
    result["id_uri"] = root.get("IdURI")
    result["extent"] = root.get("RestrictExtent")
    result["valid_from"] = root.get("RestrictStartDate")
    
    # Extract from all elements
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        text = elem.text
        
        # URLs from atom:link elements (no text)
        if elem.tag.endswith("}link"):
            href = elem.get("href")
            if href:
                if "data.xml" in href and not result.get("xml_url"):
                    result["xml_url"] = href
                elif "data.html" in href and not result.get("html_url"):
                    result["html_url"] = href
                elif ".pdf" in href and not result.get("pdf_url"):
                    result["pdf_url"] = href
                elif "data.rdf" in href and not result.get("rdf_url"):
                    result["rdf_url"] = href
                elif "data.csv" in href and not result.get("csv_url"):
                    result["csv_url"] = href
                elif "data.akn" in href and not result.get("akn_url"):
                    result["akn_url"] = href
                elif "introduction" in href.lower() and not result.get("introduction_url"):
                    result["introduction_url"] = href
                elif "body" in href.lower() and not result.get("body_url"):
                    result["body_url"] = href
                elif "schedules" in href.lower() and not result.get("schedules_url"):
                    result["schedules_url"] = href
                elif "contents" in href.lower() and not result.get("contents_url"):
                    result["contents_url"] = href
            continue
        
        if not text:
            continue
        
        # Metadata fields
        if tag == "title" and not result.get("title"):
            result["title"] = text
        elif tag == "modified" and not result.get("last_modified"):
            result["last_modified"] = text
        
        # Effects
        elif tag in ["Effect", "UnappliedEffect"]:
            if "unapplied_effects" not in result:
                result["unapplied_effects"] = []
            effect = {}
            for child in elem:
                child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if child.text:
                    effect[child_tag] = child.text
            if effect:
                result["unapplied_effects"].append(effect)
    
    # Extract type/year/number from document URI
    if result.get("document_uri") and not result.get("type"):
        parts = result["document_uri"].rstrip("/").split("/")
        if len(parts) >= 4:
            result["type"] = parts[-3]
            result["year"] = parts[-2]
            result["number"] = parts[-1]
    
    return result
