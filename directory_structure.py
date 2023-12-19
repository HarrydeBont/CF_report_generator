
# Bookkeeping of the directory structure
import os

class dir_struc:
    def __init__(self):
        self.main_root_dir = self.root_dir()
        pass
        # Courage and Fear directory for reports
        self.CF_report_path:str = r"report\\"  # 
        self.report:str = 'report'
        self.report_dir = os.path.join(self.main_root_dir, self.CF_report_path)

        
        # Courage and Fear directory for the general description
        general_description = "general_description"
        self.gendescr_path = os.path.join(self.main_root_dir, general_description)

        explanationf_path = r"text"
        self.explanation_dir = os.path.join(self.main_root_dir, explanationf_path)

        # your_path_here = "your_path"
        # self.your_path = os.path.join(self.main_root_dir, your_path_here)

    def reports_path(self):
        reports_path = self.report_dir
        return(reports_path)
        
    def explanation_path(self,_language:str = 'nl'):
        """explanation_path returns the directory+filename referring to the language required.
            If the explanation is not available in the required language ask to translate or exit.

        """
        # print(self.explanation_dir)
        path_exist = os.path.isdir(self.explanation_dir)
        if path_exist:
            # print(self.explanation_dir)
            return(self.explanation_dir, True)
        else:
            # Create Explanantion dir
            # print(self.explanation_dir)
            return(None, False)

    def explanation_file(self, _language:str):
        # e.g. _language = 'fr'
        explanation_filename = "explanation_" + _language + '.txt'
        explanation_filename = os.path.join(self.explanation_dir, explanation_filename)
        # print(explanation_filename)
        # print(self.explanation_dir)
        return(explanation_filename)

    def BLQ_file(self, _language:str):
        # e.g. _language = 'fr'
        BLQ_filename = "BLQ_" + _language + '.txt'
        BLQ_filename = os.path.join(self.explanation_dir, BLQ_filename) #The directory of explanation file and BLQ file is teh same..
        # print(explanation_filename)
        # print(self.explanation_dir)
        return(BLQ_filename)
    

    def root_dir(self):
        main_root_directory = r"D:\1-Werkmap\CF_report"
        return(main_root_directory)

    def path_VM(self,_path:str, purpose:str='useful directory'):
        """path_VM Verifies the existence of the directory path and Makes it if needed.
        """
        isDir = os.path.isdir(_path)
        if isDir:
            pass
        else:
            msg = 'Path '+ _path + ' does not exist. Create first to proceed.'
            print(msg)
            msg = "Create directory for , " + purpose + '? [Y/N]: '
            ask_permission = input(msg).upper()
            if ask_permission == "Y":
                msg = "Create " + _path + " as directory."
                print(msg)
                try:
                    os.mkdir(_path)
                except:
                    print("Failed to create directory, program halts.")
                    quit()    
            else:
                print("Program exit, by user request.")
                quit()
        

    

if __name__ == '__main__':
    d = dir_struc()
   
    # print(d.reports_path())
   