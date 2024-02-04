import difflib
from pdf2image import convert_from_path
from PIL import ImageChops
import PyPDF2

def getfile(pdf1_path, pdf2_path):
        # Open the PDF files in read binary mode
    with open(pdf1_path, 'rb') as file1, open(pdf2_path, 'rb') as file2:
        # Create PdfFileReader objects
        pdf_reader1 = PyPDF2.PdfReader(file1)
        pdf_reader2 = PyPDF2.PdfReader(file2)

    # Step 3: Generate HTML report
def generate_html_report(differences, report_path):
    with open(report_path, 'w') as f:
        f.write('<html><body>')
        for i, diff in enumerate(differences):
            diff.save(f'diff{i}.png')
            f.write(f'<img src="diff{i}.png" /><br/>')
        f.write('</body></html>')

def compare_pdfs(pdf1_path, pdf2_path):
    # # Convert PDFs to images
    images1 = convert_from_path(pdf1_path)
    images2 = convert_from_path(pdf2_path)

    # Compare images
    differences = []
    for img1, img2 in zip(images1, images2):
        diff = ImageChops.difference(img1, img2)

        if diff.getbbox():
            differences.append(diff)
            print("Images are different")
    generate_html_report(differences, 'ImageReport.html')

    # Generate HTML report of text differences   
    PDF1Count = len(PyPDF2.PdfReader(pdf1_path).pages)
    PDF2Count = len(PyPDF2.PdfReader(pdf2_path).pages)
    if PDF1Count != PDF2Count:
        print("PDFs are different")
        textdifference = []
        with open('Textdiff.html', 'w') as f:
            f.write('<html><body>')
            for i in range(PDF2Count):
                pdf1_text = PyPDF2.PdfReader(pdf1_path).pages[i].extract_text()
                pdf2_text = PyPDF2.PdfReader(pdf2_path).pages[i].extract_text()
                diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())
                textdifference.append(diff)
                f.write(f'<h2>' +diff +'</h2>')               
            f.write('</body></html>')
    else:

        print("PDFs are same")
        textdifference = []
        with open('Textdiff.html', 'w') as f:
            f.write('<html><body>')
            for i in range(24,PDF1Count):
                page = PyPDF2.PdfReader(pdf1_path).pages[i]

                if PyPDF2.PdfReader(pdf1_path).pages[i].extract_text() is not None:
                    print("Move further")
                    pdf1_text = PyPDF2.PdfReader(pdf1_path).pages[i].extract_text()
                pdf2_text = PyPDF2.PdfReader(pdf2_path).pages[i].extract_text()
                diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())
                textdifference.append(diff)
                f.write(f'<h2>' +diff +'</h2>')               
            f.write('</body></html>')
                       
                
        # # Convert PDFs to text
    # pdf1_text = PyPDF2.PdfReader(pdf1_path).pages[1].extract_text()
    # pdf2_text = PyPDF2.PdfReader(pdf2_path).pages[1].extract_text()

    # # Compare text
    # diff = difflib.HtmlDiff().make_file(pdf1_text.splitlines(), pdf2_text.splitlines())

    # # Write diff to HTML file
    # with open('Textdiff.html', 'w') as f:
    #     f.write(diff)

   



compare_pdfs('imagevalidation/imagevalidation_view/Data/0021435254_000_20240630_NEW.PDF','imagevalidation/imagevalidation_view/Data/0021435255_000_20240531_NEW.PDF')