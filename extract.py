#!/usr/bin/env python3
# Extract UK legislation data to JSON.
import sys
import argparse
from legislation.fetcher import fetch_xml, FetcherError
from legislation.parser import parse_xml, ParserError
from legislation.normalizer import normalize_legislation_data
from legislation.exporter import export, ExporterError


def main():
    # Run the extraction pipeline.
    parser = argparse.ArgumentParser(description="Extract UK legislation to JSON")
    parser.add_argument("url", help="Legislation URL (e.g., https://www.legislation.gov.uk/ukpga/2024/15)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    parser.add_argument("--format", choices=["json", "csv"], default="json",
                        help="Export format: json (default) or csv")
    
    args = parser.parse_args()
    
    try:
        print(f"Fetching: {args.url}")
        xml = fetch_xml(args.url)
        print("✓ XML fetched")
        
        print("Parsing...")
        extracted = parse_xml(xml)
        print("✓ XML parsed")
        
        print("Normalizing...")
        normalized = normalize_legislation_data(extracted)
        print("✓ Normalized")
        
        print("Exporting...")
        filepath = export(normalized, args.output, args.format)
        print(f"✓ Saved to: {filepath}")
        return 0
    
    except (FetcherError, ParserError, ExporterError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
