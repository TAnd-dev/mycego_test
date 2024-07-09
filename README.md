# Test task for Mycego

## Overview
This project creates a collage from images stored in a public Yandex Disk folder and saves the collage as a TIFF file. The script fetches images from specified folders, processes them, and combines them into a single image.

## Prerequisites
Python 3.x

requests

Pillow

## Installation
Clone the repository or download the script.

Install the required Python libraries:
`pip install requests pillow`

## Configuration
The script uses a public key to access the Yandex Disk folder and fetch images from specified subfolders. Update the PUBLIC_KEY and test_folders variables as needed.

- PUBLIC_KEY: The public key of the Yandex Disk folder.
- test_folders: A list of folder names inside the Yandex Disk folder from which images will be fetched.

## Usage
- Update the PUBLIC_KEY and test_folders variables in the script with the appropriate values.
- Run the script:
`python script.py`

## Script Explanation
### Functions
- get_folders_path(public_key, necessary_folders)

Fetches the paths of specified folders inside the Yandex Disk folder.

Returns a list of folder paths.


- get_image_urls(public_key, path)

Fetches URLs of images from a specified folder path.

Returns a dictionary where the key is the image name and the value is the image URL.


- get_images(image_urls)

Downloads images from the provided URLs.

Returns a list of images as Pillow objects.


- create_tif(images)

Creates a collage from a list of images and saves it as a TIFF file.


- Main Function main()

Fetches the paths of the specified folders.

Fetches image URLs from each folder.

Downloads the images.

Creates a collage and saves it as Result.tif.
