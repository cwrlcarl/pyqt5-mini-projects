import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QListWidgetItem, QListWidget)
from PyQt5.Qt import Qt


class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(400, 450)
        self.title = QLabel("To-Do List🎯")
        self.add_btn = QPushButton("➕", objectName="add_btn")
        self.textbox = QLineEdit()
        self.save_btn = QPushButton("Save to File", objectName="save_btn")
        self.del_btn = QPushButton("Delete", objectName="del_btn")
        self.task_list = QListWidget()
        self.file_path = os.path.join(os.path.dirname(__file__), "qtasks.txt")
        self.load_task()
        self.initUI()
        self.designUI()


    def designUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #202021;
                margin: 5px 1px;              
            }
                           
            QPushButton, QLineEdit, QListWidget {
                font-family: MADE Outer Sans;
                border-radius: 3px;
            }
                           
            QLabel {
                color: white;
                font-family: MADE Outer Sans;
                font-size: 29px;
                margin: 0;
            }        

            QLineEdit {
                color: white;
                background-color: #2f2f30;
                padding: 10px 15px;
                font-size: 15px;
                margin-top: 12px;
            }
                           
            QPushButton {
                background-color: #2e2b36;
                padding: 10px 20px;
                font-size: 15px;
                color: white;
            }
                           
            QPushButton#add_btn {
                margin-top: 12px;
            }
                           
            QPushButton#save_btn {
                background-color: #d4423e; 
            }
                           
            QPushButton#del_btn {
                background-color: #2f2f30;
                color: #878787;
            }
                           
            QListWidget {
                color: white;
                font-family: Poppins;
                font-size: 16px;
            }

            QListWidget::item {
                color: white;
                
            }
                           
            QListWidget::item:selected {
                background-color: #2f2f30;
                border-radius: 3px;
                
            }
                           
            QListWidget::item:hover {
                background-color: #2f2f30;
                border-radius: 3px;
                
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

        vbox.setContentsMargins(30, 25, 30, 25)

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