"""
Generate Courage and Fear reports (PDF) from Google Forms via Google API
report lab  https://www.reportlab.com/docs/reportlab-userguide.pdf
Token expired / renew ...
https://console.cloud.google.com/apis
create credentials: + CREATE CREDENTIALS, select OATH client ID, application type is Desktop Application
Save Your client IS and Your Client secret, download the client secret JSON to workspace
rename clientsecret.JSON tot credentials.JSON
delete old token
When asked, allow authorization again
should work for 7+ days

"""
import os
from terminal_stuff import clear_screen, tprint, get_gender, ask_client_name, select_data_source, get_document_code, ask_client_name, get_int_input, reminder_CF_Web
clear_screen(0)

from data_collector import ReportDataCollector, write_encrypted_data
#
# intialise a data collector for sending emails
data_for_email = ReportDataCollector()

from code_base_stuff import count_lines_in_directory
directory = "D:\Python\GoogleSheetAPI\\"
tprint(f'Accumulated lines of code in -{directory}- for Create_CF_report : ' + str(count_lines_in_directory(directory)), 3)


# ask report identification and setup - verify input and create/retreive doc
from check_language_selection import select_destination_language
from report_settings import get_report_language, set_report_language, set_report_candidate_name, set_report_document_code
import get_doc_id
import get_report_CF

from spelling_names import correct_capitals_in_name

from encrypt_decrypt_tools import write_encrypted_data, read_encrypted_data
single_data_source, returning_client_data = select_data_source()

from client_database import get_document_id, key_in_client_database, add_to_client_database, get_client_name
# Ask user for the document code of the report
CF_report_number = get_document_code()

# Entry of a seperate test
# Verify that there is test-data for the selected document code
# open document met URL links # zoek URL link bij document nummer
if single_data_source:
    Document_ID = get_doc_id.search_id(CF_report_number, get_doc_id.open_URL_doc(CF_report_number)) # get Document_id from a google form
if returning_client_data:
        reminder_CF_Web()
        if key_in_client_database(CF_report_number):
            Document_ID = get_document_id(CF_report_number) # get Document id from client database
        else:
            # Enter a loop where we either create a new CF_report_number with a valid key, client_name and URL, and return the Document_ID or halt the program.
            tprint(f'{CF_report_number} is not in client database..',3)
            choice = input('Do you want to add a new document_ID or halt? (A/H): ').strip().upper()
            if choice == 'A':
                tprint(f'Using {CF_report_number} as template.')
                CF_report_number = CF_report_number
                client_key = CF_report_number[:2]  # Extract the first two characters as the client key
                client_name = ask_client_name()
                Document_ID = input('Provide the document link: ').strip()
                add_to_client_database(client_key, client_name, Document_ID)
                tprint(f"{client_name} added to the database.")
            else:
                exit()

tprint('Document just  opened, has URL-ID : '+Document_ID,4)

# As the CF_report_number is verified as an existing test, the report number is available for other modules, now ask fo the gender
set_report_document_code(CF_report_number)
female_gender = get_gender()
    
# Open the test-results on the Google cloud
# Get specifics about CF test
if single_data_source:
    score = get_report_CF.get_CF_data(Document_ID)
if returning_client_data:
    # read data from encrypted_file
        # Check to see if there is new data to generate a report from, if so use the data if not input it manually
    # Define the path to the file where the encrypted data will be stored
    file_path = "d:\\Data_Vault\\encrypted_CF_data.txt"
    key_path = "d:\\Data_Vault\\key_CF_data.key"
    
    client = get_client_name(CF_report_number)

    try:
        score = decrypted_CF_data = read_encrypted_data(file_path, key_path)
    except FileNotFoundError:
        name = None
        date_time = None
        matter = None
        relation = None
        meaning = None
        tprint(f'No Data could be retreived, please refresh data to enter data to file {file_path}.',99)

# cadidate_name
if single_data_source:
    tprint(score)
    tprint(score[1][3][1])
    candidate_name  = score[1][3][1]   # name candidate eg 'Ivar Koehorst'
    candidate_name = test_subject_name = correct_capitals_in_name(candidate_name)

elif returning_client_data:
    tprint(decrypted_CF_data,3)
    candidate_name = decrypted_CF_data['name_client'].strip()  # The strip() function is used to remove any leading or trailing spaces
    candidate_name = correct_capitals_in_name(candidate_name)
    print('debug, name candidate: ', candidate_name)

tprint('De kandidaat is : '+ candidate_name)
data_for_email.collect('kandidaat', candidate_name)

# Select the CF report's destination language
lang = select_destination_language()

# set report variables for other modules to acces
set_report_language(lang)
set_report_candidate_name(candidate_name)

# test if variables are globally accesable
tprint('from Create_CF_report, language set to : '+ get_report_language()) # To test availability of the global variable
from translate_file import get_expl_file_path

# systems en operating systems library
# from os import startfile
#libraries to create the pdf file and add text to it
# adding Folder_2 to the system path
# C:\Users\HWdeB\Documents\Python\InvoiceMaker\Lib\site-packages\reportlab-3.6.12.dist-info
# sys.path.append('C:\Users\HWdeB\Documents\Python\InvoiceMaker\Lib\site-packages\reportlab-3.6.12.dist-info')

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
from translate_file import transl_explanation, transl_BLQ, transl_str, show_dutch, transl_list

# New recursive engine
from recursive_engine_extract_code_from_string import page_break, top_of_page, intialise_settings_font, set_font_size, break_to_new_line, Title_place_and_translate, place_scan_for_code
from document_properties import move_cursor_to_y_position, move_cursor_to_position, set_document_language, document_canvas
set_document_language(lang) # in order to use the recursive engine, set document properties

# set terminalmessage
terminalmessage = False

