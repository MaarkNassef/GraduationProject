import pytesseract
import fitz
from PIL import Image
import io
from resume_parser import resumeparse

def extract_text(file):
    pdf_file = fitz.open(stream=file, filetype='pdf')
    result = ''
    for page in pdf_file.pages():
        text = page.get_text('text')
        if len(text)>0:
            result += text+'\n'
            continue
        
        image_list = page.get_images()
        for image in image_list:
            xref = image[0]
            base_image = pdf_file.extract_image(xref)
            image_bytes = base_image["image"]
            img  = Image.open(io.BytesIO(image_bytes))

            pytesseract.pytesseract.tesseract_cmd=r'C:/Users/maark/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
            text=pytesseract.image_to_string(img)
            result += text

    return result

def get_skills(text: str):
    skills = resumeparse.extract_skills(text)
    return skills
