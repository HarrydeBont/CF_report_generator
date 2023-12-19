from matplotlib import pyplot as plt
import matplotlib
# import zonescore_study
from  directory_structure import dir_struc
from translate_file import transl_str, show_dutch, show_lang
from report_settings import get_report_document_code, get_report_language



def plot_it(_funct_BLQ_arg:list, _expected_gains:float, _max_gains:float, _gains_pos:int, _Eff_pwr_domain_distr:list):
    """plot_it plots the Effective Power Accumulated. Indicating the BLQ. 
        The Big Life Question that currently is being solved.
        args:: 
        1) _funct_BLQ_arg is the Effective power list of 5,
        2) _expected gains is the average effective power of the persons score (without min and max)
        3) _expected gains is the max effective power of the persons score
        4) the domain indicated 0..4 that has the minimum score.
    """
    
    # Create a list of tuples containing all the text in the diagram
    # format text used in diagram [....(variable name, variable value), ...]
    def DT(lookup_word:str):  # DT::diagram Text
        """DT looks up the word in the dictionary translated when neccesary.
        """
        # dutch_text_in_diagram = [('mogelijkheden', 'mogelijkheden'), ('prestatie', 'prestatie'), ('richting', 'richting'), ('energie', 'energie'), ('doel', 'doel'), ('iets nieuws uitproberen', 'iets nieuws uitproberen'),
        # ('uitdagingen aangaan', 'uitdagingen aangaan'), ('durven kiezen', 'durven kiezen'), ('aandacht vasthouden', 'aandacht vasthouden'), ('prioriteiten stellen', 'prioriteiten stellen'), ('huidige score', 'huidige score'), ('normale groei verwachting (1jr)','normale groei verwachting (1jr)'),
        # ('maximale groei verwachting (1jr)', 'maximale groei verwachting (1jr)'), ('Levensdomeinen', 'Levensdomeinen'), ('Ontwikkelingsuitdagingen', 'Levensdomeinen'), ('Fase van ontwikkeling', 'Fase van ontwikkeling')]
        
        # Alle tekst labels verzamelt zodat het wijzigen makkelijker gaat het eerste label verwijst naar de code het tweede label zoals het getoont wordt in de grafiek
        T = {'mogelijkheden': 'gebruik van mogelijkheden', 'prestatie': 'onder druk presteren', 'richting': 'richting hebben', 'energie': 'impact van gedrag', 'doel': 'helderheid van doelstelling', 'iets nieuws uitproberen': 'iets nieuws uitproberen',
        'uitdagingen aangaan': 'uitdagingen aangaan', 'durven kiezen': 'durven kiezen', 'aandacht vasthouden': 'aandacht vasthouden', 'prioriteiten stellen': 'prioriteiten stellen', 'volledig potentieel':'volledig potentieel', 'huidige score': 'huidige score', 'normale groei verwachting':'normale groei verwachting (1jr)',
        'maximale groei verwachting': 'maximale groei verwachting (1jr)', 'Levensdomeinen': 'Effectief vermogen', 'Ontwikkelingsuitdagingen': 'Ontwikkelingsuitdagingen', 'Fase van ontwikkeling': 'Fase van ontwikkeling', 'huidige ontwikkeling':'huidige ontwikkeling',
        'volgende aandachtsgebied':'volgende aandachtsgebied', 'gerealiseerde ontwikkeling':'gerealiseerde ontwikkeling'}
        # print('from plot BLQ::DT',show_dutch(), get_report_language())
        if get_report_language() == 'nl':
            # print(show_dutch())
            return(T[lookup_word])
        else:
            word = transl_str(T[lookup_word], get_report_language())
            return(word)

    # Project expected gains of development onto outcome of the BLQ graph
    
    def triangelize(BLQ_org):
        """Create a triangle by mirroring effective powers of the zones to the right
        Except for the center zone which is only depicted once.
        This is how we create a isosceles triangle
        """
        revBLQ_org = BLQ_org.copy()
        # Effective power as expression of BLQ
        del revBLQ_org[-1:] # removes the last item
        revBLQ_org.reverse()
        BLQ_org.extend(revBLQ_org)
        BLQ_org.insert(0,0)
        BLQ_org.insert(len(BLQ_org),0)
        return(BLQ_org)
    
    def extrapolate(_BLQ_org:list, _gains:float, _gains_pos:int):
        """Extrapolate  the future growth from the current average effective power after removing the max and min outliers
        """
        for i in range(len(_BLQ_org)- _gains_pos):
            _BLQ_org[_gains_pos+i] = _BLQ_org[_gains_pos+i] + _gains
        return(_BLQ_org)

    def zone_action(zone_score:float, zone:int):
        """ Perform zone_action to demote or promote the zone development descriptions
        demotion and promotion is determined by uppper and lower bounds of the effective power of the investigated zone
        """
        lower_bound = 0.4
        upper_bound = 0.6
        demote = -1
        same = 0
        promote = 1

        action = same
        if zone_score < lower_bound*9: action = demote
        if zone_score > upper_bound*9: action = promote
        return(action)

    def evaluate_zone(eff_domain_distr: list, _zone_distr):
        """ Evaluate the standard zones (only depended on number of zones) with the zone_action function
        """
        for i, _val in enumerate(eff_domain_distr):
            # print('***', i, _val)
            match(_zone_distr[i]): 
                case 1: # in case the zone is identified as Next
                    if(zone_action(_val,i) > 0):
                        _zone_distr[i] = _zone_distr[i] + 1 #  it can only be promoted
                case 2: # in case zone is identified as Current
                    if(zone_action(_val,i) > 0):
                        _zone_distr[i] = _zone_distr[i] + 1 #  it can only be promoted
                case 3: # in case zone is identified as Realized
                    _zone_distr[i] = min(_zone_distr[i] + zone_action(_val,i),3) #  it can only be demoted
        return(_zone_distr)

    X=0 # nog niet relevant
    N=1 # volgende aandachtsgebied
    C=2 # huidige ontwikkeling
    R=3 # gerealiseerde ontwikkeling

    def get_zone_name(_zone):
        match(_zone):
            case 1: _name = DT('volgende aandachtsgebied')
            case 2: _name = DT('huidige ontwikkeling')
            case 3: _name = DT('gerealiseerde ontwikkeling')
            case _: _name = '' 
        return(_name)

    def zone_configurator(NoZ:int):
        try:
            Zone_config = [[C,N,X,X,X], [R,C,N,X,X], [R,R,C,N,X], [R,R,R,C,N], [R,R,R,R,C]]
            return(Zone_config[NoZ-1])
        except:
            print('error wrong input for number of zones')
            exit()
    
    BLQ_gains = _funct_BLQ_arg.copy()
    BLQ_max =  _funct_BLQ_arg.copy()
    BLQ_gains = extrapolate(BLQ_gains,_expected_gains,_gains_pos).copy()
    BLQ_max = extrapolate(BLQ_max,_max_gains,_gains_pos).copy()
    # print(len(BLQ_gains))
    # print(len(BLQ_max))
    # print(_gains_pos)
    # for i in range(len(BLQ_gains)- _gains_pos):
    #     BLQ_gains[_gains_pos+i] = BLQ_gains[_gains_pos+i] + _expected_gains
    # print(BLQ_gains)

    _funct_BLQ_arg = triangelize(_funct_BLQ_arg).copy()
    BLQ_gains = triangelize(BLQ_gains).copy()
    BLQ_max = triangelize(BLQ_max).copy()

    # rev_funct_BLQ_arg = _funct_BLQ_arg.copy()
    # # Effective power as expression of BLQ
   
    # del rev_funct_BLQ_arg[-1:] # removes the last item
    # rev_funct_BLQ_arg.reverse()
    # print(rev_funct_BLQ_arg)
    # _funct_BLQ_arg.extend(rev_funct_BLQ_arg)
    # _funct_BLQ_arg.insert(0,0)
    # print(_funct_BLQ_arg)
    # _funct_BLQ_arg.insert(len(_funct_BLQ_arg),0)
    # print(_funct_BLQ_arg)
    domain = [0,1,2,3,4,5,6,7,8,9,10]
    # BLQ_score = [0, 1.2, 2.6, 2.8, 6.7, 8.4,6.7,2.8,2.6,1.2,0]
    BLQ_score = _funct_BLQ_arg.copy()
    # define BLQ framework
    ideal = [0,9,18,27,36,45,36,27,18,9,0]
    challenge_pointers = [0, 4.5, 13.5, 22.5, 31.5, 40.5]
    poss = [0,0]
    poss_x = [0,10]
    perf = [9,9]
    perf_x = [1,9]
    val = [18,18]
    val_x = [2,8]
    foc = [27,27]
    foc_x = [3,7]
    mean = [36,36]
    mean_x = [4,6]

    zone_name_text_height = 12
    xlabel_text_height = xth = 12
    ylabel_text_height = yth = 12
    yaxes_label_text_height = ylth =14
    plot_title_text_height = ptth = ylth+3

    diagram_color = 'teal'
    fig = plt.figure(figsize=(18,9.6)) 
    # Figuring out the plots Corey Schafer https://www.youtube.com/watch?v=UO98lJQ3QGI

    # plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.minorticks_on()
    plt.xticks(domain,['', DT('mogelijkheden'), DT('prestatie'), DT('richting'), DT('energie'), DT('doel'), '', '', '', '', ''], fontsize = xth, rotation = 30)
    plt.yticks(challenge_pointers,['', DT('iets nieuws uitproberen'), DT('uitdagingen aangaan'), DT('durven kiezen'), DT('aandacht vasthouden'), DT('prioriteiten stellen')], fontsize = yth)
    plt.plot(domain, ideal, color = diagram_color, label = DT('volledig potentieel')) # exterior triangle
    plt.plot(poss_x, poss, color = diagram_color, alpha = 0.4) 
    plt.plot(perf_x, perf, color =  diagram_color, alpha = 0.4)
    plt.plot(val_x, val, color = diagram_color, alpha = 0.4)
    plt.plot(foc_x, foc, color = diagram_color, alpha = 0.4)
    plt.plot(mean_x, mean, color = diagram_color, alpha = 0.4)
    plt.plot([1,1],[0,BLQ_score[1]], color = 'white', alpha = 0.4)
    plt.plot([2,2],[0,BLQ_score[2]], color = 'white', alpha = 0.4)
    plt.plot([3,3],[0,BLQ_score[3]], color = 'white', alpha = 0.4)
    plt.plot([4,4],[0,BLQ_score[4]], color = 'white', alpha = 0.4)
    plt.plot([5,5],[0,BLQ_score[5]], color = 'white', alpha = 0.4)
    plt.plot(domain, BLQ_score, color = 'aqua', alpha = 0.6, label = DT('huidige score'))
    plt.plot(domain, BLQ_gains, color = 'aqua', alpha = 0.4, label = DT('normale groei verwachting'))
    plt.plot(domain, BLQ_max, color = 'aqua', alpha = 0.2, label = DT('maximale groei verwachting'))

    # colors from palette https://matplotlib.org/2.0.2/examples/color/named_colors.html
    plt.fill_between(domain, 0, BLQ_score, facecolor = 'aqua', alpha = 0.7)
    plt.fill_between(domain, BLQ_score, BLQ_gains , facecolor = 'aqua', alpha = 0.3)
    plt.fill_between(domain, BLQ_gains, BLQ_max , facecolor = 'aqua', alpha = 0.1)
    # set figure size to have the right dimensions

    # text alignment https://matplotlib.org/stable/gallery/text_labels_and_annotations/text_alignment.html
    
    zones = []
    number_of_zones = int((_funct_BLQ_arg[5] +_max_gains) /9) + 1
    # print('Number of zones : ', number_of_zones)
    zones.extend(zone_configurator(number_of_zones))
    # print(evaluate_zone(_Eff_pwr_domain_distr, zones))
    zones = evaluate_zone(_Eff_pwr_domain_distr, zones).copy()
    
    # determine zone description to be displayed in the zone graph with get_zone_name
    # # determine vertical position of the text
    height_of_graph = _funct_BLQ_arg[5] +_max_gains # The maximum peak of the graph
    middle_of_zone1 = min(height_of_graph, 4.5)
    middle_of_zone2 = min(height_of_graph, 13.5)
    middle_of_zone3 = min(height_of_graph, 22.5)
    middle_of_zone4 = min(height_of_graph, 31.5)
    middle_of_zone5 = min(height_of_graph, 40.5)
    zone_name_text_height = 12

    # Make sure the distance between thelabels is at least 1.5 * font_size
    # print('### distance between zone3 and zone4 labels',middle_of_zone3, middle_of_zone4 )
    between1_2 = middle_of_zone2-middle_of_zone1
    if between1_2 < 9:
        middle_of_zone2 = middle_of_zone1 + 9
    between2_3 = middle_of_zone3-middle_of_zone2
    if between2_3 < 9:
        middle_of_zone3 = middle_of_zone2 + 9
    between3_4 = middle_of_zone4-middle_of_zone3
    if between3_4 < 9:
        middle_of_zone4 = middle_of_zone3 + 9
    between4_5 = middle_of_zone5-middle_of_zone4
    if between4_5 < 9:
        middle_of_zone5 = middle_of_zone4 + 9
    


    plt.text(5, middle_of_zone1, get_zone_name(zones[0]), verticalalignment = 'center', horizontalalignment = 'center', fontsize=zone_name_text_height, color = 'grey')
    plt.text(5, middle_of_zone2, get_zone_name(zones[1]), verticalalignment = 'center', horizontalalignment = 'center', fontsize=zone_name_text_height, color = 'grey')
    plt.text(5, middle_of_zone3, get_zone_name(zones[2]), verticalalignment = 'center', horizontalalignment = 'center', fontsize=zone_name_text_height, color = 'grey')
    plt.text(5, middle_of_zone4, get_zone_name(zones[3]), verticalalignment = 'center', horizontalalignment = 'center', fontsize=zone_name_text_height, color = 'grey')
    plt.text(5, middle_of_zone5, get_zone_name(zones[4]), verticalalignment = 'center', horizontalalignment = 'center', fontsize=zone_name_text_height, color = 'grey')
    
    
    plt.xlabel(DT('Levensdomeinen'), fontsize = ylth)
    plt.ylabel(DT('Ontwikkelingsuitdagingen'), fontsize = ylth)
    plt.title(DT('Fase van ontwikkeling'), fontsize = ptth)
       # Save the CF_zones to disk
    
    zones_path = 'D:\\1-Werkmap\\CF_report\\zones\\' 
    zones_dir = dir_struc()
    zones_dir.path_VM(zones_path, 'CF zones')
 
    zones_file = get_report_document_code() + '_ CF_zones.png'
   
    plt.legend(loc = 'upper left')
    plt.tight_layout()
    plt.savefig(zones_path+zones_file, transparent=False)
    plt.show()
    return(zones)

if __name__ == '__main__':
    plot_it([0.2, 7.1, 7.3, 7.5, 8.699999999999999], 2.2, 3.1, 0, [2.1, 1.1, 3.5, 0.1, 4], 'XJ-999') 
    # 1) Create descriptions for zones, realized zone, current zone of developement, adjacent zone of development 
    # 2) Label active zones
    # 3) Label X-axes, Y-axes -> set_xticklabels
        # domain = [0,1,2,3,4,5,6,7,8,9,10]
        # domain_lbls = ['', 'mogelijkheden','uitdagingen','keuzen','focus', 'doelgerichtheid']

        # plt.set_xticks(domain)
        # plt.set_xticklabels(domain,_lbls minor=False, rotation=45)
    # 4) Create a legend for the shades
    # 5) Center and align text with the height of the diagram
