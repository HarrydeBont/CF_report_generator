# https://blog.finxter.com/how-to-convert-a-string-list-to-a-float-list-in-python/#:~:text=The%20most%20Pythonic%20way%20to,x)%20built%2Din%20function.


def lostr2float(b:str = '[2.3, -1.1, 55.1]'):
    b=b.replace('[','')
    b=b.replace(']','')
    b=b.replace(',','')
    b = b.split()
    b =list(map(float, b))
    return(b)

convert = lostr2float()
print(convert, type(convert))
