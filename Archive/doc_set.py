""" doc_set will fascilitate control over default document settings. 
Think of font, font height, line height, and so on.
version 0.1 - November 2022, Harry de Bont
    Initial document
version 0.2 - 15 November 2022, Harry de Bont
    create functionality for a config file per report

"""
# from directory_structure import dir_struc

# # import objectrR_handler routine
# from objectR_handler import objecter
# Rdir = dir_struc()
# Xpro_config = objecter('reports','config_Xpro')

# def config_exist():
#     # Configuration file exist?
#     # create configuration file
#     if not(Xpro_config.verify()):
#         # create first set-up if the config file doesn't exist
#         configuration = [['content','configuration file, contains: font, font_height'],['language','nl'],['font','Helvetica'],['xs_font',10],['l_font',12],['copyright_grey', [0.25, 0.25, 0.25]],['line_height',12]]
#         #save config file as a serialized object
#         Xpro_config.write_model(configuration,True)
#     # #read the configuration file into configuration
#     # configuration  = Xpro_config.read_model(True)
#     configuration = Xpro_config.read_model(True)
# #     return(configuration)

# configuration = config_exist()

# Retrieve item from config file
# def get_config(_item:str='content'):
#     """ Retrieve _item = 'content' for set_up of the configuration file
#     """
#     test = Xpro_config.read_model(True)
#     # print('Get config here ->')
#     # print(test)
#     # print(str(type(test)))
#     # print('<- config out')
    
#     # _item_val = 'return value'
#     _item_val = np.where(test == _item )
    
#     # print(_item_val)
#     # for i,value in enumerate(test):
#     #     print( 'Inside get_config '+ )
#     return(_item_val)

# compose list of floats from string input format '[2.3, -1.1, 55.1]' - mind the spaces!
# def lostr2float(b:str = '[2.3, -1.1, 55.1]'):
#     b=b.replace('[','')
#     b=b.replace(']','')
#     b=b.replace(',','')
#     b = b.split()
#     b =list(map(float, b))
#     return(b)

# editing configuration file
# def edit_item(L:list = configuration):
#     print('Current config file items are [' + value('*.*') + ']')
#     print('Which configuration item do you want to change? : ')
#     for i in range(len(L)):
#         print('['+str(i)+'] '+L[i][0], end=" ")

#     # ask for config item to edit
#     incorrect  =True
#     while incorrect:
#         _choice = input('Edit item? [] : ')
#         try:
#             _choice = int(_choice)
#             if _choice in range(0, len(L)):
#                 incorrect = False
#             else:
#                 print('Enter a value from [0] to ['+str(len(L)-1)+']')
#         except:
#             print('Incorrect, enter a valid number ')
#     # Show old value of selected _item
#     print('Old value of ' + str(L[_choice][0]) + ' was ' + str(value(L[_choice][0])))
#     _new_value_type = type(L[_choice][1])
#     print(_new_value_type)
#     # convert input to type of the old value
#     _new_value = _new_value_type((input('What is the new value? : ')))
#     L[_choice][1] = _new_value
#     print('New configuration file content ' + value())

#     # save new configuration file (with Write_model)
#     Xpro_config.write_model(configuration,True)

# def change_lang(_val, L:list = configuration):
    
#     # ask for config item to edit
#     incorrect  =True

#     # Show old value of selected _item
#     _new_value = _val
#     L[1][1] = _new_value #change value for 'language'
    
#     # save new configuration file (with Write_model)
#     Xpro_config.write_model(configuration,True)


# save configuration file

# read item from config file
# def value(item:str='*.*',L:list = configuration):
#     """Find item's value in the config file. Show all config items with item is '*.*'
#     """
#     # show all items for search item == '*.*'
#     # print('def value line 90 var len(L) is : ', len(L))
#     if item == '*.*':
#         _answer = ''
#         for i in range(len(L)):
#             for j in range(len(L[i])):
#                 _answer = _answer + str(L[i][j]) + ' '
#             _answer = _answer + ' - '
#         return(_answer)

#     else:
#         # print('value-else line 100 var L is : ', L)
#         for i in L:
#             # print('value-else line 102 var i is : ', i)
#             if item in i:
#                 # print('value-else line 104 var item is : ', item)
#                 _find = L.index(i)
#                 # print('value-else line 106 var _find is : ', _find) 
#                 return(L[_find][1])
#         return('None',-1)

#add item to config file manually
# def add_item(L:list = configuration,_item_name:str = 'None'):
#     chosen = False
#     while not(chosen):
#         _item_name = input('Provide name of  configuration item: ')
#         _item_value = input('Provide value of  configuration item: ')
#         _item_type = input('Provide Type (String|Integer|Float|Boolean|List of floats) of configuration item [S|I|F|B|L]: ').upper()
        
#         match(_item_type):
#             case 'S': L.append([_item_name,_item_value]);  chosen = True
#             case 'I': L.append([_item_name,int(_item_value)]);  chosen = True
#             case 'F': L.append([_item_name,float(_item_value)]);  chosen = True
#             case 'B': L.append([_item_name,bool(_item_value)]);  chosen = True
#             case 'L': 
#                 _item_value = lostr2float(_item_value) # convert string list of floats to list of floats
#                 L.append([_item_name,_item_value]);  chosen = True
#             case _:
#                 print("Wrong Type, try again, only type [S|I|F|B] ")
#         Xpro_config.write_model(L,True)
#     return(L)

    #add item to config file manually

if __name__ == '__main__':
    pass

