import sys
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import pyqtgraph as pg
import os
from PySide6.QtCore import QTimer


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OptimizerClick")
        
        layout = QVBoxLayout()

        self.botao_desativar = QPushButton("Desativar Efeitos Visuais")
        self.botao_desativar.clicked.connect(self.desativar_efeitos_visuais)
        layout.addWidget(self.botao_desativar)

        self.botao_ativar = QPushButton("Ativar Efeitos Visuais")
        self.botao_ativar.clicked.connect(self.ativar_efeitos_visuais)
        layout.addWidget(self.botao_ativar)

        self.plot_cpu = pg.PlotWidget()
        layout.addWidget(self.plot_cpu)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.setFixedSize(600, 400)

        self.plot_cpu.setLabel('left', 'Uso da CPU (%)')
        self.plot_cpu.setLabel('bottom', 'Tempo (s)')
        self.plot_cpu.showGrid(x=True, y=True)

        self.uso_cpu_data = []
        self.x_data = []
        self.x_counter = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_uso_cpu)
        self.timer.start(1000)

    def desativar_efeitos_visuais(self):
        os.system("cmd /c \"REG ADD \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 2 /f\"")

    def ativar_efeitos_visuais(self):
        os.system("cmd /c \"REG ADD \"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 3 /f\"")

    def atualizar_uso_cpu(self):
        uso_cpu = psutil.cpu_percent(interval=None)

        self.uso_cpu_data.append(uso_cpu)
        self.x_data.append(self.x_counter)
        self.x_counter += 1

        if len(self.uso_cpu_data) > 100:
            self.uso_cpu_data.pop(0)
            self.x_data.pop(0)

        self.plot_cpu.plot(self.x_data, self.uso_cpu_data, clear=True)

app = QApplication(sys.argv)
jan = MainWindow()
jan.show()
sys.exit(app.exec())
