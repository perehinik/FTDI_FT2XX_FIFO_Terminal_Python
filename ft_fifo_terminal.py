# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:56:48 2020

@author: Ivan Perehiniak
"""
from __future__ import print_function
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time
import random
import threading
import atexit
import ftd2xx

BLOCK_LEN = 2048 * 32

RxTimerState = 0
deviceIndex = -1
dev = None
rx_buffer = bytearray()

top = Tk()
top.geometry("700x700")

top1 = Frame(top, height = 700, width = 200, borderwidth=2)
top2 = Frame(top, height = 700, width = 700, borderwidth=2)
top1.grid(column = 0, row = 0)
top2.grid(column = 1, row = 0)

topText = Frame(top2, height = 100, width = 700, borderwidth=2)
bottomText = Frame(top2, height = 600, width = 700, borderwidth=2)
topText.grid(column = 0, row = 0)
bottomText.grid(column = 0, row = 1)

TB1 = Text(topText, width = 60,height = 8)
TB1.pack(side="top")

TB2 = Text(bottomText, width = 58,height = 32)
ybar = Scrollbar(bottomText, orient="vertical", command=TB2.yview)
ybar.pack(side="right", fill="y")
TB2.pack(side="right", fill="both", expand=1)
TB2.config(yscroll= ybar.set)

L1var = StringVar()
L1 = Label(top1, textvariable=L1var)
L1var.set("Filter:")
L1.place(x = 30,y = 70)

L2var = StringVar()
L2 = Label(top1, textvariable=L2var)
L2var.set("S/N:")
L2.place(x = 30,y = 90)

L3var = StringVar()
L3 = Label(top1, textvariable=L3var)
L3var.set("Discription:")
L3.place(x = 30,y = 110)

STB1var = StringVar()
STB1 = Entry(top1, width=11,textvariable = STB1var)
STB1.place(x = 100,y = 90)

STB2var = StringVar()
STB2 = Entry(top1, width=11,textvariable = STB2var)
STB2.place(x = 100,y = 110)

def init():
 global deviceIndex
 #Get the device list and save the index of logic analiser into deviceIndex
 deviceList = ftd2xx.listDevices(0) # returns the list of ftdi devices S/Ns 
 deviceIndex = -1;
 status = -1;
 if deviceList : 
     print(len(deviceList), 'ftdi devices found')
     TB2.insert(END, '%d FTDI devices found\r\n'%len(deviceList))
     for x in range(0,len(deviceList)):
         #print(ftd2xx.getDeviceInfoDetail(x))
         if (STB1var.get() in str(ftd2xx.getDeviceInfoDetail(x)['serial']) or STB1var.get() is None) and (STB2var.get() in str(ftd2xx.getDeviceInfoDetail(x)['description']) or STB2var.get() is None) :
             TB2.insert(END,"Device %d details: \r\n"%x)
             TB2.insert(END,'-------------------------------------------------\r\n')
             TB2.insert(END,"Serial : " + str(ftd2xx.getDeviceInfoDetail(x)['serial'])+'\r\n')
             TB2.insert(END,"Type : "  + str(ftd2xx.getDeviceInfoDetail(x)['type'])+'\r\n')
             TB2.insert(END,"ID : " + str(ftd2xx.getDeviceInfoDetail(x)['id'])+'\r\n')
             TB2.insert(END,"Description : " + str(ftd2xx.getDeviceInfoDetail(x)['description'])+'\r\n')
             TB2.insert(END,'-------------------------------------------------\r\n')
             TB2.see("end")
             
             if deviceIndex < 0:
                 deviceIndex = x
             break
 else:
     TB2.insert(END, "no ftdi devices connected\r\n")
     TB2.see("end")
     print("no ftdi devices connected\r\n")
     
def connect():
 global deviceIndex
 global dev
 if deviceIndex >= 0 :
     print('Connecting to device with index %d \r\n'% deviceIndex)
     TB2.insert(END, 'Connecting to device with index %d \r\n'% deviceIndex)
     TB2.see("end")
     dev = ftd2xx.open(deviceIndex) #FT4HNA7Z
     status = 1
     #print(dev.getDeviceInfo())
     #time.sleep(0.1)
     #dev.setTimeouts(5000, 5000)
     #time.sleep(0.1)
     #dev.setBitMode(0x00, 0x00)
     time.sleep(0.1)
     dev.setBitMode(0x00, 0x40)
     #time.sleep(0.1)
     #dev.setUSBParameters(0x10000, 0x10000)
     #time.sleep(0.1)
     #dev.setLatencyTimer(2)
     #time.sleep(0.1)
     #dev.setFlowControl(ftd2xx.defines.FLOW_RTS_CTS, 0, 0)
     #time.sleep(0.1)
     #dev.purge(ftd2xx.defines.PURGE_RX)
     #time.sleep(0.1)
     #dev.purge(ftd2xx.defines.PURGE_TX)
     #time.sleep(0.1)
     
     print('Device connected \r\n')
     TB2.insert(END, "Device connected \r\n")
     TB2.see("end")
     
     #TB2.insert(END,"\nDevice Details :")
     #TB2.insert(END,"Serial : " , dev.getDeviceInfo()['serial'])
     #TB2.insert(END,"Type : " , dev.getDeviceInfo()['type'])
     #TB2.insert(END,"ID : " , dev.getDeviceInfo()['id'])
     #TB2.insert(END,"Description : " , dev.getDeviceInfo()['description'])
   
 elif ftd2xx.listDevices(0):
     TB2.insert(END, "no FTDI devices to be connected\r\n")
     TB2.see("end")
     print("no FTDI devices to be connected")


def disconnect():
    global dev
    dev.close()
    TB2.insert(END, "Device disconnected\r\n")
    TB2.see("end")

def send():
    global TB1var
    global dev
    tx_data = TB1.get('1.0','end-1c')
    tx_data += tx_data
    b=bytearray()
    b.extend(map(ord,tx_data))
    if len(tx_data)>0 :
        TB2.insert(END, "\r\nSending %d bytes:\r\n"%len(tx_data))
        TB2.insert(END,'-------------------------------------------------\r\n')
        TB2.insert(END,tx_data)
        TB2.insert(END,'\r\n')
        TB2.insert(END,'-------------------------------------------------\r\n')
        TB2.see("end")
        written = dev.write(tx_data)
    else :
        TB2.insert(END, "Please enter data into a top text field\r\n")
        TB2.see("end")


def read():
    global dev
    global rx_buffer
    rx_buffer = bytearray()
    while dev.getQueueStatus()>0 :

         rx_buffer += rx_data
    if len(rx_buffer)>0 :
        TB2.insert(END, "\r\nReceived %d bytes:\r\n"%len(rx_buffer))
        TB2.insert(END,'-------------------------------------------------\r\n')
        TB2.insert(END,rx_buffer.decode("utf-8") )
        TB2.insert(END,'\r\n')
        TB2.insert(END,'-------------------------------------------------\r\n')
        TB2.see("end")


def timerHandler(): # must be after ftdi functions, before buttons callback
    read()
    if RxTimerState > 0 :
        timer1 = threading.Timer(0.2, timerHandler).start()
 
def exit_handler():
    disconnect()
    print('Bye! :)')

def scanCallBack():
    global dev
    init()

def connectCallBack():
    connect()
   
def disconnectCallBack():
    disconnect()

def sendCallBack():
    send()
   
def receivingCallBack():
    global RxTimerState
    if RxTimerState > 0 :
        RxTimerState = 0
        B4.configure(bg = "grey")
    else :
        RxTimerState = 1
        B4.configure(bg = "green")
    timerHandler()

def clearCallBack():
   TB2.delete('1.0',END)
   
B = Button(top1, text = "Scan",height=2, width=19, command = scanCallBack)
B.place(x = 30,y = 20)

B1 = Button(top1, text = "Connect",height=2, width=19, command = connectCallBack)
B1.place(x = 30,y = 150)

B2 = Button(top1, text = "Disconnect",height=2, width=19, command = disconnectCallBack)
B2.place(x = 30,y = 210)

B3 = Button(top1, text = "Send",height=2, width=19, command = sendCallBack)
B3.place(x = 30,y = 270)

B4 = Button(top1, text = "Receiving",height=2, width=19, command = receivingCallBack)
B4.place(x = 30,y = 330)

B5 = Button(top1, text = "Clear",height=2, width=19, command = clearCallBack)
B5.place(x = 30,y = 430)


atexit.register(exit_handler)
top.mainloop()