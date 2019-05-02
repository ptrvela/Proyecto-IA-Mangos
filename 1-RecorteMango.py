"""
Aplicacion para detectar la imagen donde se encuentra un mango y
recortar una seccion del mismo

"""

from __future__ import division
import cv2
import numpy as np
from os import listdir


def mostar(imagen):
    imagen = cv2.resize(imagen, (600, 400))
    cv2.imshow('Mango', imagen)
    cv2.waitKey(0)

"""
    recorre el directorio en donde se encuentran las imagenes,
    para encontrar las fotografias de los mangos

"""
def rDirectorio(carpeta_entrada, carpeta_salida, lista_imagenes):
    for nombre_imagen in lista_imagenes:
        imagen = cv2.imread(carpeta_entrada + "/" +nombre_imagen)
        encontrar = encontrarMango(imagen)
        cv2.imwrite(carpeta_salida + "/" + nombre_imagen, encontrar)


"""
    Encuentra el contorno del mango en la imagen
"""
def contornoMango(imagen):
    imagen = imagen.copy()
    contornos, jerarquia =cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)

    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara

"""
    con los datos encontrados de la imagen en su contorno
    se calcula las dimensiones del cuadrado y su ubicacion
"""

def contornoRectangulo(imagen, contorno):
    imagenConElipse = imagen.copy()
    elipse = cv2.fitEllipse(contorno)
    factor_redn = 0.5
    sx = int((elipse[1][0]*factor_redn)/2)
    sy = int((elipse[1][1]*factor_redn)/2)
    x = int(elipse[0][0]) - sy
    y = int(elipse[0][1]) - sx

    #   cv2.imshow('tomate', img)
    #   cv2.waitKey(0)
    imagenConElipse = imagenConElipse[y:(y + sx*2), x:(x + sy*2)]
    return imagenConElipse

"""
    Trata la imagen para poder encontrar el cuadrado
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

    contorno_mango_grande, mascara_mango = contornoMango(mascara_limpia)

    rectangulo_mango = contornoRectangulo(imagen3, contorno_mango_grande)

    return rectangulo_mango

rDirectorio("MangosBuenos", "RecortesMangosBuenos", listdir("./MangosBuenos"))
rDirectorio("MangosMalos", "RecortesMangosMalos", listdir("./MangosMalos"))
rDirectorio("MangosVerdes", "RecortesMangosVerdes", listdir("./MangosVerdes"))
