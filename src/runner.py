thonpython
import json
import logging
import sys
from pathlib import Path
from extractors.ship_parser import ShipParser
from outputs.exporters import Exporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_filters():
    data_path = Path(__file__).resolve().parents[1] / "data" / "filters.sample.json"
    if data_path.exists():
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load filters: {e}")
    return {}

def main():
    filters = load_filters()

    parser = ShipParser()
    ship_data = parser.fetch_and_parse(filters=filters)

    exporter = Exporter()
    output_path = Path(__file__).resolve().parents[1] / "data" / "sample_output.json"
    exporter.export_json(ship_data, output_path)

    logging.info(f"Extraction completed. Output saved to: {output_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Execution interrupted by user.")
        sys.exit(1)