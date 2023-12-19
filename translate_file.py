"""Translate_file translates strings, texts to the desired destination language using the Google translator.
    1) lang_abbr2descr, returns the language abbreviation given a languages
    2) def descr2lang_abbr, returns the languages with an abbreviation
    3) avail_lang lists available languages
    4) set_lang sets the desired destination language (depricated)
    5) show_lang returns the destination language (depricated)
    6) show_dutch returns whether the destination language is Dutch (depricated)
    7) transl_explanation translates the explanation file (this txt files stores user input)
    8) transl_str translates a given string to the desired destination language
    9) translates a list to the desired destination language
    10) Lookup words, strings and sentences, files that have received feedback use corrected translation instead of automated
"""

# https://stackabuse.com/text-translation-with-google-translate-api-in-python/
import googletrans
import os
from directory_structure import dir_struc
# print(googletrans.LANGUAGES) for a listing of the languages
from googletrans import Translator
from directory_structure import dir_struc
from doc_setv02 import config4CFreport
import warnings
from report_settings import get_report_language, get_report_candidate_name, get_report_document_code
import json

dir_text = dir_struc()

# initialize feedback database
# structure: destination text in feedback {dictionary}, replace result with content
# read feedback, open to destination dictionary
translator = Translator()
def lang_abbr2descr(_abbr:str):
    """Lang_abbr2descr, returns the language abbreviation given a languages
    """
    language_dict = googletrans.LANGUAGES
    descr = dict((k,v) for k,v in language_dict.items())
    return(descr[_abbr])

def descr2lang_abbr(language:str):
    """def descr2lang_abbr, returns the languages with an abbreviation
    """
    language_dict = googletrans.LANGUAGES
    descr = dict((v,k) for k,v in language_dict.items())
    return(descr[language])

def avail_lang(terminalmessage:bool = True):
    """avail_lang lists available languages
    """
    language_dict = googletrans.LANGUAGES
    for index in language_dict.keys():
        _descr = language_dict[index]
        if terminalmessage:
            print(_descr, end = ' [')
            print(descr2lang_abbr(_descr),']', sep = '', end = ' - ')

def get_expl_file_path(lang):
    lang_codes = {
        "en": "en", # english
        "nl": "nl", # dutch
        "fr": "fr", # french
        "de": "de", # german
    }

    base_path = r'D:\1-Werkmap\CF_report\text'
    file_prefix = 'explanation_'
    file_extension = '.txt'

    language_name = lang_codes.get(lang)
    if language_name:
        file_name = f"{file_prefix}{language_name}{file_extension}"
        file_path = os.path.join(base_path, file_name)
        return file_path
    else:
        raise ValueError(f"Unsupported language code: {lang}")

def set_lang(_lang:str):
    """set_lang sets the desired destination language (depricated)
    -- This needs to be unconvoluted / untangled with change_lang from the doc_set class
    This module is depricated.
    """
    warnings.warn("Module set_lang() is being depricated, change programming where possible...", DeprecationWarning)
    global lang
    lang = _lang
    global lang_dutch
    if lang == 'nl': 
        lang_dutch = True
    else:
        lang_dutch = False
    

def show_lang():
    """show_lang returns the destination language (depricated)
    """
    warnings.warn("Module show_lang() is being depricated, change programming where possible...", DeprecationWarning)
    return(lang)

def show_dutch():
    """show_dutch returns whether the destination language is Dutch (depricated)
    """
    warnings.warn("Module show_dutch() is being depricated, change programming where possible...", DeprecationWarning)
    if get_report_language() == 'nl':
        return(True)
    else:
        return(False)

def transl_explanation(lang:str, terminalmessage:bool=False):
    """transl_explanation translates the explanation file (this txt files stores user input)
    lang is the destination language for the translation.
    """
    text_file = dir_text.explanation_file('nl')
    _file_dest = dir_text.explanation_file(lang) 
    transl_file(text_file, _file_dest, lang, terminalmessage)

def transl_BLQ(lang:str, terminalmessage:bool=False):
    """transl_BLQ translates the explanation file (this txt files stores user input)
    lang is the destination language for the translation.
    """
    text_file = dir_text.BLQ_file('nl')
    _file_dest = dir_text.BLQ_file(lang) 
    transl_file(text_file,_file_dest, lang, terminalmessage)

def transl_file(_file_name:str, _file_dest, lang:str, terminalmessage:bool=False):
    """transl_file translates thegiven file (this txt files stores user input)
    lang is the destination language for the translation.
    """
    text_file = _file_name
    f = open(text_file, 'r', encoding = 'utf8')   # read the Dutch source file -> translate 
    if f.mode == 'r':
        contents = f.read()
        if terminalmessage: print(contents)
    file_translate = Translator()
    # to do get_lang from config file
    result = file_translate.translate(contents, dest = lang, src='nl').text 
    _file_dest = open (_file_dest, 'w', encoding = 'utf8') # , encoding='utf8'
    _file_dest.write(result) # save the translated file
    _file_dest.close()
    if terminalmessage: print(result)



def transl_str(_text:str, _dest_lang:str):
    """transl_str translates a given string to the desired destination language, also reading the feedback.json, for improved translation
    """
    if _text == ' ':
        return(' ')

    # Load feedback translations
    with open('feedback.json', 'r') as f:
        feedback = json.load(f)

    result = translator.translate(_text, dest=_dest_lang, src='nl').text

    if result in feedback:
        result = feedback[result]

    return(result)


def transl_list(_text_L:list, _dest_lang:str, terminalmessage:bool = False):
    """ translates a list to the desired destination language
    """
    for i, sentence in enumerate(_text_L):
        if terminalmessage: print(sentence)
        _text_L[i] = transl_str(sentence, _dest_lang)
    return(_text_L)
    


if __name__ == "__main__":
    # transl_explanation('de')
    # print(googletrans.LANGUAGES)
    # print(lang_abbr2descr('nl'))
    # transl_explanation('fr')
    # print(transl_str("Datum", 'en'))
    # set_lang('fr')
    # print(lang_abbr2descr('af'))
    # print(transl_list(['ik ben gek', 'score'], 'fr'))
    # print(transl_str('Angst en Moed', 'en'))
    # transl_BLQ('en',True)
    # avail_lang()
    # transl_file("D:\\1-Werkmap\\CF_report\\text\\test.txt","D:\\1-Werkmap\\CF_report\\text\\test_transl.txt",'fr')
    pass