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

## Approach
- Use a simple pipeline: fetch XML, parse XML, normalize values, then export.
- Keep each module small and focused so the code is easy to read and maintain.
- Only extract data that is actually present in the XML.
- Normalize dates in one place so all date fields use the same format.
- Support both JSON and CSV exports.

## Trade-offs
- Using `xml.etree.ElementTree` keeps dependencies small, but `lxml` would be more powerful and more tolerant of XML variations.
- The parser scans tags in order, which is simple but less robust than explicit XPath queries.
- Only the first matching value is kept for repeated fields, so duplicate tags are ignored.
- CSV export stores nested data as JSON text in cells, which is simple but less user-friendly.
- There is no retry or caching for HTTP requests, so temporary network problems can fail the run.
- Type, year, and number are taken from the URI string, so a change in URL format could break extraction.
- Tests cover logic, but not live calls to legislation.gov.uk.

## Future Improvements
1. Add retry logic with exponential backoff :
Use urllib3 retry config or tenacity to retry transient HTTP failures (e.g. 429, 503) before raising an error.
2. Switch to XPath-based parsing with lxml :
Since lxml is already a dependency, replace iter() tag scanning with explicit XPath queries against the known UK legislation XML schema. This makes field extraction deterministic and namespace-aware.
3. Add a local file cache :
Cache fetched XML by URL hash to disk (or a lightweight KV store). Subsequent runs for the same legislation skip the network call entirely, speeding up bulk processing.
4. Support batch / multi-URL processing :
Accept a file of URLs or a glob of legislation types/years and process them in parallel using concurrent.futures.ThreadPoolExecutor, with a configurable concurrency limit.
5. Add integration/smoke tests :
Add an optional test class (skipped by default, enabled with an env flag) that hits one real legislation.gov.uk URL and validates the output schema, so API drift is detected early.
6. Schema validation on parsed output :
Use pydantic or a dataclass to define the expected shape of normalized output. This catches missing or wrongly-typed fields at parse time rather than silently propagating Nones downstream.
7. Improve CSV for structured fields :
Instead of encoding unapplied_effects as a JSON blob in one cell, consider either splitting into multiple rows or generating a separate linked CSV per complex field, following a normalized relational model.
8. Structured logging instead of print :
Replace print statements in main() with Python's logging module so verbosity can be controlled via --log-level and output can be redirected to files or log aggregation tools.
9. Support additional output formats :
Add Parquet, NDJSON, or RDF/Turtle as export targets, which would be more useful for downstream data science or semantic web use cases respectively.
10. Pagination / version history support :
The parser currently captures only the current version's links. Future support could traverse versions links to pull all historical versions of a piece of legislation into a single structured record.