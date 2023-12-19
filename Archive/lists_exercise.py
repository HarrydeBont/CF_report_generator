domains = [['content','configuration file, contains: font, font_height'],['font','Helvotica'],['font_height',12]]
# print(domains[1][1])
# print('de data type of domains is : ' , str(type(domains)))
domains[1][1] = 'Helvetica'
# print("""A list is mutable, a list of tuples isn't""")
# print(domains[0][1])
# print(domains[1][1])
# print(domains[2][1])
# how to search in a list
# length of a list
_n = len(domains)
# print(_n)

# browse through a list
# for i in range(_n):
#     print(domains[i][0], end=' : ')
#     print(domains[i][1])

# # is an item already in the list?
# print(['font','Helvetica'] in domains)

# find item in config file
# https://stackoverflow.com/questions/18041604/search-in-2d-list-using-python-to-find-x-y-position
def value(item:str='*.*',L:list = domains):
    """Find item's value in the config file. Show all config items with item is '*.*'
    """
    # show all items for search item == '*.*'
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

# add an item to the config file
def add_item(L:list = domains):
    chosen = False
    while not(chosen):
        _item_name = input('Provide name of  configuration item: ').upper()
        _item_value = input('Provide value of  configuration item: ').upper()
        _item_type = input('Provide Type (String|Integer|Float|Boolean) of configuration item [S|I|F|B]: ').upper()
        
        match(_item_type):
            case 'S': L.append([_item_name,_item_value]);  chosen = True
            case 'I': L.append([_item_name,int(_item_value)]);  chosen = True
            case 'F': L.append([_item_name,float(_item_value)]);  chosen = True
            case 'B': L.append([_item_name,bool(_item_value)]);  chosen = True
            case _:
                print("Wrong Type, try again, only type [S|I|F|B] ")
    return(L)

# print(value('content'))
# new_list = add_item()
# print(new_list)
# domains = new_list
# print(domains)

# edit an item's value in the config file
# show current value, edit value using the Type of the old value
# save it to configuration file
def edit_item(_item,L:list = domains):
    print('Current config file items are [' + value('*.*') + ']')
    print('Which configuration item do you want to change? : ')
    for i in range(len(L)):
        print('['+str(i)+'] '+L[i][0], end=" ")

    # ask for config item to edit
    incorrect  =True
    while incorrect:
        _choice = input('Edit item? [] : ')
        try:
            _choice = int(_choice)
            if _choice in range(0, len(L)):
                incorrect = False
            else:
                print('Enter a value from [0] to ['+str(len(L)-1)+']')
        except:
            print('Incorrect, enter a valid number ')
    # Show old value of selected _item
    print('Old value of ' + str(L[_choice][0]) + ' was ' + str(value(L[_choice][0])))
    _new_value_type = type(L[_choice][1])
    print(_new_value_type)
    # convert input to type of the old value
    _new_value = _new_value_type((input('What is the new value? : ')))
    L[_choice][1] = _new_value
    print('New configuration file content ' + value())
    # save new configuration file (with Write_model)

edit_item('*.*')



