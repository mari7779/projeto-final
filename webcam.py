import cv2
import pytesseract

# Configurando o caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ler_placa():
    url_camera = 'rtsp://admin:educere2991@192.16.3.25:37777/cam/realmonitor?channel=1&subtype=0'

    cap = cv2.VideoCapture(url_camera)

    while True:
        # Capturando o quadro atual da câmera
        ret, frame = cap.read()

        # Convertendo o quadro para escala de cinza.
        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicando threshold para destacar as regiões de texto
        _, threshold = cv2.threshold(cinza, 150, 255, cv2.THRESH_BINARY)

        # Realizando a detecção de contornos
        contornos, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterando sobre os contornos encontrados
        for contorno in contornos:
            # Obtendo as coordenadas do retângulo delimitador
            x, y, w, h = cv2.boundingRect(contorno)

            # Desenhando o retângulo na imagem original
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Recortando a região da placa
            regiao_placa = cinza[y:y+h, x:x+w]

            # Utilizando o Tesseract para realizar a OCR na região da placa
            texto_placa = pytesseract.image_to_string(regiao_placa, config='--psm 8')

            # Exibindo o texto da placa
            print("Placa: ", texto_placa)

        # Exibindo o vídeo ao vivo com os retângulos desenhados
        cv2.imshow('Placa Detectada', frame)

        # Aguardando 1 milissegundo para capturar a próxima frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberando a captura de vídeo e fechando as janelas
    cap.release()
    cv2.destroyAllWindows()

# Chamando a função para capturar vídeo da câmera IP Wi-Fi e realizar a detecção de placas
ler_placa()