#coding=utf-8
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QVBoxLayout,QWidget
from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSignal,QTimer
from PyQt5.uic import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap,QImage
import os
from threading import Thread
import sys,cv2
import time
import socket
import multiprocessing
import json
import numpy as np

class MySignals(QObject):
    
    draw_point = pyqtSignal()
    update_message = pyqtSignal()
    update_pa = pyqtSignal()
    collect_data = pyqtSignal()
    update_time = pyqtSignal()
    update_vedio = pyqtSignal()

class Asknum(QMainWindow):
    def __init__(self):
        global vehicle_num
        super().__init__()
        self.ui = loadUi('ask_num.ui', self)

        self.ui.set_num.clicked.connect(self.set_num_do)

    def set_num_do(self):
        global vehicle_num
        global ip
        vehicle_num = int(self.ui.ask_num.text())
        ip = self.ui.ask_ip.text()
        print(vehicle_num)
        self.close()

class SubWindow_p(QMainWindow):
    def __init__(self):
        global vehicle_num
        super().__init__()
        self.ui = loadUi('gxx_p.ui', self)
        self.ms = MySignals()
        self.ms.update_pa.connect(self.wait_pa)
        self.pas = [self.ui.pa_p_0,
                    self.ui.pa_p_1,
                    self.ui.pa_p_2,
                    self.ui.pa_p_3,
                    self.ui.pa_p_4,
                    self.ui.pa_p_5,
                    self.ui.pa_p_6,
                    self.ui.pa_p_7,
                    self.ui.pa_p_8,
                    self.ui.pa_p_9,
                    self.ui.pa_p_10,
                    self.ui.pa_p_11]
        self.ui.set_p.clicked.connect(self.set_piliang)
        t = Thread(target=self.wait_pa_start)
        t.start()
    def OPEN(self):
        self.show()
    def wait_pa(self):
        global pa
        for s in range(len(pa)):
            self.pas[s].setPlaceholderText(pa[s])
    def wait_pa_start(self):
        global pa
        global no_pa1
        while 1:
            if no_pa1 and (pa!=[]):
                    no_pa1 = 0
                    self.ms.update_pa.emit()
                    break
            time.sleep(0.2)
    def set_piliang(self):
        global newSockets
        global pa
        dictor = {}
        for i in range(len(newSockets)):
            for s in range(len(pa)):
                if self.pas[s].text()!='':
                    a = float(self.pas[s].text())
                else:
                    a = name[pa[s]][i]
                dictor[pa[s]] = a
            message = [5,dictor]
            message_json = json.dumps(message)
            if newSockets[i] != 0:
                try:
                    newSockets[i].send(message_json.encode("utf-8"))
                except:
                    pass

