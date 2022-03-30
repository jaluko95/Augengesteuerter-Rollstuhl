import cv2
import numpy as np


def get_position(x_value, brightness):
    cap = cv2.VideoCapture(0)#Bildquelle; bei RP normalerweise index 0 
    cap.set(11, 200)# kontrast
    
    while True:
        cap.set(10, brightness.value)#70 mittelwert, min 60, max 80
        ret, frame = cap.read() #bildinformationen lesen
        if ret is False:
            break
        
        roi = frame[100:500, 170:850]#Bildausschnitt definieren
        #roi = frame[269: 795, 537: 1416]
        
        #zur Suche der Koordinaten, wird das Bild in schwarz/weiß umgewandelt
        rows, cols, _ = roi.shape
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
        
        #mit Hile von openCV koordinaten der Pupille ermitteln
        _, threshold = cv2.threshold(gray_roi, 3, 255, cv2.THRESH_BINARY_INV)
        contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)#Koordinaten zur Weiterverarbeitung in einzelnen Variablen speichern
            
            x_value.value = int(x) #x koordinate der Pupille an die Steuerung uebergeben
            
            #zeichnen der vertikalen und horizontalen
            #cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
            cv2.line(roi, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
            break
        
        #cv2.imshow("Threshold", threshold)
        #cv2.imshow("gray roi", gray_roi)
        cv2.imshow("Roi", roi)
        #anzeigen des Eyetrackings
        
        key = cv2.waitKey(30)
        if key == 27:
            break