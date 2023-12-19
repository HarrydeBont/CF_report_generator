import io
filename = "D:\\1-Werkmap\CF_report\\text\\explanation_af.txt"
with io.open(filename,'r',encoding='utf8') as f:
    text = f.read()
# process Unicode text
with io.open(filename,'w',encoding='utf8') as f:
    f.write(text)