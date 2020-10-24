import serial,os
import requests

ser = serial.Serial('COM3', 9600)



while(1):
    Setpoint = int(ser.readline())
    if Setpoint>0:
        print(Setpoint)
        url="https://c213-control.herokuapp.com/control/?Modo=PID&A1=0.9930900&B1=0.0058096&Amostragem=0.3&SetPoint=sp&Overshoot=15&tempo=60&Proporcional=1&Integral=0.04&Derivativo=0&k=1&tal=1&fixed_scale=1"
        #url="http://127.0.0.1:5000//control/?Modo=PID&A1=0.9930900&B1=0.0058096&Amostragem=0.3&SetPoint=sp&Overshoot=15&tempo=60&Proporcional=1&Integral=0.04&Derivativo=0&k=1&tal=1&fixed_scale=1"
        url=url.replace( "sp",str(Setpoint)  )
        res = requests.get(url)
        #print("SetPoint definido:",Setpoint)

#print(int(textoEntrada)*3)
