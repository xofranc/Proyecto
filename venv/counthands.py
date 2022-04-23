#                   Se importan las librerias de python que se usaran en la ejecucion del codigo del

import math
import cv2
import mediapipe as mp
import time


#                   Se Crea la clase de python

class DetectorHands():
    #       Se inicializan los parametros de deteccion del codigo
    def __init__(self, mode=False, maxhand=2, confdetection=0.5, confseguimiento=0.5):
        self.mode = mode  # Se crea el objeto que tendra su propia variable
        self.maxhand = maxhand  # lo mismo se realizara con todos los objetos
        self.confdetection = confdetection
        self.confseguimiento = confseguimiento

        #           Se crearan los objetos que detectaran las manos y las dibujaran
        selfmpmanos = mp.solutions.hands
        self.manos = self.mpmanos(self.mode, self.maxhand, self.confdetection, self.confdetection)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]


    #               Funcion  para encontrar las manos
    def encontrarmanos(self, frame, dibujar = True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS) #dibujamos las conecxiones de los puntos de las manos
                return frame