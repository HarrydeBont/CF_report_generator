"""Calculate the effective power
    1) Courage_score - Fear_score = Effective_power
"""
_effectief_vermogen = list()

def calc_yield(_fear, _courage):
    for f1, c1 in zip(_fear, _courage):
        _effectief_vermogen.append(c1 - f1)

    return(_effectief_vermogen)