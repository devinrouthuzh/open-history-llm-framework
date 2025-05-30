# Import modules
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import Image
from os import listdir

import pandas as pd


# Import functions
def ocr(PDF_file, text_file):

    with TemporaryDirectory() as tempdir:
        
        pdf_pages = convert_from_path(
                PDF_file, 500, poppler_path=r"C:\poppler-23.08.0\Library\bin"
            )

        for page_enumeration, page in enumerate(pdf_pages, start=1):

            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
            page.save(filename, "JPEG")
            image_file_list.append(filename)

        with open(text_file, "a") as output_file:
            for image_file in image_file_list:

                text = str(((pytesseract.image_to_string(Image.open(image_file)))))
                text = text.replace("-\n", "")

                output_file.write(text)


# Read the file
input_file = sys.argv[1]
file_name, file_extension = os.path.splitext(input_file)


# Processing
out = f"{file_name}.txt"
image_file_list = []
ocr(input_file, text_file)


# Export the data
print(f"processed: {input_file}")
