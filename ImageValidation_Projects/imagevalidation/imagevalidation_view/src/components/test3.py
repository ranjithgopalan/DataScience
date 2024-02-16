import fitz

# Open the PDF file
doc = fitz.open('imagevalidation/imagevalidation_view/Data/0021435255_000_20240531_NEW.PDF')

for i in range(len(doc)):
    # Load the page
    page = doc.load_page(i)
    
    # Render the page to a pixmap (an image)
    pix = page.get_pixmap()
    
    # Save the pixmap to a file
    pix.save(f'2ndpage{i}.png')