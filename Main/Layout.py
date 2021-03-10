# -*- coding: utf-8 -*-
"""
Created on Thu May 28 23:00:29 2020

@author: swift
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 22:17:01 2020

@author: Aubrey
"""
import keras
import  tensorflow as tf
import pandas as pd
import testt   #part2
import sys, time
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QLineEdit,QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from minicamera import Camera
import cv2
import matplotlib
import subprocess
from keras.preprocessing import image
from PIL import Image
import MySQLdb
from PyQt5.QAxContainer import QAxWidget
#import MySQLdb
import os

os.environ["CUDA_VISIBLE_DEVICES"] = '1'
matplotlib.use("Qt5Agg")  # 宣告使用QT5

class Interview(QWidget):
    def __init__(self):
        super(Interview,self).__init__()
        global modelpath, saver, model2, vgg_model_new
        modelpath = 'D:\\Aubrey_file\\Main\\model1'
        saver= tf.train.import_meta_graph(modelpath + '\\model_full.meta')
        model2 = keras.models.load_model('my_model.h5')
        init_op = tf.initialize_all_variables()
        global sess
        sess = tf.Session()
        labels = ["ValueExtraversion","ValueNeuroticism","ValueAgreeableness","ValueConscientiousness","ValueOpenness"]
        sess.run(init_op)
        # Load graph and parameters, etc.
        global imgs, output
                            
        saver.restore(sess, tf.train.latest_checkpoint(modelpath))
        graph = tf.get_default_graph()
        # Get tensor names
        imgs = graph.get_tensor_by_name("image_placeholder:0")
        output = graph.get_tensor_by_name("output:0")
        #print(output)
        self.initUi()
        global camera
        camera = Camera()
        camera.show()

    def initUi(self):
        self.createGridGroupBox()
        self.undercamera()
        self.resize(1500,900)
        self.setGeometry(20, 50, 1500, 900)
        #self.timer_camera = QtCore.QTimer() # 定時器
        #self.timer_picture = QtCore.QTimer() # 定時器
        #self.timer_crop = QtCore.QTimer() # 定時器
        #self.timer_deception = QtCore.QTimer() # 定時器
        global timer_deception
        timer_deception = QtCore.QTimer()
        """
        self.cap = cv2.VideoCapture() # 準備獲取圖像
        self.CAM_NUM = 0 """   
        mainLayout = QHBoxLayout() 
        vboxLayout = QVBoxLayout()
        """
        self.label_face = QLabel()
        vboxLayout.addWidget(self.label_face)
        self.label_face.setFixedSize(680,455)"""
        self.grey_area = QLabel()
        vboxLayout.addWidget(self.grey_area)
        self.grey_area.setFixedSize(680,455)
        
        self.axWidget = QAxWidget()
        self.axWidget.setFixedSize(750, 900)
        vboxLayout.addLayout(self.finallayout)
        mainLayout.addWidget(self.axWidget)
        mainLayout.addLayout(vboxLayout)
        mainLayout.addWidget(self.gridGroupBox)
        self.setLayout(mainLayout)
        self.setWindowIcon(QtGui.QIcon("man.png"))
        self.setWindowTitle('Main Window')
        """
        self.button_open_camera_click()
        self.timer_camera.timeout.connect(self.show_camera)
        self.Oneshots()"""
        path = 'D:\\Swift Desktop\\Yi-Ting_CV  (2018).docx'                            
        self.openOffice(path,'Word.Application')
        
    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("")
        self.groupBox = QGroupBox("")
        self.layout = QGridLayout()
        font = QtGui.QFont('微軟正黑',16)
        font.setBold(True)
        font2 = QtGui.QFont('微軟正黑',13)
        nameLabel = QLabel("I.五大人格分析:")
        nameLabel.setFont(font)
        nameLabel_1 = QLabel("外向性:")
        nameLabel_1.setFont(font2)
        nameLabel_2 = QLabel("情緒不穩定性:")
        nameLabel_2.setFont(font2)
        nameLabel_3 = QLabel("親和性:")
        nameLabel_3.setFont(font2)
        nameLabel_4 = QLabel("盡責性:")
        nameLabel_4.setFont(font2)
        nameLabel_5 = QLabel("經驗開放性:")
        nameLabel_5.setFont(font2)
        setting = QPushButton("設定")
        setting.setIcon(QIcon("setting.png"))
        self.fig = plt.figure(facecolor='none')      
        self.canvas = FigureCanvas(self.fig)
        plt.close()   
        button_plot = QPushButton("人格分析")
        self.layout.addWidget(self.canvas,7,0,1,6)
        self.layout.addWidget(button_plot,8,5)
        self.layout.setSpacing(5)
        self.layout.addWidget(setting,0,0,1,6)
        self.layout.addWidget(nameLabel,1,0,1,2)
        self.layout.addWidget(nameLabel_1,2,0,1,2)
        self.layout.addWidget(nameLabel_2,3,0,1,2)
        self.layout.addWidget(nameLabel_3,4,0,1,2)
        self.layout.addWidget(nameLabel_4,5,0,1,2)
        self.layout.addWidget(nameLabel_5,6,0,1,2)
        self.gridGroupBox.setLayout(self.layout)
        setting.clicked.connect(self.settingwidgets)
        button_plot.clicked.connect(self.personality)
        
        
    def undercamera(self):
        self.finallayout = QGridLayout()
        Done = QPushButton("計算匹配度")
        Done.clicked.connect(self.match)
        self.Grade = QLineEdit("")
        self.Grade.setFrame(False)       
        self.Grade.returnPressed.connect(self.check)
        ansLabel = QLabel("回答分數(0-100):")
        font = QtGui.QFont('微軟正黑',16)
        font1 = QtGui.QFont('微軟正黑',16)
        font1.setBold(True)
        ansLabel.setFont(font)       
        finalLabel = QLabel("匹配度:")
        finalLabel.setFont(font)     
        font2 = QtGui.QFont('微軟正黑',80)
        TrueLabel = QLabel("II.真實度判定:")
        TrueLabel.setFont(font1)
        font3 = QtGui.QFont('微軟正黑體',13)
        self.predictLabel = QLabel()
        self.predictLabel.setFont(font3)
        self.finallayout.addWidget(self.predictLabel,1,0,1,2)
        self.finallayout.addWidget(TrueLabel,0,0,1,2)
        self.finallayout.addWidget(ansLabel,2,0)
        self.finallayout.addWidget(self.Grade,2,1)
        self.finallayout.addWidget(finalLabel,0,3,1,2) 
        self.finallayout.addWidget(Done,8,5)
        self.i = 0
        self.total = 0
        
    def check(self):
        txt = self.Grade.text()
        font = QtGui.QFont('微軟正黑',16)
        value_lst = []
        self.i += 1
        if (txt != 0):
            value_lst.append(txt)
            self.Grade.clear()
            print (value_lst)
            grade = int(value_lst[0])
            self.total += grade
            print (self.total)
            num = QLabel(value_lst[0])
            num.setFont(font)
            quesnum = QLabel(str(self.i)+'.')
            quesnum.setFont(font)
            self.finallayout.addWidget(quesnum,2+self.i,0)
            self.finallayout.addWidget(num,2+self.i,1)
            self.averge = self.total/self.i
            print (self.averge)
         
          
    def calldeception(self):
        c = 1
        if(c <= 20):
                timer_deception.start(20000)
                timer_deception.timeout.connect(self.deception)
                c = c + 1
            
        
    def openOffice(self, path, app):
        if not self.axWidget.setControl(app):
            return QMessageBox.critical(self, '錯誤', '没有安装  %s' % app)
        self.axWidget.dynamicCall(
            'SetVisible (bool Visible)', 'false')  # 不显示窗体
        self.axWidget.setProperty('DisplayAlerts', False)
        self.axWidget.setControl(path)
        self.axWidget.show()
        
    def about(self):     
        msgBox = QMessageBox(QMessageBox.NoIcon, 'Final','匹配度:80')
        msgBox.setIcon(1)
        msgBox.exec()
        
    def settingwidgets(self):
        self.dia = Set()
        self.dia.show()
        
    def MyFigure(self):
        angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))
        ax = self.fig.add_subplot(111, polar=True,) 
        data = [(prediction[0][0]*2), (prediction[0][1]*2), (prediction[0][2]*2), (prediction[0][3]*2), (prediction[0][4]*2), (prediction[0][0]*2)]
        # 绘制三个五边形
        floor = 0
        ceil = 2
        labels = np.array(['Extraversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness to Experience'])
        # 绘制五边形的循环
        for i in np.arange(floor, ceil + 0.5 ,0.5):
            ax.plot(angles, [i] * (6), '-', lw= 0.5, color='black')
        for i in range(5):
            ax.plot([angles[i], angles[i]], [floor, ceil], '-',lw=0.5, color='black')
         # 绘制雷达图
        ax.plot(angles, data, 'b-', lw=2, alpha=0.35)
        ax.fill(angles, data, facecolor='b', alpha=0.25)
    
        ax.set_thetagrids(angles * 180 / np.pi, labels)
        ax.spines['polar'].set_visible(False)#不显示极坐标最外的圆形
        ax.set_theta_zero_location('N')#设置极坐标的起点（即0度）在正上方向
        ax.grid(False)# 不显示分隔线
        ax.set_yticks([]) # 不显示坐标间隔
        self.canvas.draw()  
    
    def loading(self):     
        self.msgBox = QMessageBox(QMessageBox.NoIcon, 'Loading','人格特質分析中...')
        self.msgBox.setGeometry(800,580,0,0)
        self.msgBox.setIcon(1)
        self.msgBox.setStandardButtons(QMessageBox.Ok )
        self.msgBox.button(QMessageBox.Ok).animateClick(10*1000) 
        self.msgBox.exec()
        
    #part1
    def personality(self):
            self.loading()
            camera.anaoshots()
            def load_image(addr):
                    img = np.array(Image.open(addr).resize((224,224), Image.ANTIALIAS))
                    img = img.astype(np.uint8)
                    return img
  
            def predict(img):
                    global imgs, prediction
                    feed_dict ={imgs: [img]}
                    prediction = sess.run(output,feed_dict=feed_dict)
                    return prediction
                    
            global array_of_addr
            array_of_addr = []
            # this function is for read image,the input is directory name
            directory_name = 'D:\\Aubrey_file\\Main\\Personality'
            for filename in os.listdir(directory_name):
                    array_of_addr.append(directory_name + "\\" + filename)
                    for i in array_of_addr:
                            testdata = load_image(i)
            print("finish loading!")
            global prediction
            prediction = predict(testdata)
            print(prediction)
            print("ValueExtraversion: %.3f" %(prediction[0][0]))
            print("ValueNeuroticism: %.3f" %(prediction[0][1]))
            print("ValueAgreeableness: %.3f"  %(prediction[0][2]))
            print("ValueConscientiousness: %.3f" %(prediction[0][3]))
            print("ValueOpenness: %.3f"  %(prediction[0][4]))
            font2 = QtGui.QFont('微軟正黑',13)        
            scoreLabel_1 = QLabel(str(round(prediction[0][0], 3)))
            scoreLabel_1.setFont(font2)
            self.layout.addWidget(scoreLabel_1,2,2,1,2)
            scoreLabel_2 = QLabel(str(round(prediction[0][1], 3)))
            scoreLabel_2.setFont(font2)
            self.layout.addWidget(scoreLabel_2,3,2,1,2)
            scoreLabel_3 = QLabel(str(round(prediction[0][2], 3)))
            scoreLabel_3.setFont(font2)
            self.layout.addWidget(scoreLabel_3,4,2,1,2)
            scoreLabel_4 = QLabel(str(round(prediction[0][3], 3)))
            scoreLabel_4.setFont(font2)
            self.layout.addWidget(scoreLabel_4,5,2,1,2)
            scoreLabel_5 = QLabel(str(round(prediction[0][4], 3)))
            scoreLabel_5.setFont(font2)
            self.layout.addWidget(scoreLabel_5,6,2,1,2)
            self.MyFigure()
            self.calldeception()

    #part2
    def deception(self):
        for i in range(1, 10):
                if os.path.isfile('D:\\Aubrey_file\\Main\\Deception\\' +str(i)+'.txt'):
                        i = i + 1
                else:
                        img_path = 'D:\\Aubrey_file\\Main\\Done\\Done' +str(i)
                        images_features = []
                        for img in os.listdir(img_path):
                                img = img_path +'\\' + img
                                img = image.load_img(img, target_size=(150,150))
                                img = np.expand_dims(img, axis=0)
                                images_features.append(img)
                        images_features = np.vstack(images_features)
                               
                        custom = model2.predict_classes(images_features)
                        d = 0
                        t = 0
                        for c in custom:
                                if c ==0:
                                        d = d + 1
                                else:
                                        t = t + 1
                        percent = round((t / 15)*100, 2)
                        txt_path = 'D:\\Aubrey_file\\Main\\Deception\\' +str(i)+'.txt'
                        f = open(txt_path, 'w')
                        self.new = str(percent)
                        self.predictLabel.setText('Truthful '+self.new+'%')      
                        
    def match(self):
        self.extroversion_w = int(extroversion)
        self.agreeableness_w = int(agreeableness)
        self.neuroticism_w = int(neuroticism)
        self.conscientiousness_w = int(conscientiousness)
        self.openness_w = int(openness_to_experience)
        self.weight1 = int(part1)/100
        self.weight2 = int(part2)/100
        #小數點那些是人格的分數，我先寫死
        traitscore = self.extroversion_w*(round(prediction[0][0], 1)) + self.agreeableness_w*(round(prediction[0][1], 1)) + self.neuroticism_w*(round(prediction[0][2], 1)) + self.conscientiousness_w*(round(prediction[0][3], 1)) + self.openness_w*(round(prediction[0][4], 1))
        trait = traitscore*self.weight1
        print(trait)
        quesscore = self.averge*self.weight2
        match = trait + quesscore
        print (int(match))
        matchint = int(match)
        final = QLabel(str(matchint))
        font2 = QtGui.QFont('微軟正黑',80)
        final.setFont(font2)
        self.finallayout.addWidget(final,2,3,6,3)
        camera.close()
        conn=MySQLdb.connect(host="127.0.0.1",user="root", passwd="", db="interview", charset="utf8") 
        cursor=conn.cursor()     #傳回 Cursor 物件
        matchstr = str(matchint)
        cursor.execute("UPDATE candidate SET score = '"+matchstr+"' WHERE name = '曾怡瑄'")
        conn.commit()

      
