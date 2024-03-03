import numpy as np
import cv2 as cv
#from picamera2 import MappedArray, Picamera2, Preview
import math

# Ca c'est pour quand on aura la caméra raspberry

# picam2 = Picamera2()
# def camera_setup(picam, length=960, height=540):
#     picam2.configure(picam2.create_preview_configuration({"size": (length,height)}))
#     picam2.start_preview(Preview.QTGL)
#     picam2.start()

# def take_picture():
#     array = picam2.capture_array()
#     return array

test_img = cv.imread("vert.jpg")
testresized = img = cv.resize(test_img, (0,0), fx = 0.2, fy = 0.2)
def process_image_circle(src):
    #redimensionne l'img, on pourra le retirer quand on réglera la résolution de la picamera
    src = cv.resize(src, (0,0), fx = 1.5, fy = 1.5)
    #HoughCircles doit recevoir en paramètre une img noire et blanche donc conversion   
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    return gray # On retourne l'image prête à être analysée

def get_circle_from_img(src):
    # les shape d'array numpy renvoient le tuple (hauteur, longueur, dimensions)
    rows = src.shape[0]
    columns = src.shape[1]
    circles = cv.HoughCircles(src, cv.HOUGH_GRADIENT, 1, rows / 8,
                            param1=100, param2=30,
                            minRadius=0, maxRadius=0) 
    #Beaucoup de paramètres influant la détection des cercles, mais pas besoin de les changer
    # Les valeurs égales à 0 permettent de dire qu'on connait pas les propriétés des cercles qu'on
    # veut analyser, donc go pas les modifier


    if circles is not None:
        circles = np.uint16(np.around(circles))
        #for i in circles[0, :]:
        i = circles[0,:][0] # S'il y a plusieurs balles ça détectera que la 1re
        center = (i[0], i[1])
        # circle center
        
        # circle outline
        radius = i[2]
        direction = 1 # 1 = droite, 0 = tout droit, -1 = gauche. Par défaut, droite
        

        adjacentLongueurPx = rows-center[1]
        opposeLongueurPx = center[0]-columns//2
        angle = math.degrees(math.atan(opposeLongueurPx / adjacentLongueurPx))

        if angle<0: #angle < 0 --> Faut tourner à gauche
            direction = -1
            angle = abs(angle)
        angleround = round(angle, 2)
        if angleround < 3:
            angleround, direction = 0,0 # S'il faut tourner moins que 3°, on annule l'angle

        # Là c'est les dessins sur l'image
        cv.circle(src, center, 1, (0, 100, 100), 3) # Le centre
        cv.circle(src, center, radius, (0, 0, 255), 3) # Le contour du cercle
        cv.line(src,(columns//2,rows),(columns//2,center[1]),(0,255,0),2) # Ligne droite depuis l'oeil du robot
        cv.line(src, (columns//2, rows),center,(255,0,0),3) # La ligne du robot vers le centre du cercle
        cv.line(src, (columns//2, center[1]),center,(0,165,255),2) # Ligne horizontale pour compléter le triangle
        
        #Texte sur l'image
        cv.putText(src, f"Angle de rotation = {str(angleround)} deg a {'gauche' if direction<0 else 'droite'}", (50,50), cv.FONT_HERSHEY_SIMPLEX ,  
                1, (255,0,0), 2, cv.LINE_AA)
    else:
        return -1 #Pas de balle détectée
    return src

def show_image(src):
    cv.imshow("NAMeC", src)
    cv.waitKey(0)

#-----------------------------------
    
def process_image_green(src):
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)

    lower_green = np.array([40, 20, 50])
    upper_green = np.array([90, 255, 255])

    # create a mask for green color
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    return mask_green


def get_green_from_img(src, mask):

    # find contours in the green mask
    contours_green, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # loop through the green contours and draw a rectangle around them
    liste_centres = []
    general_direction = 1 # -1 = gauche, 0 = droite et gauche, 1 = droite. Droite par défaut

    for cnt in contours_green:
        contour_area = cv.contourArea(cnt)
        if contour_area > 1000: # Si faux positif: augmenter, si faux négatif: réduire. Default: 1000
            x, y, w, h = cv.boundingRect(cnt)
            center_of_rectangle = (x+(w//2),y+(h//2))

            direction = 1 #1 = droite, -1 = gauche, 0 = centre 
            center_pos = center_of_rectangle[0] - src.shape[1]//2
            if center_pos<0:
                direction = -1
            elif center_pos==0:
                direction = 0
            liste_centres.append(direction)


            cv.line(src,(src.shape[1]//2, src.shape[0]),(src.shape[1]//2,0),(0,165,255),2)

            cv.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(src, 
                       "droite" if direction==1 else ("gauche" if direction==-1 else "centre"), 
                       (x, y-10), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            
            cv.circle(src, center_of_rectangle, 4, (255, 0, 0), 4)

            cv.line(src, (src.shape[1]//2, src.shape[0]), center_of_rectangle,(0,0,255),2)
    
    if 0 in liste_centres: 
        general_direction = 0
    elif -1 in liste_centres and 1 in liste_centres:
        general_direction = 0
    elif -1 in liste_centres and not 1 in liste_centres:
        general_direction = -1
    
    cv.putText(src, 
               "droite" if general_direction==1 else ("gauche" if general_direction== -1 else "droite et gauche"),
                 (50,300), cv.FONT_HERSHEY_SIMPLEX, 0.9, 0,0,255)
            
    return src

