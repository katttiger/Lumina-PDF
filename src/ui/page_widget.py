from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class PDFPageWidget(QLabel):
    def __init__(self, page_index, engine):
        super().__init__()
        self.page_index = page_index
        self.engine = engine
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setText(f"Page {page_index+1} (loading...)")
        self.setStyleSheet(
            "background-color: #2e2e2e; color: #aaa; border: 1px solid #444;")

        self.loaded = False

    def load_page(self, zoom=1.5):
        if not self.loaded:
            qimg = self.engine.get_page_qi_image(self.page_index, zoom=zoom)
            if (qimg):
                self.setPixmap(QPixmap.fromImage(qimg))
                self.setText("")
                self.loaded = True
