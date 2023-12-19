"""
Generate Courage and Fear reports (PDF) from Google Forms via Google API
report lab  https://www.reportlab.com/docs/reportlab-userguide.pdf
Token expired?
https://console.cloud.google.com/apis
create credentials: + CREATE CREDENTIALS, select OATH client ID
Save Your client IS and Your Client secret, download the client secret JSON to workspace
rename clientsecret.JSON tot credentials.JSON
delete old token
When asked, allow authorization again
should work for 7 days

"""
# ask report identification and setup - verify input and create/retreive doc
from check_language_selection import select_destination_language
from report_settings import get_report_language, set_report_language, set_report_candidate_name, set_report_document_code
import get_doc_id
import get_report_CF

# Ask user for the document code of the report (e.g. 'AB-123')
CF_report_number = input('Provide document code: ')

# Verify that there is test-data for the selected document code
# open document met URL links # zoek URL link bij document nummer
Document_ID = get_doc_id.search_id(CF_report_number, get_doc_id.open_URL_doc(CF_report_number))
print('Document just  opened, has URL-ID : ', Document_ID)
# As the CF_report_number is verified as an existing test, make the report number available for other modules
set_report_document_code(CF_report_number)

# Open the test-results on the Google cloud
# Get specifics about CF test
score = get_report_CF.get_CF_data(Document_ID)
candidate_name = test_subject = score[1][3][1]   # name candidate eg 'Ivar Koehorst'
print('Candidate is : ', candidate_name)

# Select the CF report's destination language
lang = select_destination_language()

# set report variables for other modules to acces
set_report_language(lang)
set_report_candidate_name(candidate_name)

# test if variables are globally accesable
print('from Create_CF_report: ', get_report_language()) # To test availability of the global variable
import translate_file

# # Gimmy total lines of code!
# import count_lines
# count_lines.countlines(r"C:\Users\HWdeB\Documents\Python\GoogleSheetAPI")
# with open(r"C:\Users\HWdeB\Documents\Python\GoogleSheetAPI\Create_CF_report.py", 'r') as fp:
#     x = len(fp.readlines())
#     print('Total lines of code:', x)
# exit()

# systems en operating systems library
import sys
import os

#libraries to create the pdf file and add text to it
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import PageBreak

#library to get logo related information
from PIL import Image

# Developed Class(es)
from directory_structure import dir_struc

# Developed modules

import CF_pattern
import effective_calc
import compose_epd

import open_gend_file

from BLQ import calc_BLQ
from plot_BLQ import plot_it
from translate_file import transl_explanation, transl_str, show_dutch, transl_list

