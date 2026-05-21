import csv
import io
from typing import List, Dict, Any

class CSVExporter:
    @staticmethod
    def export(data: List[Dict[str, Any]]) -> str:
        if not data:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
