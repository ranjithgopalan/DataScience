import sys
import uuid

import PyPDF2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit,QLabel
from PyPDF2 import PdfReader
import difflib

class PDFComparer(QWidget):
    """
    A class for comparing two PDF files and displaying the differences.

    Attributes:
        file1 (str): The path of the first PDF file.
        file2 (str): The path of the second PDF file.
        btn1 (QPushButton): Button for uploading the first PDF file.
        btn2 (QPushButton): Button for uploading the second PDF file.
        file1_label (QLabel): Label for displaying the path of the first PDF file.
        file2_label (QLabel): Label for displaying the path of the second PDF file.
        compare_btn (QPushButton): Button for comparing the PDF files.
        result_label (QTextEdit): Text area for displaying the comparison result.
        reset_btn (QPushButton): Button for resetting the file paths and result.

    Methods:
        initUI(): Initializes the user interface.
        upload_file1(): Opens a file dialog to upload the first PDF file.
        upload_file2(): Opens a file dialog to upload the second PDF file.
        reset(): Resets the file paths and result.
        compare_pdfs(): Compares the PDF files and displays the differences.
        extract_text(file_path): Extracts the text content from a PDF file.
    """
    def __init__(self):
        super().__init__()

        self.file1 = None
        self.file2 = None

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface by creating and arranging the widgets.
        """
        self.setWindowTitle('PDF Text Comparer')
        layout = QVBoxLayout()

        self.btn1 = QPushButton('Upload first PDF', self)
        self.btn1.clicked.connect(self.upload_file1)    
           
        layout.addWidget(self.btn1)
        self.file1_label = QLabel('')
        layout.addWidget(self.file1_label)

        self.btn2 = QPushButton('Upload second PDF', self)
        self.btn2.clicked.connect(self.upload_file2)
        layout.addWidget(self.btn2)

        self.file2_label = QLabel('')
        layout.addWidget(self.file2_label)

        self.compare_btn = QPushButton('Compare PDFs', self)
        self.compare_btn.clicked.connect(self.compare_pdfs)
        layout.addWidget(self.compare_btn)

        self.result_label = QTextEdit()
        layout.addWidget(self.result_label)

        self.reset_btn = QPushButton('Reset', self)
        self.reset_btn.clicked.connect(self.reset)
        layout.addWidget(self.reset_btn)

        self.setLayout(layout)

    def upload_file1(self):
        """
        Opens a file dialog to upload the first PDF file.
        Updates the file path label if a file is selected.
        """
        self.file1, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF Files (*.pdf)')
        if self.file1:
            self.file1_label.setText(self.file1)

    def upload_file2(self):
        """
        Opens a file dialog to upload the second PDF file.
        Updates the file path label if a file is selected.
        """
        self.file2, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF Files (*.pdf)')
        if self.file2:
            self.file2_label.setText(self.file2)

    def reset(self):
        """
        Resets the file paths and result.
        """
        self.file1 = None
        self.file2 = None
        self.file1_label.setText('')
        self.file2_label.setText('')
        self.result_label.clear()            

    def compare_pdfs(self):
        """
        Compares the PDF files and displays the differences.
        """
        try:
            requestId = str(uuid.uuid4())
            PDF1Count = len(PyPDF2.PdfReader(self.file1).pages)
            PDF2Count = len(PyPDF2.PdfReader(self.file2).pages)
            resultfile = 'PDF_Image_Comparison_'+requestId+'.html'
            with open(resultfile, 'w') as f:
                f.write('<html><body>')
                f.write(f'<h1> Started text comparison between : ' + self.file1 + ' and '+ self.file2 +' </h1>')  
                if PDF1Count > PDF2Count:
                    print("PDFs are different")
                    f.write(f'<h2>Difference in page count between PDFs, first PDF page count: '+str(PDF1Count)+' and Second PDF page count: '+str(PDF2Count)+ ' </h2>')  
                    textdifference = []                               
                    for i in range(PDF1Count):
                        try:
                            pdf1_text = PyPDF2.PdfReader(self.file1).pages[i].extract_text()                            
                            if i > PDF2Count:
                                pdf2_text = "" 
                                diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines()) 
                            else:
                                pdf2_text = PyPDF2.PdfReader(self.file2).pages[i].extract_text()  
                                diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())                                                       
                            f.write(f'<h2> Page number: ' + str(i) +'</h2>')  
                            f.write(f'<h2>' +diff +'</h2>')  
                        except Exception as e:   
                            f.write(f'<h2> page number: ' + str(i) +'- needs to be validated manually because of Exception :- '+str(e)+'</h2>')               
                    f.write('</body></html>')
                elif PDF1Count < PDF2Count:
                    f.write(f'<h2>Difference in page count between PDFs, first PDF page count: '+str(PDF1Count)+' and Second PDF page count: '+str(PDF2Count)+ ' </h2>')  
                    textdifference = []
                    
                    for i in range(PDF2Count):
                        try:
                            pdf2_text = PyPDF2.PdfReader(self.file2).pages[i].extract_text()                                                
                            if i > PDF1Count:
                                pdf1_text = "" 
                                diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines()) 
                            else:
                                pdf1_text = PyPDF2.PdfReader(self.file1).pages[i].extract_text()  
                                diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())                                
                            f.write(f'<h2> Page number: {str(i)}</h2>')  
                            f.write(f'<h2>{diff}</h2>')  
                        except Exception as e:   
                            f.write(f'<h2> page number: {str(i)} - needs to be validated manually because of Exception: {str(e)}</h2>')              
                    f.write('</body></html>')    
                else:                                                        
                    for i in range(PDF1Count):
                        try:
                            pdf1_text = PyPDF2.PdfReader(self.file1).pages[i].extract_text()
                            pdf2_text = PyPDF2.PdfReader(self.file2).pages[i].extract_text()
                            diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())                                                       
                            f.write(f'<h2> Page number: ' + str(i) +'</h2>')  
                            f.write(f'<h2>' +diff +'</h2>')  
                        except Exception as e:   
                            f.write(f'<h2> page number: ' + str(i) +'- needs to be validated manually because of Exception :- '+str(e)+'</h2>')  
                    f.write('</body></html>')
                self.result_label.setText('PDFs are compared successfully. Please check the result file: '+resultfile)
            def extract_text(self, file_path):
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    text = ''
                    try:
                        for page in range(len(reader.pages)):
                            text += reader.pages[page].extract_text()
                        return text
                    except Exception as e:
                        print("An error of type", type(e), "occurred:", e)
        except Exception as e:
            self.result_label.setText('Error occurred while comparing PDFs: '+str(e))
            
           

def main():
    app = QApplication(sys.argv)

    comparer = PDFComparer()
    comparer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()