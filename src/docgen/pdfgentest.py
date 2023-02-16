# importing modules
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
import os

from brainflow.board_shim import BoardShim

def generate_report(
    dir_path:str=None,
    font_dir:str=None,
    subjectName:str="default",
    bandpowers:list=None,
    bandpowers_normalize:list=None,
    subjectfilepath:str=None,
    desc:str=None,
    boardID:int=None
):
    if dir_path is None: dir_path = os.path.dirname(os.path.realpath(__file__))
    if font_dir is None: font_dir = dir_path
    print("\nGenerating Report\n")
    fileName = dir_path+os.sep+f'{subjectName}_report.pdf'
    documentTitle = subjectName+"_report"

    title = 'Union Neurotech 2023'
    subTitle = 'Thinking About U: Brain Generated Abstract Imagery Prototype'
    logo = dir_path+os.sep+'logo.png'

    # define some parameters
    MARGIN = 36.0   
    page_edge_horizontal = letter[0]
    page_edge_vertical = letter[1]
    page_margin_left = MARGIN
    page_margin_right = page_edge_horizontal - MARGIN
    page_margin_bottom = MARGIN
    page_margin_top = page_edge_vertical - MARGIN

    # creating a pdf object
    pdf = canvas.Canvas(fileName, pagesize=letter)

    # Set the title
    pdf.setTitle(documentTitle)

    # registering a external font in python
    pdfmetrics.registerFont(
        TTFont('Timeless', font_dir+os.sep+'Timeless.ttf')
    )
    pdfmetrics.registerFont(
        TTFont('Timelessbd', font_dir+os.sep+'Timeless-Bold.ttf')
    )

    # creating the title by setting it's font 
    # and putting it on the canvas
    pdf.setFont('Timelessbd', 44)
    pdf.drawString(120, 715, title)
    # drawing a logo
    pdf.drawInlineImage(logo, 40, 700, width=60, height=60)

    # creating the subtitle by setting it's font, 
    # colour and putting it on the canvas
    # pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Timelessbd", 18)
    pdf.drawCentredString(300, 670, subTitle)

    def draw_divider(y):
    # drawing a line - divider
        pdf.line(page_margin_left, y, page_margin_right, y)
    draw_divider(660)

    content = [
        f"Name: {subjectName}"
    ]

    if desc is not None: content.append(f"Description: {desc}")
    if boardID is not None:
        boardinfo = BoardShim.get_board_descr(boardID)
        boardname = boardinfo["name"]
        boardchannels = boardinfo["eeg_names"]
        content.append(f"Device Model: {boardname}")
        content.append(f"Device Channels: {boardchannels}")

    # creating a multiline text using
    # textline and for loop
    text = pdf.beginText(page_margin_left, 620)
    text.setFont("Timeless", 20)
    
    for line in content:
        text.textLine(line)
        
    pdf.drawText(text)

    # Put brainwaves infographic
    brainwaves_info = dir_path+os.sep+"brainwaves.png"
    pdf.drawInlineImage(brainwaves_info, page_margin_right-200, 400, width=200, height=250)

    
    
    # saving the pdf
    pdf.save()

    print("\nDone!\n")
    print(f"Report is available at {fileName}")


if __name__ == "__main__":
    generate_report(subjectName="Leonardo", desc="A cat", boardID=22)