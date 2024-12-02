import sys, os
import pip._vendor.requests as requests
from tqdm import tqdm

name = '[Funabori Nariaki] Chokyo Soudanshitsu | 调教相谈室 [Chinese] [Digital]'
final = 212
id = 554479
formatt = 'jpg'

for i in tqdm(range(1, final + 1)):
    url = f'https://cdn.cartoonporn.to/nhentai/storage/images/{id}/{i}.{formatt}'
    
    try:
        r = requests.get(url)
        print(f'Status： {r}')
    except Exception as e:
        print(e)
        exit
    with open(f'd:\Akisamu\Desktop\output\{i}.jpg', 'wb') as out_file:
        out_file.write(r.content)

os.system('ptf')
os.system(f'rename "d:\Akisamu\Desktop\output\output.pdf" "{name}.pdf"')
os.system('del *.jpg output_lossless_compressed.pdf')
