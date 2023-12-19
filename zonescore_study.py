def zone_action(zone_score:float, zone:int):
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
    for i, _val in enumerate(eff_domain_distr):
        # print(i, _val)
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

X=0
N=1
C=2
R=3

def get_zone_name(_zone):
    match(_zone):
        case 1: _name = 'volgende aandachtsgebied'
        case 2: _name = 'huidige ontwikkeling'
        case 3: _name = 'gerealiseerde ontwikkeling'
        case _: _name = '' 
    return(_name)

def zone_configurator(NoZ:int):
    try:
        Zone_config = [[N,X,X,X,X], [C,N,X,X,X], [R,C,N,X,X], [R,R,C,N,X], [R,R,R,C,N]]
        return(Zone_config[NoZ-1])
    except:
        print('error wrong input for number of zones')
        exit()

# zones = []
# # print(zone_action(5.5,2))
# zones.extend(zone_configurator(3))
# print(zones)
# Eff_pwr_domain_distr = [1, 0.4, 8, 8, 4]
# # evaluate_zone(Eff_pwr_domain_distr)
# print(evaluate_zone(Eff_pwr_domain_distr, zones))
