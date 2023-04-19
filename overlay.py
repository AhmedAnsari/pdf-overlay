"""
This script takes two pages from a PDF document specified by the user and overlays them using OpenCV. The resulting image is then added to a new PDF document and saved to the same directory as the input PDF file with "_overlayed" added to the file name.

The input PDF file path and the page numbers of the two pages to be overlaid are passed as command line arguments. The output PDF file is created using the FPDF library.

This script requires the following libraries to be installed:

fitz
numpy
fpdf
opencv-python-headless
pillow
Usage:
python overlay_pdf_pages.py input_file_path page_number1 page_number2

Where:

input_file_path: the file path of the input PDF document
page_number1: the page number of the first page to be overlaid
page_number2: the page number of the second page to be overlaid
"""
import cv2
import fitz
import numpy as np
from fpdf import FPDF
import os
import argparse
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description='Overlay two pages of a PDF document.')
    parser.add_argument('input_file_path', help='Input PDF file path')
    parser.add_argument('page1', type=int, help='Page number of the first page to be overlaid')
    parser.add_argument('page2', type=int, help='Page number of the second page to be overlaid')
    args = parser.parse_args()

    doc = fitz.open(args.input_file_path)
    page1 = doc.load_page(args.page1)
    page2 = doc.load_page(args.page2)

    # Convert the pages to OpenCV images
    img1 = np.frombuffer(page1.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), alpha=False).samples, dtype=np.uint8)
    img1 = img1.reshape(page1.get_pixmap(matrix=fitz.Matrix(300/72, 300/72)).height, page1.get_pixmap(matrix=fitz.Matrix(300/72, 300/72)).width, 3)
    img2 = np.frombuffer(page2.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), alpha=False).samples, dtype=np.uint8)
    img2 = img2.reshape(page2.get_pixmap(matrix=fitz.Matrix(300/72, 300/72)).height, page2.get_pixmap(matrix=fitz.Matrix(300/72, 300/72)).width, 3)

    print("Image 1 shape:", img1.shape)
    print("Image 2 shape:", img2.shape)

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    # Add the two images together using OpenCV
    result = cv2.min(img1, img2)
    print("Result shape:", result.shape, "dtype:", result.dtype)

    # Create instance of FPDF class
    pdf = FPDF(unit='pt', format='a4')

    # Add new page
    pdf.add_page()

    # Convert OpenCV image to PIL image and add to PDF
    pil_image = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(pil_image)

    # Create the output file path in the same directory as the input file
    output_dir = os.path.dirname(args.input_file_path)
    # Get the file name without the extension
    file_name = os.path.splitext(os.path.basename(args.input_file_path))[0]
    output_path = os.path.join(output_dir, file_name + "_olayed.pdf")

    cv2.imwrite("temp.png", result)
    pdf.image("temp.png", x=0, y=0, w=595.276, h=841.89)

    # Save the PDF to the output path
    pdf.output(output_path, 'F')

    # Remove the temporary image file
    os.remove("temp.png")

if __name__ == '__main__':
    main()