class SubWindow(QMainWindow):
    def __init__(self):
        global vehicle_num
        super().__init__()
        self.ui = loadUi('gxx_s.ui', self)
        self.ms = MySignals()
        self.ms.update_message.connect(self.updatemessage)

        self.manuls = [
            self.ui.manul_0,
            self.ui.manul_1,
            self.ui.manul_2,
            self.ui.manul_3,
            self.ui.manul_4,
            self.ui.manul_5,
            self.ui.manul_6,
            self.ui.manul_7,
            self.ui.manul_8,
            self.ui.manul_9,
            self.ui.manul_10,
            self.ui.manul_11]
        self.guideds = [
            self.ui.guided_0,
            self.ui.guided_1,
            self.ui.guided_2,
            self.ui.guided_3,
            self.ui.guided_4,
            self.ui.guided_5,
            self.ui.guided_6,
            self.ui.guided_7,
            self.ui.guided_8,
            self.ui.guided_9,
            self.ui.guided_10,
            self.ui.guided_11]
        self.RTLs = [
            self.ui.RTL_0,
            self.ui.RTL_1,
            self.ui.RTL_2,
            self.ui.RTL_3,
            self.ui.RTL_4,
            self.ui.RTL_5,
            self.ui.RTL_6,
            self.ui.RTL_7,
            self.ui.RTL_8,
            self.ui.RTL_9,
            self.ui.RTL_10,
            self.ui.RTL_11]
        self.texts = [
            self.ui.text_0,
            self.ui.text_1,
            self.ui.text_2,
            self.ui.text_3,
            self.ui.text_4,
            self.ui.text_5,
            self.ui.text_6,
            self.ui.text_7,
            self.ui.text_8,
            self.ui.text_9,
            self.ui.text_10,
            self.ui.text_11]
        self.pas = [
            [self.ui.pa0_0,self.ui.pa1_0,self.ui.pa2_0,self.ui.pa3_0,self.ui.pa4_0,self.ui.pa5_0,self.ui.pa6_0,self.ui.pa7_0,self.ui.pa8_0,self.ui.pa9_0,self.ui.pa10_0,self.ui.pa11_0],
            [self.ui.pa0_1,self.ui.pa1_1,self.ui.pa2_1,self.ui.pa3_1,self.ui.pa4_1,self.ui.pa5_1,self.ui.pa6_1,self.ui.pa7_1,self.ui.pa8_1,self.ui.pa9_1,self.ui.pa10_1,self.ui.pa11_1],
            [self.ui.pa0_2,self.ui.pa1_2,self.ui.pa2_2,self.ui.pa3_2,self.ui.pa4_2,self.ui.pa5_2,self.ui.pa6_2,self.ui.pa7_2,self.ui.pa8_2,self.ui.pa9_2,self.ui.pa10_2,self.ui.pa11_2],
            [self.ui.pa0_3,self.ui.pa1_3,self.ui.pa2_3,self.ui.pa3_3,self.ui.pa4_3,self.ui.pa5_3,self.ui.pa6_3,self.ui.pa7_3,self.ui.pa8_3,self.ui.pa9_3,self.ui.pa10_3,self.ui.pa11_3],
            [self.ui.pa0_4,self.ui.pa1_4,self.ui.pa2_4,self.ui.pa3_4,self.ui.pa4_4,self.ui.pa5_4,self.ui.pa6_4,self.ui.pa7_4,self.ui.pa8_4,self.ui.pa9_4,self.ui.pa10_4,self.ui.pa11_4],
            [self.ui.pa0_5,self.ui.pa1_5,self.ui.pa2_5,self.ui.pa3_5,self.ui.pa4_5,self.ui.pa5_5,self.ui.pa6_5,self.ui.pa7_5,self.ui.pa8_5,self.ui.pa9_5,self.ui.pa10_5,self.ui.pa11_5],
            [self.ui.pa0_6,self.ui.pa1_6,self.ui.pa2_6,self.ui.pa3_6,self.ui.pa4_6,self.ui.pa5_6,self.ui.pa6_6,self.ui.pa7_6,self.ui.pa8_6,self.ui.pa9_6,self.ui.pa10_6,self.ui.pa11_6],
            [self.ui.pa0_7,self.ui.pa1_7,self.ui.pa2_7,self.ui.pa3_7,self.ui.pa4_7,self.ui.pa5_7,self.ui.pa6_7,self.ui.pa7_7,self.ui.pa8_7,self.ui.pa9_7,self.ui.pa10_7,self.ui.pa11_7],
            [self.ui.pa0_8,self.ui.pa1_8,self.ui.pa2_8,self.ui.pa3_8,self.ui.pa4_8,self.ui.pa5_8,self.ui.pa6_8,self.ui.pa7_8,self.ui.pa8_8,self.ui.pa9_8,self.ui.pa10_8,self.ui.pa11_8],
            [self.ui.pa0_9,self.ui.pa1_9,self.ui.pa2_9,self.ui.pa3_9,self.ui.pa4_9,self.ui.pa5_9,self.ui.pa6_9,self.ui.pa7_9,self.ui.pa8_9,self.ui.pa9_9,self.ui.pa10_9,self.ui.pa11_9],
            [self.ui.pa0_10,self.ui.pa1_10,self.ui.pa2_10,self.ui.pa3_10,self.ui.pa4_10,self.ui.pa5_10,self.ui.pa6_10,self.ui.pa7_10,self.ui.pa8_10,self.ui.pa9_10,self.ui.pa10_10,self.ui.pa11_10],
            [self.ui.pa0_11,self.ui.pa1_11,self.ui.pa2_11,self.ui.pa3_11,self.ui.pa4_11,self.ui.pa5_11,self.ui.pa6_11,self.ui.pa7_11,self.ui.pa8_11,self.ui.pa9_11,self.ui.pa10_11,self.ui.pa11_11]]
        self.sets = [
            self.ui.set_0,
            self.ui.set_1,
            self.ui.set_2,
            self.ui.set_3,
            self.ui.set_4,
            self.ui.set_5,
            self.ui.set_6,
            self.ui.set_7,
            self.ui.set_8,
            self.ui.set_9,
            self.ui.set_10,
            self.ui.set_11]
        for i2 in range(vehicle_num):
            self.manuls[i2].clicked.connect(lambda checked, arg=i2:self.set_mode_do(arg,"MANUAL"))
        for i3 in range(vehicle_num):
            self.guideds[i3].clicked.connect(lambda checked, arg=i3:self.set_mode_do(arg,"GUIDED"))
        for i4 in range(vehicle_num):
            self.RTLs[i4].clicked.connect(lambda checked, arg=i4:self.set_mode_do(arg,"RTL"))
        for i5 in range(vehicle_num):
            self.sets[i5].clicked.connect(lambda checked, arg=i5:self.set_pa_do(arg))
        for i6 in range(vehicle_num):
            self.ui.set_all.clicked.connect(lambda checked, arg=i6:self.set_pa_do(arg))
        self.updatemessage_start()
    
    def OPEN(self):
        self.show()

    def updatemessage(self):
        global locations_global
        global speeds
        global headings
        global locations_local
        global moment1
        global battery
        global vehicle_num
        global modes
        global name
        global pa
        global no_pa
        for i in range(vehicle_num):
            text = "大地坐标："+str(locations_global[i])+"\n" \
                        +"本地坐标："+str(locations_local[i])+"\n" \
                        +"速度："+str(speeds[i])+"\n" \
                        +"船艏："+str(headings[i])+"\n" \
                        +"模式："+str(modes[i])+"\n"+"\n"
            for p in pa: 
                text = text + p + ":"+ str(name[p][i]) + " "
            self.texts[i].setPlainText(text)
        if no_pa and (pa!=[]):
            no_pa = 0
            for s in range(len(pa)):
                for num in range(vehicle_num):
                    self.pas[num][s].setPlaceholderText(pa[s])
            

    def updatemessage_start(self):
        def updatemessage_thread():
            while 1:
                self.ms.update_message.emit()
                time.sleep(0.25) 
        t = Thread(target=updatemessage_thread)
        t.start()

    def set_mode_do(self,num,mode):
        global newSockets
        print(num,mode)
        message = [2,mode]
        message_json = json.dumps(message,ensure_ascii=False)
        if newSockets[num] != 0:
            try:
                newSockets[num].send(message_json.encode("utf-8"))
            except:
                pass

    def set_pa_do(self,num):
        global newSockets
        global pa
        dictor = {}
        for s in range(len(pa)):
            if self.pas[num][s].text()!='':
                print(type(self.pas[num][s].text()),'haha')
                a = float(self.pas[num][s].text())
            else:
                a = name[pa[s]][num]
            dictor[pa[s]] = a
        message = [5,dictor]
        message_json = json.dumps(message)
        if newSockets[num]!=0:
            try:
                newSockets[num].send(message_json.encode("utf-8"))
            except:
                pass

