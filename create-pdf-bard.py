import pdfkit
import qrcode
import glob

def generate_qr_code(text):
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )
  qr.add_data(text)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  return img

def create_pdf(qr_code_files):
  """Creates a PDF file with the given QR code files.

  Args:
    qr_code_files: A list of paths to QR code PNG files.
  """

  html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>QR Code Labels</title>
      </head>
      <body>
        <table style="width: 100%">
          <tr>
  """

  for qr_code_file in qr_code_files:
    with open(qr_code_file, "rb") as f:
      qr_code_bytes = f.read()

    html += f"""
              <td>
                <img src="{qr_code_bytes}" alt="QR Code">
              </td>
    """

  html += f"""
          </tr>
        </table>
      </body>
    </html>
  """

  pdfkit.from_string(html, "qr_code_labels.pdf")

if __name__ == "__main__":
  # Get a list of all of the QR code files in the qrcodes folder.
  qr_code_files = glob.glob("qrcodes/*.png")

  # Create a PDF file with the QR code files.
  create_pdf(qr_code_files)
