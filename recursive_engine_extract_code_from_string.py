from document_properties import get_margin, top_of_page, cursor_at_margin, move_cursor_to_right, pos_x, pos_y, document_size, break_to_new_line, normal_font, font_bold, set_italic, get_font_setting, does_word_fit_on_line_within_the_margins
from document_properties import Titel_top_of_page, set_font_size, move_cursor_to_position, center, get_font_setting, get_font_size, set_document_language, get_document_language, set_title_size, get_title_size
from document_properties import document_canvas, get_document_canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from translate_file import transl_str



def place_scan_for_code(input_string):
    """extracts codes from a string, executes special functions when encountering the code, the code is removed from the string"""
     
    length_code = 4
    # Base case: if the input string is empty, return an empty string. End of recursion.
    if input_string == "":
        return ""
    
    # Recursive case: if the input string starts with a code string, execute the function
    # call and return the result of the function call concatenated with the result of
    # calling this function again with the remaining string
    match input_string[:length_code]:
        case '<br>':
            result = break_normal()
            return result + place_scan_for_code(input_string[length_code:])
        case '<uc>':
            result = upper_case()
            return result + place_scan_for_code(input_string[length_code:])
        case '<ca>':
            result = case_as_is()
            return result + place_scan_for_code(input_string[length_code:])
        case '<pb>':
            result = page_break()
            return result + place_scan_for_code(input_string[length_code:])
        case '</b>':
            result = font_bold()
            return result + place_scan_for_code(input_string[length_code:])
        case '</n>':
            result = normal_font()
            return result + place_scan_for_code(input_string[length_code:])
        case '</i>':
            result = set_italic()
            return result + place_scan_for_code(input_string[length_code:])
        case '<sp>':
            result = add_a_space()    # add a space 
            return result + place_scan_for_code(input_string[length_code:])
        

    # Recursive case: if the input string does not start with a code string, return the
    # first character of the input string concatenated with the result of calling this
    # function again with the remaining string
    place_string_no_code(input_string[0], input_string[1:])
    return input_string[0] + place_scan_for_code(input_string[1:]) # proces first character in the remaining string and recursively handle the rest

def add_a_space():
    dx = stringWidth(' ',get_font_setting(),12)
    move_cursor_to_right(dx)
    return ''

def get_special_codes():
    special_codes = ['<br>', '<uc>', '<ca>', '<pb>', '</b>', '</n>', '</i>', '<sp>']
    return special_codes

def upper_case(): # just showcasing the terminal print, should rewrite for pdf
    global print_parameter
    print_parameter = 'upper_case'
    return ''

def case_as_is():
    global print_parameter
    print_parameter = 'case_as_is'
    return ''

def clean_string_from_codes(_string):
    for code in get_special_codes():
        _string = _string.replace(code, '')
    clean_string = _string
    return(clean_string)

def next_word_fit_on_line(_input_string):
    """checks after every space if the next word still  fits on the remaining space on the line.
    """
    clean_string = clean_string_from_codes(_input_string)
    
    words = clean_string.split()
    if words:
        if does_word_fit_on_line_within_the_margins(words[0]): 
            return ' '                              # we continue the next word on the same line, the space remains a space
        else:
            return ''                               # there is a  new_line because we ran out of space, space is removed new line is invoked


def page_break():
    # print('\n-----------------------------------') # terminal
    get_document_canvas().showPage()                           # pdf new page
    top_of_page()
    return ''

def place_string_no_code(_one_character_at_time, remainder_string):
        
    if _one_character_at_time == ' ':
        _one_character_at_time = next_word_fit_on_line(remainder_string) # check if the next word fits on the remaining space of the line
    if not _one_character_at_time == '\n': # do not do anything with an end_of line character rstrip messes up the layout.
        global print_parameter
        match print_parameter:
            case 'upper_case':
                # print(_one_character_at_time.upper(), end = '') # terminal
                place_character_in_pdf(_one_character_at_time.upper())
                return ''
            case 'case_as_is':
                # print(_one_character_at_time, end = '') # terminal
                place_character_in_pdf(_one_character_at_time)
                return ''


