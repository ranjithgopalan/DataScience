import sys
import uuid

import PyPDF2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit,QLabel
from PyPDF2 import PdfReader
import difflib
import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import mpld3

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
        self.setWindowTitle('PDF Image Comparer')
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
            # Convert PDFs to images
            images1 = convert_from_path(self.file1)
            images2 = convert_from_path(self.file2)
            resultfile = 'PDF_Image_Comparison_'+requestId+'.html'   
            if len(images1) > len(images2):
                html ='<h2> Started image comparison between first PDF: ' + self.file1 +' having page count: '+str(len(images1)) +' and second first PDF '+ self.file2 +' having page count: '+str(len(images1))+' </h2>\n'
                for i in range(len(images1)):
                    
                    # Convert images to NumPy arrays
                    array1 = np.array(images1[i].convert('RGB'))
                    if i > len(images2):            
                        array2 = np.zeros_like(array1)
                    else:
                        array2 = np.array(images1[2].convert('RGB'))
                        
                    # Compare arrays
                    difference = np.subtract(array1, array2)
                    # Display original images and difference side by side
                    fig, axs = plt.subplots(1, 3, figsize=(10, 10))


                    axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')

                    axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')

                    axs[2].imshow(difference)
                    axs[2].set_title('Difference')

                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                    # Convert the figure to HTML and add it to the HTML string
                    html +='<h2> Page number: ' + str(i) +'</h2>\n'
                    html += mpld3.fig_to_html(fig)
                    # Close the figure    
                    plt.close(fig)
                html += '</body></html>\n'
                with open(resultfile, 'w') as f:
                # Write the HTML string to a file
                    f.write(html)
                
            elif len(images1) < len(images2):
                html ='<h2> Started image comparison between first PDF: ' + self.file1 +' having page count: '+str(len(images1)) +' and second first PDF '+ self.file2 +' having page count: '+str(len(images1))+' </h2>\n'
                for i in range(len(images2)):
                    html='<h2> Page number: ' + str(i) +'</h2>\n'
                    # Convert images to NumPy arrays
                    array2 = np.array(images2[i].convert('RGB'))
                    if i > len(images1):            
                        array1 = np.zeros_like(array2)
                    else:
                        array1 = np.array(images1[i].convert('RGB'))
                        # Compare arrays
                    # Compare arrays
                    difference = np.subtract(array1, array2)
                    # Display original images and difference side by side
                    fig, axs = plt.subplots(1, 3, figsize=(10, 10))


                
                    axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')

                    axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')

                    axs[2].imshow(difference)
                    axs[2].set_title('Difference')

                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                    # Convert the figure to HTML and add it to the HTML string
                    html += mpld3.fig_to_html(fig)
                    # Close the figure    
                    plt.close(fig)
                html += '</body></html>\n'

                with open(resultfile, 'w') as f:
                   f.write(html)
            else:   
                html ='<h2> Started image comparison between first PDF: ' + self.file1 +' having page count: '+str(len(images1)) +' and second first PDF '+ self.file2 +' having page count: '+str(len(images1))+' </h2>\n' 
                for i in range(len(images1)):
                    html='<h2> Page number: ' + str(i) +'</h2>\n'
                    # Convert images to NumPy arrays
                    array1 = np.array(images1[i].convert('RGB'))
                    array2 = np.array(images2[i].convert('RGB'))
                    # Compare arrays
                    # Compare arrays
                    difference = np.subtract(array1, array2)
                    # Display original images and difference side by side
                    fig, axs = plt.subplots(1, 3, figsize=(10, 10))

                
                    axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')

                    axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')

                    axs[2].imshow(difference)
                    axs[2].set_title('Difference')

                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                    # Convert the figure to HTML and add it to the HTML string
                    html += mpld3.fig_to_html(fig)
                    # Close the figure
                    plt.close(fig)

                html += '</body></html>\n'

                with open(resultfile, 'w') as f:
                    f.write(html)
            self.result_label.setText('PDFs are compared successfully. Please check the result file: '+resultfile)

        except Exception as e:
            self.result_label.setText('Error occurred while comparing PDFs: '+str(e))
            
           

def main():
    app = QApplication(sys.argv)

    comparer = PDFComparer()
    comparer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()