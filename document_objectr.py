# test to objectR a document and it's configurationfile
# using multipage.pdf, C:\Users\HWdeB\Documents\Python\GoogleSheetAPI\config_test.OBJTR as test files
from objectR_handler import objecter
# import file_operations

test_combi_object = objecter('test_dir','combi_doc_config')
try:
    pdf_document = 'pdf file directory and  name.pdf'
    pdf_config = [['language','Dutch'],['gender','M'],['font','Helvetica'],['xs_font',10],['l_font',12],['copyright_grey', [0.25, 0.25, 0.25]],['line_height',12]]
    combi_object = [pdf_document, pdf_config]
    test_combi_object.write_model(combi_object)
    print( 'success!')
except:
    pass

test_combi_object.verify()
succes_save = test_combi_object.read_model()
print(succes_save)