class Goto(QMainWindow):
    def __init__(self):
        global vehicle_num
        super().__init__()
        self.ui = loadUi('goto.ui', self)
        '''
        if vehicle_num > 6:
            self.ui.setFixedSize(n*vehicle_num,m)
        else:
            self.ui.setFixedSize(n*vehicle_num,2*m)
        '''
        self.goto_norths = [
            self.ui.goto_north_0,
            self.ui.goto_north_1,
            self.ui.goto_north_2,
            self.ui.goto_north_3,
            self.ui.goto_north_4,
            self.ui.goto_north_5,
            self.ui.goto_north_6,
            self.ui.goto_north_7,
            self.ui.goto_north_8,
            self.ui.goto_north_9,
            self.ui.goto_north_10,
            self.ui.goto_north_11]
        self.goto_easts = [
            self.ui.goto_east_0,
            self.ui.goto_east_1,
            self.ui.goto_east_2,
            self.ui.goto_east_3,
            self.ui.goto_east_4,
            self.ui.goto_east_5,
            self.ui.goto_east_6,
            self.ui.goto_east_7,
            self.ui.goto_east_8,
            self.ui.goto_east_9,
            self.ui.goto_east_10,
            self.ui.goto_east_11]
        self.gotos = [
            self.ui.goto_0,
            self.ui.goto_1,
            self.ui.goto_2,
            self.ui.goto_3,
            self.ui.goto_4,
            self.ui.goto_5,
            self.ui.goto_6,
            self.ui.goto_7,
            self.ui.goto_8,
            self.ui.goto_9,
            self.ui.goto_10,
            self.ui.goto_11]
        for n1 in range(vehicle_num):
            self.goto_norths[n1].setPlaceholderText("x")
        for n2 in range(vehicle_num):
            self.goto_easts[n2].setPlaceholderText("y")

        for i1 in range(vehicle_num):
            self.gotos[i1].clicked.connect(lambda checked, arg=i1:self.goto(arg))
        for i2 in range(vehicle_num):
            self.ui.goto_all.clicked.connect(lambda checked, arg=i2:self.goto(arg))
    
    def OPEN(self):
        self.show()

    def goto(self,num):
        global newSockets
        global locations_global
        if (self.goto_easts[num].text()!='') and (self.goto_norths[num].text()!=''):
            message = [3,float(self.goto_norths[num].text()),float(self.goto_easts[num].text())]
            message_json = json.dumps(message,ensure_ascii=False)
            if newSockets[num] != 0:
                try:
                    newSockets[num].send(message_json.encode("utf-8"))
                except:
                    pass


