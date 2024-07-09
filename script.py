import math
from io import BytesIO

import requests
from urllib.parse import urlencode

from PIL import Image

# API яндекса
API_YANDEX = 'https://cloud-api.yandex.net/v1/disk/public/resources?'
# публичный ключ папки
PUBLIC_KEY = 'mRF/yMmlepx5vbO46zgC7rq4DmcX+fuJJjO29/wuZxAl11johIbtn0F+nr7uFpWEsLK2WbwBkR//qfmVHoPilw=='


# Получение путей до необходимых папок. Возвращается список с путями до папок
def get_folders_path(public_key, necessary_folders: list) -> list[str]:
    url = urlencode(dict(public_key=public_key, path='/'))
    response = requests.get(API_YANDEX + url)
    result = []

    if response.status_code != 200:
        print(f'Error: status code: {response.status_code}')
        return result

    folders = response.json()['_embedded']['items']
    for folder in folders:
        if folder['type'] == 'dir' and folder['name'] in necessary_folders:
            result.append(folder['path'])

    return result


# Получение ссылок на картинки из папки. Возвращается словарь, в котором ключом является имя, а значением ссылка
def get_image_urls(public_key, path: str) -> dict:
    url = urlencode(dict(public_key=public_key, path=path))
    response = requests.get(API_YANDEX + url)
    images = response.json()['_embedded']['items']
    result = {image['name']: image['sizes'][0]['url'] for image in images}
    return result


# Получение картинок по ссылкам. Возвращается список с картинками Pillow
def get_images(image_urls: dict) -> list:
    images = []
    for name, url in image_urls.items():
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        images.append(img)
    return images


def create_tif(images: list) -> None:
    img_width_height = 192
    image_distance = 24

    num_images = len(images)

    start_x = x = 74
    y = 96

    num_rows = math.ceil(num_images / 4)

    collage_width = 1000 if num_images >= 4 else img_width_height * num_images + x * 2 + (num_images - 1) * image_distance
    collage_height = img_width_height * num_rows + y * 2 + (num_rows - 1) * image_distance

    collage = Image.new('RGB', (collage_width, collage_height), color='white')

    for i, img in enumerate(images):
        img.thumbnail((img_width_height, img_width_height))
        collage.paste(img, (x, y))
        if (i + 1) % 4 == 0:
            x = start_x
            y += img_width_height + image_distance
        else:
            x += img_width_height + image_distance

    collage.save('Result.tif', format='TIFF')
    print('Image saved successfully (Result.tif)')


def main():
    test_folders = ['1388_6_Наклейки 3-D_2']
    folder_paths = get_folders_path(PUBLIC_KEY, test_folders)
    all_images = {}
    for folder in folder_paths:
        images = get_image_urls(PUBLIC_KEY, folder)
        all_images.update(images)

    images = get_images(all_images)
    create_tif(images)


if __name__ == '__main__':
    main()
