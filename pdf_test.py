import fitz  # PyMuPDF for text extraction
import pytesseract  # OCR for images
from PIL import Image
import io

# Ensure Tesseract is correctly set
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def search_text_in_pdf(pdf_path, search_text):
    """Search for a given text in a PDF using direct text extraction and OCR for images."""
    
    with fitz.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf, start=1):
            # Try extracting selectable text
            extracted_text = page.get_text("text").strip()

            if search_text.lower() in extracted_text.lower():
                print(f"Text found on page {page_num}")
                return True  # Found the text, no need to continue

            # If no selectable text, apply OCR
            images = page.get_images(full=True)
            if images:
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = pdf.extract_image(xref)
                    image_data = base_image["image"]

                    # Convert image data to PIL image
                    img = Image.open(io.BytesIO(image_data))

                    # Run OCR on the image
                    ocr_text = pytesseract.image_to_string(img).strip()

                    if search_text.lower() in ocr_text.lower():
                        print(f"Text found in image {img_index + 1} on page {page_num}")
                        return True  # Found the text, no need to continue

    print("Text not found in the PDF.")
    return False  # Text was not found

# Example usage
pdf_path = "R.26981.pdf"  # Update with your PDF file path
search_query = "Thermostaat"  # Text to search

# Run the search
if search_text_in_pdf(pdf_path, search_query):
    print("Text exists in the PDF.")
else:
    print("Text not found.")
