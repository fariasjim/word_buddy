import io
import sys

import convertion_logic


def run_conversion_in_browser(file_bytes: bytes, h_value: int) -> dict:
    convertion_logic.runs = []
    input_stream = io.BytesIO(file_bytes)
    output_stream = io.BytesIO()

    original_save = convertion_logic.Document.save

    def mock_save(self, path):
        if str(path).endswith(".bkup"):
            return  # Skip generating physical backup files inside the browser
        original_save(self, output_stream)

    convertion_logic.Document.save = mock_save
    try:
        convertion_logic.replace_and_highlight(
            doc_path=input_stream, save_path=output_stream, h_value=h_value
        )
    finally:
        convertion_logic.Document.save = original_save
    total_conversions = len(convertion_logic.runs)
    processed_bytes = output_stream.getvalue()
    return {"bytes": processed_bytes, "count": total_conversions}
