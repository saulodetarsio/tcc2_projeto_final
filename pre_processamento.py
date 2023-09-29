import numpy as np
import cv2

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas: ({x},{y})")
        
def tornar_imagem_cinza(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return imgGray

def retornar_imagem_blur(imgGray, kernel_gaussian_blur):
    imgBlur = cv2.GaussianBlur(imgGray, (kernel_gaussian_blur, kernel_gaussian_blur), 0)
    return imgBlur

def aplicar_filtro_canny(imgBlur, minVal, maxVal):
     imgCanny = cv2.Canny(imgBlur, minVal, maxVal)
     return imgCanny
    
def dilatar_imagem(img, valor_kernel, iteracoes):
    kernel = np.ones((valor_kernel, valor_kernel))
    imgDil = cv2.dilate(img, kernel, iterations=iteracoes)
    return imgDil

def aplicar_erosao_imagem(img, valor_kernel, iteracoes):
    kernel = np.ones((valor_kernel, valor_kernel))
    imgErode = cv2.erode(img, kernel, iterations=iteracoes)
    return imgErode
    
def binarizar_imagem(imagem, th):
    ret, imagem_b = cv2.threshold(imagem, th, 255, cv2.THRESH_BINARY)
    return imagem_b
    
def evidenciar_contornos(img):
   # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   # imgBlur = cv2.GaussianBlur(imgGray, (kernel_gaussian_blur, kernel_gaussian_blur), 1)
   
    
    
    imgDil = cv2.dilate(imgCanny, kernel, iterations=iter_dil)
    imgThre = cv2.erode(imgDil, kernel, iterations=iter_ero)
    
    return imgThre