class MainWindow(QMainWindow):

    def __init__(self):
        global vehicle_num
        super().__init__()
        self.ui = loadUi('./gxx.ui', self)
        
        
        self.ms = MySignals()
        self.ms.update_time.connect(self.update_time)
        self.ms.draw_point.connect(self.drawpoint)
        self.ms.collect_data.connect(self.collect_data)


        
        self.ui.home_lat.setPlaceholderText("lat")
        self.ui.home_lon.setPlaceholderText("lon")

        self.ui.savedata.clicked.connect(self.save_data)
        self.ui.clear_savedata.clicked.connect(self.clear_data_list)
        self.ui.set_home_0.clicked.connect(self.set_home_do_0)
        self.ui.sethome.clicked.connect(self.set_home_do)
        self.ui.clearline.clicked.connect(self.clear_line)
        self.ui.set_mode_manual.clicked.connect(lambda:self.set_mode_all("MANUAL"))
        self.ui.set_mode_guided.clicked.connect(lambda:self.set_mode_all("GUIDED"))
        self.ui.set_mode_RTL.clicked.connect(lambda:self.set_mode_all("RTL"))

        url = os.getcwd() + '/gxx03.html'
        self.ui.webview.load(QUrl.fromLocalFile(url))

        self.drawpoint_start()
        self.collect_data_start()
        self.update_time_start()
        #self.update_vedio_start()


    def update_vedio(self):
        global vedio_mark
        """
        从摄像头得到图像 先转换为RGB格式 再生成QImage对象
        再用此QImage刷新vF实例变量 以刷新视频画面
        """
        if vedio_mark==1:
            self.cam = cv2.VideoCapture('rtsp://admin:dianhang110@192.168.1.70:554/stream1')# 0代表电脑的摄像头，TP-LINK的需要改为：'rtsp://admin:dianhang110@192.168.1.60:554/stream1'
            self.w = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))       # 此处需要整数类型的数据
            self.h = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            #out_video = cv2.VideoWriter('',)
            self.ui.shipin.setAlignment(Qt.AlignCenter)
            vedio_mark = 0
        while True:
            try:
                r, f = self.cam.read()
                f = cv2.resize(f,(int(self.w/5),int(self.h/5)))
                f = cv2.flip(f,1)
                if r:
                    self.ui.shipin.setPixmap(QPixmap.fromImage(
                        QImage(cv2.cvtColor(f, cv2.COLOR_BGR2RGB),
                            int(self.w/5),
                            int(self.h/5),
                            13)))
                time.sleep(0.025)
            except:
                pass
    
    def update_vedio_start(self):
        t = Thread(target=self.update_vedio)
        t.start()

    def update_time(self):
        global moment1
        self.ui.moment.setPlainText(str(moment1))

    def update_time_start(self):
        global moment1
        def updatetime_thread():
            global moment1
            while 1:
                self.ms.update_time.emit()
                time.sleep(0.2) 
        t = Thread(target=updatetime_thread)
        t.start()

    def drawpoint(self):
        global locations_global
        value = locations_global
        self.ui.webview.page().runJavaScript("test_gxx({0});".format(value)) 
        
    def drawpoint_start(self):
        def drawpoint_thread():
            while 1:
                self.ms.draw_point.emit()
                time.sleep(0.25) 
        t = Thread(target=drawpoint_thread)
        t.start()

    def save_data(self):
        global data_list
        def savedata_thread():
            if os.path.exists(self.ui.wenjian.text()+'.txt'):
                os.remove(self.ui.wenjian.text()+'.txt')
            with open(self.ui.wenjian.text()+'.txt','w') as f:
                for data in data_list:
                    f.write(data+'\n')
                f.close()
            print('ok ok ok')
        t = Thread(target=savedata_thread)
        t.start()
        self.ui.setFixedSize(1874, 1040)
        self.ui.message.append('数据已储存：'+self.ui.wenjian.text()+'.txt')

    def clear_data_list(self):
        global data_list
        data_list = []
        self.ui.message.append('已清空缓存')
    
    
    def collect_data(self):
        global data_list
        global name
        global dva
        global speeds 
        global locations_global 
        global locations_local 
        global headings 
        global moment1
        global suanfa_start

        if 0 in suanfa_start:
            moment1 = 0.0
        else:    
            dictor = {}
            dictor['moment'] = moment1
            dictor['speeds'] = speeds
            dictor['locations_global'] = locations_global
            dictor['locations_local'] = locations_local
            dictor['headings'] = headings
            for data in dva:
                dictor[data] = name[data]
            data_list.append(json.dumps(dictor))
            moment1 = moment1 + 0.2    
    def collect_data_start(self):
        global moment1
 
        def collect_data_thread():
            global moment1
            while 1:
                self.ms.collect_data.emit()
                time.sleep(0.2) 
        t = Thread(target=collect_data_thread)
        t.start()
    

    def set_home_do(self):
        global newSockets
        if (self.ui.home_lat.text()!='') and (self.ui.home_lon.text()!=''):
            message = [1,float(self.ui.home_lat.text()),float(self.ui.home_lon.text())]
            message_json = json.dumps(message,ensure_ascii=False)
            for i in range(len(newSockets)):
                if newSockets[i] != 0:
                    try:
                        newSockets[i].send(message_json.encode("utf-8"))
                        self.ui.message.append(str(i)+'号船设定原点：'+'['+self.ui.home_lat.text()+self.ui.home_lon.text()+']')
                    except:
                        self.ui.message.append(str(i)+'号船设置原点错误')
            self.ui.webview.page().runJavaScript("set_home_new({0});".format([float(self.ui.home_lon.text()),float(self.ui.home_lat.text())]))

    def set_home_do_0(self):
        global newSockets
        global locations_global
        message = [1,locations_global[0][1],locations_global[0][0]]
        message_json = json.dumps(message,ensure_ascii=False)
        for i in range(len(newSockets)):
            if newSockets[i] != 0:
                try:
                    newSockets[i].send(message_json.encode("utf-8"))
                    self.ui.message.append(str(i)+'号船设定原点：'+'['+str(locations_global[0][1])+str(locations_global[0][0])+']')
                except:
                    self.ui.message.append(str(i)+'号船设置原点错误')
        self.ui.webview.page().runJavaScript("set_home_new({0});".format([locations_global[0][0],locations_global[0][1]]))
    
    def clear_line(self):
        self.ui.webview.page().runJavaScript("clearline();")

    def set_mode_all(self,mode):
        global newSockets
        message = [2,mode]
        message_json = json.dumps(message)
        for i in range(len(newSockets)):
            if newSockets[i] != 0:
                try:
                    newSockets[i].send(message_json.encode("utf-8"))
                    self.ui.message.append(str(i)+'号船设置模式：'+mode)
                except:
                    self.ui.message.append(str(i)+'号船设置模式失败')

