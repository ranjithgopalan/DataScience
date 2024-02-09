from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from pdf2image import convert_from_path
import mpld3
import numpy as np
from PyQt5.QtWidgets import QTextEdit
import uuid
import PyPDF2
from PyQt5.QtWidgets import QLineEdit
import difflib

class PDFComparer(QWidget):
    """
    A class that represents a PDF Comparer widget.

    Attributes:
        file1 (str): The path of the first PDF file.
        file2 (str): The path of the second PDF file.
        window1 (QWidget): The main window of the PDF Comparer widget.
        resultfile (str): The name of the result file.

    Methods:
        __init__(): Initializes the PDFComparer widget.
        run_function(index): Runs the corresponding function based on the selected index in the combo box.
        initRegressionUI(): Initializes the PDF Regression UI.
        FormValidationUI(): Initializes the Form Validation UI.
        reset(): Resets the file paths and result.
        PDFRegression(): Compares the PDF files and displays the differences.
    """

    def __init__(self):
        """
        Initializes the PDFComparer widget.
        """
        super().__init__()
        self.setWindowTitle('Document Comparer')
        self.file1 = None
        self.file2 = None

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(150, 80, 150, 80)
        self.label = QLabel("Select Form validation type", self)
        self.layout.addWidget(self.label)

        self.comboBox = QComboBox(self)
        self.comboBox.addItem("")
        self.comboBox.addItem("PDF Regression")
        self.comboBox.addItem("Form Validation")
        self.comboBox.currentIndexChanged.connect(self.run_function)
        self.comboBox.setStyleSheet("background-color: lightblue; font: bold 14px;")

        self.layout.addWidget(self.comboBox, alignment=Qt.AlignCenter)

    def run_function(self, index):
        if index == 0:
            print("Function 1")
        elif index == 1:
            self.initRegressionUI()
        elif index == 2:
            self.FormValidationUI()
            # self.function3()

    def initRegressionUI(self):
        """
        Initializes the Regression UI.

        This method sets up the UI elements for PDF regression, including buttons for selecting PDF files,
        a button for comparing the PDFs, a text area for displaying the result, and a button for resetting the UI.

        Args:
            None

        Returns:
            None
        """
        self.window1 = QWidget()
        self.window1.setWindowTitle('PDFRegression')
        requestId = str(uuid.uuid4())
        self.resultfile = 'PDF_Image_Comparison_'+requestId+'.html' 
        layout = QVBoxLayout(self.window1)
        layout.setSpacing(20)
        layout.setContentsMargins(150, 80, 150, 80)
        button = QPushButton("Select PDF1", self.window1)
        button.clicked.connect(self.select_file1)
        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file1_path_label = QLabel(self.window1)
        layout.addWidget(self.file1_path_label, alignment=Qt.AlignCenter)

        button = QPushButton("Select PDF1", self.window1)
        button.clicked.connect(self.select_file2)
        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file2_path_label = QLabel(self.window1)
        layout.addWidget(self.file2_path_label, alignment=Qt.AlignCenter)

        compare_btn = QPushButton('Compare PDFs', self.window1)
        compare_btn.clicked.connect(self.PDFRegression)
        layout.addWidget(compare_btn)

        self.result_label = QTextEdit(self.window1)
        layout.addWidget(self.result_label)

        reset_btn = QPushButton('Reset', self.window1)
        reset_btn.clicked.connect(self.reset)
        layout.addWidget(reset_btn)

        self.window1.show()
        self.window1.setStyleSheet("background-color: lightblue; font: bold 14px;")


    def FormValidationUI(self):
        """
        Creates the FormValidationUI window and sets up the user interface.

        This method creates a window titled 'FormValidationUI' and sets up the user interface
        with various buttons, labels, and text fields. It connects the button click events to
        their respective functions and displays the window.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        self.window1 = QWidget()
        self.window1.setWindowTitle('FormValidationUI')
        requestId = str(uuid.uuid4())
        self.resultfile = 'PDF_Image_Comparison_'+requestId+'.html' 
        layout = QVBoxLayout(self.window1)
        layout.setSpacing(20)
        layout.setContentsMargins(150, 80, 150, 80)
        button = QPushButton('Upload Form', self.window1)
        button.clicked.connect(self.select_file1)
        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file1_path_label = QLabel(self.window1)
        layout.addWidget(self.file1_path_label, alignment=Qt.AlignCenter)

        label = QLabel("Enter Form Name:", self)
        layout.addWidget(label)

        lineEdit = QLineEdit(self.window1)
        layout.addWidget(lineEdit)

        button = QPushButton("Upload Target PDF", self.window1)
        button.clicked.connect(self.select_file2)
        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file2_path_label = QLabel(self.window1)
        layout.addWidget(self.file2_path_label, alignment=Qt.AlignCenter)

        compare_btn = QPushButton('Validate Form', self.window1)
        compare_btn.clicked.connect(self.validFormInDocument)
        layout.addWidget(compare_btn)

        self.result_label = QTextEdit(self.window1)        
        layout.addWidget(self.result_label)

        reset_btn = QPushButton('Reset', self.window1)
        reset_btn.clicked.connect(self.reset)
        layout.addWidget(reset_btn)
        self.window1.setStyleSheet("background-color: lightblue; font: bold 14px;")

        self.window1.show()

    def reset(self):
        """
        Resets the file paths and result.
        """
        # self.file1 = None
        # self.file2 = None
        self.lineEdit.setText('')
        self.file1_path_label.setText('')
        self.file2_path_label.setText('')
        self.result_label.clear()     


    def PDFRegression(self):
        """
        Compares the PDF files and displays the differences.
        """
        try:

            if self.file1 is None:
                print("No file selected")
                return 'No file selected'
            images1 = convert_from_path(self.file1)
            images2 = convert_from_path(self.file2)
            # resultfile = 'PDF_Image_Comparison_'+requestId+'.html'   
            if len(images1) > len(images2):
                html ='<h2> Started image comparison between first PDF: ' + self.file1 +' having page count: '+str(len(images1)) +' and second first PDF '+ self.file2 +' having page count: '+str(len(images1))+' </h2>\n'
                for i in range(len(images1)):
                    
                    # Convert images to NumPy arrays
                    array1 = np.array(images1[i].convert('RGB'))
                    import matplotlib.pyplot as plt

                    if i > len(images2):            
                        array2 = np.zeros_like(array1)
                    else:
                        array2 = np.array(images1[2].convert('RGB'))

                    # Compare arrays
                    difference = np.subtract(array1, array2)
                    # Display original images and difference side by side
                    fig, axs = plt.subplots(1, 3, figsize=(10, 10))


                    # Display the first image
                    im1 = axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')
                    fig.colorbar(im1, ax=axs[0], orientation='horizontal')

                    # Display the second image
                    im2 = axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')
                    fig.colorbar(im2, ax=axs[1], orientation='horizontal')

                    # Display the difference
                    im3 = axs[2].imshow(difference, cmap='coolwarm')
                    axs[2].set_title('Difference')
                    fig.colorbar(im3, ax=axs[2], orientation='horizontal')

                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                    # Convert the figure to HTML and add it to the HTML string
                    html +='<h2> Page number: ' + str(i) +'</h2>\n'
                    html += mpld3.fig_to_html(fig)
                    # Close the figure    
                    plt.close(fig)
                html += '</body></html>\n'
                with open(self.resultfile, 'w') as f:
                # Write the HTML string to a file
                    f.write(html)
                
            elif len(images1) < len(images2):
                html ='<h2> Started image comparison between first PDF: ' + self.file1 +' having page count: '+str(len(images1)) +' and second first PDF '+ self.file2 +' having page count: '+str(len(images1))+' </h2>\n'
                for i in range(len(images2)):
                    
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


                
                    # Display the first image
                    im1 = axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')
                    fig.colorbar(im1, ax=axs[0], orientation='horizontal')

                    # Display the second image
                    im2 = axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')
                    fig.colorbar(im2, ax=axs[1], orientation='horizontal')

                    # Display the difference
                    im3 = axs[2].imshow(difference, cmap='coolwarm')
                    axs[2].set_title('Difference')
                    fig.colorbar(im3, ax=axs[2], orientation='horizontal')

                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                    # Convert the figure to HTML and add it to the HTML string
                    html +='<h2> Page number: ' + str(i) +'</h2>\n'
                    html += mpld3.fig_to_html(fig)
                    # Close the figure    
                    plt.close(fig)
                html += '</body></html>\n'

                with open(self.resultfile, 'w') as f:
                   f.write(html)
                
            else:   
                html ='<h2> Started image comparison between first PDF: ' + self.file1 +' having page count: '+str(len(images1)) +' and second first PDF '+ self.file2 +' having page count: '+str(len(images1))+' </h2>\n' 
                for i in range(len(images1)):
                    
                    # Convert images to NumPy arrays
                    array1 = np.array(images1[i].convert('RGB'))
                    array2 = np.array(images2[i].convert('RGB'))
                    # Compare arrays
                    # Compare arrays
                    difference = np.subtract(array1, array2)
                    # Display original images and difference side by side
                    fig, axs = plt.subplots(1, 3, figsize=(10, 10))

                
                    # Display the first image
                    im1 = axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')
                    fig.colorbar(im1, ax=axs[0], orientation='horizontal')

                    # Display the second image
                    im2 = axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')
                    fig.colorbar(im2, ax=axs[1], orientation='horizontal')

                    # Display the difference
                    im3 = axs[2].imshow(difference, cmap='coolwarm')
                    axs[2].set_title('Difference')
                    fig.colorbar(im3, ax=axs[2], orientation='horizontal')

                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                    # Convert the figure to HTML and add it to the HTML string
                    html +='<h2> Page number: ' + str(i) +'</h2>\n'
                    html += mpld3.fig_to_html(fig)
                    # Close the figure
                    plt.close(fig)

                html += '</body></html>\n'

                with open(self.resultfile, 'w') as f:
                    f.write(html)
            return self.result_label.setText('PDFs are compared successfully. Please check the result file: '+self.resultfile)
            # return 'PDFs are compared successfully. Please check the result file: '+self.resultfile

        except Exception as e:
            self.result_label.setText('Error occurred while comparing PDFs: '+str(e))           
            # return 'Error occurred while comparing PDFs: '+str(e)

    def validFormInDocument(self): 
            try:
                FormTobeValidated = self.file1
                FormName =  self.lineEdit.text()
                TargetPDF=  self.file2

                PDF1Count = len(PyPDF2.PdfReader(FormTobeValidated).pages)
                PDF2Count = len(PyPDF2.PdfReader(TargetPDF).pages)
                html ='<h2> Started image comparison between first PDF: ' + FormTobeValidated+' having page count: '+str(len(PDF1Count)) +' and second first PDF '+ TargetPDF+' having page count: '+str(len(PDF2Count))+' </h2>\n'
                FormFound= False
                for i in range(PDF2Count):
                    pdf2_text = PyPDF2.PdfReader(TargetPDF).pages[i].extract_text()
                    if FormName in pdf2_text:
                        StartPostitionInTargetPDF = i
                        FormFound= True
                        break
                if  FormFound == False:
                    html+='<h2> Form: '+ FormTobeValidated + ' NOT found in the target PDF ' +TargetPDF+ ' Please upload the correct form for validation </h2>\n'
                    return self.result_label.setText('Form: '+ FormTobeValidated + ' NOT found in the target PDF ' +TargetPDF+ ' Please upload the correct form for validation')     

                for j in range(PDF1Count):
                    diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())

                    images1 = convert_from_path(FormTobeValidated)
                    images2 = convert_from_path(TargetPDF)
                    # Convert images to NumPy arrays
                    array1 = np.array(images1[j].convert('RGB'))
                    array2 = np.array(images2[StartPostitionInTargetPDF].convert('RGB'))
                    StartPostitionInTargetPDF+=1
                    # Compare arrays
                    # Compare arrays
                    difference = np.subtract(array1, array2)
                    # Display original images and difference side by side
                    fig, axs = plt.subplots(1, 3, figsize=(10, 10))

                    
                    # Display the first image
                    im1 = axs[0].imshow(array1)
                    axs[0].set_title('PDF 1')
                    fig.colorbar(im1, ax=axs[0], orientation='horizontal')

                    # Display the second image
                    im2 = axs[1].imshow(array2)
                    axs[1].set_title('PDF 2')
                    fig.colorbar(im2, ax=axs[1], orientation='horizontal')

                    # Display the difference
                    im3 = axs[2].imshow(difference, cmap='coolwarm')
                    axs[2].set_title('Difference')
                    fig.colorbar(im3, ax=axs[2], orientation='horizontal')


                    # Remove axis
                    for ax in axs:
                        ax.axis('off')

                        # Convert the figure to HTML and add it to the HTML string
                    html += mpld3.fig_to_html(fig)
                        # Close the figure
                    plt.close(fig)

                html += '</body></html>\n'

                    # Write the HTML string to a file
                with open(self.resultfile, 'w') as f:
                    f.write(html)        
                self.result_label.setText('Given form is  compared with Traget PDF successfully. Please check the result file: '+self.resultfile)

            except Exception as e:
                self.result_label.setText('Error occurred while comparing PDFs: '+str(e))
  

    def select_file1(self):
        file_dialog = QFileDialog(self)
        self.file1, _ = file_dialog.getOpenFileName()
        if self.file1:
            self.file1_path_label.setText(f"File path: {self.file1}")

    def select_file2(self):
        file_dialog = QFileDialog(self)
        self.file2, _ = file_dialog.getOpenFileName()
        if self.file2:
            self.file2_path_label.setText(f"File path: {self.file2}")

app = QApplication([])
window = PDFComparer()
window.show()
app.exec_()