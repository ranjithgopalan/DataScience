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

    def __init__(self):

        super().__init__()

        self.setWindowTitle('Document Comparer')

        self.file1 = None

        self.file2 = None

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(20)

        self.layout.setContentsMargins(40, 40, 40, 40)

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

        self.window1 = QWidget()

        self.window1.setWindowTitle('PDFRegression')

        requestId = str(uuid.uuid4())

        self.resultfile = 'PDF_Image_Comparison_'+requestId+'.html' 

        layout = QVBoxLayout(self.window1)

        layout.setSpacing(20)

        layout.setContentsMargins(20, 20, 20, 20)

        button = QPushButton("Select file1", self.window1)

        button.clicked.connect(self.select_file1)

        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file1_path_label = QLabel(self.window1)

        layout.addWidget(self.file1_path_label, alignment=Qt.AlignCenter)

        button = QPushButton("Select File2", self.window1)

        button.clicked.connect(self.select_file2)

        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file2_path_label = QLabel(self.window1)

        layout.addWidget(self.file2_path_label, alignment=Qt.AlignCenter)

        compare_btn = QPushButton('Compare PDFs', self.window1)

        compare_btn.clicked.connect(self.PDFRegression)

        layout.addWidget(compare_btn)

        # return_value = self.PDFRegression()

        self.result_label = QTextEdit(self.window1)

        # result_label.setText(f"Return value: {return_value}")

        layout.addWidget(self.result_label)

        reset_btn = QPushButton('Reset', self.window1)

        reset_btn.clicked.connect(self.reset)

        layout.addWidget(reset_btn)

        self.window1.show()


    def FormValidationUI(self):

        self.window1 = QWidget()

        self.window1.setWindowTitle('FormValidationUI')

        requestId = str(uuid.uuid4())

        self.resultfile = 'PDF_Text_Comparison_'+requestId+'.html' 

        layout = QVBoxLayout(self.window1)

        layout.setSpacing(20)

        layout.setContentsMargins(20, 20, 20, 20)

        button = QPushButton('Upload Form', self.window1)

        button.clicked.connect(self.select_file1)

        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.file1_path_label = QLabel(self.window1)

        layout.addWidget(self.file1_path_label, alignment=Qt.AlignCenter)

        label = QLabel("Enter Form Name:", self)

        layout.addWidget(label)

        self.lineEdit = QLineEdit(self.window1)

        layout.addWidget(self.lineEdit)

        label1 = QLabel("Enter Expected Start Page Number:", self)

        layout.addWidget(label1)

        self.pageNumber = QLineEdit(self.window1)

        layout.addWidget(self.pageNumber)
 
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

        self.window1.show()

    def reset(self):

        """

        Resets the file paths and result.

        """

        # self.file1 = None

        # self.file2 = None

        self.lineEdit.setText('')

        self.pageNumber.setText('')

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

                PageNumber = self.pageNumber.text()

                TargetPDF=  self.file2

                # print(FormName)

                PDF1Count = len(PyPDF2.PdfReader(FormTobeValidated).pages)

                PDF2Count = len(PyPDF2.PdfReader(TargetPDF).pages)

                # print(PDF1Count)

                # print(PDF2Count)

                html ='<h2> Started image comparison between first PDF: ' + FormTobeValidated+' having page count: '+str(PDF1Count) +' and second first PDF '+ TargetPDF+' having page count: '+str(PDF2Count)+' </h2>\n'

                FormFound= False

                PresentInDec = False

                count = 0

                for i in range(PDF2Count):

                    try:

                        pdf2_text = PyPDF2.PdfReader(TargetPDF).pages[i].extract_text()

                        # pdf1_text = PyPDF2.PdfReader(FormTobeValidated).pages[0].extract_text()

                        # print(pdf1_text)

                        if FormName in pdf2_text:

                            if((count == 0 or 'DEC' in pdf2_text) and 'DEC' not in FormName):

                                PresentInDec = True

                                count = 1

                            else:

                                StartPostitionInTargetPDF = i

                                FormFound= True

                                break

                    except Exception as e:   

                            html1='<h2></h2>'

                if  FormFound == False:

                    html+='<h2> Form: '+ FormName + ' NOT found in the target PDF ' +TargetPDF+ ' Please upload the correct form for validation </h2>\n'

                    return self.result_label.setText('Form: '+ FormName + ' NOT found in the target PDF ' +TargetPDF+ ' Please upload the correct form for validation')     

 
                with open(self.resultfile, 'w') as f:

                    f.write('<html><body>')

                    f.write(f'<h1> Started text comparison between Form: ' + self.file1 + ' and Target pdf: '+ self.file2 +' </h1>')  

                    actualStartposition = StartPostitionInTargetPDF+1

                    if str(actualStartposition) != PageNumber:

                        f.write(f'<h1> Expected start page number of Form- '+FormName+' is ' + str(PageNumber) + ' and doesnt match actual start page number - '+ str(actualStartposition) +' </h1>')  

                    else:

                        f.write(f'<h1> Expected start page number of Form- '+FormName+' is ' + str(PageNumber) + ' and matches actual start page number - '+ str(actualStartposition) +' </h1>') 

                    for j in range(PDF1Count):

                        try:

                            pdf1_text = PyPDF2.PdfReader(FormTobeValidated).pages[j].extract_text()

                            # print(pdf1_text)

                            pdf2_text = PyPDF2.PdfReader(TargetPDF).pages[StartPostitionInTargetPDF].extract_text()

                            # print(pdf2_text)

                            diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())

                            f.write(f'<h2> Page number: ' + str(StartPostitionInTargetPDF+1) +'</h2>')  

                            f.write(f'<h2>' +diff +'</h2>')

                            StartPostitionInTargetPDF += 1;  

                        except Exception as e:   

                            f.write(f'<h2> page number: ' + str(StartPostitionInTargetPDF+1) +'- needs to be validated manually because of Exception :- '+str(e)+'</h2>')  

                    f.write('</body></html>')

                #     images1 = convert_from_path(FormTobeValidated)

                #     images2 = convert_from_path(TargetPDF)

                #     # Convert images to NumPy arrays

                #     array1 = np.array(images1[j].convert('RGB'))

                #     array2 = np.array(images2[StartPostitionInTargetPDF].convert('RGB'))

                #     StartPostitionInTargetPDF+=1

                #     # Compare arrays

                #     # Compare arrays

                #     difference = np.subtract(array1, array2)

                #     # Display original images and difference side by side

                #     fig, axs = plt.subplots(1, 3, figsize=(10, 10))


                #     # Display the first image

                #     im1 = axs[0].imshow(array1)

                #     axs[0].set_title('PDF 1')

                #     fig.colorbar(im1, ax=axs[0], orientation='horizontal')

                #     # Display the second image

                #     im2 = axs[1].imshow(array2)

                #     axs[1].set_title('PDF 2')

                #     fig.colorbar(im2, ax=axs[1], orientation='horizontal')

                #     # Display the difference

                #     im3 = axs[2].imshow(difference, cmap='coolwarm')

                #     axs[2].set_title('Difference')

                #     fig.colorbar(im3, ax=axs[2], orientation='horizontal')


                #     # Remove axis

                #     for ax in axs:

                #         ax.axis('off')

                #         # Convert the figure to HTML and add it to the HTML string

                #     html += mpld3.fig_to_html(fig)

                #         # Close the figure

                #     plt.close(fig)

                # html += '</body></html>\n'

                    # Write the HTML string to a file

                # with open(self.resultfile, 'w') as f:

                #     f.write(html)        

                self.result_label.setText('Given form is  compared with Traget PDF successfully. Please check the result file: '+self.resultfile)

            except Exception as e:

                self.result_label.setText('Error occurred while comparing PDFs: '+str(e))

    # def function3(self):

    #     # ...

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