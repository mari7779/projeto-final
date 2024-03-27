import cv2
import pytesseract
import mysql.connector
from datetime import datetime
from imutils.video import VideoStream
import time
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def conectar(host, user, senha, banco):
    return mysql.connector.connect(host=host, user=user, password=senha, database=banco)

def detectar_placa(frame):

    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    placa = pytesseract.image_to_string(frame_cinza, config='--psm 8')

    placa_filtrada = re.sub(r'[^A-Z0-9]', '', placa)

    if placa_filtrada:
        print('Placa do carro:', placa_filtrada)

        conn = conectar("localhost", "root", "Projeto0324.", "armaz_placas")
        c = conn.cursor()

        data_hora_acesso = datetime.now()

        c.execute("INSERT INTO placas (placa, data_hora_acesso) VALUES (%s, %s)", (placa_filtrada, data_hora_acesso))
        conn.commit()
        print("Placa inserida com sucesso!")

        def lista_placas():
            c.execute("SELECT * FROM placas")
            placas = c.fetchall()
            print("Placas armazenadas:")
            for placa in placas:
                print(placa)

        c.close()
        conn.close()

        cv2.imshow('Frame', frame)

def open_camera_and_process():
    url_camera = 'rtsp://admin:educere2991@192.168.3.25:37777/cam/realmonitor?channel=1&subtype=0'
    vs = VideoStream(src=url_camera).start()

    time.sleep(2.0)

    while True:
        frame = vs.read()

        detectar_placa(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vs.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    open_camera_and_process()
