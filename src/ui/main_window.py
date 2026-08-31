from PyQt6.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, QToolBar, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
from src.core.engine import PDFEngine
from src.ui.page_widget import PDFPageWidget


class LuminaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lumina PDF Reader")
        self.resize(1024, 768)

        self.engine = PDFEngine()
        self.init_ui()

    def init_ui(self):
        self.toolbar = QToolBar("Main toolbar")
        self.addToolBar(self.toolbar)

        self.btn_open = QPushButton("Open PDF")
        self.btn_open.clicked.connect(self.open_file)
        self.toolbar.addWidget(self.btn_open)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.scroll_area.setWidget(self.container)
        self.setCentralWidget(self.scroll_area)

    def on_scroll(self, value):
        viewport_height = self.scroll_area.viewport().height()
        current_top = value
        current_bottom = current_top+viewport_height+500

        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, PDFPageWidget):
                position = widget.geometry().top()
                if current_top <= (position+1000) and current_bottom >= (position-1000):
                    widget.load_page(zoom=1.5)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            if self.engine.load_document(file_path):
                self.render_document()
            else:
                print("The engine couldn't load the document. Check the file path!")

    def render_document(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for i in range(self.engine.get_page_count()):
            page_widget = PDFPageWidget(i, self.engine)
            self.layout.addWidget(page_widget)

        if self.layout.count() > 0:
            first_page = self.layout.itemAt(0).widget()
            if isinstance(first_page, PDFPageWidget):
                first_page.load_page(zoom=1.5)
