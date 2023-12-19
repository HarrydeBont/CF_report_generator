import googletrans
from googletrans import Translator

translator = Translator()
def select_destination_language():
    """select_destination_language selects and verifies the destination language for the report.
    """
    not_language_sel = True
    while not_language_sel:
        # ask language of the report
        
        lang = input('Language of the report [Enter] for default Dutch, [?] for available languages  : ') 
        if (lang == '') or (lang == None):
            lang = 'nl'
            not_language_sel = False
        elif lang == '?':
            print('Choose a language:  ', avail_lang())
        else:
            correct = verify_lang(lang)
            if not(correct): input('Wrong language selected  [Enter to try again] ')
            not_language_sel = False
        # print('from module select_destination_language, lang for return is', lang)
    return(lang)

def avail_lang():
    """avail_lang lists available languages
    """
    language_dict = googletrans.LANGUAGES
    for index in language_dict.keys():
        _descr = language_dict[index]
        print(_descr, end = ' [')
        print(descr2lang_abbr(_descr),']', sep = '', end = ' - ')

def descr2lang_abbr(language:str):
    """def descr2lang_abbr, returns the languages with an abbreviation
    """
    language_dict = googletrans.LANGUAGES
    descr = dict((v,k) for k,v in language_dict.items())
    return(descr[language])

def verify_lang(_lang:str):
    """verify_lang verifies if a language exists as a google translation destination
    """
    language_dict = googletrans.LANGUAGES
    if _lang in language_dict:
        return(True)
    else: 
        return(False)
    