# Read and check validity of data in test_result
global text_poss, text_cap, text_val, text_driv, text_mean
text_poss: str = ''
text_cap: str = ''
text_val: str = ''
text_driv: str = ''
text_mean: str = ''
data_error_code = 0
if single_data_source:
    if not score[0]: tprint('No data in Document, yet..',4)
    try:
        data_error_code += 1 # error code 1
        if not score[1][2][1]: tprint('No data in Document (no time_stamp), yet..',4)
        data_error_code += 0.1 # error code 1.1
        follow_up = 'yes' # score[1][0][1]      # does the candidate want an explanation
        # collect data for email
        data_for_email.collect('feedback', score[1][0][1])
        data_error_code += 0.1 # error code 1.2
        client_name = score[1][1][1]    # client company name eg. 'Jordie Oortman'
        data_error_code += 0.1 # error code 1.3
        date_report = score[1][2][1]    # datum time report eg. '7-11-2022 8:57'
        data_error_code += 0.1 # error code 1.4
        test_subject_name = score[1][3][1]   # name candidate eg 'Ivar Koehorst'
        data_error_code += 0.1 # error code 1.5
        consistency = score[1][4][1]    # consistency questions reciprocally eg. '2,3
        data_error_code += 0.1 # error code 1.6
        consistency = float(consistency.replace(',', '.')) # convert string to float
        data_error_code += 0.1 
        tprint('Consistency of test '+ CF_report_number + ' is '+ str(consistency), 3)
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
        fear = [fear_poss,fear_cap, fear_val, fear_driv, fear_mean]
        data_error_code += 1    # error code 3.9

        # Retreive courage scores
        courage_poss = int(score[0][0][1]) # courage possibilities
        courage_cap = int(score[0][1][1]) # courage capabilities
        courage_val = int(score[0][2][1]) # courage values
        courage_driv = int(score[0][3][1]) # courage drives
        courage_mean = int(score[0][4][1]) # courage mean
        courage = [courage_poss,courage_cap, courage_val, courage_driv, courage_mean]
        data_error_code += 1    # error code 4.9

        total_effectivity = sum(courage) - sum(fear)
        data_error_code += 1    # error code 5.9
        data_error_code += 1        # error code 6.9
        data_error_code += 1        # error code 7.9

        # Effective power is the difference between  courage and fear
        data_error_code += 0.1      # error code 8.0
        Eff_pwr = list()
        data_error_code += 0.1      # error code 8.1
        Eff_pwr = effective_calc.calc_yield(fear, courage) # calculate the effective power
        data_error_code += 0.1      # error code 8.2
        # Eff_pwr_descr = compose_epd.compose_epd(Eff_pwr) # generate the domain  descriptions depending on the description from the test
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
        data_error_code += 1

    except:
        if data_error_code == 1: 
            tprint('Quiting program. data in document, '+ CF_report_number+'  probably empty, . Error code: '+  str(data_error_code),99)
            exit()
        else:
            tprint('Quiting program. data in document, '+ CF_report_number+'  not valid. Error code: '+ str(data_error_code),99)
            exit()
        
