"""The open_gend_module returns the text for the general description of the CF pattern.
1)  Uses windows notepad to open and edit the text for the general description of the CF pattern.
2)  text file: 'XJ-083,Ivar Koehorst - Algemene omschrijving CF patroon.txt'
"""
from os import startfile
import os
from directory_structure import dir_struc

textF = dir_struc()

def open_gend(report_num, test_subject):
    CF_text_path = r"D:/1-Werkmap/CF_report/text/"
    textF.path_VM(CF_text_path, 'text document')
    CF_text_path = CF_text_path + report_num + ", " + test_subject+ r" - Algemene omschrijving CF patroon.txt"
    Fexists = os.path.exists(CF_text_path)

    def open_read_close():
        """Opens the text file for reviewing and editing, close after"""

        try:
            file = open(CF_text_path, "r")
            _open_gend_text = file.read()
            file.close()
            return(_open_gend_text)
        except:
            print('Something went wrong handling the general description file. Exit program.')
            os.exit()
    
    error_msg = 0
    if Fexists:
        # print("Opening existing file..")
        startfile(os.path.normpath(CF_text_path))

    else:
        try:
            # print('No such path and file yet, creating')
            file = open(CF_text_path, "w")
            error_msg += 1
            file.write(" en komt op basis van deze test over als iemand die ...")
            error_msg += 1
            file.close()
            error_msg += 1
            startfile(os.path.normpath(CF_text_path))
            error_msg += 1
        except:
            print('Unexpected error, error code: ' + error_msg + 'Unable to handle general description file, quitting program.')
            os.exit()

    # Editing
    wait = input('Enter to proceed [press any key] : ')
    open_gend_text = open_read_close()
    return(open_gend_text)

if __name__ == '__main__':
    print(open_gend('XJ-083', 'Piet de Bruijn'))


