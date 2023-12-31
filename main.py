from cvzone.PoseModule import PoseDetector
import cv2
import cvzone

video = cv2.VideoCapture('vd06.mp4')
detector = PoseDetector()

while True:
    check, img = video.read()
    img = cv2.resize(img, (1280, 720))
    resultado = detector.findPose(img)
    pontos, bbox = detector.findPosition(img, draw=False)
    if len(pontos) >= 1:
        x, y, w, h = bbox['bbox']
        cabeca = pontos[0][1]
        joelho = pontos[26][1]
        diferenca = joelho - cabeca
        if diferenca <= 0:
            cvzone.putTextRect(img, 'QUEDA DETECTADA', (x, y - 80), scale=3, thickness=3, colorR=(0, 0, 255))
    
    cv2.imshow('IMG', img)
    
    # Adicione um atraso de 100 milissegundos (0,1 segundo) entre cada quadro.
    key = cv2.waitKey(100)
    
    # Se pressionar a tecla 'q', saia do loop.
    if key == ord('q'):
        break

# Feche a janela e libere a captura de vídeo quando o loop terminar.
video.release()
cv2.destroyAllWindows()
