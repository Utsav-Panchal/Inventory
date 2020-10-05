from base64 import b64encode


def conversion_image_into_bs64(file_location):
    with open(f"{file_location}", "rb") as img_file:
        img_file = b64encode(img_file.read())
    return img_file
