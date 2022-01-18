import os
import pathlib
from pathlib import Path
import threading
import random
images = []
memo_images1 = []
memo_images2 = []
memo_images = []
def image_creator():

    for image in os.listdir('picture'):
        path = Path(image)
        image_root = path.absolute().root

        images.append(image)

        extention_list = ['.JPG', '.PNG', '.GIF', '.TIFF', '.WEBP', '.INDD', '.erer', '.JPEG']
        for i in range(len(images)):
            try:
                extention_control = pathlib.Path(images[i]).suffix

                if extention_control.upper() in extention_list:
                    memo_image = f'picture{image_root}{os.path.basename(images[i])}'
                    if len(memo_images1) < 25 and memo_image not in memo_images1:
                        memo_images1.append(memo_image)
                    if len(memo_images2) < 25 and memo_image not in memo_images2:
                        memo_images2.append(memo_image)
                else:
                    pass
            except (RuntimeError, TypeError, NameError, IndexError, PIL.UnidentifiedImageError):
                pass

    random.shuffle(memo_images1)
    random.shuffle(memo_images2)
    memo_images = memo_images1 + memo_images2
    return memo_images








