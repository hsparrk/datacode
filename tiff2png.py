from glob import glob

from PIL import Image

from tqdm import tqdm


files = glob('/mmdetection/data/spalling_images_tiff/*', recursive=True)



for file in tqdm(files):
    file_name = (file.split('/')[-1]).split('.')[0]
    img = Image.open(file)

    img.save(f'/mmdetection/data/spalling_images_png/{file_name}.png')