def recv_message(newSocket,clientAddr):
    global name
    global vehicle_num
    global pa
    global dva
    global sva
    num = clientAddr[1]-9990
    while 1:
        try:
            recvData = newSocket.recv(2048)
            recvData = json.loads(recvData.decode("UTF-8"),strict=False)
        except:
            continue
        if recvData[0]==1:
            speeds[num] = float(recvData[1])
            locations_global[num][0] = float(recvData[2][0])
            locations_global[num][1] = float(recvData[2][1])
            headings[num] = float(recvData[3])
            locations_local[num][0] = float(recvData[4][0])
            locations_local[num][1] = float(recvData[4][1])
            modes[num] = recvData[5]
            suanfa_start[num] = recvData[6]
            #battery[num] = recvData[7]
        if recvData[0]==2:
            for nam in pa:
                name[nam][num] = recvData[1][nam]
            for nam in dva:
                name[nam][num] = recvData[2][nam]
            for nam in sva:
                name[nam][num] = recvData[3][nam]
def send_message(newSocket,clientAddr):
    global name
    global vehicle_num
    global pa
    global dva
    global sva
    
    thread_r = Thread(target=recv_message,args=(newSocket,clientAddr))
    thread_r.setDaemon(True)
    thread_r.start()
    
    while 1:
        #start将要传输的信息进行打包，编号为4
        try:
            packege = {}
            for nam in sva:
                packege[nam+'s'] = name[nam]
            message = [4,packege]
            #end打包
            sendData_json = json.dumps(message,ensure_ascii=False)
            newSocket.send(sendData_json.encode())
            time.sleep(0.1)
        except:
            break
