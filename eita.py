import cv2
import pytesseract
import imutils
import mysql.connector
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_license_plate(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 100, 200)

    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            plate = gray[y:y + h, x:x + w]
            plate_text = pytesseract.image_to_string(plate, config='--psm 11')

            if plate_text:
                return plate_text.strip()
    return None

def conectar(host, user, senha, banco):
    return mysql.connector.connect(host=host, user=user, password=senha, database=banco)

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame")
            break

        plate_text = read_license_plate(frame)

        if plate_text:
            print("Placa de licença:", plate_text)

        cv2.imshow('Frame', frame)

        conn = conectar("localhost", "root", "Projeto0324.", "armaz_placas")
        c = conn.cursor()

        data_hora_acesso = datetime.now()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        c.execute("INSERT INTO placas (placa, data_hora_acesso) VALUES (%s, %s)", (plate_text, data_hora_acesso))
        conn.commit()

        def listar_placas():
            c.execute("SELECT * FROM placas")
            placas = c.fetchall()
            print("Placas armazenadas:")
            for placa in placas:
                print(placa)
        
        c.close()
        conn.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "_main_":
    main()