import fitz
import textwrap

RESUME_TEXT = """
{{NAME}}
{{EMAIL}}
{{ADDRESS}}
{{PHONE}}

Objective:
{{OBJECTIVE}}

Eduaction:
{{EDUCATION}}

Experience:
{{EXPERIENCE}}

Projects:
{{PROJECTS}}

Skills:
{{SKILLS}}
"""

def GeneratePDF(Text: str) -> bytes:
    Text = textwrap.fill(Text, width=105, replace_whitespace=False)
    text = Text.split('\n')
    pdf_file = fitz.open()
    for i, line in enumerate(text):
        if i%40 == 0:
            page = pdf_file.new_page(-1)
            y = 0
        y += 20
        page.insert_text(fitz.Point(30,y), line)
    return pdf_file.tobytes()
