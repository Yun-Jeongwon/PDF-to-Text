# ! pip install PyMuPDF Pillow
# ! apt-get install poppler-utils --upgrade
# ! pip install pdf2image
# ! pip install easyocr
# ! pip install opencv-python-headless==4.5.4.60

# Flask로 받아와야할 부분
# file = 'TestPDF.pdf'

import fitz
import io
from PIL import Image
import sys
import os
import easyocr
from pdf2image import convert_from_path

fitz_pdf = fitz.open(file)
pdf = 'PDF.pdf'
all_text = []
n = len(fitz_pdf)

for i in range(n):
  page = fitz_pdf.load_page(i)
  text = page.get_text("text")
  all_text.append(text)
  for rect in text:
    annot = page.add_redact_annot(rect)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
fitz_pdf.save(pdf, garbage=3, deflate=True)

images = convert_from_path(pdf, fmt='png')
reader = easyocr.Reader(['en', 'ko'], gpu=False)

for i in range(n):
  img_byte_arr = io.BytesIO()
  images[i].save(img_byte_arr, format='png')
  img_byte_arr = img_byte_arr.getvalue()
  result = reader.readtext(img_byte_arr)
  for j in range(len(result)):
    all_text[i] = all_text[i] + result[j][1]
  
result_dict = {}
for i in range(len(all_text)):
  result_dict[i] = all_text[i]


# PDF to Text result
  
for i in range(len(result_dict)):
  print('\n\n 페이지 %d \n\n'%i)
  print(result_dict[i])

# word search

# target -> 사용자에게 입력받을 부분
# target = '수학'
index = -1
all_result = {} # 전체 결과값
result_page = [] # 해당 단어가 있는 페이지 리스트
for i in range(len(result_dict)):
  all_result[i] = []
  while True:
    index = result_dict[i].find(target, index + 1)
    if index == -1:
        break
    print('index=%d' % index)
    all_result[i].append(index)

for i in range(len(all_result.keys())):
  if all_result.get(i):
    result_page.append(i)