class Set(QWidget):
    def __init__(self):
        super(Set,self).__init__()
        self.initUi()

    def initUi(self):
        self.createGridGroupBox()
        self.creatVboxGroupBox()
        self.resize(600,400)
        self.setGeometry(40, 100, 600, 400)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.vboxGroupBox)
        self.setLayout(mainLayout)
        self.setWindowIcon(QtGui.QIcon("setting.png"))
        self.setWindowTitle('Setting')

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("")
        layout = QGridLayout()
        font = QtGui.QFont('微軟正黑',16)
        font.setBold(True)
        font2 = QtGui.QFont('微軟正黑',13)
        nameLabel = QLabel("權重設定")
        nameLabel.setFont(font)
        firstLabel = QLabel("第一部分(人格分析):")
        firstLabel.setFont(font2)
        secondLabel = QLabel("第二部分(問答分數):")
        secondLabel.setFont(font2)
        noLabel = QLabel("%")
        noLabel_2 = QLabel("%")
        self.Edit_1 = QLineEdit()
        self.Edit_1.setFixedSize(80,30)
        self.Edit_2 = QLineEdit()
        self.Edit_2.setFixedSize(80,30)
        layout.addWidget(nameLabel,0,0)
        layout.addWidget(firstLabel,1,0)
        layout.addWidget(secondLabel,2,0)
        layout.addWidget(noLabel,2,2)
        layout.addWidget(noLabel_2,1,2)
        layout.addWidget(self.Edit_1,1,1)
        layout.addWidget(self.Edit_2,2,1)
        self.gridGroupBox.setLayout(layout)


    def creatVboxGroupBox(self):
        self.vboxGroupBox = QGroupBox("")
        layout = QGridLayout() 
        font = QtGui.QFont('微軟正黑',16)
        font2 = QtGui.QFont('微軟正黑',13)
        nameLabel = QLabel("人格比重")
        nameLabel.setFont(font)
        nameLabel_1 = QLabel("外向性:")
        nameLabel_1.setFont(font2)
        nameLabel_2 = QLabel("情緒不穩定性:")
        nameLabel_2.setFont(font2)
        nameLabel_3 = QLabel("親和性:")
        nameLabel_3.setFont(font2)
        nameLabel_4 = QLabel("盡責性:")
        nameLabel_4.setFont(font2)
        nameLabel_5 = QLabel("經驗開放性:")
        nameLabel_5.setFont(font2)
        self.LineEdit_1 = QLineEdit("")
        self.LineEdit_2 = QLineEdit("")
        self.LineEdit_3 = QLineEdit("")
        self.LineEdit_4 = QLineEdit("")
        self.LineEdit_5 = QLineEdit("")
        noLabel = QLabel("%")
        noLabel_2 = QLabel("%")
        noLabel_3 = QLabel("%")
        noLabel_4 = QLabel("%")
        noLabel_5 = QLabel("%")
        Save = QPushButton("確定")
        concel = QPushButton("取消")
        layout.addWidget(nameLabel,0,0)
        layout.addWidget(nameLabel_1,1,0)
        layout.addWidget(nameLabel_2,2,0)
        layout.addWidget(nameLabel_3,3,0)
        layout.addWidget(nameLabel_4,4,0)
        layout.addWidget(nameLabel_5,5,0)
        layout.addWidget(self.LineEdit_1,1,1)
        layout.addWidget(self.LineEdit_2,2,1)
        layout.addWidget(self.LineEdit_3,3,1)
        layout.addWidget(self.LineEdit_4,4,1)
        layout.addWidget(self.LineEdit_5,5,1)
        layout.addWidget(noLabel,1,2)
        layout.addWidget(noLabel_2,2,2)
        layout.addWidget(noLabel_3,3,2)
        layout.addWidget(noLabel_4,4,2)
        layout.addWidget(noLabel_5,5,2)
        layout.addWidget(Save,6,3)
        layout.addWidget(concel,6,4)
        self.vboxGroupBox.setLayout(layout)
        
        Save.clicked.connect(self.save_weight)
        concel.clicked.connect(self.Concel)         
        
        
    def save_weight(self):
        global extroversion, agreeableness, neuroticism, conscientiousness, openness_to_experience
        extroversion = self.LineEdit_1.text()
        agreeableness = self.LineEdit_2.text()
        neuroticism = self.LineEdit_3.text() 
        conscientiousness = self.LineEdit_4.text()
        openness_to_experience = self.LineEdit_5.text()
        global part1, part2
        part1 = self.Edit_1.text()
        part2 = self.Edit_2.text()
        self.hide()
        
    def Concel(self):
        self.close()