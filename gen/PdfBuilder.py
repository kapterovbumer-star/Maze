from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os


class PdfBuilder:
    def __init__(self, output_filename: str):
        self.output_filename = output_filename

    def create_pdf(self, images: list[dict]):
        """
        Create a PDF from a list of images with titles.
        
        Args:
            images (list[dict]): List of dictionaries, each containing:
                                 - "title": Title for the page
                                 - "image_filename": Path to the PNG image
        """
        c = canvas.Canvas(self.output_filename, pagesize=letter)
        page_width, page_height = letter

        for entry in images:
            title = entry.get("title", "")
            image_filename = entry.get("image_filename", "")
            
            if not os.path.exists(image_filename):
                print(f"Warning: File '{image_filename}' not found. Skipping.")
                continue

            # Add title
            if title:
                c.setFont("Helvetica-Bold", 16)
                c.drawString(72, page_height - 72, title)

            # Add image (resizing to fit the page if needed)
            img = ImageReader(image_filename)
            img_width, img_height = img.getSize()
            scale = min(page_width / img_width, (page_height - 100) / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale

            x = (page_width - scaled_width) / 2
            y = (page_height - scaled_height - 100) / 2
            c.drawImage(image_filename, x, y, width=scaled_width, height=scaled_height)

            # Finish the page
            c.showPage()

        # Save the PDF
        c.save()
        print(f"PDF saved as '{self.output_filename}'.")


# Example Usage
if __name__ == "__main__":
    images = [
        {"title": "Page 1", "image_filename": "image1.png"},
        {"title": "Page 2", "image_filename": "image2.png"},
        {"title": "Page 3", "image_filename": "image3.png"}
    ]
    pdf_builder = PdfBuilder("output.pdf")
    pdf_builder.create_pdf(images)