def place_character_in_pdf(_char):
    
    if _char:
        get_document_canvas().setFont(get_font_setting(),get_font_size())
        get_document_canvas().drawString(pos_x(), pos_y(), _char)
        dx = stringWidth(_char,get_font_setting(),get_font_size())
        move_cursor_to_right(dx)


def break_normal():
    # print('') # terminal break to new line
    break_to_new_line()
    return ''

def intialise_settings_font():
    input_string = "<ca></n>"  # initiatialize case_as_is <ca> and normal_font </n> should be set (implicitely) a start of a new document
    place_scan_for_code(input_string)
    set_title_size(22)

def center_place_and_translate(_input_string:str):
    _clean_string = clean_string_from_codes(_input_string)
    # print(_clean_string)
    _clean_string = transl_str(_clean_string, get_document_language())
    _input_string = transl_str(_input_string, get_document_language())
    center(_clean_string)
    place_scan_for_code(_input_string)

def center_and_place(_input_string:str):
    _clean_string = clean_string_from_codes(_input_string)
    # print(_clean_string)
    center(_clean_string)
    place_scan_for_code(_input_string)

def Title_place_and_translate(_input_string:str):
    set_font_size(get_title_size())
    place_scan_for_code('</b>')
    _input_string = transl_str(_input_string, get_document_language())
    place_scan_for_code(_input_string)
    place_scan_for_code('</n>')

if __name__ == '__main__':
    #libraries to create the pdf file and add text to it
    from reportlab.pdfgen import canvas

    report = 'test_extract_code_from_string.pdf'
    print('Initialising PDF document: ', report)
    set_document_language('en')
    print('Document language set to English')


    document_canvas(canvas.Canvas(report))
    get_document_canvas().setPageSize(document_size())

    intialise_settings_font()

    # Test the function
    # Create Title page
    big = 22
    small = 12
    
    Titel_top_of_page()
    set_font_size(big)
    break_to_new_line(6)

    center_place_and_translate('</b>Angst en Moed')
    break_to_new_line()
    
    center_place_and_translate('</n>profiel')
    break_to_new_line(2)
    
    set_font_size(small)
    center_place_and_translate('In opdracht van')
    
    set_font_size(18)
    break_to_new_line()
    center_and_place('Harry de Bont')
    break_to_new_line(2)
    
    set_font_size(small)
    center_place_and_translate('</n>Kandidaat')

    set_font_size(18)
    break_to_new_line()
    center_and_place('</n>Dirk de Jong')
    break_to_new_line(5)

    set_font_size(small)
    center_place_and_translate('Test')
    break_to_new_line()
    center_and_place('TX-004')
    break_to_new_line(2)
    center_place_and_translate('Datum')
    break_to_new_line()
    center_and_place('1-9-2019 12:20:59')


    place_scan_for_code('<pb>')



    # Create General description
    top_of_page()
    intialise_settings_font()
    set_font_size(22)
    Title_place_and_translate('Toelichting bij het Angst en Moed profiel')
    break_to_new_line(2)
    set_font_size(12)
    _file_name = r'D:\1-Werkmap\CF_report\text\explanation_nl.txt'
    with open(_file_name,'r', encoding = 'utf8', errors='strict') as file:
            # reading each line    
            for line in file:
                # input_string = line.rstrip('\n') # remove remaining new line code(s)
                input_string = line
                if len(line)>1:
                    if line[-2] == '.' or line[-3:-1] == '. ' or line[-4:-1] == '.  ':
                        input_string = input_string.rstrip() + '<sp>' #add execution code <sp> to create space between lines where needed.
                result = place_scan_for_code(input_string)


    get_document_canvas().save()
    print('Saved report:', report)
    # print(result)