# Read and check validity of data in test_result
data_error_code = 0
if not score[0]: print('No data in Document, yet..')
try:
    # print('Wil een gesprek?: ', score[1][0][1])
    # print('Opdrachtgever: ', score[1][1][1])
    # print('Date/tijd report: ', score[1][2][1])
    # print('Kandidaat: ', score[1][3][1])
    # print('Consistentie test antwoorden: ', score[1][4][1])
    # print('Consistentie met open vragen: ', score[1][5][1])
    # print('Weight open vragen: ', score[1][6][1])
    # print('Angst: ', score[0][0][0])
    # print(score)
    data_error_code += 1 # error code 1
    if not score[1][0][1]: print('No data in Document, yet..')
    data_error_code += 0.1 # error code 1.1
    follow_up = score[1][0][1]      # does the candidate want an explanation
    data_error_code += 0.1 # error code 1.2
    client_name = score[1][1][1]    # client company name eg. 'Jordie Oortman'
    data_error_code += 0.1 # error code 1.3
    date_report = score[1][2][1]    # datum time report eg. '7-11-2022 8:57'
    data_error_code += 0.1 # error code 1.4
    test_subject = score[1][3][1]   # name candidate eg 'Ivar Koehorst'
    data_error_code += 0.1 # error code 1.5
    consistency = score[1][4][1]    # consistency questions reciprocally eg. '2,3
    data_error_code += 0.1 # error code 1.6
    consistency = float(consistency.replace(',', '.')) # convert string to float
    data_error_code += 0.1 
    print('Consistency of test ',CF_report_number,' is ', consistency)
    data_error_code += 0.1 # error code 1.8
    consistency_questions = score[1][5][1] # consistency questions and open answers eg. '0,36'
    data_error_code += 0.1 # error code 1.9
    consistency_questions = float(consistency_questions.replace(',', '.')) # convert string to float

    data_error_code += 1    # error code 2.9

    # Retreive fear scores
    fear_poss = int(score[0][0][0]) # fear possibilities / read string convert to int
    fear_cap = int(score[0][1][0]) # fear capabilities
    fear_val = int(score[0][2][0]) # fear values
    fear_driv = int(score[0][3][0]) # fear drives
    fear_mean = int(score[0][4][0]) # fear mean
    # print(fear_poss,fear_cap, fear_val, fear_driv, fear_mean)
    fear = [fear_poss,fear_cap, fear_val, fear_driv, fear_mean]
    data_error_code += 1    # error code 3.9

    # Retreive courage scores
    courage_poss = int(score[0][0][1]) # courage possibilities
    courage_cap = int(score[0][1][1]) # courage capabilities
    courage_val = int(score[0][2][1]) # courage values
    courage_driv = int(score[0][3][1]) # courage drives
    courage_mean = int(score[0][4][1]) # courage mean
    #print(courage_poss,courage_cap, courage_val, courage_driv, courage_mean)
    courage = [courage_poss,courage_cap, courage_val, courage_driv, courage_mean]
    data_error_code += 1    # error code 4.9

    total_effectivity = sum(courage) - sum(fear)
    data_error_code += 1    # error code 5.9

    # print('Total effectivity is: ', total_effectivity)
    data_error_code += 1        # error code 6.9
    # print(compose_epd.compose_general_descr(total_effectivity))
    data_error_code += 1        # error code 7.9

    # Effective power is the difference between  courage and fear
    data_error_code += 0.1      # error code 8.0
    Eff_pwr = list()
    data_error_code += 0.1      # error code 8.1
    Eff_pwr = effective_calc.calc_yield(fear, courage) # calculate the effective power
    data_error_code += 0.1      # error code 8.2
    # Eff_pwr_descr = compose_epd.compose_epd(Eff_pwr) # generate the domain  descriptions depending on th
    data_error_code += 0.1
    text_poss = score[0][0][8] # test possibilities
    data_error_code += 0.1
    text_cap = score[0][1][8] # test capabilities
    data_error_code += 0.1
    text_val = score[0][2][8] # test values
    data_error_code += 0.1
    text_driv = score[0][3][8] # test drive
    data_error_code += 0.1
    text_mean = score[0][4][8] # test meaning
    data_error_code += 0.1
    # print(text_poss, text_cap, text_val, text_driv, text_mean)
    data_error_code += 1

except:
    if data_error_code == 1: 
        print('Quiting program. data in document, ', CF_report_number,'  probably empty, . Error code: ', data_error_code)
        sys.exit()
    else:
        print('Quiting program. data in document, ', CF_report_number,'  not valid. Error code: ', data_error_code)
        sys.exit()

#Reading values from Google sheet
CF_report_client = test_subject
BLQ , gain_avg, gain_max, pos_min, Eff_domain_distr = calc_BLQ(fear,courage)
plot_it(BLQ, gain_avg, gain_max, pos_min, Eff_domain_distr)

# create and save CF pattern image
#print(fear, courage, CF_report_number)
CF_pattern.create_pattern(fear, courage)

# Read Courage and Fear pattern
pattern_path = 'D:\\1-Werkmap\\CF_report\\pattern\\'
pattern_file = CF_report_number + '_ CF_pattern.png'
CF_file = pattern_path + pattern_file

# Read Zones diagram
zones_path = 'D:\\1-Werkmap\\CF_report\\zones\\'
zones_file = CF_report_number + '_ CF_zones.png'
zones_file = zones_path + zones_file



# config document settings, font and so on
from doc_setv02 import config4CFreport


# configuration file for this specific CF-report

configurator = config4CFreport()  #document setting  class

configurator.config_exist()

# document language
# set_lang(lang) # set language in translation settings
configurator.change_lang() # store translation setting in config file  This goes wrong here <---------------

lang_dutch = show_dutch()
print('Report language is : ',lang, " Dutch? ", lang_dutch)


# print(configurator.value())
font_default = configurator.value('font')        # Default font
# RGB_grey = [0.25, 0.25, 0.25]
RGB_grey = configurator.value('copyright_grey')  # Font colors copyright footer
# xxs_font = configurator.value('xxs_font')  # Font height extra extra small 
xs_font  = configurator.value('xs_font')  # Font height extra small 9
# s_font   = configurator.value('s_font')  # Font height small
# n_font   = configurator.value('n_font')  # Font height normal
l_font   = configurator.value('l_font')  # Font height large - 12
# xl_font  = configurator.value('xl_font')  # Font height extra large
# xxl_font = configurator.value('xxl_font')  # Font height extra extra large
line_height = configurator.value('line_height') # Set line height default
footer_txt = configurator.value('footer') # tekst of footer

