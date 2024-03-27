import cv2
import pytesseract
from consulta import criar_conexao
from imutils.video import VideoStream
import imutils

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

rtsp_url = 'rtsp://admin:educere2991@192.16.3.25:37777/cam/realmonitor?channel=1&subtype=0'

camera = VideoStream(src=rtsp_url).start()

cv2.waitKey(1000)


con = criar_conexao("localhost", "root", "Bruno30042003", "armaz_placas")

while True:
    frame = camera.read()

    if frame is None:
        print("Erro ao capturar o frame. Verifique a conexão com a câmera.")
        break

    frame = imutils.resize(frame, width=800)
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_desfocado = cv2.GaussianBlur(frame_cinza, (5, 5), 0)

    placa = pytesseract.image_to_string(frame_desfocado, config='--psm 8')

    print('Placa do carro:', placa)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.stop()
cv2.destroyAllWindows()