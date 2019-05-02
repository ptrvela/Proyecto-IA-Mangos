# -*- coding: utf-8 -*-
"""
    -Aplicacion para entrenar una RNA

    -Algoritmo utilizado: backpropagation

    -3 neuronas en la capa de salida
    -n neuronas en la capa de entrada
    -n datos de entrada

    -El numero de neuronas para la primera capa oculta es igual al
     numero de neuronas en la capa de entrada

    -El numero de neuronas en la segunda capa es n/2

    -Factor de correcion 0.03

    -Error Minimo Aceptado 0.05

"""

import neurolab as nl
import numpy as np
import scipy as sp

#lectura de la matriz de datos
datos = np.matrix(sp.genfromtxt("TrainingData.csv", delimiter=" "))

#salida de la neurona
columnaSalida = 3

#datos de entrada a la neurona
entrada = datos[:,:-3]

#datos de salida de la neurona
objetivo = datos[:,-3:]

#maximo y minimo para cada dato de entrada a la neurona
maxmin = np.matrix([[ -5, 5] for i in range(len(entrada[1,:].T))])

# valores para las capas de la neurona
capa_entrada = entrada.shape[0]
capa_oculta1 = int(capa_entrada*0.5)
capa_salida = 3

# Crear red neuronal con 4 capas:
# 1 de entrada
# 2 ocultas
# 1 de salida
rna = nl.net.newff(maxmin, [ capa_entrada, capa_entrada, capa_oculta1, capa_salida])

#Cambio de algoritmo a back progation simple
rna.trainf = nl.train.train_gd

#Datos para la RNA
error = rna.train(entrada, objetivo, epochs=7500000, show=100, goal=0.01, lr=0.01)


#rna.save("neurona.tmt")
# Simulacion RNA
rna.save("Trained-RNA.tmt")
salida = rna.sim(entrada)

print salida
