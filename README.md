# UK Legislation Data Pipeline

A small Python CLI pipeline that extracts explicit metadata from UK legislation XML on legislation.gov.uk.

## What it does

- Fetches legislation XML from a legislation.gov.uk URL
- Parses available metadata and document links
- Normalizes dates to `YYYY-MM-DD`
- Exports output as JSON or CSV
- Keeps extraction explicit: no inference, no guessing, no AI enrichment

## Installation

```bash
# Create and activate a virtual environment (Unix / macOS)
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Create Environment
python -m venv env
source env/bin/activate 
```
```bash
python extract.py https://www.legislation.gov.uk/ukpga/2024/15
python extract.py https://www.legislation.gov.uk/ukpga/2024/15 --output ./my_output
python extract.py https://www.legislation.gov.uk/ukpga/2024/15 --format csv
```

## Output

The exporter builds a filename from the legislation type, year, and number. Example outputs:

- `output/ukpga_2024_15.json`
- `output/ukpga_2024_15.csv`


## Project structure

```
LegalDataPipeline/
├── extract.py
├── requirements.txt
├── README.md
├── sample_output.json
├── env/
├── legislation/
│   ├── __init__.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── normalizer.py
│   └── exporter.py
└── tests/
    └── test_basic.py
```

## How it works

### `extract.py`

- CLI entry point
- Parses `url`, `--output`, and `--format`
- Runs fetch → parse → normalize → export

### `legislation/fetcher.py`

- Validates legislation.gov.uk URLs
- Converts any URL to `/data.xml`
- Fetches XML over HTTP
- Raises `FetcherError` for invalid or failed requests

### `legislation/parser.py`

- Parses XML with `xml.etree.ElementTree`
- Extracts values explicitly present in the XML
- Reads links and metadata from XML elements and attributes
- Populates `unapplied_effects` when present

### `legislation/normalizer.py`

- Normalizes date strings to ISO format
- Builds a consistent normalized output dictionary
- Preserves missing fields as `None`

### `legislation/exporter.py`

- Exports normalized output to JSON or CSV
- Creates the output directory if needed
- Builds filenames from type/year/number
- Flattens lists/dicts for CSV cells

## Testing

```bash
python -m unittest discover -v tests
```

The tests cover:

- URL normalization
- XML parsing handling
- date normalization
- JSON and CSV export

## License

MIT
