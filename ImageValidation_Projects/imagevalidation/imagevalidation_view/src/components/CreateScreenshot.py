import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger, PdfMerger
import os

class ScreenshotPDF(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 200, 150)
        self.setWindowTitle('Screenshot to PDF')

        self.layout = QVBoxLayout()

        self.prefix_input = QLineEdit(self)
        self.layout.addWidget(self.prefix_input)

        self.capture_btn = QPushButton('Capture Screenshot', self)
        self.capture_btn.clicked.connect(self.capture_screenshot)
        self.layout.addWidget(self.capture_btn)

        self.create_pdf_btn = QPushButton('Create PDF', self)
        self.create_pdf_btn.clicked.connect(self.create_pdf)
        self.layout.addWidget(self.create_pdf_btn)

        self.setLayout(self.layout)

        self.show()

    def capture_screenshot(self):
        # Capture screenshot
        screenshot = QApplication.screens()[0].grabWindow(0)

        # Get filename from user
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '/home', 'PDF Files (*.png)')
        if filename:
            # Separate directory and filename
            directory, name = os.path.split(filename)

            # Add prefix to filename
            filename = os.path.join(directory, self.prefix_input.text() + name)

            # Save screenshot as PNG
            screenshot.save(filename, 'png')

            print('Screenshot saved.')

    def create_pdf(self):
        # Initialize PdfFileMerger
        pdf_merger = PdfMerger()

        # Get all PNG files in directory
        directory = '/home'
        for filename in os.listdir(directory):
            if filename.endswith('.png'):
                # Convert PNG to PDF
                pdf_filename = os.path.join(directory, filename.replace('.png', '.pdf'))
                pdf = canvas.Canvas(pdf_filename)
                pdf.drawImage(os.path.join(directory, filename), 0, 0, width=595, height=842)
                pdf.save()

                # Append PDF to PdfFileMerger
                pdf_merger.append(pdf_filename)

        # Merge the PDFs
        pdf_merger.write(os.path.join(directory, self.prefix_input.text() + "merged.pdf"))
        pdf_merger.close()

        print('PDF created.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotPDF()
    sys.exit(app.exec_())