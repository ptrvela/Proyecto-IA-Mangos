<h1>Madurez de mangos usando un RNA 

Este conjunto de programas tiene como objetivo poder dar una probabilidad de madurez de los mangos, tiene dos objetivos a cumplir:

Entrenar una red neuronal artificial con el fin de poder detectar la madurez de los mangos.
Tener una aplicación de escritorio por el cual un usuario pueda analizar un mango cualquiera.
Características!
Cuenta con su propia RNA, pero puede entrenar la propia.
Solo se necesita tener clasificadas las imágenes en verde, maduro y podrido para poder entrenar la neurona.
Una interfaz gráfica para analizar la madurez de un mango.
La idea principal es que solo se necesite de mangos para reconocer mangos.

Tecnología
Este proyecto utiliza una serie de proyectos de código abierto para funcionar correctamente:

OpenCV – Biblioteca para el tratado de imágenes.
Neurolab - biblioteca de redes neuronales algoritmos básicos con configuraciones de red flexibles y algoritmos de aprendizaje.
Tkinter Interfaz gráfica para Python
Y por supuesto este proyecto es de código abierto con un repositorio público En GitHub.

Installation
Se necesita de Python 2.7 para correr los programas.

Instalar las bibliotecas necesarias para el entrenamiento de la RNA:

$ pip install opencv-python
$ pip install neurolab
Instrucciones de uso
La descripción del proyecto y de las instrucciones del uso de las bibliotecas para usarlas en otros proyectos está en.

Clasifique todas las imágenes de mangos a las que tenga acceso, entre, verde, maduro y podrido, cree las siguientes capertas y coloquelos ahi>

mangos-verdes: mangos verdes
mangos-buenos: mangos maduros
mangos-malos: mangos podridos
cree las siguientes carpetas, ahi se almacenaran recortes de los mangos.

mangos-recortados-buenos
mangos-recortados-malos
mangos-recortados-verdes
Ejecute los siguientes comandos, tome en cuenta que el entrenamiento es tardado y depende de la capacidad de computo y cantidad de imagenes que se utilizen para entrenar.

$ python recortar_mangos.py
$ python entrada_neurona.py
$ python Red_neuronal.py
Reconocer un mangos
$ cd interfaz
$ python interfaz.py
