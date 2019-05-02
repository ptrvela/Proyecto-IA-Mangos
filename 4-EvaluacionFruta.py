"""
Aplicacion para extraer un recorte de la imagen donde se encuentra
un mangos.

"""

from __future__ import division
import cv2
import numpy as np
from PIL import Image
from os import listdir
import os
import neurolab as nl
import scipy as sp


def mostar(imagen):
    imagen = cv2.resize(imagen, (600, 400))
    cv2.imshow('mango', imagen)
    cv2.waitKey(0)

def encontar_contorno(imagen):
    imagen = imagen.copy()
    img, contornos, jerarquia = cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes =[(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara

def contorno_rectangulo(imagen, contorno):
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

def ecnontrar_mango(imagen):
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
    ######cv2.imshow('mango', mascara1)######
    ######cv2.waitKey(0)######

    min_amarillo2 = np.array([180, 100, 120])
    max_amarillo2 = np.array([248, 234, 239])
    mascara2 = cv2.inRange(imagen_azul, min_amarillo2,max_amarillo2)
    ######cv2.imshow('mango', mascara2)######
    ######cv2.waitKey(0)######


    mascara = mascara1 + mascara2

    ##cv2.imshow('mango', mascara)
    ##cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mascara_cerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    mascara_limpia = cv2.morphologyEx(mascara_cerrada, cv2.MORPH_OPEN, kernel)

    contorno_mango_grande, mascara_mango = encontar_contorno(mascara_limpia)

    rectangulo_mango = contorno_rectangulo(imagen3, contorno_mango_grande)

    return rectangulo_mango

    #contorno_mango_gramde, mascara_mango = encontar_contorno(mascara_limpia)

    #rectangulo_mango = contorno_rectangulo(imagen3, contorno_mango_gramde)
    #rectangulo_tomate = cv2.resize(rectangulo_tomate, (100, 50))
    # recortar(rectangulo_tomate)
    #return rectangulo_mango

"""

===============================================================================================================

"""

def sacar_pixels(imagen):
    #se abre la imagen
    im = Image.open(imagen)
    im = im.resize((40, 10), Image.ANTIALIAS)
    #im = im.resize((100, 50), Image.ANTIALIAS)
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


def normalizar(valor):
    salida = (valor*1.)/255.
    return salida

"""
=======================================================================================
"""

imagen1 = cv2.imread("malo1.jpg")
imagen1 = ecnontrar_mango(imagen1)
cv2.imwrite("mango-recortado.jpg",imagen1)

cadena =  sacar_pixels("mango-recortado.jpg")

if(os.path.exists("datos-mango.csv")== True):
    os.remove("datos-mango.csv")

archivo_entrenamiento = open("datos-mango.csv", "a")

archivo_entrenamiento.write(cadena)
archivo_entrenamiento.close()

datos = np.matrix(sp.genfromtxt("datos-mango.csv", delimiter=" "))

print datos.shape

rna = nl.load("Trained-RNA.tmt")

salida = rna.sim(datos)

podrido = salida[0][0] * 100
maduro = salida[0][1] * 100
verde = salida[0][2] * 100

resultado = ""

if (podrido > 80.):
    if (maduro > 40.):
        resultado = "el mango esta a punto de podrirse"
    else:
        resultado = "el mango esta podrido"
elif (maduro > 80.):
    if (podrido > 40.):
        resultado = "el mango esta pasandose de su madurez"
    elif (verde > 40.):
        resultado = "El mango esta a punto de llegar a su madurez"
    else:
        resultado = "El mango esta en su mejor punto"
elif (verde > 80.):
    if (maduro > 40.):
        resultado = "el mango esta madurando"
    else:
        resultado = "el mango esta verde"

print resultado
