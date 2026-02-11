import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QIcon, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QSize

class IconGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('生成图标')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        self.label = QLabel('正在生成图标...')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.generateIcon()
    
    def generateIcon(self):
        pixmap = QPixmap(256, 256)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆形背景
        painter.setBrush(QBrush(QColor(76, 175, 80)))
        painter.setPen(QPen(QColor(56, 142, 60), 8))
        painter.drawEllipse(8, 8, 240, 240)
        
        # 绘制日历图标
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor(255, 255, 255), 4))
        
        # 日历主体
        painter.drawRect(60, 70, 136, 110)
        
        # 日历顶部
        painter.setBrush(QBrush(QColor(255, 152, 0)))
        painter.drawRect(60, 70, 136, 30)
        
        # 日历环
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawEllipse(75, 60, 20, 20)
        painter.drawEllipse(161, 60, 20, 20)
        
        # 绘制勾选标记
        painter.setBrush(QBrush(QColor(76, 175, 80)))
        painter.setPen(QPen(QColor(76, 175, 80), 8))
        
        path = QPainterPath()
        path.moveTo(90, 150)
        path.lineTo(115, 165)
        path.lineTo(166, 125)
        painter.drawPath(path)
        
        painter.end()
        
        # 保存图标
        icon_path = 'clock_in_icon.png'
        pixmap.save(icon_path)
        
        self.label.setText(f'图标已生成: {icon_path}')
        self.setWindowIcon(QIcon(icon_path))
        
        print(f'图标已保存到: {icon_path}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    generator = IconGenerator()
    generator.show()
    sys.exit(app.exec_())