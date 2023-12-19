import googletrans
from googletrans import Translator

translator = Translator()
def lang_abbr2descr(_abbr:str):
    language_dict = googletrans.LANGUAGES
    descr = dict((k,v) for k,v in language_dict.items())
    return(descr[_abbr])

def descr2lang_abbr(language:str):
    language_dict = googletrans.LANGUAGES
    descr = dict((v,k) for k,v in language_dict.items())
    return(descr[language])

def avail_lang():
    language_dict = googletrans.LANGUAGES
    for index in language_dict.keys():
        _descr = language_dict[index]
        print(_descr, end = ' [')
        print(descr2lang_abbr(_descr),']', sep = '', end = ' - ')
    # print(language_dict['nl'])
    # language_list = list(language_dict.values()) 
    # print("translations available: ", end = ' ')
    
    # # Printing all the items of the Dictionary
    # #  print(language_dict.items())
    # for lang in language_list:
    #     print(lang, end=" ,")

def verify_lang(_lang:str):
    language_dict = googletrans.LANGUAGES
    if _lang in language_dict:
        return(True)
    else: 
        return(False)
    
if __name__ == '__main__':
    avail_lang()
    #print(descr2lang_abbr('dutch'))
    # print(verify_lang('zu'))

    

