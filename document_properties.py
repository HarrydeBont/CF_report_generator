from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth

page_width, page_height = A4                # unit is pixels
page_width_pxl, page_height_pxl = A4        # dirty solution (resolve later)
page_width_mm, page_height_mm = (210,297)   # unit is mm
mm_per_pixel = page_width_mm/page_width     # unit is mm/pixel

def document_canvas(_c:object):
    global canvas_recursive
    canvas_recursive = _c

def get_document_canvas():
    global canvas_recursive
    return canvas_recursive

def document_size():
    global page_width_pxl, page_height_pxl
    page_width_pxl, page_height_pxl = A4
    return page_width_pxl, page_height_pxl

def get_margin():
    global margin
    margin = 25/mm_per_pixel                 # set margin to xx mm unit is pixels
    return margin

def top_of_page():
    global x, y
    x = get_margin()
    y = page_height - get_margin()

def Titel_top_of_page():
    """Move cursor to top of the page for placement of the titel. Sets x = margin, y = 2 * margin"""
    global x, y
    x = get_margin()
    y = page_height - 2*get_margin()

def pos_x():
    global x
    return x

def pos_y():
    global y
    return y

def move_cursor_to_right(dx):
    global x
    x = x + dx
    return x

def move_cursor_to_position(_x):
    global x
    x = _x

def move_cursor_to_y_position(_y_coordinate):
    global y
    y = _y_coordinate


def cursor_at_margin():
    global x
    x = get_margin()

def break_to_new_line(_nr_of_lines:int = 1):
    global x,y
    x = get_margin()
    y = y - _nr_of_lines * get_line_height()
    return x, y

def center(text):
    """ Calculate center x starting position for a given text (without code)
    """
    text_width = stringWidth(text, get_font_setting(), get_font_size())
    center_pos = (page_width - text_width)/2
    move_cursor_to_position(center_pos)
    return center_pos

def get_line_height():
    global line_height
    return line_height

def set_line_height(_font_size):
    global line_height
    line_height = 1.5 * _font_size
    return line_height

def get_remaining_space_on_line():
    remaining_space_on_line = page_width_pxl - pos_x() - get_margin()
    return remaining_space_on_line

def normal_font():
    global font_setting
    font_setting = 'Helvetica'
    return ''

def font_bold():
    global font_setting
    match font_setting:
        case 'Helvetica': font_setting = 'Helvetica-Bold'
        case 'Helvetica-Oblique': font_setting = 'Helvetica-BoldOblique'
    return ''

def set_italic():
    global font_setting
    match font_setting:
        case 'Helvetica': font_setting = 'Helvetica-Oblique'
        case 'Helvetica-Bold' : font_setting = 'Helvetica-BoldOblique'
    return ''

def get_font_setting():
    global font_setting
    return font_setting

def does_word_fit_on_line_within_the_margins(word):
    if stringWidth(word,get_font_setting(),get_font_size()) < get_remaining_space_on_line():
        return(True)
    else:
        break_to_new_line()
        return(False)

def set_font_size(_size:float):
    global font_size
    font_size = _size
    set_line_height(font_size)

def get_font_size():
    global font_size
    return font_size

def set_title_size(_size):
    global title_font_size
    title_font_size = _size
    return title_font_size

def get_title_size():
    global title_font_size
    return title_font_size

def set_document_language(_lang:str):
    global document_language
    document_language = _lang

def get_document_language():
    global document_language
    return document_language
