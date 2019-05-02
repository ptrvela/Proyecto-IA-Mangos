"""
    Librerias necesarias para el funionanmiento de la interfaz
"""
from __future__ import division
import cv2
import numpy as np
from os import listdir
import os
import neurolab as nl
import scipy as sp
import cPickle as pickle
import dill
from Tkinter import *
from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH, RAISED, RIGHT
from ttk import Frame, Style, Button
from tkFileDialog import askopenfilename


class Mango(Frame):
    """
    ESta para solo contiene codigo de interfaz dibujo de ventas label imagen
    """
    global contornoMango
    global contornoRectangulo
    global encontrarMango
    global extraerPixeles
    global normalizar

    """
        muestra tkflied para abrir un archivo
        guarda la ruta del archivo
        llama al metodo neuronas que es donde hace la evaluacion de la imagen
        y retorna
    """
    def abrir(self):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        self.neuronas(filename)
        self.imagen(filename)

        """
        carga la imagen que se selecciono en pantalla
        """
    def imagen(self, filename):
        bard = Image.open(filename)
        bard = bard.resize((400,550), Image.ANTIALIAS)
        bardejov = ImageTk.PhotoImage(bard)
        label1 = Label(self, image=bardejov)
        label1.image = bardejov
        label1.place(x=10, y=25)

        """
        funcion principal de la clase
        """

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

        """
        muestra en pantalla los datos obtenidos
        en el label que se dibuja
        """

    def salida1(self, texto):
        label = Label(self, text=texto, fg="#0417F9", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=700, y=150)


    def salida2(self, texto):
        label = Label(self, text=texto, fg="#0417F9", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=700, y=200)

    def salida3(self, texto):
        label = Label(self, text=texto, fg="#0417F9", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=700, y=250)

    def estado(self, texto):
        label = Label(self, text=texto, fg="#27FF00", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=550, y=350)


        """
            en este metodo estan doas las funciones a llamar
        """
    def initUI(self):
        self.parent.title("MANGOS")
        self.pack(fill=BOTH, expand=True)
        Style().configure("TFrame", background="#FFFFFF")
        # self.imagen("inicio.jpg")
        self.salida1("")
        self.salida2("")
        self.salida3("")
        self.estado("")

        AbrirButton = Button(self, text="Abrir")
        AbrirButton.pack(side=RIGHT, padx=5, pady=5)
        AbrirButton.place(x=800, y=25)
        AbrirButton["command"] = self.abrir

        label = Label(self, text="Datos de salida", fg="#000000", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=550, y=60)

        label = Label(self, text="(Salida1) PODRIDO:", fg="#FF00F3", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=500, y=150)

        label = Label(self, text="(Salida2) MADURO:", fg="#FF00F3", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=500, y=200)

        label = Label(self, text="(Salida3) VERDE:", fg="#FF00F3", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=500, y=250)

        label = Label(self, text="Estado del MANGO:", fg="#0040ff", bg="#FFFFFF", font = "Helvetica 16 bold italic")
        label.place(x=500, y=300)
        """
    ESta parte contiene el analisis de las imagenes
    encontrando imagen
    recortando
    redimensionando
    envia a la rna
    la rna devuelve datos que son mostrados en la parte visual
    """

    def contornoMango(imagen):
        imagen = imagen.copy()
        img, contornos, jerarquia =\
            cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contour_sizes = \
            [(cv2.contourArea(contorno), contorno) for contorno in contornos]
        mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

        mascara = np.zeros(imagen.shape, np.uint8)
        cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
        return mayor_contorno, mascara

        """
        encuentra el rectangulo
        """
    def contornoRectangulo(imagen, contorno):
        imagenConElipse = imagen.copy()
        elipse = cv2.fitEllipse(contorno)
        factor_redn = 0.5
        sx = int((elipse[1][0]*factor_redn)/2)
        sy = int((elipse[1][1]*factor_redn)/2)
        x = int(elipse[0][0]) - sy
        y = int(elipse[0][1]) - sx
        #cv2.elipse(imagenConElipse, elipse, green, 2, cv2.LINE_AA)
        #cv2.rectangle(imagenConElipse, (x,y), ((x + sy*2), (y + sx*2)), (255,0,0),2)
        imagenConElipse = imagenConElipse[y:(y + sx*2), x:(x + sy*2)]
        return imagenConElipse

        """
        encuentra la imagen
        """
    def encontrarMango(imagen):
        imagen2 = imagen.copy()
        imagen3 = imagen.copy()
        imagen2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2HSV)
        max_dimension = max(imagen2.shape)
        scale = 700/max_dimension
        imagen2 = cv2.resize(imagen2, None, fx=scale, fy=scale)
        imagen3 = cv2.resize(imagen3, None, fx=scale, fy=scale)
        imagen_azul = cv2.GaussianBlur(imagen2, (7, 7), 0)
        min_amarillo = np.array([0, 155, 25])
        max_amarillo = np.array([256, 256, 256])

        mascara1 = cv2.inRange(imagen_azul, min_amarillo, max_amarillo)

        min_amarillo2 = np.array([180, 100, 120])
        max_amarillo2 = np.array([248, 234, 239])

        mascara2 = cv2.inRange(imagen_azul, min_amarillo2,max_amarillo2)

        mascara = mascara1 + mascara2

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        mascara_cerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
        mascara_limpia = cv2.morphologyEx(mascara_cerrada, cv2.MORPH_OPEN, kernel)

        contorno_mango_grande, mascara_mango = contornoMango(mascara_limpia)

        rectangulo_mango = contornoRectangulo(imagen3, contorno_mango_grande)
        #rectangulo_tomate = cv2.resize(rectangulo_tomate, (100, 50))
        # recortar(rectangulo_tomate)
        return rectangulo_mango

    """

    ===============================================================================================================

    """
    """
    de la imagen cortada saca los pixeles
    """
    def extraerPixeles(imagen):
        #se abre la imagen
        im = Image.open(imagen)
        im = im.resize((40, 10), Image.ANTIALIAS)
        #im.save("hola.jpg")
        #lectura de pixels
        pixels = im.load()

        filas, columnas = im.size
        decimales = 4
        cadena = ""
        for columna in range (columnas):
            for fila in range(filas):
                #se separan los valores RGB y se escriben en el archivo
                rojo = str(normalizar(pixels[fila,columna][0]))
                verde = str(normalizar(pixels[fila,columna][1]))
                azul = str(normalizar(pixels[fila,columna][2]))
                cadena = cadena + rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "

        return cadena

        """
        normaliza las salidas a rangos de 0 y 1
        """
    def normalizar(valor):
        salida = (valor*1.)/255.
        return salida


        """
        funcion principal del analisi de datos
        hasta el envio por ls rna
        devolviendo los datos de entrada
        """

    def neuronas(self, filedir):
        imagen = cv2.imread(filedir)
        imagen = encontrarMango(imagen)
        cv2.imwrite("mangoRecortado.jpg",imagen)
        cadena =  extraerPixeles("mangoRecortado.jpg")
        if(os.path.exists("datosMango.csv")== True):
            os.remove("datosMango.csv")
        archivo_entrenamiento = open("datosMango.csv", "a")
        archivo_entrenamiento.write(cadena)
        archivo_entrenamiento.close()
        datos = np.matrix(sp.genfromtxt("datosMango.csv", delimiter=" "))
        rna = nl.load("Trained-RNA.tmt")
        salida = rna.sim(datos)
        self.salida1(str(salida[0][0]))
        self.salida2(str(salida[0][1]))
        self.salida3(str(salida[0][2]))
        podrido = salida[0][0] * 100
        maduro = salida[0][1] * 100
        verde = salida[0][2] * 100

        if (podrido > 80.):
            if (maduro > 40.):
                resultado = "El Mango esta a punto de PODRIRSE, debe consumirse pronto"
                self.estado(resultado)
            else:
                resultado = "El Mango esta PODRIDO, NO es apto para su consumo"
                self.estado(resultado)
        elif (maduro > 80.):
            if (podrido > 40.):
                resultado = "El Mango esta PASANDO su punto madurez"
                self.estado(resultado)
            elif (verde > 40.):
                resultado = "El Mango esta A PUNTO DE LLEGAR a su madurez"
                self.estado(resultado)
            else:
                resultado = "El Mango esta en su MEJOR PUNTO"
                self.estado(resultado)
        elif (verde > 80.):
            if (maduro > 40.):
                resultado = "El Mango esta MADURANDO"
                self.estado(resultado)
            else:
                resultado = "El Mango esta VERDE, aun no puede ser consumido"
                self.estado(resultado)





def main():
    root = Tk()
    root.geometry("900x600")
    root.resizable(False,False)
    app = Mango(root)
    root.mainloop()


if __name__ == '__main__':
    main()
