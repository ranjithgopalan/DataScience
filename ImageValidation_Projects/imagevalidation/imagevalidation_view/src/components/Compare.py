# import fitz
import wand
import os
from PIL import Image
pdf1 = fitz.open("file1.pdf")
pdf2 = fitz.open("file2.pdf")

# extract all images from page 1 of both PDFs
page1_img1 = pdf1[0].get_image(dpi=300)
page1_img2 = pdf2[0].get_image(dpi=300)

# save images
page1_img1.save("page1_img1.png")
page1_img2.save("page1_img2.png")


def pdf_to_image(pdf_path, page_num):
    os.system(f"pdftoppm -gray -png -r 300 {pdf_path} output")
    return wand.Image(filename=f"output-{page_num}.png")


def comparePixels(file1_img1, file2_img1):
    diff_count = 0
    for x in range(300):
        for y in range(400):
            if file1_img1.getpixel((x, y)) != file2_img1.getpixel((x, y)):
                diff_count += 1

    print(f"Number of different pixels: {diff_count}")


file1_img1 = pdf_to_image("C:/Users/ranji/OneDrive/H1B Extension_21_March 2024/H1B Extension_21_March 2024/H4 Extension/I539/i-539A_Rithikesh R.pdf", 1)
file2_img2 = pdf_to_image("C:/Users/ranji/OneDrive/H1B Extension_21_March 2024/H1B Extension_21_March 2024/H4 Extension/I539/i-539A_Rithikesh RCopy.pdf", 1)
comparePixels(file1_img1, file2_img2)