def build_variables(newSocket,clientAddr):
    global name
    global vehicle_num
    global pa
    global dva
    global sva
    while 1:
        try:
            recvData = newSocket.recv(2048)
            recvData = json.loads(recvData.decode("UTF-8"),strict=False)
        except:
            continue
        if recvData[0]==2:
            pa = list(recvData[1].keys())
            pa.sort()
            dva = list(recvData[2].keys())
            dva.sort()
            sva = list(recvData[3].keys())
            sva.sort()
            for i in pa:
                name[i] = []
            for i in dva:
                name[i] = []
            for i in sva:
                name[i] = []
            for i in range(vehicle_num):    
                for j in pa:
                    if len(name[j])<vehicle_num:
                        name[j].append(0.0)
                for j in dva:
                    if len(name[j])<vehicle_num:
                        name[j].append(0.0)
                for j in sva:
                    if len(name[j])<vehicle_num:
                        name[j].append(0.0)
        else:
            continue
        break
def wait_connection():
    global newSockets
    global vehicle_num
    global is_variables
    global ip

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip, 10000))
    serverSocket.listen(100)#vehicle_num

    for i in range(100):#vehicle_num
        newSocket, clientAddr = serverSocket.accept()
        if is_variables:
            is_variables = 0
            build_variables(newSocket,clientAddr)
        num = clientAddr[1]-9990
        newSockets[num] = newSocket
        print(clientAddr,"has connected")
        '''
        thread = Thread(target=recv_message,args=(newSocket,clientAddr))
        thread.start()
        '''
        thread = Thread(target=send_message,args=(newSocket,clientAddr))
        thread.start()
    print("all vehicles clear !")

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    vehicle_num = 0
    ip = ''
    vedio_ip = ''

    app0 = QApplication([])
    num_ask = Asknum()
    num_ask.show()
    app0.exec_()
    
    speeds = []
    locations_global = []
    locations_local = []
    headings = []
    modes = []
    suanfa_start = []
    battery = []
    newSockets = []

    name = locals()
    pa = []
    dva = []
    sva = []
    data_list = []
    is_variables = 1
    no_pa = 1
    no_pa1 = 1
    vedio_mark = 1
    moment1 = 0.0
    for num in range(vehicle_num):
        speeds.append(0.0)
        locations_global.append([0.0,0.0])
        locations_local.append([0.0,0.0])
        headings.append(0.0)
        newSockets.append(0.0)
        modes.append('none')
        suanfa_start.append(0)
        battery.append(0.0)

    thread = Thread(target=wait_connection)
    thread.start()
    
    app1 = QApplication([])
    mainw = MainWindow()
    mainw.show()
    subwindow = SubWindow()
    subwindow_p = SubWindow_p()
    goto = Goto()
    mainw.ui.zhuangtai.clicked.connect(subwindow.OPEN)
    mainw.ui.piliang.clicked.connect(subwindow_p.OPEN)
    mainw.ui.goto_multi.clicked.connect(goto.OPEN)
    app1.exec_()

    print("lsn&gxx")
    sys.exit()

   