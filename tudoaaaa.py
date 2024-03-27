import cv2
import pytesseract
from imutils.video import VideoStream
import imutils
import mysql.connector
from datetime import datetime 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

rtsp_url = 'rtsp://admin:educere2991@192.16.3.25:37777/cam/realmonitor?channel=1&subtype=0'

# Inicializando o stream de vídeo usando imutils
camera = VideoStream(src=rtsp_url).start()
# Aguarde um curto período para garantir que o stream seja iniciado corretamente
# (você pode ajustar o valor conforme necessário)
cv2.waitKey(1000)


def conectar(host, user, senha, banco):
    return mysql.connector.connect(host=host, user=user, password=senha, database=banco)



while True:
    frame = camera.read()

    if frame is None:
        print("Erro ao capturar o frame. Verifique a conexão com a câmera.")
        break

    # Redimensionando o frame para um tamanho específico (opcional)
    frame = imutils.resize(frame, width=800)

    # Convertendo o frame para escala de cinza
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicando um desfoque para melhorar o OCR
    frame_desfocado = cv2.GaussianBlur(frame_cinza, (5, 5), 0)

    # Usando o Tesseract para realizar o OCR no frame
    placa = pytesseract.image_to_string(frame_desfocado, config='--psm 8')

    # Exibindo a placa detectada
    print('Placa do carro:', placa)

    conn = conectar("localhost", "root", "Bruno30042003", "armaz_placas")
    c = conn.cursor()

    data_hora = datetime.now()
    c.execute("INSERT INTO placas (placa) VALUES (%s, %s)", (placa, data_hora))
    conn.commit()
    print("Placa inserida com sucesso!")
    
    c.close()
    conn.close()

    # Exibindo o frame com a placa destacada (opcional)
    cv2.imshow('Frame', frame)

    # Se a tecla 'q' for pressionada, saia do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
cv2.destroyAllWindows()
