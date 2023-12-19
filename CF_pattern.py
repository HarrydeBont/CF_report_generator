"""Generates a courage and Fear pattern image from the test-data.
1) Create a graph with three scores: Fear, Courage and Effective power.
2) Save the graph to file using the _test_code (e.g. 'XJ-001') to compose the filename {_test_code + '_ CF_pattern.png'}.
"""

# https://www.delftstack.com/howto/python/python-spline/  --- spline interpolation
# https://matplotlib.org/stable/api/markers_api.html --- markers for the plot
# https://matplotlib.org/stable/gallery/color/named_colors.html --- colors
# https://discuss.python.org/t/global-variables-shared-across-modules/16833 problem with global variables

import os

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

import effective_calc
from directory_structure import dir_struc
from report_settings import get_report_document_code, get_report_language
from translate_file import transl_str, show_lang, show_dutch, set_lang

# configurator = config4CFreport()

# import CF_score here
def create_pattern(_fear:list, _courage:list):
    """Create a graph with three scores: Fear, Courage and Yield.
    Save the graph as a file using the test code (e.g. 'XJ-001') to compose the filename.
    """
        # print(_fear, _courage, _test_code)
    zero = [0,0,0,0,0]
    # fear = _fear # Fear score
    # courage = _courage # courage score
    # fear = [47,39,46,41,63] # Fear score
    # courage = [51,58,49,51,55] # courage score
    effectief_vermogen = list()

    # # Calculate the yield/effectief vermogen
    # effectief_vermogen = effective_calc.calc_yield(_fear, _courage)

    # Calculate the yield/effectief vermogen

    for f1, c1 in zip(_fear, _courage):
        effectief_vermogen.append(c1 - f1)

    n = len(_fear)
    x = range(0, n)

    fear_i = interpolate.splrep(x, _fear, s=0)
    xfit = np.arange(0, n-1, np.pi/50)
    fearfit = interpolate.splev(xfit, fear_i, der=0)

    courage_i = interpolate.splrep(x, _courage, s=0)
    xfit = np.arange(0, n-1, np.pi/50)
    couragefit = interpolate.splev(xfit, courage_i, der=0)

    effectief_vermogen_i = interpolate.splrep(x, effectief_vermogen, s=0)
    xfit = np.arange(0, n-1, np.pi/50)
    effectief_vermogenfit = interpolate.splev(xfit, effectief_vermogen_i, der=0)

    max_score = max(max(_fear),max(_courage),max(effectief_vermogen))
    min_score = min(min(_fear),min(_courage),min(effectief_vermogen))
    # print(min_score, max_score)


    plt.figure(figsize=(10,5)) # Set dimensionality of the plot figure

    # Define text in plot
    Angst_score = "Angst score"
    Moed_score = "Moed score"
    Score = 'Score'

    Effectief_vermogen = "Effectief vermogen"
    _result = []
    CF_pattern_X_axes = ['1. mogelijkheden','2. prestatie','3. waarden', '4. focus', '5. doel']
    for index, item in enumerate(CF_pattern_X_axes):
        # print('from CF_pattern:: printing labels X_axes. Language: ', get_report_language())
        result = transl_str(item, get_report_language())
        _result.append(result)
    CF_pattern_X_axes = _result

    # print(str(type(['Mogelijkheden','Presteren','Kiezen', 'Focus', 'Doelgerichtheid'])))

    Angst_en_Moed_patroon = "Angst en Moed patroon"
    if not(get_report_language=='nl'):
        Angst_score = transl_str(Angst_score, get_report_language())
        Moed_score = transl_str(Moed_score, get_report_language())
        Effectief_vermogen = transl_str(Effectief_vermogen, get_report_language())
        Angst_en_Moed_patroon = transl_str(Angst_en_Moed_patroon, get_report_language())
        Score = transl_str(Score, get_report_language())

    plt.plot(x,zero, 'grey')
    plt.plot(x, _fear, 'or', label = Angst_score)
    plt.plot(xfit, fearfit,'firebrick')

    plt.plot(x, _courage, 'go', label = Moed_score)
    plt.plot(xfit, couragefit,'darkgreen')

    plt.plot(x, effectief_vermogen, 'yo', label = Effectief_vermogen)
    plt.plot(xfit, effectief_vermogenfit,'olive')

    plt.xticks(x,CF_pattern_X_axes)
    plt.ylabel("{_Score} [{min} - {max}]".format (_Score = Score, min=min_score, max=max_score))

    # plt.plot(x, _courage, "-r", label="Moed")

    plt.legend(loc="upper left")

    plt.title(Angst_en_Moed_patroon)

    # Save the CF_pattern to disk
    
    pattern_path = 'D:\\1-Werkmap\\CF_report\\pattern\\' 
    pattern_dir = dir_struc()
    pattern_dir.path_VM(pattern_path, 'CF patterns')
 
    pattern_file = get_report_document_code() + '_ CF_pattern.png'
    plt.savefig(pattern_path+pattern_file, transparent=False)
    plt.show()

if __name__ == '__main__':
    # create_pattern([47,39,46,41,63],[51,58,49,51,55], 'XJ-999')
    set_lang('af')
    _result = []
    test = ['mogelijkheden','presteren','kiezen', 'focus', 'doelgerichtheid']
    #  print(str(type(['Mogelijkheden','Presteren','Kiezen', 'Focus', 'Doelgerichtheid'])))
    for index, item in enumerate(test):
        result = transl_str(item,get_report_language())
        _result.append(result)
    print(_result)