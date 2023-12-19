"""This routine creates comprehensible sentences from the effective power scores.
    1) Uses 5 bounds to determine descriptions e.g. 'is soms minder effectief'
    2) Composes sentences from the descriptions.
    3) General description of the effetive power
    4) Description for the consistency of the test-result 
    4) Specific effectiveness power descriptions per domains (edp)
"""
import re # import regular expression to manipulate strings
from translate_file import transl_str, show_dutch, show_lang, transl_list
from report_settings import get_report_language

# definitions domain descriptions
gepb: int  = [(-500,-5),(-5,5),(5,20),(20,100),(100,500)]# general score effective power bounds
gepd: str = [' is in het algemeen niet effectief', ' is soms minder effectief', ' is meestal effectief', ' is effectief', ' is zeer effectief'] # general effective power descrip[tion per score

# definitions consistentie descriptions
consb: float  = [(0,-0.5),(0.5,1),(1,2.5),(2.5,3),(3,5)]# general score effective power boundsd
consd: str = ['zeer hoog, de test is betrouwbaar.', 'hoog, de test is betrouwbaar.', 'voldoende, de test is betrouwbaar.', 'matig, de test is indicatief.', 'laag, de test is onbetrouwbaar.'] # general effective power descrip[tion per score

domains = ['Mogelijkheden', 'Presteren', 'Kiezen', 'Focus', 'Doelgerichtheid']
epds = 'Het effectief vermogen' # effective_power_description sentence start
epd_domain = ['om mogelijkheden te verkennen', 'om te presteren', 'om keuzes te maken', 'om zich te focussen', 'om prioriteiten te stellen'] # effective power per domain
epde = 'is' # effective_power_description sentence end

epqb: int  = [(-100,-5),(-5,5),(5,20),(20,40),(40,100)]# effective power qualification  bounds
epqd: str = ['nauwelijks', 'beperkt', '', 'ruim', 'zeer ruim']
epqe: str = 'aanwezig.' # effective power qualification sentence end
# epdr: str = [] # Effective Power Description Result

def compose_general_descr(total_score:int, _test_subject:str = 'John Doe'):
    for indexG, bounds in enumerate(gepb):   # determine the qualifier
        if bounds[0] <= total_score < bounds[1]:
            General_qualifier = gepd[indexG]
            return_text = _test_subject + General_qualifier
            if not(show_dutch()): return_text = transl_str(return_text, get_report_language())
    return(return_text)

def compose_consistentie(_consistentie:float):
    for indexC, bounds in enumerate(consb):   # determine the qualifier
        if bounds[0] <= _consistentie < bounds[1]: # compare the bounds with the value
            consistentie_descr = consd[indexC]  # assign description.
            return_text = "De consistentie van de gegeven antwoorden in de vijf categoriën is <br> " + consistentie_descr
            if not(show_dutch()): return_text = transl_str(return_text, get_report_language())
    return(return_text)

def compose_epd(scores:list): # compose the effective power description

    epdr = []
    for index, score in enumerate(scores):
        
        
        for index2, bounds in enumerate(epqb):   # determine the qualifier
            if bounds[0] <= score < bounds[1]:
                qualifier = epqd[index2]

        epdr.append(re.sub(' +', ' ',(epds + ' ' + epd_domain[index]+ ' ' + epde + ' ' + qualifier + ' ' + epqe))) # compose effective power description / re == remove (regedit) two or more spaces and replace with one
        
    if not(show_dutch()): epdr = transl_list(epdr, get_report_language()).copy()
    return(epdr)

if __name__ == '__main__':
    domain_score=list()
    # input score for demonstration purposes()
    for index, a_domain in enumerate(domains):
        domain_score.append(int(input('Score '+a_domain+'[-100 <-> 100] : ')))
        
    print(compose_epd(domain_score))