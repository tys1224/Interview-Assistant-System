from PyQt5 import QtGui
from functools import partial
import MySQLdb
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget,QFrame,QApplication,QDialog,
        QMessageBox,QVBoxLayout, QLineEdit,QTableWidgetItem,QTableWidget,QLabel,QHBoxLayout,QGridLayout,QPushButton,QCheckBox)
import sys
import os
#from minicamera import Camera
from Main import Interview

#建立介面類
class creat_view(QDialog):
    def __init__(self,parent = None):
        super(creat_view,self).__init__(parent)

        #設定介面大小、名稱、背景
        self.resize(960,800)
        self.setWindowTitle('Database')
        #self.setStyleSheet("background-image:url(picccc.png)")

        #窗體屬性
        self.setWindowFlags(Qt.Widget)

        conn=MySQLdb.connect(host="127.0.0.1",user="root", passwd="", db="interview", charset="utf8") 
        cursor=conn.cursor()     #傳回 Cursor 物件
        cursor.execute("SELECT * FROM candidate")
        data = cursor.fetchall()

        #資料列名
        col_lst = [tup[0] for tup in cursor.description]
        horizontalHeader = ["選取","姓名","年齡","性别","學歷","匹配度"]

        #資料的大小
        row = len(data)
        vol = len(data[0])


        #插入表格
        self.MyTable = QTableWidget(row,vol+1)
        font = QtGui.QFont('微軟雅黑',10)

        #設定字型、表頭
        self.MyTable.horizontalHeader().setFont(font)
        self.MyTable.setHorizontalHeaderLabels(horizontalHeader)
        #設定豎直方向表頭不可見
        self.MyTable.verticalHeader().setVisible(True)
        self.MyTable.setFrameShape(QFrame.NoFrame)
        self.List = []          
        
        #構建表格插入資料
        for i in range(row):   
            self.ck = QCheckBox()
            self.List.append(self.ck)
            h = QHBoxLayout()
            h.setAlignment(Qt.AlignCenter)
            h.addWidget(self.ck)
            self.w = QWidget()
            self.w.setLayout(h)
            self.MyTable.setCellWidget(i, 0, self.w)             
            for j in range(vol):
                temp_data = data[i][j]  # 臨時記錄，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 轉換後可插入表格     
                self.MyTable.setItem(i, j+1, data1)
            
            
 
        #編輯按鈕
        self.qle = QLineEdit()
        #增刪查改四個按鈕
        addButton = QPushButton("新增欄位")
        okButton = QPushButton("新增資料")
        deleteButton = QPushButton("刪除")

        #設定按鈕內字型樣式
        addButton.setFont(font)
        okButton.setFont(font)
        deleteButton.setFont(font)

        #垂直佈局
        Label = QLabel("輸入搜尋姓名:")
        search = QPushButton("搜尋!")
        Start = QPushButton("開始面試")
        Glayout = QGridLayout()
        Glayout.addWidget(Label,0,0)
        Glayout.addWidget(self.qle,0,1)
        Glayout.addWidget(search,0,2)
        Glayout.addWidget(addButton,1,3)
        Glayout.addWidget(okButton,1,4)
        Glayout.addWidget(deleteButton,1,5)
        Glayout.addWidget(self.MyTable,2,0,10,6)
        Glayout.addWidget(Start,12,5)
        
        self.setLayout(Glayout)
        
        addButton.clicked.connect(partial(self.add_data,cursor,conn))#插入實現
        okButton.clicked.connect(partial(self.new_data, cursor, conn,col_lst))#插入實現
        deleteButton.clicked.connect(partial(self.del_line,cursor,conn))#刪除實現
        search.clicked.connect(partial(self.search_data,conn))#查詢實現
        Start.clicked.connect(self.Main)#查詢實現

    #新增空表格
    def add_data(self,cursor,conn):
        #獲取行數
        row = self.MyTable.rowCount()
        #在末尾插入一空行
        self.MyTable.insertRow(row)
        self.ck = QCheckBox()
        self.List.append(self.ck)
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(self.ck)
        self.w = QWidget()
        self.w.setLayout(h)
        self.MyTable.setCellWidget(row, 0, self.w)
        
    def del_line(self,cursor,conn):#還無法刪掉ADD的欄
        reply = QMessageBox.question(self, 'Message', 'Are you sure to delete it ?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply ==  QMessageBox.Yes:
            row = self.MyTable.rowCount()
            for i in range (row):
                if self.List[i].isChecked():
                    item = self.MyTable.item(i, 1)
                    del_d = item.text() 
                    if len(del_d) != 0:
                        cursor.execute("DELETE FROM candidate WHERE name = '"+del_d+"'")#在資料庫刪除資料
                        conn.commit()
                        self.MyTable.removeRow(i)
                    else:                                        
                        self.MyTable.removeRow(i)
                        
    def new_data(self,cursor,conn,col_lst):#無法輸入空值
        row1 = self.MyTable.rowCount()
        value_lst = []
        for i in range (row1):
            if self.List[i].isChecked():   
                for j in range (4):
                    item = self.MyTable.item(i, j+1)
                    txt = item.text()
                    if(len(txt)==0):
                        value_lst.append("Null")
                    else:
                        value_lst.append(txt)
        cursor.execute("INSERT INTO candidate(name, age, gender, education) VALUES (%s,%s,%s,%s)",value_lst)
        conn.commit()
        
    def search_data(self,conn):
        row1 = self.MyTable.rowCount()
        txt = self.qle.text()
        for i in range(row1):
            item = self.MyTable.item(i, 1)
            name = item.text()
            if (txt == name):
                item.setForeground(QtGui.QBrush(Qt.red))
                
    def Main(self):
        self.hide()
        ex = Interview()
        ex.show()
        sys.exit(app.exec_())


def main():
    #顯示
    app = QApplication(sys.argv)
    c = creat_view()
    c.show()
    sys.exit(app.exec_())

main()
    

