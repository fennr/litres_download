from fpdf import FPDF
import os
from config import BOOK_NAME, BOOK_ID

pdf = FPDF()
folder = os.listdir(f"{BOOK_NAME}_{BOOK_ID}")
folder = sorted(folder, key=lambda x: int(os.path.splitext(x)[0]))
images = []

for file in folder:
    images.append(f"{BOOK_NAME}_{BOOK_ID}/{file}")

print(images)

for image in images:
    pdf.add_page()
    pdf.image(image, 0, 0, 210, 297)
    print(f"add page {image}")
print("create pdf...")
pdf.output(f"{BOOK_NAME}_{BOOK_ID}.pdf", "F")

print("finish")
