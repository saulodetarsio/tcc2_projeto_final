from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from process import Video
from criar_elementos import *


class Janela(QMainWindow):
    def __init__(self):
        super(Janela,self).__init__()
        
        loadUi("janela.ui", self)
        
        #vídeo
        self.vs=Video()
        
        #Imagens
        self.vs.change_pixmap.connect(self.frame_update)
        self.vs.change_pixmap_canny.connect(self.frame_teste)
        self.vs.change_pixmap_imagem_result.connect(self.frame_teste_img_result)
        
        #COR
        self.vs.cor_verde.connect(self.atualizar_verde)
        self.vs.cor_amarelo.connect(self.atualizar_amarelo)
        self.vs.cor_laranja.connect(self.atualizar_laranja)
        self.vs.cor_n_reconhecida.connect(self.atualizar_cor_n_reconhecida)
        
        #TAMANHO
        self.vs.tamanho_pequeno.connect(self.atualizar_pequeno)
        self.vs.tamanho_medio.connect(self.atualizar_medio)
        self.vs.tamanho_grande.connect(self.atualizar_grande)
        self.vs.tamanho_n_reconhecido.connect(self.atualizar_tamanho_n_reconhecido)
        
        #PROCESSO
        self.vs.num_aceitos.connect(self.atualizar_num_aceitos)
        self.vs.num_n_aceitos.connect(self.atualizar_num_n_aceitos)
        
        #Modo inicial
        self.label_modo.setText('MODO 1 (COR)')
        self.label_titulo_img_result.setText("COR DO CENTRO DO OBJETO")
        renderizar_elementos_cor(self, self.infos_modo)
        
   
    def radio1_clicked(self):        
        self.label_modo.setText('MODO 1 (COR)')
        self.label_titulo_img_result.setText("COR DO CENTRO DO OBJETO")
        clearLayout(self.infos_modo)
        renderizar_elementos_cor(self, self.infos_modo)
     
    def radio2_clicked(self):
        self.label_modo.setText('MODO 2 (TAMANHO)')
        self.label_titulo_img_result.setText("DIMENSÕES DA IMAGEM")
        clearLayout(self.infos_modo)
        renderizar_elementos_tamanho(self, self.infos_modo)
    
    
    def radio3_clicked(self):
        self.label_modo.setText('MODO 3 (PROCESSO)')
        self.label_titulo_img_result.setText("CONTROLE DE QUALIDADE")
        clearLayout(self.infos_modo)
        renderizar_elementos_processo_qualidade(self, self.infos_modo)
            

    @pyqtSlot()
    def on_radioButton_cor_clicked(self):
        self.vs.modo_sistema = 1
        self.radio1_clicked()
        
    @pyqtSlot()
    def on_radioButton_tamanho_clicked(self):
        self.vs.modo_sistema = 2
        self.radio2_clicked()
    
    def on_radioButton_controleQualidade_clicked(self):
        self.vs.modo_sistema = 3
        self.radio3_clicked()
    
    #Para iniciar e parar a operação
    @pyqtSlot()
    def on_pushButton_iniciar_clicked(self):
        if not self.vs.isRunning():
            self.vs.stop=False
            self.vs.start()
            
    @pyqtSlot()
    def on_pushButton_parar_clicked(self):
        self.vs.stop=True
    
    #Para as imagens
    @pyqtSlot(QImage)
    def frame_update(self,image):
        self.label_img_origin.setPixmap(QPixmap.fromImage(image))
    
    @pyqtSlot(QImage)
    def frame_teste(self,image):
        self.label_img_canny.setPixmap(QPixmap.fromImage(image))
    
    @pyqtSlot(QImage)
    def frame_teste_img_result(self,image):
        self.label_img_mode.setPixmap(QPixmap.fromImage(image))
    
    
    #Métodos para cores
    @pyqtSlot(int)
    def atualizar_verde(self, valor):
        self.infos_modo.itemAt(0).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_amarelo(self, valor):
        self.infos_modo.itemAt(1).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_laranja(self, valor):
        self.infos_modo.itemAt(2).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_cor_n_reconhecida(self, valor):
        self.infos_modo.itemAt(3).itemAt(1).widget().display(valor)
    
    #Métodos para tamanhos
    @pyqtSlot(int)
    def atualizar_pequeno(self, valor):
        self.infos_modo.itemAt(0).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_medio(self, valor):
        self.infos_modo.itemAt(1).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_grande(self, valor):
        self.infos_modo.itemAt(2).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_tamanho_n_reconhecido(self, valor):
        self.infos_modo.itemAt(3).itemAt(1).widget().display(valor)
    
    #Métodos para o processo
    @pyqtSlot(int)
    def atualizar_num_aceitos(self, valor):
        self.infos_modo.itemAt(0).itemAt(1).widget().display(valor)
    
    @pyqtSlot(int)
    def atualizar_num_n_aceitos(self, valor):
        self.infos_modo.itemAt(1).itemAt(1).widget().display(valor)
        
       
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    my_janela=Janela()
    my_janela.show()
    app.exec_()