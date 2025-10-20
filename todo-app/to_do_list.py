import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QListWidgetItem, QListWidget)
from PyQt5.Qt import Qt


class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(450, 500)
        self.title = QLabel("Daily Task(‾◡◝)")
        self.add_btn = QPushButton("Add")
        self.textbox = QLineEdit()
        self.save_btn = QPushButton("Save")
        self.del_btn = QPushButton("Delete")
        self.task_list = QListWidget()
        self.file_path = os.path.join(os.path.dirname(__file__), "qtasks.txt")
        self.load_task()
        self.initUI()
        self.designUI()


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #202021;
                margin: 5px;              
            }
                           
            QPushButton, QLineEdit, QListWidget {
                font-family: Arial;
                border-radius: 10px; 
            }
                           
            QLabel {
                color: #70d14f;
                font-family: Ari-W9500;
                font-size: 35px;

            }        

            QLineEdit {
                color: white;
                background-color: #202021;
                border: 1px solid #828285;
                padding: 10px 15px;
                font-size: 15px;
                
            }
                           
            QPushButton {
                background-color: #70d14f;
                padding: 10px 50px;
                font-size: 15px;
                font-weight: bold;
            }
                           
            QListWidget {
                color: white;
                font-family: Arial;
                font-size: 17px;
                border: 1px solid #828285;
            }

            
        """)


    def initUI(self):
        self.textbox.setPlaceholderText("Add task...")

        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add_task)

        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_tasks)

        self.del_btn.setCursor(Qt.PointingHandCursor)
        self.del_btn.clicked.connect(self.del_task)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.textbox)
        hbox1.addWidget(self.add_btn)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.save_btn)
        hbox2.addWidget(self.del_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.title)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.task_list)
        vbox.addLayout(hbox2)

        vbox.setContentsMargins(20, 20, 20, 20)

        self.setLayout(vbox)


    def add_task(self):
        task = self.textbox.text()
        if not task:
            return

        item = QListWidgetItem(task)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.task_list.addItem(item)
        self.textbox.clear()


    def del_task(self):
        selected_task = self.task_list.currentItem()
        if not selected_task:
            return
        
        row_num = self.task_list.row(selected_task)
        self.task_list.takeItem(row_num)


    def save_tasks(self):
        with open(self.file_path, "w") as file:
            for i in range(self.task_list.count()):
                item = self.task_list.item(i)

                if item.checkState() == Qt.Checked:
                    file.write("[x] " + item.text() + "\n")
                else:
                    file.write("[ ] " + item.text() + "\n")


    def load_task(self):
        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, "r") as file:
            for line in file:
                task = line.strip()
                checked = task.startswith("[x] ")
                unchecked = task.startswith("[ ] ")

                task_text = task[4:].strip()

                if task_text:
                    item = QListWidgetItem(task_text)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

                    if checked:
                        item.setCheckState(Qt.Checked)
                    elif unchecked:
                        item.setCheckState(Qt.Unchecked)

                    self.task_list.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tdl = ToDoList()
    tdl.show()
    sys.exit(app.exec_())