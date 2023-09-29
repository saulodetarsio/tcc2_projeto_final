from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


def clearLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())


def renderizar_elementos_cor(self, layout):
    #Elaborar infos de cor
    linha1 = QHBoxLayout()
    linha2 = QHBoxLayout()
    linha3 = QHBoxLayout()
    linha4 = QHBoxLayout()
    
    #1
    label1 = QLabel("VERDE")
    label1.setStyleSheet("background: green; color: white");
    label1.setFont(QFont('Arial font', 11));
    label1.setAlignment(Qt.AlignCenter)
    
    lcd1 = QLCDNumber()
    lcd1.setDigitCount(3)
    lcd1.display(self.vs.verde)
    
    linha1.addWidget(label1);
    linha1.addWidget(lcd1);
    
    #2
    label2 = QLabel("AMARELO")
    label2.setStyleSheet("background: rgb(255, 192, 65); color: white");
    label2.setFont(QFont('Arial font', 11));
    label2.setAlignment(Qt.AlignCenter)
    
    lcd2 = QLCDNumber()
    lcd2.setDigitCount(3)
    lcd2.display(self.vs.amarelo)
    
    linha2.addWidget(label2);
    linha2.addWidget(lcd2);
    
    #3
    label3 = QLabel("LARANJA")
    label3.setStyleSheet("background: rgb(255, 85, 0); color: white");
    label3.setFont(QFont('Arial font', 11));
    label3.setAlignment(Qt.AlignCenter)
    
    lcd3 = QLCDNumber()
    lcd3.setDigitCount(3)
    lcd3.display(self.vs.laranja)
    
    linha3.addWidget(label3);
    linha3.addWidget(lcd3);
    
    #4
    label4 = QLabel("INDEFINIDO")
    label4.setStyleSheet("background: red; color: white");
    label4.setFont(QFont('Arial font', 11));
    label4.setAlignment(Qt.AlignCenter)
    
    
    lcd4 = QLCDNumber()
    lcd4.setDigitCount(3)
    lcd4.display(self.vs.tam_n_r)
    
    linha4.addWidget(label4);
    linha4.addWidget(lcd4);
    
    layout.addLayout(linha1)
    layout.addLayout(linha2)
    layout.addLayout(linha3)
    layout.addLayout(linha4)

def renderizar_elementos_tamanho(self, layout):
    #Elaborar infos de cor
    linha1 = QHBoxLayout()
    linha2 = QHBoxLayout()
    linha3 = QHBoxLayout()
    linha4 = QHBoxLayout()
    
    #1
    label1 = QLabel("PEQUENO")
    label1.setStyleSheet("background: green; color: white");
    label1.setFont(QFont('Arial font', 11));
    label1.setAlignment(Qt.AlignCenter)
    
    lcd1 = QLCDNumber()
    lcd1.setDigitCount(3)
    lcd1.display(self.vs.tam_p)
    
    
    linha1.addWidget(label1);
    linha1.addWidget(lcd1);
    
    #2
    label2 = QLabel("MÉDIO")
    label2.setStyleSheet("background: rgb(255, 192, 65); color: white");
    label2.setFont(QFont('Arial font', 11));
    label2.setAlignment(Qt.AlignCenter)
    
    lcd2 = QLCDNumber()
    lcd2.setDigitCount(3)
    lcd2.display(self.vs.tam_m)

    linha2.addWidget(label2);
    linha2.addWidget(lcd2);
    
    #3
    label3 = QLabel("GRANDE")
    label3.setStyleSheet("background: rgb(255, 85, 0); color: white");
    label3.setFont(QFont('Arial font', 11));
    label3.setAlignment(Qt.AlignCenter)
    
    lcd3 = QLCDNumber()
    lcd3.setDigitCount(3)
    lcd3.display(self.vs.tam_g)
    
    linha3.addWidget(label3);
    linha3.addWidget(lcd3);
    
    #4
    label4 = QLabel("INDEFINIDO")
    label4.setStyleSheet("background: red; color: white");
    label4.setFont(QFont('Arial font', 11));
    label4.setAlignment(Qt.AlignCenter)
    
    lcd4 = QLCDNumber()
    lcd4.setDigitCount(3)
    lcd4.display(self.vs.tam_n_r)
    
    linha4.addWidget(label4);
    linha4.addWidget(lcd4);
    
    
    layout.addLayout(linha1)
    layout.addLayout(linha2)
    layout.addLayout(linha3)
    layout.addLayout(linha4)

def renderizar_elementos_processo_qualidade(self, layout):
    #Elaborar infos de cor
    linha1 = QHBoxLayout()
    linha4 = QHBoxLayout()
    
    #1
    label1 = QLabel("ACEITOS")
    label1.setStyleSheet("background: green; color: white");
    label1.setFont(QFont('Arial font', 11));
    label1.setAlignment(Qt.AlignCenter)
    
    lcd1 = QLCDNumber()
    lcd1.setDigitCount(3)
    lcd1.display(self.vs.num_a)
    
    linha1.addWidget(label1);
    linha1.addWidget(lcd1);
    
    #4
    label4 = QLabel("NÃO ACEITOS")
    label4.setStyleSheet("background: red; color: white");
    label4.setFont(QFont('Arial font', 11));
    label4.setAlignment(Qt.AlignCenter)
    
    lcd4 = QLCDNumber()
    lcd4.setDigitCount(3)
    lcd1.display(self.vs.num_n_a)
     
    linha4.addWidget(label4);
    linha4.addWidget(lcd4);
    
    
    layout.addLayout(linha1)
    layout.addLayout(linha4)

