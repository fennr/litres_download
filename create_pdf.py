import os
from PIL import Image
from config import BOOK_NAME, BOOK_ID

path_to_folder = f"books/{BOOK_NAME}_{BOOK_ID}"
folder = os.listdir(path_to_folder)

folder = sorted(folder, key=lambda x: int(os.path.splitext(x)[0]))

images = []
for file in folder:
    images.append(f"{path_to_folder}/{file}")

print(images)

f_image = Image.open(images[0]).convert('RGB')
print(f"add page {images[0]}")

o_images = []
for image_path in images[1:]:
    img = Image.open(image_path).convert('RGB')
    o_images.append(img)
    print(f"add page {image_path}")

print("create pdf...")

output_path = f"books/{BOOK_NAME}_{BOOK_ID}.pdf"
f_image.save(output_path, save_all=True, append_images=o_images)

print("finish")
