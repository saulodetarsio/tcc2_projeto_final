import numpy as np
import cv2
import time

def findDistance(pts1, pts2):
    return ((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5

def validar_area(area, area_aceitavel, fator, limiar=50):
    
    medido = area/(fator**2)
    print(f"Área medida: {medido}")
    flag = False
    
    if(area_aceitavel + limiar >= medido >= area_aceitavel - limiar ):
        flag = True
    
    return flag
        
      
def reorder(myPoints):
    myPointsNew = np.zeros_like(myPoints)
    
    myPoints = myPoints.reshape((4, 2))
    
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    
    return myPointsNew

def retangulo(imgConts2, obj, scale, centro, intervalos):
    nPoints = reorder(obj[3])
    
    nw = round(findDistance(nPoints[0][0]//scale, nPoints[1][0]//scale), 1)
    nh = round(findDistance(nPoints[0][0]//scale, nPoints[2][0]//scale), 1)
    
    #arrows
    cv2.arrowedLine(imgConts2, (nPoints[0][0][0], nPoints[0][0][1]),
                    (nPoints[1][0][0], nPoints[1][0][1]),
                    (255, 0, 255), 2, 8, 0, 0.08)
    
    cv2.arrowedLine(imgConts2, (nPoints[0][0][0], nPoints[0][0][1]),
                    (nPoints[2][0][0], nPoints[2][0][1]),
                    (255, 0, 255), 2, 8, 0, 0.08)
    
    #Bounding box
    x, y, w, h = obj[4]
    
   
    cv2.putText(imgConts2, f'{int(nw)}mm',
                (x+w//2, y-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                (0, 0, 255), 1)
    
    cv2.putText(imgConts2, f'{int(nh)}mm',
                (x+10, -10+y+h//2), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.8,
                (0, 0, 255), 1)
    
    cv2.circle(imgConts2, (centro[0],centro[1]), 2, (255, 255, 255), -1)
  
    pivo = np.max([nw, nh])
    
    tamanho_p = ""
    if pivo >= intervalo[0][0] and pivo < intervalo[0][1]:
        tamanho_p =  "PEQUENO"
    elif pivo >= intervalo[1][0] and pivo < intervalo[1][1]:
        tamanho_p = "MEDIO"
    elif pivo >= intervalo[2][0] and pivo <= intervalo[2][1]:
        tamanho_p =  "GRANDE"
    
    return tamanho_p, pivo, imgConts2


def circulo(imgConts2, obj, scale, centro, intervalos):
    p1x = obj[3][0][0][0]
    p1y = obj[3][0][0][1]
    
    
    cv2.circle(imgConts2, (centro[0],centro[1]), 2, (255, 255, 255), -1)
    
    cv2.line(imgConts2, (centro[0],centro[1]), (p1x, p1y),
             (0, 0, 255), 2)
    
    soma = 0
    c = np.array(centro)
    for i in obj[3][0]:
        soma = soma+findDistance(i, c)
    
    media = soma/len(obj[3][0])
    raio = media / scale
    
    cv2.circle(imgConts2, (centro[0],centro[1]), int(media), (0, 0, 255), 2)
   
    cv2.putText(imgConts2, f'r={round(raio, 2)}mm',
                (centro[0] - 20, centro[1]+10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5,
                (0, 0, 255), 1)
    
    d = raio * 2
    palavra_p = ""
    if d >= intervalo[0][0] and d <= intervalo[0][1]:
        palavra_p =  "PEQUENO"
    elif d >= intervalo[1][0] and d <= intervalo[1][1]:
        palavra_p = "MEDIO"
    elif d >= intervalo[2][0] and d <= intervalo[2][1]:
        palavra_p = "GRANDE"
    
    return palavra_p, d, imgConts2
    

def inferir_cor(imagem, centro):
    vermelho1 = (159, 50, 70), (180, 255, 255)
    vermelho2 = (0, 50, 70), (9, 255, 255)
    
    verde = (36, 50, 70), (89, 255, 255)
    azul = (90, 50, 70), (128, 255, 255) 
    
    amarelo = (25, 50, 70), (35, 255, 255)
    roxo = (129, 50, 70), (158, 255, 255)
    
    laranja = (10, 50, 70), (24, 255, 255)
    
    cores = [vermelho1, vermelho2,  verde, azul, amarelo, laranja]
    cores_label = ["VERMELHO", "VERMELHO", "VERDE", "AZUL", "AMARELO", "LARANJA"]
    
    limiar = 15
    cores_img = imagem[centro[1]-limiar:centro[1]+limiar, centro[0]-limiar:centro[0]+limiar]
    
    cores_img_copy = []
    
    if(len(cores_img) != 0):
        cores_img_copy = cv2.resize(cores_img, (0,0), None, 5, 5)
    
    else:
        return "OBJETO NÃO RECONHECIDO", cores_img_copy
    
    img_hsv = cv2.cvtColor(cores_img, cv2.COLOR_BGR2HSV)
    
    
    b = int(np.mean(cores_img[:, :, 0]))
    g = int(np.mean(cores_img[:, :, 1]))
    r = int(np.mean(cores_img[:, :, 2]))
    
    angulo = int(np.mean(img_hsv[:, :, 0]))
    
    cores_img_dim = cv2.resize(cores_img, (0,0), None, 5, 5)
    img_hsv_dim = cv2.resize(img_hsv, (0,0), None, 5, 5)
    
    i = 0
    for l, u in cores:
        if(angulo >= l[0] and angulo <= u[0]):
           break
        i = i+1

    return cores_label[i], cores_img_copy
    
def inferir_tamanho(imagem, final_contours, centro, scale, intervalos):   
    result = ""
    for obj in final_contours:
        if obj[0] == 4:
            result = retangulo(imagem, obj, scale, centro, intervalos)
        elif obj[0] == 5:
            print("Prepara o pentágono")
        elif obj[0] == 6:
            print("Prepara o hexágono")
        elif obj[0] > 6:
            result = circulo(imagem, obj, scale, centro, intervalos)
    
    if(len(result) == 0):
        return None, None, None
    
    return result
    
def obter_caracteristicas_imagem(imagem, contornos):

    final_contours = []
    centro_figura = (-1, -1)
    j = 0
    imagem_c = imagem.copy()
    
    # list for storing names of shapes
    i = 0
    for cont in contornos:
        area = cv2.contourArea(cont)
        if area > 500:
            # cv2.approxPloyDP() function to approximate the shape
            peri = cv2.arcLength(cont, True)
            approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            
            # finding center point of shape
            M = cv2.moments(cont)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                centro_figura = (x, y)
            
            final_contours.append([len(approx), area, peri, approx, bbox, cont])
            
            a = len(approx)
            if a  == 3:
              j = ""
            elif a == 4:
              j = "FACE QUADRADA"
            elif a == 5:
              j = ""
            elif a == 6:
              j = 3
            else:
              j = "FACE CIRCULAR"

    return centro_figura, final_contours, j
    
def obter_contornos(imagem, modo): 
    contours, hierarchy = cv2.findContours(imagem, modo, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy
    