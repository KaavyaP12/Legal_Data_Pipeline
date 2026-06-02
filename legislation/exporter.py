# Export legislation data to JSON format.
import csv
import json
from pathlib import Path


class ExporterError(Exception):
    # Raised when exporting data fails.
    pass


def _make_output_path(data, output_dir: str, suffix: str) -> Path:
    try:
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise ExporterError(f"Failed to create output directory: {e}")

    leg_type = data.get("type") or "legislation"
    year = data.get("year") or "unknown"
    number = data.get("number") or "unknown"

    if "(" in leg_type:
        leg_type = leg_type.split("(")[-1].rstrip(")")

    return path / f"{leg_type}_{year}_{number}.{suffix}"


def export_to_json(data: dict[str, object], output_dir: str = "output") -> str:
    # Export legislation data to JSON file.
    filepath = _make_output_path(data, output_dir, "json")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        raise ExporterError(f"Failed to write JSON file: {e}")

    return str(filepath)


def export_to_csv(data: dict[str, object], output_dir: str = "output") -> str:
    # Export legislation data to a single-row CSV file.
    # Lists and complex fields are JSON-encoded into cells.

    filepath = _make_output_path(data, output_dir, "csv")
    flat = {
        k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else "" if v is None else str(v))
        for k, v in data.items()
    }

    try:
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat.keys()))
            writer.writeheader()
            writer.writerow(flat)
    except OSError as e:
        raise ExporterError(f"Failed to write CSV file: {e}")

    return str(filepath)


def export(data, output_dir: str = "output", fmt: str = "json") -> str:
    # Dispatch export to the requested format (json|csv).
    fmt = (fmt or "json").lower()
    if fmt == "json":
        return export_to_json(data, output_dir)
    elif fmt == "csv":
        return export_to_csv(data, output_dir)
    else:
        raise ExporterError(f"Unsupported export format: {fmt}")
