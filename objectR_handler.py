"""This modue intializes,stores, reads and verifies objects on the physical drive
History:
 - version 1.0, April 2022, Author: Harry de Bont
 - version 1.1, November 2022, Author: Harry de Bont
    minor adjustments
reference: https://www.geeksforgeeks.org/create-a-directory-in-python/
"""

import pickle
import os
from directory_structure import dir_struc
import numpy as np

objtr_root = dir_struc()

class objecter:
    """
    This class serializes objects, reads or saves them to file.
    Two functions: write_model (to file), read_model (from file)
    Args objtr_dir, objtr_file, terminalmessage = True
    """
    def __init__(self, objtr_dir:str, objtr_file:str, terminalmessage:bool = False):
        error_code =  0
        try:
            self.objtr_dir:str = objtr_root.root_dir() + '\\' + objtr_dir
            error_code += 10
            error_str = 'creating object directory'
            isDir = os.path.isdir(self.objtr_dir)
            error_code += 10
            error_str = self.objtr_dir + 'object directory does not exist'
            self.objtr = self.objtr_dir + "\\" + objtr_file + ".OBJTR"
            error_code += 10
            error_str = 'creating object directory and file_path'
            if isDir:
                msg = "object -"+ self.objtr_dir + " - directory validated.."
                if terminalmessage: print(msg)
            else:
                msg = self.objtr_dir, " -object path doesn't exist. Create first to proceed."
                if terminalmessage: print(msg)
                ask_permission = input("Create directory? [Y/N]: ").upper()
                if ask_permission == "Y":
                    error_code += 1
                    if terminalmessage: 
                        msg = "Create " + self.objtr_dir + " as directory."
                        print(msg)
                    try:
                        os.mkdir(self.objtr_dir)
                    except:
                        if terminalmessage: print("Failed to create directory, program halts.")
                        quit()    
                else:
                    if terminalmessage: print("Program exit, by user request.")
                    quit()
        except:
            print('Objecter::Unexpected Error: ', error_code, ' ', error_str)
            quit()
                

    def write_model(self, model_object, terminalmessage = False):
        with open(self.objtr, 'wb') as my_file: # write bytes to preserve the data
            pickle.dump(model_object, my_file)
            my_file.close()
            if terminalmessage: 
                msg = "Object -" + self.objtr + "- saved."
                print(msg)

    def read_model(self, terminalmessage = False):
        # Check whether the specified path - self.objtr - is an existing file.
        isFile = os.path.isfile(self.objtr)
        if isFile:
            try:
                with open(self.objtr, 'rb') as my_file: # read file as bytes
                    if terminalmessage: print('From read_model/objecR_handler : opening file: ', my_file)
                    my_object = pickle.load(my_file)
                    my_file.close()
                    msg = "From read_model/objectR_handler Retreiving -" + self.objtr + " as an object."
                    if terminalmessage: 
                        print(msg)
                        print(my_object)
                    return(my_object)
            except:
                print('Unexpected error while retreiving pickle file : ', self.objtr)
                exit()
        else:
            msg = 'Program exit file', str(self.objtr), ' does not exist.'
            if terminalmessage: print(msg)
            exit()
    
    def verify(self, terminalmessage = False):
        # check if file exists
        isFile = os.path.isfile(self.objtr)
        # check if file is not empty
        try:
            _size = os.path.getsize(self.objtr)
        except:
            _size = -1
        _verify = isFile and (_size > 0)
        msg = self.objtr + ' file, exists with file size : ' + str(_size)
        if terminalmessage: print(msg)
        return(_verify)

if __name__ == '__main__':
    # directory structure
    Rdir = dir_struc()
    test_config = objecter('reports','config_Xpro')
    
    # Verify configuration file exist
    print('Config file exists?: ', test_config.verify())

    # create configuration file
    if not(test_config.verify()):
        config = np.array([['content','configuration file, contains: font, font_height'],['font','Helvetica'],['font_height',12]])
        test_config.write_model(config,True)
    configuration  = test_config.read_model()

# Find item in config file
# this is the <numpy> version
# def get_config(_item:str='content'):
#     """ Retrieve _item = 'content' for set_up of the configuration file
#     """
#     test = test_config.read_model()
#     print('Get config here ->')
#     print(test)
#     print(str(type(test)))
#     print('<- config out')
    
#     _item_val = np.where(test == _item )
#     # _item_val = 'return value'
#     print(_item_val)
#     # for i,value in enumerate(test):
#     #     print( 'Inside get_config '+ )
#     return(_item_val)
# this is the <list> version
# https://stackoverflow.com/questions/18041604/search-in-2d-list-using-python-to-find-x-y-position
# def value(item:str='*.*',L:list = configuration):
#     """Find item's value in the config file. Show all config items with item is '*.*'
#     """
#     # show all items for search item == '*.*'
#     if item == '*.*':
#         _answer = ''
#         for i in range(len(L)):
#             for j in range(len(L[i])):
#                 _answer = _answer + str(L[i][j]) + ' '
#             _answer = _answer + ' - '
#         return(_answer)

#     else:
#         for i in L:
#             if item in i:
#                 _find = L.index(i)
#                 return(L[_find][1])
#         return('None',-1)


        
# # add item to config file
# def add_config(_configuration_file_object:objecter = configuration):
#     print(value())
#     _item_name = input('What item to add?: ')
#     msg = str('What value for '+_item_name+ '? : ')
#     _item_value = input(msg)
#     _add_item = [[_item_name,_item_value]]
#     _configuration_file_object = _configuration_file_object + _add_item
    
#     # Edit description accordingly
#     # config_description = print(value()
#     # print(str(type(_configuration_file_object[[0][0]]))+' '+str(_configuration_file_object[[0][0]]))
#     # _configuration_file_object[[0][0]] = print(value() + ', ' + _item_name 
#     _configuration_file_object[[0]].append(_item_name)
    
#     # test_config.write_model(_configuration_file_object)
#     print(value())
    



