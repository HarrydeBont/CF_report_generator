


def calc_BLQ(_fear, _courage):
    """BLQ calculates the Big Life Question a candidate is dealing with.
    Arguments are Fear scores, Courage scores. Out comes key figures for generating a description and a graph.
"""
    BLQ_score = [] #Big Life Question Score
    Eff_pwr_domain_distr = []
    avg_Eff_pwr = []
    # Step through scores of Fear and Courage to create effective power distribution per domain and BLQ_score (acumulated value)
    for i, (F_score, C_score) in enumerate(zip(_fear,_courage)):
        domain = i+1
        Eff_power_tot = C_score/10 - F_score/10
        # print(domain, -1* F_score/10, C_score/10, f'{(Eff_power_tot):.2f}' )
        Eff_pwr_domain = (C_score - F_score)/10
        if domain == 1: 
            BLQ_poss = Eff_pwr_domain
            Eff_pwr_domain_distr.append(Eff_pwr_domain)
            BLQ_score.append(BLQ_poss)
            avg_Eff_pwr.append(Eff_pwr_domain)
        if domain == 2: 
            BLQ_perf = BLQ_poss + Eff_pwr_domain
            Eff_pwr_domain_distr.append(Eff_pwr_domain)
            BLQ_score.append(BLQ_perf)
            avg_Eff_pwr.append(Eff_pwr_domain)
        if domain == 3: 
            BLQ_val = BLQ_perf + Eff_pwr_domain
            Eff_pwr_domain_distr.append(Eff_pwr_domain)
            BLQ_score.append(BLQ_val)
            avg_Eff_pwr.append(Eff_pwr_domain)
        if domain == 4:
            BLQ_foc = BLQ_val + Eff_pwr_domain
            Eff_pwr_domain_distr.append(Eff_pwr_domain)
            BLQ_score.append(BLQ_foc)
            avg_Eff_pwr.append(Eff_pwr_domain)
        if domain == 5: 
            BLQ_mean = BLQ_foc + Eff_pwr_domain
            Eff_pwr_domain_distr.append(Eff_pwr_domain)
            BLQ_score.append(BLQ_mean)
            avg_Eff_pwr.append(Eff_pwr_domain)

    # calculates the position <in where?> of the lowest score <of what?>
    min_pos_eff_pwr = min(range(len(Eff_pwr_domain_distr)), key=Eff_pwr_domain_distr.__getitem__) 

    # calculates the average of effective power distribution without max and min
    max_gain:float = max(Eff_pwr_domain_distr) 
    avg_Eff_pwr.remove(max(avg_Eff_pwr))
    avg_Eff_pwr.remove(min(avg_Eff_pwr))
    avg_Eff_pwr = sum(avg_Eff_pwr)/len(avg_Eff_pwr) 

    # print('max gains for development ', max_gain)
    # print('Expected gains for development ', avg_Eff_pwr)
    # print('Average BLQ score is ', BLQ_score)
    # print('Effective power distribution', Eff_pwr_domain_distr)
    return(BLQ_score, avg_Eff_pwr, max_gain, min_pos_eff_pwr, Eff_pwr_domain_distr)