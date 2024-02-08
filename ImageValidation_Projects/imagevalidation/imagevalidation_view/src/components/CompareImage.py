import numpy as np
from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import mpld3

# Convert PDFs to images
images1 = convert_from_path('imagevalidation/imagevalidation_view/Data/0021435254_000_20240630_NEW.PDF')
images2 = convert_from_path('imagevalidation/imagevalidation_view/Data/0021435255_000_20240531_NEW.PDF')


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