# Basic tests for legislation pipeline.
import unittest
import json
from legislation.fetcher import normalize_url, FetcherError
from legislation.parser import parse_xml, ParserError
from legislation.normalizer import normalize_date, normalize_legislation_data
from legislation.exporter import export_to_json, export_to_csv
import tempfile
import os
import csv


class TestFetcher(unittest.TestCase):
    # Test URL normalization.
    def test_normalize_basic_url(self):
        self.assertEqual(normalize_url("https://www.legislation.gov.uk/ukpga/2024/15"),
                        "https://www.legislation.gov.uk/ukpga/2024/15/data.xml")
    
    def test_normalize_trailing_slash(self):
        self.assertEqual(normalize_url("https://www.legislation.gov.uk/ukpga/2024/15/"),
                        "https://www.legislation.gov.uk/ukpga/2024/15/data.xml")
    
    def test_invalid_domain(self):
        with self.assertRaises(FetcherError):
            normalize_url("https://example.com/page")


class TestParser(unittest.TestCase):
    # Test XML parsing.
    def test_invalid_xml(self):
        with self.assertRaises(ParserError):
            parse_xml("<not valid xml")
    
    def test_empty_xml(self):
        result = parse_xml("<root></root>")
        self.assertIsInstance(result, dict)


class TestNormalizer(unittest.TestCase):
    # Test data normalization.
    def test_normalize_date_uk_format(self):
        self.assertEqual(normalize_date("24 May 2024"), "2024-05-24")
    
    def test_normalize_date_iso(self):
        self.assertEqual(normalize_date("2024-05-24"), "2024-05-24")
    
    def test_normalize_date_invalid(self):
        self.assertIsNone(normalize_date("not a date"))
    
    def test_normalize_data(self):
        data = {"title": "Test Act", "year": "2024", "enactment_date": "24 May 2024"}
        result = normalize_legislation_data(data)
        self.assertEqual(result["title"], "Test Act")
        self.assertEqual(result["enactment_date"], "2024-05-24")
        self.assertEqual(result["versions"], [])
    
    def test_json_serializable(self):
        data = {"title": "Test"}
        normalized = normalize_legislation_data(data)
        json_str = json.dumps(normalized, indent=2)
        self.assertIn("Test", json_str)

    def test_export_csv(self):
        data = {"title": "Test", "type": "t", "year": "2024", "number": "1"}
        normalized = normalize_legislation_data(data)
        with tempfile.TemporaryDirectory() as td:
            path = export_to_csv(normalized, td)
            self.assertTrue(os.path.exists(path))
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertGreaterEqual(len(rows), 1)
                self.assertEqual(rows[0].get("title"), "Test")


if __name__ == "__main__":
    unittest.main()
