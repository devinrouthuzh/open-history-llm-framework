# Import modules
import os
import sys
from doctr.io import DocumentFile
from doctr.models import ocr_predictor


# Read the file
input_file = sys.argv[1]
file_name, file_extension = os.path.splitext(input_file)

doc = DocumentFile.from_pdf(input_file)


# Processing
# Instantiate a pretrained model
predictor = ocr_predictor(pretrained=True)

# Run the model - per document!
result = predictor(doc)


# Export the data
string_result = result.render()

output_file = f"{file_name}.txt"
with open(output_file, "w") as file:
    file.write(string_result)

print(f"processed: {input_file}")
