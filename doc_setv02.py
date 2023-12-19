""" doc_set will fascilitate control over default document settings. 
Think of font, font height, line height, and so on.
version 0.1 - November 2022, Harry de Bont
    Initial document
version 0.2 - 15 November 2022, Harry de Bont
    1) convert to a class - done
    2) create CF report adjustment to doc_set being a class done
    3) create functionality for a config file per report [config_name] done
    4) In if __name__ == '__main__': filename input to retreive the right config file done

"""

# import objectrR_handler routine
from objectR_handler import objecter
from report_settings import get_config_file_name, get_report_language

class config4CFreport():
    """
    This class creates or retreives a configuration file (e.g. 'Henk Moos_AB-123_config') for the CF_report that is generated. 
    Functions: config_exist, lostr2float, edit_item, value, add_item
    Args
    """
    def __init__(self, terminalmessage:bool = True):
        
        # Format config_name = 'John Doe_AB-999'
        self.terminalmessage = terminalmessage
        self.report_CFfile_name = get_config_file_name()
        # print('from init config4CFreport intializing configuration file with name : ', self.report_CFfile_name)
        self.CF_report_config = objecter('config',self.report_CFfile_name)
        self.config_exist()
        self.configuration = self.CF_report_config.read_model()
        # print('from init of class config4CFreport, the type of configuration is : ', str(type(self.configuration)))
        # print('This is the configuration_file: ', self.configuration)
        
       
    def config_exist(self, terminalmessage:bool =  False):
        """
        create configuration file
        Configuration file exist?
        """
        if not(self.CF_report_config.verify()):
            try:
                # create first set-up if the config file doesn't exist
                self.configuration = [['content','configuration file, contains: font, font_height'],['language','nl'],['gender', 'male'], ['font','Helvetica'],['xs_font',9],['l_font',12],['copyright_grey', [0.25, 0.25, 0.25]],['line_height',12], ['footer','MonadCompany Copyright © 2023']]
                #save config file as a serialized object
                if terminalmessage: print('Creating configuration file')
                self.CF_report_config.write_model(self.configuration, terminalmessage)
            except:
                print('Failed to open or create configuration file')
                exit()
        else: 
            print('configuration file: already exists')
        # #read the configuration file into configuration
        # configuration  = CF_report_config.read_model()
        # self.configuration = self.CF_report_config.read_model()  # 
        return(self.CF_report_config.read_model()) # return the configuration file

    # un-convolution doc_set ;)
    # 
    def change_lang(self, terminalmessage:bool = False):
        """
        change language setting in configuration file
        """
        if terminalmessage:
            print('from change_lang in doc_setv02. Report language : ', get_report_language())
        self.edit_item('language', get_report_language()) # <-------------------- this goes wrong, get_report_language is True
        #change value for 'language'     
        # save new configuration file (with Write_model)
        if terminalmessage:
            print('from change_lang in doc_setv02. self.configuration : ', self.configuration)
        self.CF_report_config.write_model(self.configuration, terminalmessage)

    # # compose list of floats from string input format '[2.3, -1.1, 55.1]' - mind the spaces!
    def lostr2float(self,b:str = '[2.3, -1.1, 55.1]'):
        b=b.replace('[','')
        b=b.replace(']','')
        b=b.replace(' ','')
        b = b.split(sep = ',')
        b =list(map(float, b))
        return(b)

    # editing configuration file
    def edit_item(self, _item:str='?', _value:any = None, terminalmessage:bool = False):
        L = self.configuration
        if _item == '?':
            print('Current config file items are [' + self.value('*.*') + ']')
            print('Which configuration item do you want to change? : ')
            for i in range(len(L)):
                print('['+str(i)+'] '+L[i][0], end=" ")

        # ask for config item to edit
        incorrect  = True
        if _item == '?':
            while incorrect:
                _choice = input('Edit item? [] : ')
                try:
                    _choice = int(_choice)
                    if _choice in range(0, len(L)):
                        incorrect = False
                    else:
                        print('Index error use a value from [0] to ['+str(len(L)-1)+']')
                except:
                    print('Incorrect, enter a valid number ')
            # Show old value of selected _item
            print('Old value of ' + str(L[_choice][0]) + ' was ' + str(self.value(L[_choice][0])))
           
            # convert input to type of the old value
            if isinstance(L[_choice][1], list):
                _new_value = (input('What is the new value? : '))
                _new_value = self.lostr2float(_new_value)
                if len(_new_value) == 3:
                    L[_choice][1] = _new_value # new value assigned
                else: 
                    print('-------->  Can not process list type, with length other than 3, try again or exit.')
            else:
                _new_value_type = type(L[_choice][1])
                # print(_new_value_type)
                _new_value = _new_value_type((input('What is the new value? : ')))
                L[_choice][1] = _new_value # new value
        else:
            try:
                val, index = self.in_config(_item)
                if terminalmessage: print(val, index)
                if val is not None:
                    L[index][1] = _value
                else:
                    print('Error, value found in configuration file is None.')
                    quit()
            except:
                print('Error, unable to find the value, while trying to edit it .', end = ' -0- ')
                print('The configuration file is: ',L, end = ' -0- ')
                print('The search item is : ', _item, "it's value : ", _value)
                success = False
                quit()
            return(True)

        if self.terminalmessage: print('New configuration file content ' + self.value())

        # save new configuration file (with Write_model)
        self.CF_report_config.write_model(self.configuration)

    def get_langDutch(self):
        result = self.value('language')
        if result == 'nl':
            return(True)
        else:
            return(False)

    def get_footer(self):
        result = self.value('footer')
        return(result)
    
    def get_font(self):
        result = self.value('font')
        return(result)
    
    def get_xsfont_height(self):
        result = self.value('xs_font')
        return(result)
    
    def get_lfont_height(self):
        result = self.value('l_font')
        return(result)
    
    def get_lang(self):
        result = self.value('language')
        return(result)
    
    def get_footer_color(self):
        result = self.value('copyright_grey')
        return(result)
    
    def get_lineheight(self):
        result = self.value('line_height')
        return(result)

    def get_gender(self):
        result = self.value('gender')
        return(result)

    def in_config(self, item:str):
        """ in_config looks for item in the configuration file, 
        returns the value of the item <any> and the index of the item <int> in the configuration file
        """
        L = self.configuration
        for i in L:
            if item in i:
                return (L[L.index(i)][1], L.index(i))
        return (None, None)

    # # read item from config file
    def value(self, item:str='*.*'):
        L = self.configuration
        # L = self.CF_report_config.read_model()
        # print(L)
        # print(str(type(L)))

        """Find item's value in the config file. Show all config items with item is '*.*'
        """
        # show all items for search item == '*.*'
        # print('def value line 90 var len(L) is : ', len(L))
        if item == '*.*':
            _answer = ''
            for i in range(len(L)):
                for j in range(len(L[i])):
                    _answer = _answer + str(L[i][j]) + ' '
                _answer = _answer + ' - '
            return(_answer)

        else:
            for i in L:
                if item in i:
                    _find = L.index(i)
                    return(L[_find][1])
            return('None',-1)

    #add item to config file
    def add_item(self, _item_name:str = 'None', ):
        L = self.configuration
        chosen = False
        while not(chosen):
            _item_name = input('Provide name of  configuration item: ')
            _item_value = input('Provide value of  configuration item: ')
            _item_type = input('Provide Type (String|Integer|Float|Boolean|List of floats) of configuration item [S|I|F|B|L]: ').upper()
            
            match(_item_type):
                case 'S': L.append([_item_name,_item_value]);  chosen = True
                case 'I': L.append([_item_name,int(_item_value)]);  chosen = True
                case 'F': L.append([_item_name,float(_item_value)]);  chosen = True
                case 'B': L.append([_item_name,bool(_item_value)]);  chosen = True
                case 'L': 
                    _item_value = self.lostr2float(_item_value) # convert string list of floats to list of floats
                    L.append([_item_name,_item_value]);  chosen = True
                case _:
                    print("Wrong Type, try again, only type [S|I|F|B|L] ")
            self.CF_report_config.write_model(L)
        return(L)

if __name__ == '__main__':
    test_subject = input('Give name candidate : ')
    CF_report_number = input('Give test ID : ')
    config_file_name = str(test_subject) + '_' + str(CF_report_number) + '_config'
    test_me = config4CFreport()
    test_me.config_exist()
    user_quit = False
    while not(user_quit):
        Menu = int(input('Choose menu option. [0] add item, [1] edit item, [2] lookup value, [3] test in_config, module, [4] test edit item, [5[ get footer, [99] exit menu -> [0|1|2|3|4|5|99]: '))
        match(Menu):
            case 0 : test_me.add_item()
            case 1 : test_me.edit_item()
            case 2 : print(test_me.value('*.*'))
            case 3 : print(test_me.in_config('xs_font'))
            case 4:  print(test_me.edit_item('xs1_font', 9)) # Non-user functionality added to edit_item
            case 5:  print(test_me.get_footer())
            case 6:  print(test_me.get_gender())
            case 99: quit()
            case _ : print("Wrong Type, try again, only type [0|1|2|99] "); user_quit = True
    
