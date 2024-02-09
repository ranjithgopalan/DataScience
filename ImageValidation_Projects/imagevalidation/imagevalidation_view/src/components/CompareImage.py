import PyPDF2
import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import mpld3
from PyPDF2 import PdfReader
import difflib

# Convert PDFs to images
images1 = convert_from_path('imagevalidation/imagevalidation_view/Data/0021435254_000_20240630_NEW.PDF')
images2 = convert_from_path('imagevalidation/imagevalidation_view/Data/0021435255_000_20240531_NEW.PDF')



def ImageCompareForRegression(images1,images2): 
    # Create an HTML page with the comparison images
    html = '<html><body>\n'
    if len(images1) > len(images2):
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
            html += mpld3.fig_to_html(fig)
            # Close the figure    
            plt.close(fig)
        html += '</body></html>\n'

        # Write the HTML string to a file
        with open('comparison.html', 'w') as f:
            f.write(html)
            
    elif len(images1) < len(images2):
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

        # Write the HTML string to a file
        with open('comparison.html', 'w') as f:
            f.write(html)
    else:    
        for i in range(len(images1)):
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

        # Write the HTML string to a file
        with open('comparison.html', 'w') as f:
            f.write(html)

FormName = '0021435254_000_20240630_NEW.PDF'
TotalNumberOfPages = 1
StartPostitionInTargetPDF=44
def validFormInDcoument(FormTobeValidated,FormName,FormPages,TargetPDF): 
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
        return "Form not found in Target PDF"       

    for j in range(PDF1Count):
        pdf1_text = PyPDF2.PdfReader(FormTobeValidated).pages[j].extract_text()
        pdf2_text = PyPDF2.PdfReader(TargetPDF).pages[StartPostitionInTargetPDF].extract_text()
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
    with open('comparison.html', 'w') as f:
        f.write(html)

