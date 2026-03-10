import os
from PIL import Image

media_dir = 'media/item_images'
for f in os.listdir(media_dir):
    if f.endswith('.jpg'):
        try:
            Image.open(os.path.join(media_dir, f))
            print(f'{f}: OK')
        except Exception as e:
            print(f'{f}: INVALID - {e}')