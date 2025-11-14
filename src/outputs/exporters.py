thonpython
import json
import logging
import csv

class Exporter:
    def export_json(self, data, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info("JSON exported successfully.")
        except Exception as e:
            logging.error(f"Failed to export JSON: {e}")

    def export_csv(self, data, path):
        try:
            if not data:
                raise ValueError("No data for CSV export.")

            keys = data[0].keys()
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            logging.info("CSV exported successfully.")
        except Exception as e:
            logging.error(f"Failed to export CSV: {e}")