# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:28:27 2020

@author: hiltger
"""
import sys, time
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QLineEdit,QMessageBox
import cv2
import os
import subprocess


class Camera(QWidget):
    def __init__(self):
        super(Camera,self).__init__()
        self.initUi()
        
    def initUi(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(770, 50, 695, 470)
        self.timer_camera = QtCore.QTimer() # 定時器
        self.timer_picture = QtCore.QTimer() # 定時器
        self.timer_crop = QtCore.QTimer()
        self.cap = cv2.VideoCapture() # 準備獲取圖像
        self.CAM_NUM = 0   
        vboxLayout = QVBoxLayout()
        self.label_face = QLabel()
        vboxLayout.addWidget(self.label_face)
        self.label_face.setFixedSize(680,455)
        self.setLayout(vboxLayout)
        self.button_open_camera_click()
        self.timer_camera.timeout.connect(self.show_camera)
        self.Oneshots()
        
    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QMessageBox.warning(
                    self, u"Warning", u"請檢測相機與電腦是否連接正確",
                    buttons=QMessageBox.Ok,
                    defaultButton=QMessageBox.Ok)
            else:
                self.timer_camera.start(0.1)



    def show_camera(self):
        flag, self.image = self.cap.read()

        self.image=cv2.flip(self.image, 1) # 左右翻轉
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.label_face.setScaledContents(True)
    
    #第一部分拍照        
    def Onetake(self):
        now_time = time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time()))
        path = "D:\\Aubrey_file\\Main\\Personality"
        if not os.path.isdir(path):
            os.mkdir(path)
        cv2.imwrite(path+'\\pic_'+str(now_time)+'.jpg',self.image)
        
            
    def Oneshots(self):
        c = 1
        if self.cap.isOpened():
            rval,frame = self.cap.read()
        else:
            rval = False
            print("read error")
        while rval:
            if(c <= 20):
                self.timer_crop.start(1000)
                self.timer_crop.timeout.connect(self.Onetake)
                c = c + 1
            else:
                break
    
    #第二部分拍照
    def takePhoto(self):
        now_time = time.strftime('%m-%d-%H-%M-%S',time.localtime(time.time()))
        folderpath = 'D:\\Aubrey_file\\Main\\Capture'
        list = os.listdir(folderpath) # dir is your directory path
        number_files = len(list)
        if (number_files <=14):
                cv2.imwrite(os.path.join(folderpath , 'pic_' + str(now_time) + '.jpg'), self.image)
        else:
                self.autocrop(folderpath)

    def anaoshots(self):
        self.timer_crop.stop()
        if self.cap.isOpened():
            rval,frame = self.cap.read()
            c = 1
            while rval:
                    if(c <= 15):
                            self.timer_picture.start(1000)
                            self.timer_picture.timeout.connect(self.takePhoto)
                            c = c + 1
                    else:
                            break
        else:
            rval = False
            print("read error")
    
    def autocrop(self, path):
        temp = path    #截圖先存這
        cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done1"   #autocrop過的圖
        list = os.listdir(cnt_path) # dir is your directory path
        number_files = len(list)
        if (number_files <=14):
                img_path = "D:\\Aubrey_file\\Main\\Done\\Done1"
        else:
                cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done2"   #autocrop過的圖
                list = os.listdir(cnt_path) # dir is your directory path
                number_files = len(list)
                if (number_files <=14):
                        img_path = 'D:\\Aubrey_file\\Main\\Done\\Done2'
                else:
                        cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done3"   #autocrop過的圖
                        list = os.listdir(cnt_path) # dir is your directory path
                        number_files = len(list)
                        if (number_files <=14):
                                img_path = 'D:\\Aubrey_file\\Main\\Done\\Done3'
                        else:
                                cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done4"   #autocrop過的圖
                                list = os.listdir(cnt_path) # dir is your directory path
                                number_files = len(list)
                                if (number_files <=14):
                                        img_path = 'D:\\Aubrey_file\\Main\\Done\\Done4'
                                else:
                                        cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done5"   #autocrop過的圖
                                        list = os.listdir(cnt_path) # dir is your directory path
                                        number_files = len(list)
                                        if (number_files <=14):
                                                img_path = 'D:\\Aubrey_file\\Main\\Done\\Done5'
                                        else:
                                                cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done6"   #autocrop過的圖
                                                list = os.listdir(cnt_path) # dir is your directory path
                                                number_files = len(list)
                                                if (number_files <=14):
                                                        img_path = 'D:\\Aubrey_file\\Main\\Done\\Done6'
                                                else:
                                                        cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done7"   #autocrop過的圖
                                                        list = os.listdir(cnt_path) # dir is your directory path
                                                        number_files = len(list)
                                                        if (number_files <=14):
                                                                img_path = 'D:\\Aubrey_file\\Main\\Done\\Done7'
                                                        else:
                                                                cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done8"   #autocrop過的圖
                                                                list = os.listdir(cnt_path) # dir is your directory path
                                                                number_files = len(list)
                                                                if (number_files <=14):
                                                                        img_path = 'D:\\Aubrey_file\\Main\\Done\\Done8' 
                                                                else:
                                                                        cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done9"   #autocrop過的圖
                                                                        list = os.listdir(cnt_path) # dir is your directory path
                                                                        number_files = len(list)
                                                                        if (number_files <=14):
                                                                                img_path = 'D:\\Aubrey_file\\Main\\Done\\Done9'
                                                                        else:
                                                                                cnt_path = "D:\\Aubrey_file\\Main\\Done\\Done10"   #autocrop過的圖
                                                                                list = os.listdir(cnt_path) # dir is your directory path
                                                                                number_files = len(list)
                                                                                if (number_files <=14):
                                                                                        img_path = 'D:\\Aubrey_file\\Main\\Done\\Done10'
        reject = "D:\\Aubrey_file\\Main\\Reject"   #偵測不到臉的圖
        command = "autocrop -i {} -o {} -r {} -w 224 -H 224".format(temp,img_path,reject)
        subprocess.call(command, shell=True)
        
    def close(self):
        if self.timer_camera.isActive() != False:
            ok = QPushButton()
            cacel = QPushButton()

            msg = QMessageBox(QMessageBox.Warning, u"關閉", u"是否關閉！")
            msg.addButton(ok,QMessageBox.ActionRole)
            msg.addButton(cacel, QMessageBox.RejectRole)
            msg.setGeometry(800,700,0,0)
            ok.setText(u'確定')
            cacel.setText(u'取消')

            if msg.exec_() != QMessageBox.RejectRole:

                if self.cap.isOpened():
                    self.cap.release()
                if self.timer_camera.isActive():
                        self.timer_camera.stop()
                        self.timer_picture.stop()
                        self.timer_deception.stop()
                        
 
