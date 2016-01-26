from reportlab.pdfgen import canvas

aux = canvas.Canvas("prueba.pdf")

aux.drawString(0,0,"Posicion Original (X,Y) = (0,0)")
aux.drawString(50,100,"Posicion (X,Y) = (50,100)")
aux.drawString(150,20,"Posicion (X,Y) = (150,20)")

aux.showPage()
aux.save()