# print(font_default)

# Import company's logos
style_path = 'D:\\1-Werkmap\\0 - MonadCompany\\9 - Afbeeldingen&videos MonadCompany\\Huisstijl\\'
company_logo = style_path + 'factuur header2.jpg'
text_logo = style_path + 'MonadCompany logo shift to courage.jpg'
background_circle = style_path + 'Cirkelpunt_2400_x_2400 round bleached.jpg'
background_full = style_path + 'Cover sheet Courage and Fear report - xxs.png'

#Page information
page_width, page_height = A4                # unit is pixels
page_width_mm, page_height_mm = (210,297)   # unit is mm
mm_per_pixel = page_width_mm/page_width     # unit is mm/pixel
# print('mm_per_pixel:', mm_per_pixel)


# CF_report variables
margin = 25/mm_per_pixel                    # Margin of the document unit is mm
max_text_length = page_width - 2 * margin     # Maximu length available for text

# Groene cirkel Logo met bedrijfsadres
im = Image.open(company_logo)
width, height = im.size
ratio = width/height
image_width = page_width/4
image_height = int(image_width / ratio)

# MonadCompany Shift to Courage
im1 = Image.open(text_logo)
width, height = im1.size
ratio = width/height
logo_width = (page_width - margin)/2
image_width1 = logo_width
image_height1 = int(image_width1 / ratio)

# MonadCompany logo faded achtergrond
im2 = Image.open(background_circle)
width, height = im2.size
ratio = width/height
logo_width = page_width - 2 * margin
image_width2 = logo_width
image_height2 = int(image_width2 / ratio)

# MonadCompany CF report full background
im3 = Image.open(background_full)
width, height = im3.size
ratio = width/height
logo_width = page_width
image_width3 = logo_width
image_height3 = int(image_width3 / ratio)

# CF pattern from test_subject
CFp = Image.open(CF_file)
width, height = CFp.size
ratio = width/height
image_width4 = page_width*0.9
image_height4 = int(image_width4 / ratio)

# CF pattern from test_subject
ZF = Image.open(zones_file)
width, height = ZF.size
ratio = width/height
image_width5 = page_width*0.9
image_height5 = int(image_width5 / ratio)



