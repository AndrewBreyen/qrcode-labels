from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os

# Define the folder containing your QR code PNG files
qr_code_folder = 'qrcodes'

# Define the output PDF file name
output_pdf = 'output.pdf'

# Define the number of columns and rows for your label sheet
columns = 6
rows = 5  # Adjust as needed

# Calculate label width and height based on Avery 8640 label dimensions
label_width = 2.625 * inch  # 2.625 inches
label_height = 1 * inch    # 1 inch

# Create a PDF document
doc = SimpleDocTemplate(output_pdf, pagesize=letter)

# Initialize a list to store table elements
elements = []

# Loop through the PNG files in the folder and add them to the PDF
qr_code_files = [filename for filename in os.listdir(qr_code_folder) if filename.endswith('.png')]

# Calculate the number of labels per page
labels_per_page = columns * rows

# Divide the QR codes into pages with labels
for page_start in range(0, len(qr_code_files), labels_per_page):
    page_end = page_start + labels_per_page
    qr_codes_on_page = qr_code_files[page_start:page_end]

    # Create a 2D list to hold QR code images arranged in rows and columns
    qr_code_matrix = []
    for i in range(rows):
        row_start = i * columns
        row_end = row_start + columns
        qr_code_row = []
        for j in range(row_start, row_end):
            if j < len(qr_codes_on_page):
                qr_code_path = os.path.join(qr_code_folder, qr_codes_on_page[j])
                img = Image.open(qr_code_path)
                img = img.resize((int(label_width), int(label_height)))
                qr_code_row.append(img)
            else:
                qr_code_row.append('')  # Empty cell for labels without QR codes
        qr_code_matrix.append(qr_code_row)

    # Create a table to hold the QR code images
    table = Table(qr_code_matrix, colWidths=label_width, rowHeights=label_height)

    # Style the table (optional)
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table.setStyle(style)

    # Add the table to the list of elements
    elements.append(table)

# Build the PDF document
doc.build(elements)

print(f'PDF file "{output_pdf}" has been created with QR codes.')
