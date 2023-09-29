import cv2
from cilindros import *
from datetime import datetime, timedelta
from date_time_event import Untiltime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread
from pre_processamento import *
from obter_caracteristicas import *

class Video(QThread):
    #Imagens
    change_pixmap = pyqtSignal(QImage)
    change_pixmap_canny = pyqtSignal(QImage)
    change_pixmap_imagem_result = pyqtSignal(QImage)
    
    #por cor
    cor_amarelo = pyqtSignal(int)
    amarelo = 0
    cor_verde = pyqtSignal(int)
    verde = 0
    cor_laranja = pyqtSignal(int)
    laranja = 0
    cor_n_reconhecida = pyqtSignal(int)
    cor_n_r = 0
    
    #Por tamanho
    tamanho_pequeno = pyqtSignal(int)
    tam_p = 0
    tamanho_medio = pyqtSignal(int)
    tam_m = 0
    tamanho_grande = pyqtSignal(int)
    tam_g = 0
    tamanho_n_reconhecido = pyqtSignal(int)
    tam_n_r = 0
    
    #Aceito ou não no processo
    num_aceitos = pyqtSignal(int)
    num_a = 0
    num_n_aceitos = pyqtSignal(int)
    num_n_a = 0
    
    #Temporizadores dos pistões
    time1 = 3.6
    time2 = 5.5
    time3 = 7.3
    
    #
    ultima_analise = 0
    limiar_tempo_analise = 0.7
    
    
    def __init__(self):
        super(Video, self).__init__()
        self.modo_sistema = 1
        self.stop = False
        self.modo_sistema = 1
        self.imagem_result =  np.zeros([90, 90, 3],  dtype=np.uint8)
        
    def atualizar_imagem_result(self, imagem):
        self.imagem_result = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        h, w, ch = self.imagem_result.shape
        #resultante
        convertToQtFormat3 = QImage(self.imagem_result, w, h, ch*w, QImage.Format_RGB888)
        self.change_pixmap_imagem_result.emit(convertToQtFormat3)
        
            
    
    def run(self):
        cap = cv2.VideoCapture(0)
       
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Erro: SEM FRAME!")
                cap.release()
                break
            
            ## COMEÇA AQUI
            imagem_perspectiva_fake = frame.copy()[39:343, 253:455]
            
            imagem_cinza = tornar_imagem_cinza(imagem_perspectiva_fake)
            
            max_val_canny = 200
            min_val_canny = 80
            imagem_canny = aplicar_filtro_canny(imagem_cinza, min_val_canny, max_val_canny)
            
            indices = np.where(imagem_canny == [255])
            tam = len(indices[0])
            limiar_dist_centro = 6
            limiar_deteccao_bordas = 0
            
            #Todo o processamento aqui
            if(tam > limiar_deteccao_bordas):
                #Dimensões da janela
                y_janela = imagem_canny.shape[0]
                x_janela = imagem_canny.shape[1]
                
                #calculando as posições extremas do objeto
                ponto_inicial = (indices[1][0], indices[0][0])
                ponto_final = (indices[1][tam-1], indices[0][tam-1])
                
                #posição do centro do objeto
                media_y_pontos = (ponto_final[1]+ponto_inicial[1])//2
                
                #a distância do centro do objeto em relação ao centro vertical da janela
                diff_def = media_y_pontos-y_janela//2
                
                
                if(diff_def < limiar_dist_centro and diff_def > 0):
                    
                    conts, hierarchy = obter_contornos(imagem_canny, modo=cv2.RETR_EXTERNAL)
                    centro, final_contours = obter_caracteristicas_imagem(imagem_perspectiva_fake, conts)
                    
                    #Cores
                    if self.modo_sistema == 1:
                        cor, imagem_r = inferir_cor(imagem_perspectiva_fake, centro)
                        #Disparo do cilindro
                        
                        if cor != None and len(imagem_r) > 0 and time.time() - self.ultima_analise >= self.limiar_tempo_analise:
                            self.ultima_analise = time.time()
                            
                            if(cor == "VERDE"):
                                date1 = datetime.now() + timedelta(0, self.time1)
                                th1 = Untiltime(disparar_cilindro_1, dateOrtime=date1)
                                th1.start()
                                self.verde = self.verde+1
                                self.cor_verde.emit(self.verde)
                               
                                
                            elif(cor == "AMARELO"):
                                date2 = datetime.now() + timedelta(0, self.time2)
                                th2 = Untiltime(disparar_cilindro_2, dateOrtime=date2)
                                th2.start()
                                self.amarelo = self.amarelo+1
                                self.cor_amarelo.emit(self.amarelo)
                               
                            elif (cor == "LARANJA"):
                                date3 = datetime.now() + timedelta(0, self.time3)
                                th3 = Untiltime(disparar_cilindro_3, dateOrtime=date3)
                                th3.start()
                                self.laranja = self.laranja+1
                                self.cor_laranja.emit(self.laranja)
                            
                            else:
                                self.cor_n_r = self.cor_n_r+1
                                self.cor_n_reconhecida.emit(self.cor_n_r)
                                image_r = np.zeros([90, 90, 3],  dtype=np.uint8)
                            
                            cv2.imshow("Result", imagem_r)
                            self.atualizar_imagem_result(imagem_r)
                            
                    # Pequeno, médio, grande  q
                    elif self.modo_sistema == 2:
                        fator_escala = 360
                        tam, p, imagem_r = inferir_tamanho(imagem_perspectiva_fake, final_contours, centro, scale=fator_escala/100)
                        
                        #Disparo do cilindro
                        if tam != None and tam != "" and time.time() - self.ultima_analise >= self.limiar_tempo_analise:
                            self.ultima_analise = time.time()
                            
                            if(tam == "PEQUENO"):
                                date1 = datetime.now() + timedelta(0, self.time1)
                                th1 = Untiltime(disparar_cilindro_1, dateOrtime=date1)
                                th1.start()
                                self.tam_p = self.tam_p+1
                                self.tamanho_pequeno.emit(self.tam_p)
                                
                            elif(tam == "MEDIO"):
                                date2 = datetime.now() + timedelta(0, self.time2)
                                th2 = Untiltime(disparar_cilindro_2, dateOrtime=date2)
                                th2.start()
                                self.tam_m = self.tam_m+1
                                self.tamanho_medio.emit(self.tam_m)
                                
                            elif (tam == "GRANDE"):
                                date3 = datetime.now() + timedelta(0, self.time3)
                                th3 = Untiltime(disparar_cilindro_3, dateOrtime=date3)
                                th3.start()
                                self.tam_g = self.tam_g+1
                                self.tamanho_grande.emit(self.tam_g)
                            else:
                                self.tam_n_r = self.tam_n_r+1
                                self.tam_n_reconhecido.emit(self.tam_n_r)
                                image_r = np.zeros([90, 90, 3],  dtype=np.uint8)
                              
                        print(f"TAMANHO: {tam} e {p}")
                        self.atualizar_imagem_result(imagem_r)
                        
                    #Fora do processo
                    elif self.modo_sistema == 3 and time.time() - self.ultima_analise >= self.limiar_tempo_analise:
                        self.ultima_analise = time.time()
                        
                        padrao_cor = "VERDE"
                        area_aceitavel = 1256.63
                    
                        cor = inferir_cor(imagem_perspectiva_fake, centro)[0]
                        
                        ret_circ = False
                        
                        if len(final_contours) > 0:
                            area = final_contours[0][1]
                            ret_circ = validar_area(area, area_aceitavel, 3.6, limiar=50)
                            
                        
                        
                        resp = cor == padrao_cor and ret_circ
                       
                        
                         
                        if not resp: 
                            date3 = datetime.now() + timedelta(0, self.time3)
                            th3 = Untiltime(disparar_cilindro_3, dateOrtime=date3)
                            th3.start()
                            self.num_n_a = self.num_n_a+1
                            self.num_n_aceitos.emit(self.num_n_a)
                            self.imagem_result =  np.zeros([40, 180, 3],  dtype=np.uint8)
                            cv2.putText( self.imagem_result, 'DEFEITUOSA', (20, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 0, 255), 1)
                            
                        else:
                            self.num_a = self.num_a+1
                            self.num_aceitos.emit(self.num_a)
                            self.imagem_result =  np.zeros([40, 120, 3],  dtype=np.uint8)
                            cv2.putText( self.imagem_result, 'ACEITA', (20, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0, 255, 0), 1)
                        
                        
                        self.atualizar_imagem_result(self.imagem_result)
                        print(f"Aceito no processo? {resp}")
                
            
                 # O pontinho branco no meio da imagem canny
                cv2.circle(imagem_canny, (x_janela//2, y_janela//2), 3, 255, -1)
            
            ## PARA A GUI
            imagem_perspectiva_fake = cv2.cvtColor(imagem_perspectiva_fake, cv2.COLOR_BGR2RGB)
            h, w, ch = imagem_perspectiva_fake.shape
            #Imagem verdadeira
            convertToQtFormat = QImage(imagem_perspectiva_fake, w, h, ch*w, QImage.Format_RGB888)
            self.change_pixmap.emit(convertToQtFormat)
            
            #Imagem canny
            convertToQtFormat2 = QImage(imagem_canny, w, h, w, QImage.Format_Grayscale8)
            self.change_pixmap_canny.emit(convertToQtFormat2)
            
            if self.stop:
                cap.release()
                break

if __name__ == "__main__":
    cv = Video()
    cv.start()

