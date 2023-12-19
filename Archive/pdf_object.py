# https://stackoverflow.com/questions/65310852/how-to-make-a-python-object-with-an-attribute-that-is-a-pdf-file
""" pdf_object will serialize the information generated per report .
version 0.1 - 14  November 2022, Harry de Bont
    Initial document only pdf
version 0.2 - 15 November 2022, Harry de Bont
    more data to serialize (score, config and pdf)
    first todo doc_set adjust to version 0.2

"""
from objectR_handler import objecter
from directory_structure import dir_struc

objtr_root = dir_struc()

class pdf_2_objctr:
   
    def __init__(self,_dir:str,_pdf_name:str):
        self.objctr_pdf = objecter(_dir,_pdf_name,True)
  

    def convert_pdf2objectr(self, score, config, pdf_path): <------------------------------------------- # we zijn hier actie is uitbreiden naar score, config en pdf per rapport. Eerst doc_set ombouwen naar config per CF-report. dan terug hier... 15/11/2022
        if self.objctr_pdf.verify():

            with open(config_path, 'rb') as config_file:
                config_data = config_file
                config_file.close()

            with open(pdf_path, 'rb') as pdf_file:
                # pdf_data = file.read()
                self.objctr_pdf.write_model(pdf_file.read())
                pdf_file.close()

    def convert_objectr2pdf(self, pdf_path):
        _pdf_data = self.objctr_pdf.read_model()
        with open(pdf_path, 'wb') as file:
            file.write(_pdf_data)
            file.close()
        return(_pdf_data)

report_path = r"PDF_store"

pdf_file = 'Ivar Koehorst_XJ-083.pdf'
test = pdf_2_objctr(report_path,pdf_file)
test.convert_pdf2objectr(pdf_file)

save_path = objtr_root.root_dir() + '\\newpdf_1.pdf'
test.convert_objectr2pdf(save_path)

