import os

from i2p import *


if __name__ == "__main__":
    # get path
    folder_path = os.path.join('')
    # father folder's name
    base_file_name = os.path.basename(os.getcwd())

    print(f"{base_file_name} is been processing")

    convert_images_to_pdf(folder_path, output_path=f'{base_file_name}.pdf')
    pdf_compression(output_name=base_file_name)

    print(f"{base_file_name} has been processed")

