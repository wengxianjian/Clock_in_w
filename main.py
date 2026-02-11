import sys
import json
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QCheckBox, QPushButton, QCalendarWidget, 
    QLabel, QLineEdit, QMessageBox, QFontDialog, QSplitter, QFrame, QInputDialog, QTextEdit, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QTextCharFormat

class ClockInApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()
        self.updateDayCount()
        self.updateCalendar()
    
    def initUI(self):
        self.setWindowTitle('每日打卡')
        self.setGeometry(100, 100, 900, 700)
        
        # 设置图标
        if os.path.exists('clock_in_icon.png'):
            self.setWindowIcon(QIcon('clock_in_icon.png'))
        
        # 设置护眼颜色方案
        self.setEyeFriendlyColors()
        
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 顶部设置区域
        settings_frame = QFrame()
        settings_frame.setStyleSheet('''
            QFrame {
                background-color: #F0F4F8;
                border-radius: 8px;
                padding: 5px;
            }
        ''')
        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)
        
        # 初始日期设置
        self.start_date_label = QLabel('初始日期:')
        self.start_date_label.setStyleSheet('color: #2C3E50; font-weight: bold;')
        self.start_date_edit = QLineEdit()
        self.start_date_edit.setText(datetime.now().strftime('%Y-%m-%d'))
        self.start_date_edit.setStyleSheet('''
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                padding: 5px;
                color: #2C3E50;
            }
        ''')
        self.save_start_date_btn = QPushButton('保存')
        self.save_start_date_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        ''')
        
        # 字体设置
        self.font_label = QLabel('字体大小:')
        self.font_label.setStyleSheet('color: #2C3E50; font-weight: bold;')
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems([str(i) for i in range(8, 37)])
        self.font_size_combo.setCurrentText('16')
        self.font_size_combo.setStyleSheet('''
            QComboBox {
                background-color: #FFFFFF;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                padding: 5px;
                color: #2C3E50;
                font-size: 14px;
                min-width: 80px;
            }
            QComboBox:hover {
                border: 2px solid #3498DB;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #BDC3C7;
                border-radius: 3px;
                width: 10px;
                height: 10px;
                background-color: #BDC3C7;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                selection-background-color: #3498DB;
                selection-color: white;
                padding: 5px;
            }
        ''')
        self.font_size_combo.currentTextChanged.connect(self.changeFont)
        
        settings_layout.addWidget(self.start_date_label)
        settings_layout.addWidget(self.start_date_edit)
        settings_layout.addWidget(self.save_start_date_btn)
        settings_layout.addStretch()
        settings_layout.addWidget(self.font_label)
        settings_layout.addWidget(self.font_size_combo)
        
        settings_frame.setLayout(settings_layout)
        main_layout.addWidget(settings_frame)
        
        # 标题和打卡天数 - 紧凑布局
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        title_label = QLabel('每日计划打卡')
        title_font = QFont('Microsoft YaHei', 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet('color: #2C3E50; padding: 5px;')
        
        self.day_count_label = QLabel('今天是打卡的第 0 天')
        day_count_font = QFont('Microsoft YaHei', 12)
        self.day_count_label.setFont(day_count_font)
        self.day_count_label.setStyleSheet('color: #27AE60; font-weight: bold; padding: 5px;')
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.day_count_label)
        
        main_layout.addLayout(header_layout)
        
        # 今日任务区域 - 独占一行
        task_frame = QFrame()
        task_frame.setStyleSheet('''
            QFrame {
                background-color: #E8F6F3;
                border-radius: 8px;
                padding: 10px;
            }
        ''')
        task_layout = QVBoxLayout()
        task_layout.setSpacing(5)
        task_layout.setContentsMargins(5, 5, 5, 5)
        
        task_title = QLabel('今日任务')
        task_title.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        task_title.setStyleSheet('color: #16A085; padding: 2px;')
        task_layout.addWidget(task_title)
        
        self.task_list = QListWidget()
        self.task_list.setMinimumHeight(300)
        self.task_list.setStyleSheet('''
            QListWidget {
                background-color: #FFFFFF;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 4px;
                font-size: 14px;
            }
            QListWidget::item:hover {
                background-color: #D5F4E6;
            }
        ''')
        task_layout.addWidget(self.task_list)
        
        # 任务管理按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_task_btn = QPushButton('添加任务')
        self.add_task_btn.setStyleSheet('''
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        ''')
        self.delete_task_btn = QPushButton('删除任务')
        self.delete_task_btn.setStyleSheet('''
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        ''')
        self.edit_task_btn = QPushButton('修改任务')
        self.edit_task_btn.setStyleSheet('''
            QPushButton {
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D68910;
            }
        ''')
        
        button_layout.addWidget(self.add_task_btn)
        button_layout.addWidget(self.delete_task_btn)
        button_layout.addWidget(self.edit_task_btn)
        task_layout.addLayout(button_layout)
        
        task_frame.setLayout(task_layout)
        main_layout.addWidget(task_frame)
        
        # 打卡日历区域 - 独占一行
        calendar_frame = QFrame()
        calendar_frame.setStyleSheet('''
            QFrame {
                background-color: #FEF9E7;
                border-radius: 8px;
                padding: 10px;
            }
        ''')
        calendar_layout = QVBoxLayout()
        calendar_layout.setSpacing(2)
        calendar_layout.setContentsMargins(3, 3, 3, 3)
        
        calendar_title = QLabel('打卡日历')
        calendar_title.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        calendar_title.setStyleSheet('color: #F39C12; padding: 0px; margin: 0px;')
        calendar_layout.addWidget(calendar_title)
        
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumDate(QDate.currentDate().addMonths(-12))
        self.calendar.setMaximumDate(QDate.currentDate().addMonths(12))
        self.calendar.setMinimumHeight(250)
        self.calendar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.calendar.setStyleSheet('''
            QCalendarWidget {
                background-color: #FFFFFF;
                border: 2px solid #F39C12;
                border-radius: 5px;
            }
            QCalendarWidget QTableView {
                background-color: #FFFFFF;
                selection-background-color: #F39C12;
                selection-color: white;
                alternate-background-color: #FEF9E7;
                font-size: 12px;
            }
            QCalendarWidget QToolButton {
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #E67E22;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background-color: #E67E22;
            }
            QCalendarWidget QSpinBox {
                background-color: #FFFFFF;
                border: 1px solid #BDC3C7;
                border-radius: 3px;
                padding: 2px;
                color: #2C3E50;
                font-size: 12px;
            }
        ''')
        calendar_layout.addWidget(self.calendar)
        
        calendar_frame.setLayout(calendar_layout)
        main_layout.addWidget(calendar_frame)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # 信号连接
        self.add_task_btn.clicked.connect(self.addTask)
        self.delete_task_btn.clicked.connect(self.deleteTask)
        self.edit_task_btn.clicked.connect(self.editTask)
        self.save_start_date_btn.clicked.connect(self.saveStartDate)
        self.calendar.selectionChanged.connect(self.onDateSelected)
    
    def setEyeFriendlyColors(self):
        """设置护眼颜色方案"""
        palette = QPalette()
        
        # 设置窗口背景色 - 护眼浅绿色
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        
        # 设置控件背景色
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 248, 255))
        
        # 设置文字颜色
        palette.setColor(QPalette.Text, QColor(44, 62, 80))
        palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
        
        # 设置按钮颜色
        palette.setColor(QPalette.Button, QColor(52, 152, 219))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        
        # 设置高亮颜色
        palette.setColor(QPalette.Highlight, QColor(52, 152, 219))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        QApplication.setPalette(palette)
    
    def loadData(self):
        """加载数据"""
        self.data_file = 'clock_in_data.json'
        
        if not os.path.exists(self.data_file):
            # 创建默认数据
            self.data = {
                'start_date': datetime.now().strftime('%Y-%m-%d'),
                'tasks': [
                    {'name': '醒了立刻起床', 'days': 0, 'completed': []},
                    {'name': '锻炼身体一分钟', 'days': 0, 'completed': []},
                    {'name': '阅读一页书', 'days': 0, 'completed': []}
                ]
            }
            self.saveData()
        else:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        
        # 更新初始日期输入框
        self.start_date_edit.setText(self.data['start_date'])
        
        # 加载任务列表
        self.loadTasks()
    
    def saveData(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def loadTasks(self):
        """加载任务到列表"""
        self.task_list.clear()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 获取当前字体大小
        try:
            font_size = int(self.font_size_combo.currentText())
        except:
            font_size = 14
        
        for task in self.data['tasks']:
            item = QListWidgetItem()
            
            # 创建任务项的布局
            task_widget = QWidget()
            task_layout = QHBoxLayout()
            task_layout.setContentsMargins(5, 5, 5, 5)
            task_layout.setSpacing(10)
            
            # 复选框
            checkbox = QCheckBox()
            
            # 计算任务开始的第几天
            start_date = datetime.strptime(self.data['start_date'], '%Y-%m-%d')
            today_date = datetime.strptime(today, '%Y-%m-%d')
            days_passed = (today_date - start_date).days + 1
            
            task_text = f"{task['name']} {days_passed}天"
            checkbox.setText(task_text)
            checkbox.setStyleSheet(f'''
                QCheckBox {{
                    color: #2C3E50;
                    font-size: {font_size}px;
                    padding: 5px;
                    spacing: 5px;
                }}
                QCheckBox::indicator {{
                    width: {font_size + 6}px;
                    height: {font_size + 6}px;
                    border: 2px solid #BDC3C7;
                    border-radius: 3px;
                    background-color: #FFFFFF;
                }}
                QCheckBox::indicator:checked {{
                    background-color: #27AE60;
                    border-color: #27AE60;
                    image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld0JveD0iMCAwIDE4IDE4Ij48cGF0aCBkPSJNMyA5bDMgM2w3LTciIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPjwvc3ZnPg==);
                }}
                QCheckBox::indicator:hover {{
                    border-color: #27AE60;
                }}
            ''')
            
            # 检查今天是否已完成
            if today in task['completed']:
                checkbox.setChecked(True)
            
            # 连接信号
            checkbox.stateChanged.connect(lambda state, t=task, d=today: self.toggleTaskCompletion(t, d, state))
            
            task_layout.addWidget(checkbox)
            
            # 完成情况编辑框
            notes_edit = QTextEdit()
            notes_edit.setMaximumHeight(80)
            notes_edit.setMinimumWidth(250)
            notes_edit.setPlaceholderText('完成情况...')
            
            # 获取今天的完成情况
            if 'notes' not in task:
                task['notes'] = {}
            if today in task['notes']:
                notes_edit.setText(task['notes'][today])
            
            # 设置编辑框样式
            notes_edit.setStyleSheet(f'''
                QTextEdit {{
                    background-color: #FFFFFF;
                    border: 2px solid #BDC3C7;
                    border-radius: 5px;
                    padding: 5px;
                    color: #2C3E50;
                    font-size: {max(10, font_size - 2)}px;
                }}
                QTextEdit:focus {{
                    border: 2px solid #3498DB;
                }}
            ''')
            
            # 连接信号，保存完成情况
            notes_edit.textChanged.connect(lambda: self.saveTaskNotes(task, today, notes_edit))
            
            task_layout.addWidget(notes_edit)
            
            task_widget.setLayout(task_layout)
            
            # 设置item的大小
            item.setSizeHint(task_widget.sizeHint())
            
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, task_widget)
    
    def saveTaskNotes(self, task, date, notes_edit):
        """保存任务完成情况"""
        if 'notes' not in task:
            task['notes'] = {}
        task['notes'][date] = notes_edit.toPlainText()
        self.saveData()
    
    def toggleTaskCompletion(self, task, date, state):
        """切换任务完成状态"""
        if state == Qt.Checked:
            if date not in task['completed']:
                task['completed'].append(date)
        else:
            if date in task['completed']:
                task['completed'].remove(date)
        
        self.saveData()
        self.updateCalendar()
    
    def addTask(self):
        """添加任务"""
        dialog = QInputDialog(self)
        dialog.setWindowTitle('添加任务')
        dialog.setLabelText('请输入任务名称:')
        dialog.setTextValue('')
        dialog.setStyleSheet('''
            QInputDialog {
                background-color: #F0F4F8;
            }
            QInputDialog QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
            }
            QInputDialog QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #3498DB;
                border-radius: 5px;
                padding: 8px;
                color: #2C3E50;
                font-size: 14px;
                min-height: 30px;
            }
            QInputDialog QLineEdit:focus {
                border: 2px solid #2980B9;
            }
            QDialogButtonBox QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-weight: bold;
                font-size: 14px;
                min-width: 80px;
                min-height: 35px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #2980B9;
            }
            QDialogButtonBox QPushButton:pressed {
                background-color: #1A5276;
            }
        ''')
        if dialog.exec_() == QInputDialog.Accepted:
            task_name = dialog.textValue()
            if task_name.strip():
                new_task = {
                    'name': task_name.strip(),
                    'days': 0,
                    'completed': [],
                    'notes': {}
                }
                self.data['tasks'].append(new_task)
                self.saveData()
                self.loadTasks()
    
    def deleteTask(self):
        """删除任务"""
        current_item = self.task_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setWindowTitle('警告')
            msg.setText('请先选择要删除的任务')
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet('''
                QMessageBox {
                    background-color: #F0F4F8;
                }
                QMessageBox QLabel {
                    color: #2C3E50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            ''')
            msg.exec_()
            return
        
        row = self.task_list.row(current_item)
        if row < len(self.data['tasks']):
            del self.data['tasks'][row]
            self.saveData()
            self.loadTasks()
    
    def editTask(self):
        """修改任务"""
        current_item = self.task_list.currentItem()
        if not current_item:
            msg = QMessageBox(self)
            msg.setWindowTitle('警告')
            msg.setText('请先选择要修改的任务')
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet('''
                QMessageBox {
                    background-color: #F0F4F8;
                }
                QMessageBox QLabel {
                    color: #2C3E50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            ''')
            msg.exec_()
            return
        
        row = self.task_list.row(current_item)
        if row < len(self.data['tasks']):
            old_name = self.data['tasks'][row]['name']
            dialog = QInputDialog(self)
            dialog.setWindowTitle('修改任务')
            dialog.setLabelText('请输入新的任务名称:')
            dialog.setTextValue(old_name)
            dialog.setStyleSheet('''
                QInputDialog {
                    background-color: #F0F4F8;
                }
                QInputDialog QLabel {
                    color: #2C3E50;
                    font-size: 14px;
                    font-weight: bold;
                }
                QInputDialog QLineEdit {
                    background-color: #FFFFFF;
                    border: 2px solid #3498DB;
                    border-radius: 5px;
                    padding: 8px;
                    color: #2C3E50;
                    font-size: 14px;
                    min-height: 30px;
                }
                QInputDialog QLineEdit:focus {
                    border: 2px solid #2980B9;
                }
                QDialogButtonBox QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 25px;
                    font-weight: bold;
                    font-size: 14px;
                    min-width: 80px;
                    min-height: 35px;
                }
                QDialogButtonBox QPushButton:hover {
                    background-color: #2980B9;
                }
                QDialogButtonBox QPushButton:pressed {
                    background-color: #1A5276;
                }
            ''')
            if dialog.exec_() == QInputDialog.Accepted:
                new_name = dialog.textValue()
                if new_name.strip():
                    self.data['tasks'][row]['name'] = new_name.strip()
                    self.saveData()
                    self.loadTasks()
    
    def saveStartDate(self):
        """保存初始日期"""
        date_str = self.start_date_edit.text()
        try:
            # 验证日期格式
            datetime.strptime(date_str, '%Y-%m-%d')
            self.data['start_date'] = date_str
            self.saveData()
            self.updateDayCount()
            self.loadTasks()
            self.updateCalendar()
            msg = QMessageBox(self)
            msg.setWindowTitle('成功')
            msg.setText('初始日期已保存')
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet('''
                QMessageBox {
                    background-color: #F0F4F8;
                }
                QMessageBox QLabel {
                    color: #2C3E50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
            ''')
            msg.exec_()
        except ValueError:
            msg = QMessageBox(self)
            msg.setWindowTitle('错误')
            msg.setText('请输入正确的日期格式 (YYYY-MM-DD)')
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet('''
                QMessageBox {
                    background-color: #F0F4F8;
                }
                QMessageBox QLabel {
                    color: #2C3E50;
                    font-size: 12px;
                }
                QPushButton {
                    background-color: #E74C3C;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #C0392B;
                }
            ''')
            msg.exec_()
    
    def changeFont(self):
        """修改字体大小"""
        font_size = int(self.font_size_combo.currentText())
        
        # 应用字体大小到所有控件
        font = QFont('Microsoft YaHei', font_size)
        
        # 更新标签字体
        self.start_date_label.setFont(font)
        self.font_label.setFont(font)
        
        # 更新打卡天数标签
        self.day_count_label.setFont(QFont('Microsoft YaHei', font_size))
        
        # 更新任务列表
        self.loadTasks()
        
        # 更新日历字体
        calendar_font_size = max(10, font_size - 2)
        self.calendar.setStyleSheet(f'''
            QCalendarWidget {{
                background-color: #FFFFFF;
                border: 2px solid #F39C12;
                border-radius: 5px;
            }}
            QCalendarWidget QTableView {{
                background-color: #FFFFFF;
                selection-background-color: #F39C12;
                selection-color: white;
                alternate-background-color: #FEF9E7;
                font-size: {calendar_font_size}px;
            }}
            QCalendarWidget QToolButton {{
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
                font-size: {font_size}px;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: #E67E22;
            }}
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {{
                background-color: #F39C12;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }}
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {{
                background-color: #E67E22;
            }}
            QCalendarWidget QSpinBox {{
                background-color: #FFFFFF;
                border: 1px solid #BDC3C7;
                border-radius: 3px;
                padding: 2px;
                color: #2C3E50;
                font-size: {font_size}px;
            }}
        ''')
        
        msg = QMessageBox(self)
        msg.setWindowTitle('成功')
        msg.setText(f'字体大小已设置为 {font_size}pt')
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet('''
            QMessageBox {
                background-color: #F0F4F8;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        ''')
        msg.exec_()
    
    def updateDayCount(self):
        """更新打卡天数"""
        start_date = datetime.strptime(self.data['start_date'], '%Y-%m-%d')
        today = datetime.now()
        days_passed = (today - start_date).days + 1
        self.day_count_label.setText(f'今天是打卡的第 {days_passed} 天')
    
    def updateCalendar(self):
        """更新日历显示"""
        # 重置日历格式
        for i in range(self.calendar.minimumDate().dayOfYear(), self.calendar.maximumDate().dayOfYear() + 1):
            date = self.calendar.minimumDate().addDays(i - self.calendar.minimumDate().dayOfYear())
            self.calendar.setDateTextFormat(date, QTextCharFormat())
        
        # 标记完成的日期
        for task in self.data['tasks']:
            for completed_date in task['completed']:
                try:
                    date_obj = datetime.strptime(completed_date, '%Y-%m-%d')
                    qdate = QDate(date_obj.year, date_obj.month, date_obj.day)
                    
                    # 设置完成日期的格式 - 使用护眼绿色
                    fmt = QTextCharFormat()
                    fmt.setBackground(QColor(76, 175, 80))  # 护眼绿色
                    fmt.setForeground(QColor(255, 255, 255))  # 白色文字
                    fmt.setFontWeight(QFont.Bold)  # 加粗
                    self.calendar.setDateTextFormat(qdate, fmt)
                except:
                    pass
    
    def onDateSelected(self):
        """日期选择事件"""
        selected_date = self.calendar.selectedDate()
        date_str = selected_date.toString('yyyy-MM-dd')
        
        # 显示选中日期的任务完成情况
        completed_tasks = []
        for task in self.data['tasks']:
            if date_str in task['completed']:
                completed_tasks.append(task['name'])
        
        if completed_tasks:
            msg = f"{date_str} 完成的任务:\n" + '\n'.join(completed_tasks)
        else:
            msg = f"{date_str} 没有完成任何任务"
        
        message_box = QMessageBox(self)
        message_box.setWindowTitle('任务完成情况')
        message_box.setText(msg)
        message_box.setIcon(QMessageBox.Information)
        message_box.setStyleSheet('''
            QMessageBox {
                background-color: #F0F4F8;
            }
            QMessageBox QLabel {
                color: #2C3E50;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        ''')
        message_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClockInApp()
    ex.show()
    sys.exit(app.exec_())