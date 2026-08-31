import fitz
from PyQt6.QtGui import QImage


class PDFEngine:
    def __init__(self):
        self.doc = None
        self.current_page = None

    def load_document(self, file_path):
        try:
            self.doc = fitz.open(file_path)
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False

    def get_page_count(self):
        if (self.doc):
            return len(self.doc)
        else:
            0

    def get_page_pixmap(self, page_number, zoom=1.0):
        if not self.doc:
            return None

        page = self.doc[page_number]
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        return pix

    def get_page_qi_image(self, page_number, zoom=1.0):
        pix = self.get_page_pixmap(page_number, zoom)
        if not pix:
            return None
        qimg = QImage(pix.samples, pix.width, pix.height,
                      pix.stride, QImage.Format.Format_RGB888)
        return qimg
