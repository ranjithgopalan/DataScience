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
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image, ImageDraw, ImageFont
 
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
        FormTobeValidated = self.file1
        TargetPDF=  self.file2
        image1 = convert_from_path(FormTobeValidated)
        image2 = convert_from_path(TargetPDF)
        PDF1Count = len(PyPDF2.PdfReader(FormTobeValidated).pages)
        PDF2Count = len(PyPDF2.PdfReader(TargetPDF).pages)
        try:
            if PDF1Count > PDF2Count:
                for i in range(PDF1Count):
                    # Convert images to NumPy arrays
                    images1 = []  # Define the variable "images1"
                    array1 = np.array(images1[i].convert('RGB'))
                    if i > len(image2):            
                        array2 = np.zeros_like(array1)
                    else:
                        array2 = np.array(images1[2].convert('RGB'))
                    try:
                        border_size = 10
                        img1 = self.add_gradient_border(image1[j], border_size)
                        img2 = self.add_gradient_border(image2[j], border_size)
                        # Convert the images to grayscale
                        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                        # Compute the absolute difference between the images
                        diff = cv2.absdiff(img1_gray, img2_gray)
                               
                        # Apply a binary threshold to the difference (this will highlight the differences)
                        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                               
                        # Find contours in the threshold image
                        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                               
                        # Draw the contours on the original images
                        cv2.drawContours(img1, contours, -1, (0,255,0), 3)
                        cv2.drawContours(img2, contours, -1, (0,255,0), 3)
                               
                        # Create a PDF file
                        pdf = PdfPages('output.pdf')
                        # Create a figure
                        fig = plt.figure(figsize=(20,10))
                           
                        # Set a larger font size for the titles
                        plt.rcParams.update({'font.size': 22})
                           
                        # Check if there are any differences
                        if np.any(thresh):
                            # There are differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            plt.subplot(1,3,3), plt.imshow(thresh, cmap='gray'), plt.title('Differences')
                        else:
                            # There are no differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            # Create an image with the text "No differences"
                            img = Image.new('RGB', (img1.shape[1], img1.shape[0]), color = (73, 109, 137))
                            d = ImageDraw.Draw(img)
                            fnt = ImageFont.truetype('imagevalidation/imagevalidation_view/src/components/michaelmarker-lite.ttf', 15)
                            d.text((10,10), "No differences", font=fnt, fill=(255, 255, 255))
                            plt.subplot(1,3,3), plt.imshow(img), plt.title('Differences')
                   
                            # Add a title to the figure
                            plt.suptitle('Image Comparison', fontsize=30)
   
                            # Save the figure to the PDF
                            pdf.savefig(fig)
                    except Exception as e:  
                        pdf.attach_note('page number: ' + str(j+1) +'- needs to be validated manually because of Exception :- '+str(e))  
                # Close the PDF file
                pdf.close()
            elif PDF1Count < PDF2Count:
                for j in range(PDF2Count):
                    # Convert images to NumPy arrays
                    array2 = np.array(images2[i].convert('RGB'))
                    if i > len(images1):            
                        array1 = np.zeros_like(array2)
                    else:
                        array1 = np.array(images1[i].convert('RGB'))
                    try:
                        border_size = 10
                        img1 = self.add_gradient_border(image1[j], border_size)
                        img2 = self.add_gradient_border(image2[j], border_size)
                        # Convert the images to grayscale
                        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                        # Compute the absolute difference between the images
                        diff = cv2.absdiff(img1_gray, img2_gray)
                               
                        # Apply a binary threshold to the difference (this will highlight the differences)
                        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                               
                        # Find contours in the threshold image
                        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                               
                        # Draw the contours on the original images
                        cv2.drawContours(img1, contours, -1, (0,255,0), 3)
                        cv2.drawContours(img2, contours, -1, (0,255,0), 3)
                               
                        # Create a PDF file
                        pdf = PdfPages('output.pdf')
                        # Create a figure
                        fig = plt.figure(figsize=(20,10))
                           
                        # Set a larger font size for the titles
                        plt.rcParams.update({'font.size': 22})
                           
                        # Check if there are any differences
                        if np.any(thresh):
                            # There are differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            plt.subplot(1,3,3), plt.imshow(thresh, cmap='gray'), plt.title('Differences')
                        else:
                            # There are no differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            # Create an image with the text "No differences"
                            img = Image.new('RGB', (img1.shape[1], img1.shape[0]), color = (73, 109, 137))
                            d = ImageDraw.Draw(img)
                            fnt = ImageFont.truetype('imagevalidation/imagevalidation_view/src/components/michaelmarker-lite.ttf', 15)
                            d.text((10,10), "No differences", font=fnt, fill=(255, 255, 255))
                            plt.subplot(1,3,3), plt.imshow(img), plt.title('Differences')
                   
                            # Add a title to the figure
                            plt.suptitle('Image Comparison', fontsize=30)
   
                            # Save the figure to the PDF
                            pdf.savefig(fig)
                    except Exception as e:  
                        pdf.attach_note('page number: ' + str(j+1) +'- needs to be validated manually because of Exception :- '+str(e))  
                # Close the PDF file
                pdf.close()  
            else:
                for j in range(PDF1Count):
                    try:
                        border_size = 10
                        img1 = self.add_gradient_border(image1[j], border_size)
                        img2 = self.add_gradient_border(image2[j], border_size)
                        # Convert the images to grayscale
                        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                        # Compute the absolute difference between the images
                        diff = cv2.absdiff(img1_gray, img2_gray)
                               
                        # Apply a binary threshold to the difference (this will highlight the differences)
                        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                               
                        # Find contours in the threshold image
                        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                               
                        # Draw the contours on the original images
                        cv2.drawContours(img1, contours, -1, (0,255,0), 3)
                        cv2.drawContours(img2, contours, -1, (0,255,0), 3)
                               
                        # Create a PDF file
                        pdf = PdfPages('output.pdf')
                        # Create a figure
                        fig = plt.figure(figsize=(20,10))
                           
                        # Set a larger font size for the titles
                        plt.rcParams.update({'font.size': 22})
                           
                        # Check if there are any differences
                        if np.any(thresh):
                            # There are differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            plt.subplot(1,3,3), plt.imshow(thresh, cmap='gray'), plt.title('Differences')
                        else:
                            # There are no differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            # Create an image with the text "No differences"
                            img = Image.new('RGB', (img1.shape[1], img1.shape[0]), color = (73, 109, 137))
                            d = ImageDraw.Draw(img)
                            fnt = ImageFont.truetype('imagevalidation/imagevalidation_view/src/components/michaelmarker-lite.ttf', 15)
                            d.text((10,10), "No differences", font=fnt, fill=(255, 255, 255))
                            plt.subplot(1,3,3), plt.imshow(img), plt.title('Differences')
                   
                            # Add a title to the figure
                            plt.suptitle('Image Comparison', fontsize=30)
   
                            # Save the figure to the PDF
                            pdf.savefig(fig)
                    except Exception as e:  
                        pdf.attach_note('page number: ' + str(j+1) +'- needs to be validated manually because of Exception :- '+str(e))  
                # Close the PDF file
                pdf.close()
        # return 'Error occurred while comparing PDFs: '+str(e)    
        except Exception as e:
            self.result_label.setText('Error occurred while comparing PDFs: '+str(e))      
           
    def add_gradient_border(input_image, border_size):
        row, col = input_image.shape[:2]
        border_img = cv2.copyMakeBorder(input_image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=[0,0,0])
        for i in range(border_size):
            color = int(255 * (i / border_size))  # gradient from black to white
            border_img[i:i+1, :] = color
            border_img[:, i:i+1] = color
            border_img[row+2*i:row+2*(i+1), :] = color
            border_img[:, col+2*i:col+2*(i+1)] = color
        return border_img
 
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
                # Load the images
                # img1 = cv2.imread('2ndpage1.png')
                # img2 = cv2.imread('page1.png')
                image1 = convert_from_path(FormTobeValidated)
                image2 = convert_from_path(TargetPDF)
                # Add gradient borders to the images
                for j in range(PDF1Count):
                    try:
                        border_size = 10
                        img1 = self.add_gradient_border(image1[j], border_size)
                        img2 = self.add_gradient_border(image2[StartPostitionInTargetPDF], border_size)
                        # Convert the images to grayscale
                        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                        # Compute the absolute difference between the images
                        diff = cv2.absdiff(img1_gray, img2_gray)
                           
                        # Apply a binary threshold to the difference (this will highlight the differences)
                        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
                           
                        # Find contours in the threshold image
                        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                           
                        # Draw the contours on the original images
                        cv2.drawContours(img1, contours, -1, (0,255,0), 3)
                        cv2.drawContours(img2, contours, -1, (0,255,0), 3)
                           
                        # Create a PDF file
                        pdf = PdfPages('output.pdf')
                         # Create a figure
                        fig = plt.figure(figsize=(20,10))
                       
                        # Set a larger font size for the titles
                        plt.rcParams.update({'font.size': 22})
                       
                        # Check if there are any differences
                        if np.any(thresh):
                            # There are differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            plt.subplot(1,3,3), plt.imshow(thresh, cmap='gray'), plt.title('Differences')
                        else:
                            # There are no differences
                            plt.subplot(1,3,1), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)), plt.title('Image 1')
                            plt.subplot(1,3,2), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)), plt.title('Image 2')
                            # Create an image with the text "No differences"
                            img = Image.new('RGB', (img1.shape[1], img1.shape[0]), color = (73, 109, 137))
                            d = ImageDraw.Draw(img)
                            fnt = ImageFont.truetype('imagevalidation/imagevalidation_view/src/components/michaelmarker-lite.ttf', 15)
                            d.text((10,10), "No differences", font=fnt, fill=(255, 255, 255))
                            plt.subplot(1,3,3), plt.imshow(img), plt.title('Differences')
               
                        # Add a title to the figure
                        plt.suptitle('Image Comparison', fontsize=30)
 
                        # Save the figure to the PDF
                        pdf.savefig(fig)
                    except Exception as e:  
                        pdf.attach_note('page number: ' + str(StartPostitionInTargetPDF+1) +'- needs to be validated manually because of Exception :- '+str(e))  
                # Close the PDF file
                pdf.close()
               
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