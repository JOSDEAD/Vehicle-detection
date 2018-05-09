from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import serial 
# argumentos necesarios para iniciar el programa
ap = argparse.ArgumentParser()
# informacion de como esta estructurada la red neuronal
ap.add_argument("-p", "--prototxt", required=True)
# modelo entrenado
ap.add_argument("-m", "--model", required=True)
probabilidadMinima=0.2
args = vars(ap.parse_args())
probabilidad=0.2
# Se inicializan las clases con las que esta entrenado el modelo usado
CLASES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
# se cargan colores random para asignar a cada objeto detectado
COLORES = np.random.uniform(0, 255, size=(len(CLASES), 3))

# Se carga el modelo
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
#se estable conexion con arduino
ser = serial.Serial('/dev/ttyACM0', 9600) 
# se carga la camara de video y se espera un tiempo para que se inicie la grabacion
camara = VideoStream(src=1).start()
time.sleep(2.0)


# Se crea una imagen negra simulando que la lampara esta apagada
img = np.zeros((900,1600,3), np.uint8)
cv2.namedWindow("lampara", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("lampara",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)




# ciclo que va por todas la imagen que capta la camara
while True:
        
	# se capta cada imagen de la camara y se le da un tamano
	imagen = camara.read()
	imagen = imutils.resize(imagen, width=400)

	# se para cada imagen a una matriz de 2 dimensiones
	(h, w) = imagen.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(imagen, (300, 300)),
		0.007843, (300, 300), 127.5)

	# se pasa la imagen transformada por la red
	net.setInput(blob)
    # se obtiene las objetosDetectados de lo que es la imagen
	objetosDetectados = net.forward()
    # se pone el fondo negro de la lampara para decir que esta apagada
	img[:] = (0, 0, 0)
        ser.write('0')
    #se apaga el led de la lampara
	# se recorre por todos los objetos detectados
	for i in np.arange(0, objetosDetectados.shape[2]):
		# se obtiene la probabilidad que tiene cada objeto
		probabilidad = objetosDetectados[0, 0, i, 2]

		# Solo pasan los objetos que son mayores a la probabilidad minima
		if probabilidad > probabilidadMinima:
            # se obtiene el indice de la etiqueta cada objeto detectado, 
            #luego se averigua en donde estan hubicados en la imagen para dibujar la caja de deteccion

			idx = int(objetosDetectados[0, 0, i, 1])
			caja = objetosDetectados[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = caja.astype("int")

			if(CLASES[idx]=="car" or CLASES[idx]=="person" or CLASES[idx]=="bicycle" or CLASES[idx]=="motorbike" or CLASES[idx]=="bus"):
				# Se dibuja la caja de deteccion
				img[:] = (255, 255, 255)
                                ser.write('1')
                #se enciende el led de la lampara
				label = "{}: {:.2f}%".format(CLASES[idx],
					probabilidad * 100)
				cv2.rectangle(imagen, (startX, startY), (endX, endY),
					COLORES[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(imagen, label, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORES[idx], 2)

	# Se muestra la imagen de la camara
	cv2.imshow("Frame", imagen)
	key = cv2.waitKey(1) & 0xFF
    # se dibuja la imagen de la lampara
	cv2.imshow('lampara',img)

	# S para detener el ciclo
	if key == ord("s"):
		break



# Se cierran las ventanas y se detiene la camara
cv2.destroyAllWindows()
camara.stop()