if returning_client_data:
    follow_up = 'yes' # score[1][0][1]      # does the candidate want an explanation
    # collect data for email
    data_for_email.collect('feedback', follow_up)
    client_name = candidate_name
    date_report = decrypted_CF_data['time_stamp_test']    # datum time report eg. '7-11-2022 8:57'
    test_subject_name = candidate_name   # name candidate eg 'Ivar Koehorst'
    
    consistency = float(decrypted_CF_data['stDev']['stDev_courage_and_fear']['stdev']) # score[1][4][1]    # consistency questions reciprocally eg. '2,3
    # tprint(consistency)
    # consistency = float(consistency.replace(',', '.')) # convert string to float
    
    tprint('Consistency of test '+CF_report_number+' is '+ str(consistency),3)
    # Check consistency of answers to open questions 51 until 54 with courage and fear score
    # consistency_questions = score[1][5][1] # consistency questions and open answers eg. '0,36'
    # consistency_questions = float(consistency_questions.replace(',', '.')) # convert string to float
    answers = {}  # to store the user responses

    for i in range(51, 55):  # loop from 51 to 54
        answer_key = f'vraag_{i}'
        tprint(decrypted_CF_data[answer_key],99)
        
        # Store user responses in the 'answers' dictionary
        answers[f'fear_{i}'] = get_int_input('How many instance words of fear? [Enter a whole number, Enter for zero] : ')
        answers[f'courage_{i}'] = get_int_input('How many instance words of courage? [Enter a whole number, Enter for zero] : ')    

    # Now you can access the user responses as follows:
    open_answer_fear_51 = answers['fear_51']
    open_answer_courage_51 = answers['courage_51']
    open_answer_fear_52 = answers['fear_52']
    open_answer_courage_52 = answers['courage_52']
    open_answer_fear_53 = answers['fear_53']
    open_answer_courage_53 = answers['courage_53']
    open_answer_fear_54 = answers['fear_54']
    open_answer_courage_54 = answers['courage_54']
    open_answer_fear = open_answer_fear_51 + open_answer_fear_52 + open_answer_fear_53 + open_answer_fear_54
    open_answer_courage = open_answer_courage_51 + open_answer_courage_52 + open_answer_courage_53 + open_answer_courage_54
    tprint ('Total instances of fear: '+ str(open_answer_fear),99)
    tprint ('Total instances of courage: '+ str(open_answer_courage),3)
    # correlate open_answers instances with free_energy
    free_energy = decrypted_CF_data['free_energy']
    # define relation between open answer instances and free_energy
    relation_OQ_free_energy = 25

    open_answers_correlate = (open_answer_courage - open_answer_fear) * relation_OQ_free_energy
    # tprint(open_answers_correlate)
    # tprint(free_energy)
    open_answer_consistency = abs(open_answers_correlate - free_energy) < 25

    # Retreive fear scores
    fear_poss = decrypted_CF_data['fear_possibilities'] # int(score[0][0][0]) # fear possibilities / read string convert to int
    fear_cap = decrypted_CF_data['fear_performance']  # int(score[0][1][0]) # fear capabilities
    fear_val = decrypted_CF_data['fear_values'] # int(score[0][2][0]) # fear values
    fear_driv = decrypted_CF_data['fear_focus'] # int(score[0][3][0]) # fear drives
    fear_mean = decrypted_CF_data['fear_meaning']# int(score[0][4][0]) # fear mean
    # tprint(fear_poss + ' ' + fear_cap + ' ' + fear_val + ' ' + fear_driv + ' ' + fear_mean)
    fear = [fear_poss,fear_cap, fear_val, fear_driv, fear_mean]
    # tprint(fear) 


    # Retreive courage scores
    courage_poss = decrypted_CF_data['courage_possibilities']# int(score[0][0][1]) # courage possibilities
    courage_cap = decrypted_CF_data['courage_performance']# int(score[0][1][1]) # courage capabilities
    courage_val = decrypted_CF_data['courage_values']# int(score[0][2][1]) # courage values
    courage_driv = decrypted_CF_data['courage_focus']# int(score[0][3][1]) # courage drives
    courage_mean = decrypted_CF_data['courage_meaning']# int(score[0][4][1]) # courage mean
    # tprint(courage_poss + ' ' + courage_cap + ' ' + courage_val + ' ' + courage_driv + ' ' + courage_mean)
    courage = [courage_poss,courage_cap, courage_val, courage_driv, courage_mean]
    
    # tprint(courage)
    total_effectivity = sum(courage) - sum(fear)
    # tprint(total_effectivity)
    # tprint(decrypted_CF_data['free_energy'])


    # tprint('Total effectivity is: '+ total_effectivity)
    
    # tprint(compose_epd.compose_general_descr(total_effectivity))
    

    # Effective power is the difference between  courage and fear
    
    Eff_pwr = list()
    
    Eff_pwr = effective_calc.calc_yield(fear, courage) # calculate the effective power

    
    # Eff_pwr_descr = compose_epd.compose_epd(Eff_pwr) # generate the domain  descriptions based on the test outcome 

    def level_description(level, test_outcome):
        descriptions = {
            'Mogelijkheden': {
                'Growth': 'Maakt goed gebruik van mogelijkheden en heeft een open en nieuwsgierige houding.',
                'Fixed': 'Maakt waarschijnlijk onvoldoende gebruik van mogelijkheden voelt zich bekneld of zonder opties.',
                'Doubt': 'Maakt gebruik van mogelijkheden, kan in spannende situaties in paniek raken waardoor hij zich afsluit of afzondert.'
            },
            'Kwaliteiten': {
                'Growth': 'Levert kwaliteit en daagt zichzelf uit nieuwe vaardigheden te leren.',
                'Fixed': 'Levert waarschijnlijk een suboptimaal resultaat, voelt zich onbekwaam of onzeker, gaat daardoor nieuwe uitdagende situaties zeker uit de weg.',
                'Doubt': 'Realiseert kwaliteit, kan zich onder (prestatie)druk faalangstig voelen. Gaat liever de uitdaging uit de weg.'
            },
            'Waarden': {
                'Growth': 'Voelt goed wat hij wil en maakt neemt beslissingen.',
                'Fixed': 'Kan lastig voelen wat goed voor zichzelf is en laat daardoor de keuze over aan anderen.',
                'Doubt': 'Neemt beslissingen, kan door overtuiging of verwachtingen van anderen van koers afraken, verliest daardoor belangrijke zaken voor zichzelf uit het oog.'
            },
            'Drijfveren': {
                'Growth': 'Is een doorzetter en zal in de meeste gevallen zaken kunnen volbrengen ondanks tegenslag.',
                'Fixed': 'Kan door de overtuiging dat anderen of de omstandigheden tegenwerken veel energie verliezen. Hierdoor is het gevoel van eigen verantwoordelijkheid en invloed vaak afwezig.',
                'Doubt': 'Houdt vol, kan bij tegenwerking of tegenslag, energie en focus verliezen.'
            },
            'Talent': {
                'Growth': 'Geeft het beste van zichzelf en kan zich daaraan overgeven.',
                'Fixed': 'Heeft waarschijnlijk minder overzicht door de hoeveelheid werk die hij denkt te moeten doen, ervaart daarbij stress.',
                'Doubt': 'Zet zijn talent in, kan bij drukte het overzicht verliezen en in de stress raken.'
            }
        }
        
        try:
            return descriptions[level][test_outcome]
        except KeyError:
            return 'Invalid level or test_outcome.'

    # Determine level description

    def test_outcome(value=float):
        if value > 5:
            return 'Growth'
        elif value < -5:
            return 'Fixed'
        else:
            return 'Doubt'

    # level 1 test possibilities          # score[0][0][8] 
    level = int(decrypted_CF_data['free_energy_possibilities'])
    level_indication = test_outcome(level)
    text_poss = level_description('Mogelijkheden', level_indication)

    # level 2 test capabilities
    level = int(decrypted_CF_data['free_energy_performance'])
    level_indication = test_outcome(level)
    text_cap = level_description('Kwaliteiten', level_indication)

    # level 3 test values
    level = int(decrypted_CF_data['free_energy_values'])
    level_indication = test_outcome(level)
    text_val = level_description('Waarden', level_indication)

    # level 4 test drive
    level = int(decrypted_CF_data['free_energy_focus'])
    level_indication = test_outcome(level)
    text_driv = level_description('Drijfveren', level_indication)

    # score[0][4][8] # test meaning
    level = int(decrypted_CF_data['free_energy_meaning'])
    level_indication = test_outcome(level)
    text_mean = level_description('Talent', level_indication)
# Collect_data_for email
data_for_email.collect('datum_tijd', date_report)
data_for_email.collect('naam_klant', client_name)


# Create general description for email to client
def test_outcome(value=float):
            if value > 5:
                return 'positief'
            elif value < -5:
                return 'negatief'
            else:
                return 'twijfelachtig'
            
total = sum(Eff_pwr)
eff_description = f'Het algemene beeld van {candidate_name} is {test_outcome(total)}.'
# collect data for email
data_for_email.collect('uitslag', eff_description)
# tprint(eff_description,7)


