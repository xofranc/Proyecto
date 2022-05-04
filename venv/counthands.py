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
        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxhand, self.confdetection, self.confseguimiento)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]

    #               Funcion  para encontrar las manos
    def encontrarmanos(self, frame, dibujar=True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)  # dibujamos las conecxiones de los puntos de las manos
                return frame


    def encontrarposicion(self, frame, ManoNum=0, dibujar=True):
        xlista = []
        ylista = []
        bbox =  []
        self.lista=[]
        if self.resultados.multi_hand_landmarks:
            miMano= self.resultados.multi_hand_landmarks[ManoNum]
            for id, lm in enumerate(miMano.Landnark):
                alto, ancho, C = frame.shape    #extraemos las dimensiones en fps
                cx, cy = int(lm.x * ancho), int(lm.y *alto)     #Convertimos la informacion el pixeles
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([id, cx, cy])
                if dibujar:
                    cv2.circle(frame(cx, cy), 5, (0, 0, 0), cv2.FILLED)  # Dibujanos un circulo

            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax
            if dibujar:
                cv2.rectangle(frame(xmin - 20, ymin - 20), (xmax - 20, ymax - 20), (0,255,2), 2)
            return self.lista, bbox


    #               Funcion para detectar y dibujar los dedos arriba
    def dedosarriba(self):
            dedos = ()
            if self.lista[self.tip[0]][1] > self.lista[self.tip[0]-1][1]:
                dedos.append(1)
            else:
                dedos.append(0)
            for id in range(1, 5):
                if self.lista[self.tip[id]][2] < self.lista[self.tip[id]-2][2]:
                    dedos.append(1)
                else:
                    dedos.append(0)

            return dedos



    #              funcion para detectar la distancia entre dedos

    def distancia(self, p1, p2, frame, dibujar=True, r=15, t=3):
        x1, y1 = self.lista[p1][1:]
        x2, y2 = self.ista[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if dibujar:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), t)
        cv2.circle(frame, (x1, y1), r, (0, 0, 255), cv2.FILLED)
        Cv2.circle(frame, (x2, y2), r, (0, 0, 255), cv2.FILLED)
        Cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, frame, [x1, y1, x2, y2, cx, cy]



    #               Funcion Principal
    def main():
        ptiempo = 0
        ctiempo = o


        #           leemos la camara webs
        cap = cv2.VideoCapture(1)
        # Creamos el detector de manos
        detector =  detectormanos()
        #realizamos la deteccion de las manos
        while true:
            ret, frame = cap.read()
            #una vez obtenida la informacion se envia
            frame = detector.encontrarmanos(frame)
            lista , bbox = detector.encontrarposicion(frame)
