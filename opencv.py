import cv2

img = cv2.imread("C:\\Users\\Pichau\\Desktop\\mari\\sistema_final\\carro.jpg")
#cv2.imshow("img", img)

cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("cinza", img)

_, bin = cv2.threshold(cinza, 90, 255, cv2.THRESH_BINARY)
#cv2.imshow("binary", img)

desfoque = cv2.GaussianBlur(bin, (5, 5), 0)
#cv2.imshow("defoque", desfoque)

contornos, hierarquia = cv2.findContours(desfoque, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(img, contornos, -1, (0, 255, 0), 1)
#cv2.imshow('cont', img)

for c in contornos:
    perimetro = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
    if len(approx) == 4:
        (x, y, alt, lar) = cv2.boundingRect()
        cv2.rectangle()

cv2.waitKey(0)
cv2.destroyAllWindows()