#Reading values from Google sheet
CF_report_client = candidate_name
# Read values for effective power description
BLQ , gain_avg, gain_max, position_of_minimum_effective_power, Eff_domain_distr = calc_BLQ(fear,courage)
# plot effective power diagram and retreive zones for description
# the gains of future devvelopment are projected onto this minimum value
# tprint('*** position of minimal effective power : '+ position_of_minimum_effective_power)
zones = plot_it(BLQ, gain_avg, gain_max, position_of_minimum_effective_power, Eff_domain_distr)

# create and save CF pattern image
#tprint(fear + ' ' +  courage + ' ' +  CF_report_number)
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
configurator.change_lang() # store translation setting in config file  

lang_dutch = show_dutch()

# tprint(configurator.value())
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

# tprint(font_default)

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
# tprint('mm_per_pixel:' + ' ' +  mm_per_pixel)
# set recursive document properties




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

# CF pattern from cf_report_client
CFp = Image.open(CF_file)
width, height = CFp.size
ratio = width/height
image_width4 = page_width*0.9
image_height4 = int(image_width4 / ratio)

# CF pattern from cf_report_client
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
    CF_report_file = CF_report_file.replace(' ','_')
    CF_report_file_path = CF_report_path+CF_report_file
    # collect data for email: attachement
    data_for_email.collect('attachement', CF_report_file_path)
    CF_text_file = str(CF_report_client) + '_' + str(CF_report_number) +'.txt'
    

    tprint('creating PDF document: ' + ' ' +  CF_report_path + ' ' + CF_report_file)
    c = canvas.Canvas(CF_report_path + CF_report_file)
    document_canvas(c) # set document canvas for the recursive engine to the same canvas
    c.setPageSize(A4)

    # CF_report margins
    y = page_height - image_height
    x = margin
    
    # Functions for tekst and set-up pages
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
        return(left)
    
    def fit_otl(x, word,font,font_size):
        """Does the word fit on the line. 
        """
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
        """place places a word or a short string of words. 
        Encounter the word '<br>' will invoke a new line.
        Todo: incorporate test_extract_code_from_string
        """
        
        c.setFont(font,font_size)
        if word=='<br>':      # line break code in the word string? Note that the break-string needs to be seperated from other word to be recognized. Maybe another string is connected to the break command?
            x,y = invoke_nl(x,y,lh)
        elif word == '<pb>': # page break
            c.showPage()
            x=margin
            y=page_height-margin
        else:
            if translate and (not(lang_dutch)): word = transl_str(word,lang)
            word = word + ' ' # add a space here
            if fit_otl(x, word, font, font_size):
                c.drawString(x, y, word)  # place word
            else:
                x,y = invoke_nl(x,y, line_height) 
                c.drawString(x, y, word) # place word
            text_width = stringWidth(word,font,font_size)
            x =  x + text_width
        return(x,y)

    def print_file(x,y,_file_name,fh, lh):
        with open(_file_name,'r', encoding = 'utf8', errors='strict') as file:
            # reading each line    
            for line in file: 
                # reading each word        
                for word in line.split():
                    # displaying the words
                    x,y = place(x, y, word, font_default, fh, lh)
                    
           
        file.close()
        return(x,y)
    
    def count_gender_words(input_txt:str):
        count_zichzelf = input_txt.count('zichzelf')
        count_hij = input_txt.count('hij ')

        tprint(f"Occurrences of 'zichzelf': {count_zichzelf}")
        tprint(f"Occurrences of 'hij ': {count_hij}")

        return input_txt


    def change_gender_to_female(male_txt:str):
        # count gender words
        count_gender_words(male_txt)
        # search and replace
        # zichzelf:= haarzelf
        # hij := zij 
        female_txt = male_txt.replace('zichzelf','haarzelf')
        female_txt = female_txt.replace('hij ','zij ')
        return(female_txt)

   # Define and place footnote
    def footnote():
        # Set position to bottom    
        y  = 2*line_height
        # Copyright
        # RGB font colour
        c.setFillColorRGB(0.43,0.43,0.43) #choose your 
        center(footer_txt,font_default,xs_font, y)

    c.drawInlineImage(text_logo, margin/2,
                    page_height - image_height1-25,
                    image_width1, image_height1)

    c.drawInlineImage(background_full, 0,
                    0,
                    image_width3, image_height3)

    # Solve the character flaws reading text from text files
    # https://docs.reportlab.com/reportlab/userguide/ch3_fonts/ 
    
    fh = l_font # font_height
    lh = int(fh*1.5) # line_height
    tfh = int(fh*1.8) # Title font_height
    tlh = int(tfh*1.8) # Title line_height

    def create_title_page():
        """Title page
        Only translate relevant items not proper names e.g. 'Erik Geelhorst'
        """
        y  = page_height - 30*line_height
        move_cursor_to_y_position(y)
        center('Angst en Moed','Helvetica-Bold',22, y, True)

        y -= 3*line_height
        center('profiel', font_default,22, y, True)
        

        # Opdrachtgever aanhef // **** modify to client variable
        # print('Wijzig de code hier...', client) # What variable is global holding client?
        y -= 5*line_height
        center('In opdracht van',font_default,l_font, y, True)
        # Opdrachtgever naam
        text_o = 'geen'
        if CF_report_number[0:2] == 'XJ':
            text_o = "EXPRO Engineering B.V."
        if CF_report_number[0:2] == 'YS':
            text_o = "Your Professionals B.V."
        if CF_report_number[0:2] == 'DD':
            text_o = "Deep Dive - group coaching"
        if CF_report_number[0:2] == 'TX':
            text_o = "Harry de Bont"
        y -= 2*line_height
        center(text_o,font_default,18, y, True)
        # collect data for email
        data_for_email.collect('test_code', CF_report_number)
        data_for_email.collect('opdrachtgever', text_o)

        # Kandidaat aanhef
        y -= 4*line_height
        center('Kandidaat',font_default,l_font, y, True)
        # Kandidaat naam
        y -= 2*line_height
        center(candidate_name,font_default,18, y)
        
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
    def create_general_introduction_recursive_engine():
            # Create General description
            # this routine needs the same document object parsed c.canvas TODO
        # top_of_page() instead move to position
        
        intialise_settings_font()
        set_font_size(22)
        Title_place_and_translate('Toelichting bij het Angst en Moed profiel')
        break_to_new_line(2)
        set_font_size(12)
        lang
        # _file_name = r'D:\1-Werkmap\CF_report\text\explanation_nl.txt'
        _file_name = get_expl_file_path(lang)
        with open(_file_name,'r', encoding = 'utf8', errors='strict') as file:
                # reading each line    
                for line in file:
                    # input_string = line.rstrip('\n') # remove remaining new line code(s)
                    input_string = line
                    if len(line)>1:
                        if line[-2] == '.' or line[-3:-1] == '. ' or line[-4:-1] == '.  ':
                            input_string = input_string.rstrip() + '<sp>' #add execution code <sp> to create space between lines where needed.
                    result = place_scan_for_code(input_string)


    # # This function creates a general introduction with the old pdf functions
    # def create_general_introduction():
    #     """Page #2"""
    #     c.showPage()
    #     # start at margin height
    #     y = page_height - margin
    #     x = margin


    #     # Center background image
    #     c.drawInlineImage(background_circle, (page_width - image_width2)/2,
    #                     (page_height - image_height2)/2,
    #                     image_width2, image_height2)

        

    #     # Text properties
    #     fh = l_font # font_height
    #     lh = int(fh*1.5) # line_height
        
    #     # Plaats titel
    #     c.setFont('Helvetica-Bold', tfh)
    #     text = 'Toelichting op het Angst- en Moed profiel'
    #     if not(lang_dutch): text = transl_str(text,lang)
    #     c.drawString(x, y, text)
    #     x,y = invoke_nl(x,y,tlh)
    #     expl_file  = CF_report_dir.explanation_file(lang)
    #     expl_file_exist = os.path.isfile(expl_file)
    #     if not(expl_file_exist):    # only translate the Dutch source when subsequent file doesn't exist
    #         transl_explanation(lang) # translates and saves the file
    #         expl_file  = CF_report_dir.explanation_file(lang)
    #     x,y = print_file(x,y,expl_file, fh, lh)

    #     # Place footnote
    #     footnote()

    def create_page_courage_and_fear():
        """#Page courage and fear"""
        c.showPage()

        y = page_height - margin
        x = margin

        fh = l_font # font_height
        lh = int(l_font*1.5) # line_height
        
        # Plaats titel
        c.setFont('Helvetica-Bold', tfh)
        text = 'Angst- en Moed Profiel van'
        if not(lang_dutch): text = transl_str(text, lang) + ' ' + test_subject_name
        else: text = text + ' ' + test_subject_name
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

        # create local from global variable // read and tranlate text from test form
        text_poss_1 = text_poss
        text_cap_1 = text_cap
        text_val_1 = text_val
        text_driv_1 = text_driv
        text_mean_1 = text_mean
        
        # store the description of the levels for email_sender
        data_for_email.collect('details_1', text_poss)
        data_for_email.collect('details_2', text_cap)
        data_for_email.collect('details_3', text_val)  
        data_for_email.collect('details_4', text_driv)
        data_for_email.collect('details_5', text_mean)

        if female_gender: 
            tprint('Changing gender to female in text..',4)
            text_poss_1 = change_gender_to_female(text_poss_1)
            text_cap_1 = change_gender_to_female(text_cap_1)
            text_val_1 = change_gender_to_female(text_val_1)
            text_driv_1 = change_gender_to_female(text_driv_1)
            text_mean_1 = change_gender_to_female(text_mean_1)
        domains_descr2 = [text_poss_1,text_cap_1, text_val_1, text_driv_1, text_mean_1]
        if not(show_dutch()): domains_descr2 = transl_list(domains_descr2, lang).copy()

        # 1st) De consistentie van de antwoorden op de test vragen
        consitency_description = compose_epd.compose_consistentie(consistency)
        # collect data for email
        data_for_email.collect('validatie', consitency_description)
        if not(lang_dutch): consitency_description = transl_str(consitency_description, lang)
        consistency_description_words = consitency_description.split()
        for word in consistency_description_words:
            x,y = place(x,y,word, font_default, fh, True)
        x,y = invoke_nl(x,y,2*lh)

        # Algemene indruk van angst en moed profiel    
        gen_CF = (open_gend_file.open_gend(CF_report_number, test_subject_name))
        # collect data for email
        data_for_email.collect('kenmerkend', gen_CF)
        
        if not(lang_dutch): gen_CF = transl_str(gen_CF, lang)
        
        gen_CF_split = gen_CF.split()
    
        # beschrijving van de hoogte van het effectief vermogen
        ged = compose_epd.compose_general_descr(total_effectivity, test_subject_name)
        # if not(lang_dutch): ged = transl_str(ged, lang)
        x,y = place(x,y,ged, font_default, fh)
        # if x != margin: x,y = place(x,y,' ',  font_default,fh,lh)  # spaces between the words

        for gen_descr_word in gen_CF_split:     # Describe the domain effectivity in qualitative terms, write word for word
            x,y = place(x,y, gen_descr_word,  font_default,fh,lh, False)  # text values
            # if x != margin:x,y = place(x,y,' ',  font_default,fh,lh)  # spaces between the words
        x,y = invoke_nl(x,y,2*lh)

        # plaats de tekst, een deel gegenereerd één deel uit de google sheet geladen
        for index_d, (a_descr, a_domain) in enumerate(zip(domains_descr1,domains_descr2)):
            
            x,y = place(x,y,str(index_d+1),  font_default,fh,lh, False)  # text values
            x,y = place(x,y,'. ',  font_default,fh,lh, False)  # text values period
            for quality_word in a_descr:     # Describe the domain effectivity in qualitative terms
                x,y = place(x,y,quality_word,  font_default,fh,lh, False)  # text values
                # if x != margin: x,y = place(x,y,' ',  font_default,fh,lh)  # text values
            
            for domain_word in a_domain.split(): # Describe the domain effectivity in  descriptive terms 
                x,y = place(x,y,domain_word,  font_default,fh,lh, False)  # text values
                # if x != margin: x,y = place(x,y,' ',  font_default,fh,lh)  # text values
            x,y = invoke_nl(x,y,lh)

        # place CF pattern image
        c.drawImage(CF_file, margin/2, y-image_height4,
                    image_width4, image_height4)

        # Place footnote
        footnote()

    def create_page_effective_power_graph():
        """Page #4"""
        c.showPage()
        fh = l_font # font_height
        lh = int(l_font*1.5) # line_height
        y = page_height - margin
        x = margin
        
        # Title placement
        c.setFont('Helvetica-Bold', tfh) 
        text = 'Fase van ontwikkeling van'
        if not(lang_dutch): text = transl_str(text, lang) + ' ' + test_subject_name
        else: text = text + ' ' + test_subject_name
        x,y = place(x, y, text, 'Helvetica-Bold',tfh, tlh)
        x,y = invoke_nl(x,y,2*tlh)
            
        # place zones diagram
        c.drawImage(zones_file, margin/2, y-image_height5,
                    image_width5, image_height5)
        y = y - image_height5
        x,y = invoke_nl(x,y,2*lh)


        # Read -translate and place BLQ.txt The standard text
        BLQ_file  = CF_report_dir.BLQ_file(lang)
        BLQ_file_exist = os.path.isfile(BLQ_file)
        if not(BLQ_file_exist):    # only translate the Dutch source when subsequent file doesn't exist
            transl_BLQ(lang) # translates and saves the file
            BLQ_file  = CF_report_dir.BLQ_file(lang)
        x,y = print_file(x,y,BLQ_file, fh, lh)
        
        # Place footnote
        footnote()


    def create_page_effective_power_description():
        """ # Page #5 
        """
        c.showPage()
        fh = l_font # font_height
        lh = int(l_font*1.5) # line_height
        y = page_height - margin
        x = margin

        # Title placement
        c.setFont('Helvetica-Bold', tfh) 
        text = 'Focus op ontwikkeling voor '
        if not(lang_dutch): text = transl_str(text, lang) + ' ' + test_subject_name
        else: text = text + ' ' + test_subject_name
        x,y = place(x, y, text, 'Helvetica-Bold',tfh, tlh)
        x,y = invoke_nl(x,y,2*tlh)

        # x,y = place(x,y,str(zones),'Helvetica-Bold',fh, lh)
        
        # Find the zone numbers that are, realized, current, new or not relevant
        def find_zones(_zones, _zone_phase):
            result = []
            offset = -1
            while True:
                try:
                    offset = _zones.index(_zone_phase, offset+1)
                except ValueError:
                    return result
                result.append(offset)

        # Zone definition
        X=0 # nog niet relevant (Not relevant)
        N=1 # volgende aandachtsgebied (New)
        C=2 # huidige ontwikkeling (Current)
        R=3 # gerealiseerde ontwikkeling (Realized)
        
        Zone_Numbers_For_Realized = find_zones(zones,R)
        Zone_Numbers_For_Current = find_zones(zones,C)
        Zone_Numbers_For_New = find_zones(zones,N)
        Zone_Numbers_For_No_relevance = find_zones(zones,X)
        
        def compose_zone_text_current(_zone_numbers, _zone_text):
            zone_txt_display = False
            previous_index = 0
            for index, _zone in enumerate(_zone_numbers):
                if previous_index != index:
                    add_code  = True # When there are more than one current zone description we want to add (add_code) a break <br> and another description start in the text to emphasize the new item.
                else: add_code = False
                match _zone:
                    case 0:
                        if add_code:
                            _zone_text = _zone_text + ' <br> Ga ook iets vaker iets nieuws uit proberen. Door meer nieuwe mogelijkheden te verkennen dan diegene je tot nu toe gewend bent, krijg je inzicht in datgene wat jou persoonlijk nieuwsgierig maakt. '
                        else: 
                            _zone_text = _zone_text + ' iets vaker iets nieuws uit te proberen. Door meer nieuwe mogelijkheden te verkennen dan diegene je tot nu toe gewend bent, krijg je inzicht in datgene wat jou persoonlijk nieuwsgierig maakt. '
                        zone_txt_display = True
                    case 1:
                        if add_code:
                            _zone_text = _zone_text + ' <br> Ga ook iets vaker andere uitdagingen aan. Door jezelf vaker uit te dagen om iets te verbeteren, en het effect ervan te bemerken zul je meer zelfzekerheid en initiatief ontwikkelen.'
                        else:
                            _zone_text = _zone_text + ' iets vaker andere uitdagingen aan te gaan. Door jezelf vaker uit te dagen om iets te verbeteren, en het effect ervan te bemerken zul je meer zelfzekerheid en initiatief ontwikkelen.'
                        zone_txt_display = True
                    case 2:
                        if add_code:
                            _zone_text = _zone_text + ' <br> Kies ook meer voor jezelf. Door meer te kiezen voor datgene wat jij belangrijk vindt, raak je meer betrokken en neemt het gevoel van belang voor jou toe.'
                        else:
                            _zone_text = _zone_text + ' meer te kiezen voor jezelf. Door meer te kiezen voor datgene wat jij belangrijk vindt, raak je meer betrokken en neemt het gevoel van belang voor jou toe.'
                        zone_txt_display = True
                    case 3:
                        if add_code:
                            _zone_text = _zone_text +' <br> Houdt ook langer je aandacht vast. Wanneer je instaat bent om langer je aandacht vast te houden, op iets dat voor jou belangrijk is, creëer je iets nieuws dat ook voor anderen zichtbaar is. De impact van je handelen neemt hierdoor toe.'
                        else:
                            _zone_text = _zone_text +' langer je aandacht vasthouden. Wanneer je instaat bent om langer je aandacht vast te houden, op iets dat voor jou belangrijk is, creëer je iets nieuws dat ook voor anderen zichtbaar is. De impact van je handelen neemt hierdoor toe.'
                        zone_txt_display = True
                    case 4:
                        if add_code:
                            _zone_text = _zone_text + ' <br> beter prioriteiten te stellen in lijn met jouw doel. Wanneer je jouw prioriteiten helder hebt, kun je (voor jou) minder relevante zaken goed loslaten. Hierdoor raak je in een flow en krijgt hetgeen je doet meer betekenis.'
                        else:
                            _zone_text = _zone_text + ' beter prioriteiten te stellen in lijn met jouw doel. Wanneer je jouw prioriteiten helder hebt, kun je (voor jou) minder relevante zaken goed loslaten. Hierdoor raak je in een flow en krijgt hetgeen je doet meer betekenis.'
                        zone_txt_display = True
                previous_index = index
            if not zone_txt_display:_zone_text = ''
            return(_zone_text)
        
        def compose_zone_text_new(_zone_numbers, _zone_text):
            zone_txt_display = False
            for _zone in _zone_numbers:
                match _zone:
                    case 0:
                        _zone_text = _zone_text + ' iets vaker iets nieuws uit te proberen. Door meer nieuwe mogelijkheden te verkennen dan diegene je tot nu toe gewend bent, krijg je inzicht in datgene wat jou persoonlijk nieuwsgierig maakt. '
                        zone_txt_display = True
                    case 1:
                        _zone_text = _zone_text + ' iets vaker andere uitdagingen aan te gaan. Door jezelf vaker uit te dagen om iets te verbeteren, en het effect ervan te bemerken zul je meer zelfzekerheid en initiatief ontwikkelen.'
                        zone_txt_display = True
                    case 2:
                        _zone_text = _zone_text + ' meer te kiezen voor jezelf. Door meer te kiezen voor datgene wat jij belangrijk vindt, raak je meer betrokken en neemt het gevoel van belang voor jou toe.'
                        zone_txt_display = True
                    case 3:
                        _zone_text = _zone_text + ' langer je aandacht vasthouden. Wanneer je instaat bent om langer je aandacht vast te houden, op iets dat voor jou belangrijk is, creëer je iets nieuws dat ook voor anderen zichtbaar is. De impact van je handelen neemt hierdoor toe.'
                        zone_txt_display = True
                    case 4:
                        _zone_text = _zone_text + ' beter prioriteiten te stellen in lijn met jouw doel. Wanneer je jouw prioriteiten helder hebt, kun je (voor jou) minder relevante zaken goed loslaten. Hierdoor raak je in een flow en krijgt hetgeen je doet meer betekenis.'
                        zone_txt_display = True
            if not zone_txt_display:_zone_text = ''
            return(_zone_text)
        
        def compose_zone_text_no_relevance(_zone_numbers, _zone_text):
            zone_txt_display = False
            for _zone in _zone_numbers:
                match _zone:
                    case 0:
                        _zone_text = _zone_text + ' <br> - Nieuwe mogelijkheden verkennen. Uiteraard zul je nog steeds nieuwe mogelijkheden kunnen blijven verkennen, de meerwaarde voor jouw persoonlijke ontwikkeling ligt echter bij het onderwerp van je actuele ontwikkeling.'
                        zone_txt_display = True
                    case 1:
                        _zone_text = _zone_text + ' <br> - Uitdagingen aangaan. Uitdagingen aangaan is altijd iets wat een onderdeel van je werk en leven is, de focus hierop levert echter minder voor je op dan het onderwerp van je actuele ontwikkeling.'
                        zone_txt_display = True
                    case 2:
                        _zone_text = _zone_text + ' <br> - Kiezen voor jezelf. Kiezen voor jezelf is belangrijk en moet je steeds doen. Aandacht hieraan geven echter is minder effectief voor jouw persoonlijke ontwikkeling dan aandacht te schenken aan het punt van je actuele ontwikkeling.'
                        zone_txt_display = True
                    case 3:
                        _zone_text = _zone_text + ' <br> - Aandacht vasthouden. Je aandacht vasthouden is iets wat leidt tot manifestatie van datgene wat je belangrijk vindt. Wanneer je je echter hier op focust levert dat minder op dan het onderwerp van je actuele uitdaging.'
                        zone_txt_display = True
                    case 4:
                        _zone_text = _zone_text + ' <br> - Prioriteiten stellen. Dit is een belangrijk aspect dat betekenis geeft, stress reduceert en de focus verhoogt. Jouw onmiddellijke aandacht wordt echter gevraagd op het punt van je actuele ontwikkeling.'
                        zone_txt_display = True
            if not zone_txt_display:_zone_text = ''
            return(_zone_text)

        def compose_zone_text_realized(_zone_numbers, _zone_text):
            zone_txt_display = False
            for _zone in _zone_numbers:
                match _zone:
                    case 0:
                        _zone_text = _zone_text + ' <br> - Nieuwe mogelijkheden verkennen doe je al meer dan voldoende. Uiteraard zul je nog steeds nieuwe mogelijkheden kunnen blijven verkennen, de meerwaarde voor jouw persoonlijke ontwikkeling ligt echter bij het onderwerp van je actuele ontwikkeling.'
                        zone_txt_display = True
                    case 1:
                        _zone_text = _zone_text + ' <br> - Uitdagingen aangaan is iets wat je steeds doet. Uitdagingen aangaan is altijd iets wat een onderdeel van je werk en leven blijft, teveel aandacht hierop levert echter minder voor je op dan het onderwerp van je actuele ontwikkeling.'
                        zone_txt_display = True
                    case 2:
                        _zone_text = _zone_text + ' <br> - Keuzen maken zonder jezelf te verliezen is iets wat je vanzelfsprekend vindt. Kiezen voor jezelf moet je blijven doen. Extra aandacht hieraan geven echter is minder effectief voor jouw persoonlijke ontwikkeling.'
                        zone_txt_display = True
                    case 3:
                        _zone_text = _zone_text + ' <br> - Aandacht vasthouden is iets wat jij doet. Je aandacht vasthouden leidt tot manifestatie van datgene wat je belangrijk vindt. Wanneer je echter teveel op hierop focust levert dat minder op dan het onderwerp van je actuele uitdaging.'
                        zone_txt_display = True
                    case 4:
                        _zone_text = _zone_text + ' <br> - Prioriteiten stellen is een tweede natuur. Je hebt zelfrealisatie bereikt. Wees jezelf en geniet en inspireer anderen.' # Wanneer dit gerealiseerd is het punt van zelfrealisatie bereikt. 
                        zone_txt_display = True
            if not zone_txt_display:_zone_text = ''
            return(_zone_text)

        # <als gerealisserde ontwikkeling> if 3 in zones
        # op basis van je huidige effectiefvermogen is heb jij de volgende uitdaging al voldoende onder de knie: 
        zone_text_realized = 'Op basis van je huidige effectief vermogen heb jij de volgende ontwikkeling al voldoende onder de knie:'
        zone_text_current = 'Op basis van je huidige effectiefvermogen is het jouw actuele uitdaging om'
        zone_text_new = 'Nadat je actuele uitdaging voldoende gerealiseerd hebt, wordt het belangrijk om'
        zone_text_no_relevance = 'Alhoewel je in de praktijk de onderstaande uitdagingen vaak genoeg tegenkomt, geeft de focus hierop, momenteel minder een bijdrage aan je totale effectief vermogen. Ga onderstaande uitdagingen aan wanneer dat nodig is maar besteed er relatief minder tijd en energie aan:'

        zone_text_realized = compose_zone_text_realized(Zone_Numbers_For_Realized, zone_text_realized)
        zone_text_current = compose_zone_text_current(Zone_Numbers_For_Current, zone_text_current)
        zone_text_new = compose_zone_text_new(Zone_Numbers_For_New, zone_text_new)
        zone_text_no_relevance = compose_zone_text_no_relevance(Zone_Numbers_For_No_relevance, zone_text_no_relevance)
        
        # translate when other than Dutch
        if not(lang_dutch): 
            if zone_text_realized != '': zone_text_realized = transl_str(zone_text_realized, lang)
            if zone_text_current != '': zone_text_current =  transl_str(zone_text_current, lang)
            if zone_text_new != '': zone_text_new = transl_str(zone_text_new, lang)
            if zone_text_no_relevance != '': zone_text_no_relevance = transl_str(zone_text_no_relevance, lang)

        # Split in to words, ready for placement
        zone_text_realized = zone_text_realized.split()    
        zone_text_current = zone_text_current.split()
        zone_text_new = zone_text_new.split()
        zone_text_no_relevance = zone_text_no_relevance.split()

        # place text word for word
        
        # What requires your focus now
        if zone_text_current:
            title = 'Dit vraagt jouw aandacht nu.'
            if not(lang_dutch): title = transl_str(title,lang)
            x,y = place(x,y,title,'Helvetica-Bold', fh, lh)
            x,y = invoke_nl(x,y, lh)

            for index, zone_text_word in enumerate(zone_text_current):
                x,y = place(x,y,zone_text_word,'Helvetica', fh, lh)
                # if x != margin: x,y = place(x,y,' ','Helvetica', fh, lh)
            x,y = invoke_nl(x,y,2*lh)

        # What will require your future focus
        if zone_text_new:
            title = 'Dit vraagt in de toekomst jouw aandacht.'
            if not(lang_dutch): title = transl_str(title,lang)
            x,y = place(x,y,title,'Helvetica-Bold', fh, lh)
            x,y = invoke_nl(x,y, lh)

            for zone_text_word in zone_text_new:
                x,y = place(x,y,zone_text_word,'Helvetica', fh, lh)
                # if x != margin: x,y = place(x,y,' ','Helvetica', fh, lh)
            x,y = invoke_nl(x,y,2*lh)

        # What already is realized
        if zone_text_realized:
            title = 'Wat je al gerealiseerd hebt.'
            if not(lang_dutch): title = transl_str(title,lang)
            x,y = place(x,y,title,'Helvetica-Bold', fh, lh)
            x,y = invoke_nl(x,y, lh)

            for zone_text_word in zone_text_realized:
                x,y = place(x,y,zone_text_word,'Helvetica', fh, lh)
                # if x != margin: x,y = place(x,y,' ','Helvetica', fh, lh)
            x,y = invoke_nl(x,y,2*lh)

        # What need less attention then actual or next    
        if zone_text_no_relevance:
            title = 'Geef hier alleen noodzakelijke aandacht aan.'
            if not(lang_dutch): title = transl_str(title,lang)
            x,y = place(x,y,title,'Helvetica-Bold', fh, lh)
            x,y = invoke_nl(x,y, lh)

            for zone_text_word in zone_text_no_relevance:
                x,y = place(x,y,zone_text_word,'Helvetica', fh, lh)
                #if x != margin: x,y = place(x,y,' ','Helvetica', fh, lh)
            x,y = invoke_nl(x,y,2*lh)
                
        # Place footnote
        footnote()

    tprint('Creating CF_report for : ' + ' ' + CF_report_client, 5)
    
    create_title_page()
    # create_general_introduction()
    page_break() # For some reason the recursive engine starts at the beginning of the document so an additional page break is needed.

    create_general_introduction_recursive_engine()
    create_page_courage_and_fear()
    create_page_effective_power_graph()
    create_page_effective_power_description()

    #Saving the pdf file
    trying = True
    while trying:
        try:
            c.save()
            tprint('Saving report:' + ' ' +  CF_report_client,4)
            trying = False
            clear_screen(5)
        except:
            tprint("something went wrong while saving the file ...",99)
            answer = input('Try again? [Y/N] : ').upper()
            if answer == 'N':
                trying = False
            else:
                tprint('attempting again',3)
        
    os.system(CF_report_file_path)
    tprint('Thanks for using create_CF_report!',99)

if __name__=='__main__':
    create_CF_report()
        # File paths
    # save collected data to an encrypted file
    file_path = "d:\\Data_Vault\\encrypted_CF_data_email.txt"
    key_path = "d:\\Data_Vault\\key_CF_data_email.key"

    # Write the collected data to an encrypted file
    data_for_email.write_to_file(file_path, key_path)
    print('email data collection consists of ...')
    print(data_for_email.get_data())
    print('Reminder: Run Expro_body (in folder Thunderbird), for sending this report by email')