#def function CF_report
def create_CF_report(terminalmessage:bool = True):
    
    #Creating a pdf file and setting a naming convention
    CF_report_dir = dir_struc()
    CF_report_path = CF_report_dir.reports_path() #'D:\\1-Werkmap\\CF_report\\report\\'
    CF_report_dir.path_VM(CF_report_path, 'reports') # creating directory if needed
    CF_report_file = str(CF_report_client) + '_' + str(CF_report_number) +'.pdf'
       
    CF_text_file = str(CF_report_client) + '_' + str(CF_report_number) +'.txt'
    

    print('creating PDF document: ', CF_report_path+CF_report_file)
    c = canvas.Canvas(CF_report_path + CF_report_file)
    c.setPageSize(A4)

    # CF_report margins
    y = page_height - image_height
    x = margin
    

    # Center text
    def center(text, font, font_size, vert_pos, translate:bool = False):
        """ Calculate center position and place text  .
        """
        if translate and (not(lang_dutch)): text = transl_str(text,lang)
        c.setFont(font,font_size)
        text_width = stringWidth(text,font,font_size)
        
    
        center_pos = (page_width - text_width)/2
        c.drawString(center_pos, vert_pos, text)

    def remain(x):
        """ Determines the space left in the current line in pixels.
        """
        left = page_width -  margin - x
        #print('space left on line: ', left)
        return(left)
    
    def fit_otl(x, word,font,font_size):
        """Does the word fit on the line. 
        """
        #print('de lengte van de tekst is: ', stringWidth(word,font,font_size))
        if stringWidth(word,font,font_size) < (remain(x)):
            return(True)
        else:
            return(False)
    
    def invoke_nl(x,y, line_height = 10):
        """Invoke a new line when still space to do so."""
        if y - line_height > margin:
            y = y - line_height
            x = margin
        else:
            c.showPage()
            x=margin
            y=page_height-margin
        return(x,y)
 
    
    def place(x, y, word, font, font_size=l_font, line_height=18, translate:bool = False):
        # print('-',word,'-')
        if translate and (not(lang_dutch)): word = transl_str(word,lang)
        c.setFont(font,font_size)
        if fit_otl(x, word, font, font_size):
            
            c.drawString(x, y, word)  # place word
        else:
            x,y = invoke_nl(x,y, line_height)
            c.drawString(x, y, word) # place word
        text_width = stringWidth(word,font,font_size)
        x =  x + text_width
        return(x,y)

    # Define and place footnote
    def footnote():
        # Set position to bottom    
        y  = 2*line_height
        # Copyright
        # RGB font colour
        c.setFillColorRGB(0.43,0.43,0.43) #choose your 
        center(footer_txt,font_default,xs_font, y)

    # Creating the report
    # print('t', stringWidth('t',font_default,10))
    # print(' ', stringWidth('t',font_default,10))
    # print('e', stringWidth('t',font_default,10))
    #Drawing the images
    c.drawInlineImage(text_logo, margin/2,
                    page_height - image_height1-25,
                    image_width1, image_height1)

    c.drawInlineImage(background_full, 0,
                    0,
                    image_width3, image_height3)


    # Titel 
    # Only translate relevant items not proper names e.g. 'Erik Geelhorst'
    y  = page_height - 30*line_height
    center('Angst en Moed','Helvetica-Bold',22, y, True)
    y -= 3*line_height
    center('profiel', font_default,22, y, True)
    

    # Opdrachtgever aanhef
    y -= 5*line_height
    center('In opdracht van',font_default,l_font, y, True)
    # Opdrachtgever naam
    text_o = 'Geen opdrachtgever'
    if CF_report_number[0:2] == 'XJ':
        text_o = "EXPRO Engineering B.V."
    else:
        if CF_report_number[0:2] == 'YS':
            text_o = "Your Professional B.V."
    y -= 2*line_height
    center(text_o,font_default,18, y, True)

    # Kandidaat aanhef
    y -= 4*line_height
    center('Kandidaat',font_default,l_font, y, True)
    # Kandidaat naam
    y -= 2*line_height
    center(test_subject,font_default,18, y)
    
    # Testnummer aanhef
    y -= 15*line_height
    center('Test',font_default,10, y, True)
    # Testnummer
    y -= line_height
    center(CF_report_number,font_default,10, y)
    
    # Datum aanhef
    y -= 2*line_height
    center('Datum',font_default,10, y, True)
    # Datum
    y -= line_height
    center(date_report,font_default,10, y)


    # Place footnote
    footnote()
    
    # Page #2 
    c.showPage()
    # start at margin height
    y = page_height - margin
    x = margin

    fh = l_font # font_height
    lh = int(fh*1.5) # line_height
    tfh = int(fh*1.8) # Title font_height
    tlh = int(tfh*1.8) # Title line_height
    # Center background image
    c.drawInlineImage(background_circle, (page_width - image_width2)/2,
                    (page_height - image_height2)/2,
                    image_width2, image_height2)

    

    # Text properties
    fh = l_font # font_height
    lh = int(fh*1.5) # line_height
    # print(fh, lh)
    
    # Plaats titel
    c.setFont('Helvetica-Bold', tfh)
    text = 'Toelichting op het Angst- en Moed profiel'
    if not(lang_dutch): text = transl_str(text,lang)
    c.drawString(x, y, text)
    x,y = invoke_nl(x,y,tlh)

    # opening the text file
    # should we parse the language only from this point? 
    expl_file  = CF_report_dir.explanation_file(lang)
    expl_file_exist = os.path.isfile(expl_file)
    if not(expl_file_exist):    # only translate the Dutch source when subsequent file doesn't exist
        transl_explanation(lang) # translates and saves the file
        expl_file  = CF_report_dir.explanation_file(lang)
    with open(expl_file,'r') as file:
        # reading each line    
        for line in file:

            for line in file:
   
                # reading each word        
                for word in line.split():
                    if word == '<br>':
                        x,y = invoke_nl(x,y,lh)
                    else:
                        # displaying the words
                        x,y = place(x,y,word, font_default,fh,lh)
                        # x,y = place(x,y,' ', font_default,fh,lh)
    file.close()

    # Place footnote
    footnote()

    #Page #3
    c.showPage()
    
    # # Center background image
    # c.drawInlineImage(background_circle, (page_width - image_width2)/2,
    #                 (page_height - image_height2)/2,
    #                 image_width2, image_height2)

    y = page_height - margin
    x = margin

    fh = l_font # font_height
    lh = int(l_font*1.5) # line_height
    # print(l_font, lh)
    
    # Plaats titel
    c.setFont('Helvetica-Bold', tfh)
    text = 'Angst- en Moed Profiel van'
    if not(lang_dutch): text = transl_str(text, lang) + ' ' + test_subject
    else: text = text + ' ' + test_subject
    x,y = place(x, y, text, 'Helvetica-Bold',tfh, tlh)
    x,y = invoke_nl(x,y,2*tlh)
    
    fh = l_font # font_height
    lh = int(l_font*1.5) # line_height
    
    Eff_pwr_descr = compose_epd.compose_epd(Eff_pwr) # generate the domain  descriptions depending on th
    textq_poss_split = Eff_pwr_descr[0].split()
    textq_cap_split = Eff_pwr_descr[1].split()
    textq_val_split = Eff_pwr_descr[2].split()
    textq_driv_split = Eff_pwr_descr[3].split()
    textq_mean_split = Eff_pwr_descr[4].split()
    domains_descr1 = (textq_poss_split,textq_cap_split, textq_val_split, textq_driv_split, textq_mean_split)
    
    text_poss_split = text_poss # .split()
    text_cap_split = text_cap # .split()
    text_val_split = text_val # .split()
    text_driv_split = text_driv #.split()
    text_mean_split = text_mean # .split()
    domains_descr2 = [text_poss_split,text_cap_split, text_val_split, text_driv_split, text_mean_split]
    # print(domains_descr2, str(type(domains_descr2)))
    if not(show_dutch()): domains_descr2 = transl_list(domains_descr2, lang).copy()
    # print(domains_descr2, str(type(domains_descr2)))

    # 1st) De consistentie van de antwoorden op de test vragen
    gecons = compose_epd.compose_consistentie(consistency)
    if not(lang_dutch): gecons = transl_str(gecons, lang)

    x,y = place(x,y,gecons, font_default, fh, True)
    x,y = invoke_nl(x,y,2*lh)

    # Algemene indruk van angst en moed profiel    
    gen_CF = (open_gend_file.open_gend(CF_report_number, test_subject))
    if not(lang_dutch): gen_CF = transl_str(gen_CF, lang)
    gen_CF_split = gen_CF.split()
   
    # beschrijving van de hoogte van het effectief vermogen
    ged = compose_epd.compose_general_descr(total_effectivity, test_subject)
    # if not(lang_dutch): ged = transl_str(ged, lang)
    x,y = place(x,y,ged, font_default, fh)
    x,y = place(x,y,' ',  font_default,fh,lh)  # spaces between the words

    for gen_descr_word in gen_CF_split:     # Describe the domain effectivity in qualitative terms, write word for word
        x,y = place(x,y, gen_descr_word,  font_default,fh,lh, False)  # text values
        x,y = place(x,y,' ',  font_default,fh,lh)  # spaces between the words
    x,y = invoke_nl(x,y,2*lh)

    # plaats de tekst, een deel gegenereerd één deel uit de google sheet geladen
    for index_d, (a_descr, a_domain) in enumerate(zip(domains_descr1,domains_descr2)):
        
        x,y = place(x,y,str(index_d+1),  font_default,fh,lh, False)  # text values
        x,y = place(x,y,'. ',  font_default,fh,lh, False)  # text values period
        for quality_word in a_descr:     # Describe the domain effectivity in qualitative terms
            x,y = place(x,y,quality_word,  font_default,fh,lh, False)  # text values
            x,y = place(x,y,' ',  font_default,fh,lh)  # text values
        
        for domain_word in a_domain.split(): # Describe the domain effectivity in  descriptive terms  <----------------------------------------------------------------------------- fout?
            x,y = place(x,y,domain_word,  font_default,fh,lh, False)  # text values
            x,y = place(x,y,' ',  font_default,fh,lh)  # text values
        x,y = invoke_nl(x,y,lh)

    # place CF pattern image
    c.drawImage(CF_file, margin/2, y-image_height4,
                image_width4, image_height4)

    # Place footnote
    footnote()


    #Page #4
    c.showPage()
    y = page_height - margin
    x = margin
    
    c.setFont('Helvetica-Bold', tfh) 
    text = 'Fase van ontwikkeling van'
    if not(lang_dutch): text = transl_str(text, lang) + ' ' + test_subject
    else: text = text + ' ' + test_subject
    x,y = place(x, y, text, 'Helvetica-Bold',tfh, tlh)
    x,y = invoke_nl(x,y,2*tlh)
        
    # place zones diagram
    c.drawImage(zones_file, margin/2, y-image_height5,
                image_width5, image_height5)
    # Place footnote
    footnote()

    print('Creating CF_report for : ', CF_report_client)
    #Saving the pdf file
    try:
        print('Saving report:', CF_report_client)
        c.save()
    except:
        print("something went wrong while saving the file ...")


create_CF_report()