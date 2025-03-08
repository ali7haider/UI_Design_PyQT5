import os
import json
import fitz  # PyMuPDF for text extraction
import pytesseract  # OCR for images
from PIL import Image
import io
from PyQt5.QtWidgets import QMessageBox

class PdfSearchManager:
    CACHE_FILE = "cache_pdf.json"  # JSON file to store extracted text

    def __init__(self, parent=None):
        """Initialize and load the cache from JSON."""
        self.parent = parent  # To show QMessageBox in the UI
        self.cache = self.load_cache()

        # Set Tesseract path
        self.tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

        # Check if Tesseract is installed
        if not self.is_tesseract_available():
            self.show_tesseract_warning()

    def is_tesseract_available(self):
        """Check if Tesseract OCR is installed and accessible."""
        return os.path.exists(self.tesseract_path)

    def show_tesseract_warning(self):
        """Show a warning message if Tesseract is not installed."""
        message = (
            "Tesseract OCR is required for text extraction from scanned PDFs but was not found.\n\n"
            "To install it:\n"
            "1. Download from: https://github.com/UB-Mannheim/tesseract/wiki\n"
            "2. Install and note the installation path (default: C:\\Program Files\\Tesseract-OCR\\)\n"
            "3. Restart this application."
        )

        if self.parent:
            QMessageBox.warning(self.parent, "Tesseract OCR Not Found", message)
        else:
            print(message)  # Fallback if no GUI is available

    def load_cache(self):
        """Load existing cache from JSON or create an empty one if not found."""
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty if JSON is corrupted
        return {}

    def save_cache(self):
        """Save the current cache to a JSON file."""
        try:
            with open(self.CACHE_FILE, "w", encoding="utf-8") as file:
                json.dump(self.cache, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file. If the text exists in cache, use that instead.
        If not, extract it and update the cache.
        """
        if pdf_path in self.cache:
            return self.cache[pdf_path]  # Return cached text

        extracted_text = self._process_pdf_text(pdf_path)  # Extract text from PDF
        self.cache[pdf_path] = extracted_text  # Store in cache
        self.save_cache()  # Save updated cache

        return extracted_text

    def _process_pdf_text(self, pdf_path):
        """Extract text from a PDF file using both direct text extraction and OCR."""
        extracted_text = ""

        try:
            with fitz.open(pdf_path) as pdf:
                for page in pdf:
                    # Try extracting selectable text
                    page_text = page.get_text("text").strip()
                    if page_text:
                        extracted_text += page_text + "\n"
                    else:
                        # If no text is found, perform OCR
                        extracted_text += self._perform_ocr(page, pdf) + "\n"

        except Exception as e:
            print(f"Error processing PDF '{pdf_path}': {e}")

        return extracted_text.strip()

    def _perform_ocr(self, page, pdf):
        """Run OCR on images in the PDF page if no selectable text is found."""
        if not self.is_tesseract_available():
            return ""  # Skip OCR if Tesseract is unavailable

        ocr_text = ""
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            try:
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_data = base_image["image"]

                # Convert to PIL image
                img = Image.open(io.BytesIO(image_data))

                # Run OCR on the image
                ocr_text += pytesseract.image_to_string(img).strip() + "\n"

            except Exception as e:
                print(f"Error performing OCR on image {img_index}: {e}")

        return ocr_text.strip()
