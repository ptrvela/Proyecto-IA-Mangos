# -*- coding: utf-8 -*-
"""
- Aplicacion para leer los recortes de las carpetas especificas, creadas por "RecorteMango"

- Redimensionar las imagenes con un algoritmo sin perdida (ANTIALIAS)
  dejando las imagenes de tamaño 40 x 10

- Normaliza los datos entre 0 y 1 con tres decimales
  agrega 3 datos al final, para identificar el nivel de madurez de los mangos
  quedando de esta manera

                            1 0 0   Podrido
                            0 1 0   Maduro
                            0 0 1   Verde

  -Lee todos los pixeles de cada imagen, y los guarda en "TrainingData.csv"
"""
from PIL import Image
from os import listdir
import os


"""
    Extrae los pixeles de las imagenes recortadas
    para ser guardados en un archivo "TrainingData.csv"

"""
def extraerPixeles(direccion, entrada):
    #Abre la imagen
    im = Image.open(direccion)

    #redimensiona la imagen con ANTIALIS, algoritmo con menos perdida
    im = im.resize((40, 10), Image.ANTIALIAS)

    #im = im.resize((100, 50), Image.ANTIALIAS)
    #im.save("hola.jpg")
    #lectura de pixels
    pixeles = im.load()

    #se abre el archivo para lectura-Escritura
    archivoEntrenamiento = open("TrainingData.csv", "a")
    filas, columnas = im.size
    decimales = 4
    for columna in range (columnas):
        for fila in range(filas):

            #se separan los valores RGB y se escriben en el archivo
            rojo = str(normalizar(pixeles[fila,columna][0]))
            verde = str(normalizar(pixeles[fila,columna][1]))
            azul = str(normalizar(pixeles[fila,columna][2]))
            cadena = rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "
            archivoEntrenamiento.write(cadena)

    #pix[x,y] = value # Set the RGBA Value of the image (tuple)
    archivoEntrenamiento.write(entrada)
    archivoEntrenamiento.write("\n")
    archivoEntrenamiento.close()

"""
    recorre el directorio en donde se encuentran
    las imagenes recortadas de los mangos

"""
def rDirectorio(carpeta_entrada, lista_imagenes, salida):
    for nombre_imagen in lista_imagenes:
        print nombre_imagen
        extraerPixeles(carpeta_entrada + "/" +nombre_imagen, salida)

"""
    Normaliza los datos, para facilitar el entrenamiento

"""
def normalizar(valor):
    salida = (valor*1.)/255.
    return salida


if(os.path.exists("TrainingData.csv")== True):
    os.remove("TrainingData.csv")
    
rDirectorio("RecortesMangosBuenos", listdir("./RecortesMangosBuenos"), "0 1 0")
rDirectorio("RecortesMangosMalos",  listdir("./RecortesMangosMalos"), "1 0 0")
rDirectorio("RecortesMangosVerdes", listdir("./RecortesMangosVerdes"), "0 0 1" )
