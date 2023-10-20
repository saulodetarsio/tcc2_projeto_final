import cv2
from cilindros import *
from datetime import datetime, timedelta
from date_time_event import Untiltime
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread
from pre_processamento import *
from obter_caracteristicas import *

class Video(QThread):
    
    max_val_canny = 200
    min_val_canny = 100
    
    
    #Imagens
    change_pixmap = pyqtSignal(QImage)
    change_pixmap_canny = pyqtSignal(QImage)
    change_pixmap_imagem_result = pyqtSignal(QImage)
    
    cor_amarelo = pyqtSignal(int)
    cor_verde = pyqtSignal(int)
    cor_laranja = pyqtSignal(int)
    cor_n_reconhecida = pyqtSignal(int)
    
    tamanho_pequeno = pyqtSignal(int)
    tamanho_medio = pyqtSignal(int)
    tamanho_grande = pyqtSignal(int)
    tamanho_n_reconhecido = pyqtSignal(int)
    
    num_aceitos = pyqtSignal(int)
    num_n_aceitos = pyqtSignal(int)
    
    #por cor
    
    amarelo = 0
    verde = 0
    laranja = 0
    cor_n_r = 0
    
    #Por tamanho
    
    tam_p = 0
    tam_m = 0
    tam_g = 0
    tam_n_r = 0
    
    #Aceito ou não no processo
    num_a = 0
    num_n_a = 0
    
  
    #Auxiliar
    ultima_analise = 0
    limiar_tempo_analise = 0.7
    
    
    def __init__(self):
        super(Video, self).__init__()
        self.modo_sistema = 1
        self.stop = False
        self.modo_sistema = 1
        self.imagem_result =  np.zeros([90, 90, 3],  dtype=np.uint8)
        
        
        self.time1 = 4
        self.time2 = 5.9
        self.time3 = 7.5
        
        self.pequeno_min = 10
        self.pequeno_max = 17.99
        self.medio_min = 18
        self.medio_max = 32.99
        self.grande_min = 33
        self.grande_max = 99.99
        
        self.area_aceitavel = 1256.63
        
        self.cor_padrao = "VERDE"
        
        self.forma_padrao = "FACE CIRCULAR"
        
        self.fator_escala = 360
        
    def atualizar_imagem_result(self, imagem):
        self.imagem_result = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        h, w, ch = self.imagem_result.shape
        #resultante
        convertToQtFormat3 = QImage(self.imagem_result, w, h, ch*w, QImage.Format_RGB888)
        self.change_pixmap_imagem_result.emit(convertToQtFormat3)
        
            
    def agendar_cilindro1(self):
        date1 = datetime.now() + timedelta(0, self.time1)
        th1 = Untiltime(disparar_cilindro_1, dateOrtime=date1)
        th1.start()
    
    def agendar_cilindro2(self):
        date2 = datetime.now() + timedelta(0, self.time2)
        th2 = Untiltime(disparar_cilindro_2, dateOrtime=date2)
        th2.start()
    
    def agendar_cilindro3(self):
        date3 = datetime.now() + timedelta(0, self.time3)
        th3 = Untiltime(disparar_cilindro_3, dateOrtime=date3)
        th3.start()
        
    def run(self):
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            """
            print(f"Tempos: {self.time1}, {self.time2}, {self.time3}")
            print(f"Pequeno: {self.pequeno_min} a {self.pequeno_max}")
            print(f"Médio: {self.medio_min} a {self.medio_max}")
            print(f"Grande: {self.grande_min} a {self.grande_max}")
            print(f"Área aceita: {self.area_aceitavel}")
            print(f"Cor padrão: {self.cor_padrao}")
            print(f"Forma padrão: {self.forma_padrao}")
            print(f"Fator de escala: {self.fator_escala}")
            print("-------------------------------")
            """
            ret, frame = cap.read()
            
            if not ret:
                print("Erro: SEM FRAME!")
                cap.release()
                break
            
            ## COMEÇA AQUI
            imagem_perspectiva_fake = frame.copy()[39:343, 253:455]
            
            imagem_cinza = tornar_imagem_cinza(imagem_perspectiva_fake)
            
            imagem_canny = aplicar_filtro_canny(imagem_cinza, self.min_val_canny, self.max_val_canny)
            
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
                    centro, final_contours, tipo_peca = obter_caracteristicas_imagem(imagem_perspectiva_fake, conts)
                    
                    #Cores
                    if self.modo_sistema == 1:
                        cor, imagem_r = inferir_cor(imagem_perspectiva_fake, centro)
                        #Disparo do cilindro
                        
                        if cor != None and len(imagem_r) > 0 and time.time() - self.ultima_analise >= self.limiar_tempo_analise:
                            self.ultima_analise = time.time()
                            
                            if(cor == "VERDE"):
                                self.agendar_cilindro1()
                                self.verde = self.verde+1
                                self.cor_verde.emit(self.verde)
                            elif(cor == "AMARELO"):
                                self.agendar_cilindro2()
                                self.amarelo = self.amarelo+1
                                self.cor_amarelo.emit(self.amarelo)
                            elif (cor == "LARANJA"):
                                self.agendar_cilindro3()
                                self.laranja = self.laranja+1
                                self.cor_laranja.emit(self.laranja)
                            
                            else:
                                self.cor_n_r = self.cor_n_r+1
                                self.cor_n_reconhecida.emit(self.cor_n_r)
                                image_r = np.zeros([90, 90, 3],  dtype=np.uint8)
                            
                            cv2.imshow("Result", imagem_r)
                            self.atualizar_imagem_result(imagem_r)
                            
                    # Pequeno, médio, grande
                    elif self.modo_sistema == 2:
                        
                        intervalos = [[self.pequeno_min, self.pequeno_max],
                                      [self.medio_min, self.medio_max],
                                      [self.grande_min, self.grande_max]]
                        
                        tam, p, imagem_r = inferir_tamanho(imagem_perspectiva_fake, final_contours, centro, self.fator_escala/100, intervalos)
                        
                        #Disparo do cilindro
                        if tam != None and tam != "" and time.time() - self.ultima_analise >= self.limiar_tempo_analise:
                            self.ultima_analise = time.time()
                            
                            if(tam == "PEQUENO"):
                                self.agendar_cilindro1()
                                self.tam_p = self.tam_p+1
                                self.tamanho_pequeno.emit(self.tam_p)
                                
                            elif(tam == "MEDIO"):
                                self.agendar_cilindro2()
                                self.tam_m = self.tam_m+1
                                self.tamanho_medio.emit(self.tam_m)
                                
                            elif (tam == "GRANDE"):
                                self.agendar_cilindro3()
                                self.tam_g = self.tam_g+1
                                self.tamanho_grande.emit(self.tam_g)
                            else:
                                self.tam_n_r = self.tam_n_r+1
                                self.tam_n_reconhecido.emit(self.tam_n_r)
                                image_r = np.zeros([90, 90, 3],  dtype=np.uint8)
                              
                        print(f"TAMANHO: {tam} e {p}")
                        if tam != None and p != None:
                            self.atualizar_imagem_result(imagem_r)
                        
                    #Fora do processo
                    elif self.modo_sistema == 3 and time.time() - self.ultima_analise >= self.limiar_tempo_analise:
                        self.ultima_analise = time.time()
                        
                        cor = inferir_cor(imagem_perspectiva_fake, centro)[0]
                        
                        ret_area = False
                        
                        if len(final_contours) > 0:
                            area = final_contours[0][1]
                            ret_area = validar_area(area, self.area_aceitavel, self.fator_escala/100, limiar=50)
                            
                        resp = cor == self.cor_padrao and ret_area and tipo == self.forma_padrao
                       
                        
                        if not resp: 
                            self.agendar_cilindro3()
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

