from reportlab.pdfgen import canvas

def hello(c):
    from reportlab.lib.units import inch

    #First Example
    c.setFillColorRGB(1,0,0) #choose your font colour
    c.setFont("Helvetica", 30) #choose your font type and font size
    c.drawString(100,100,"Hello World") # write your text

    #Second Example
    c.setStrokeColorRGB(0,1,0.3) #choose your line color
    c.line(2,2,2*inch,2*inch)

    #Third Example
    c.setFillColorRGB(1,1,0) #choose fill colour
    c.rect(4*inch,4*inch,2*inch,3*inch, fill=1) #draw rectangle

c = canvas.Canvas("hello.pdf")

hello(c)
c.showPage()
c.save()