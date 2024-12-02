import os
import reportlab
import re
from tqdm import tqdm
import numpy as np
from natsort import natsorted
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO

image_formate = ('.jpg', '.png', '.jpeg', '.webp')


def convert_images_to_pdf(folder_path, output_path):
    # 获取文件夹内所有图片文件的路径
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(image_formate)]
    image_files = natsorted(image_files)
    # print(image_files)
    letter = None
    w, h = 1, 1
    for p in image_files:
        letter = Image.open(p).size
        if letter[0] < w:
            letter = (w, letter[1])
        if letter[1] < h:
            letter = (letter[0], h)
        w, h = letter
    print(f"canvas size = {letter}")
    # 创建一个新的PDF文件
    c = canvas.Canvas(output_path, pagesize=letter)
    # reportlab.rl_config.invariant = 1

    for image_file in tqdm(image_files):
        # 打开并调整图像大小以适应PDF页面
        image = Image.open(image_file)
        image_width, image_height = image.size
        print(f"original size = ({image_width}, {image_height})")
        pdf_width, pdf_height = letter
        aspect_ratio = image_width / float(image_height)
        image_width = int(pdf_width if pdf_width < pdf_height else aspect_ratio * pdf_height)
        image_height = int(pdf_height if pdf_height < pdf_width else image_width / aspect_ratio)
        image = image.resize((image_width, image_height))

        # 将Pillow的图像对象转换为ImageReader对象
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        image_reader = ImageReader(image_io)

        # 将图像添加到PDF页面
        print(f"fixed size = ({image_width}, {image_height})")
        c.drawImage(image_reader, 0, 0, width=image_width, height=image_height)

        # 在下一页绘制
        c.showPage()

    # 保存并关闭PDF文件
    c.save()


def pdf_compression(output_name) -> None:
    reader = PdfReader(f"{output_name}.pdf")
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)

    with open(f"{output_name}_lossless_compressed.pdf", "wb") as f:
        writer.write(f)



