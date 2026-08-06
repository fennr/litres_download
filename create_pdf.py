import os
from PIL import Image
from config import BOOK_NAME, BOOK_ID

path_to_folder = f"books/{BOOK_NAME}_{BOOK_ID}"
folder = os.listdir(path_to_folder)

folder = sorted(folder, key=lambda x: int(os.path.splitext(x)[0]))

images = []
for file in folder:
    images.append(f"{path_to_folder}/{file}")

f_image = Image.open(images[0]).convert('RGB')
print(f"\radd page {images[0]}", end="", flush=True)

def image_generator():
    for image_path in images[1:]:
        print(f"\radd page {image_path}", end="", flush=True)
        yield Image.open(image_path).convert('RGB')

output_path = f"books/{BOOK_NAME}_{BOOK_ID}.pdf"

f_image.save(output_path, save_all=True, append_images=image_generator())
f_image.close()

print("\nfinish")
