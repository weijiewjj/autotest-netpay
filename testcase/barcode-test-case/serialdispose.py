
# import serial
# ser=serial.Serial("/dev/ttyUSB0",9600,timeout=0.5) #使用USB连接串行口
# #ser=serial.Serial("COM1",9600)
# print (ser.name)#打印设备名称
# print(ser.port)#打印设备名
# ser.open() #打开端口
# # s = ser.read(10)#从端口读10个字节
# # ser.write("hello")#向端口写数据
# # ser.close()#关闭端口
# data=''
# while serial.inWaiting() > 0:
#     data += serial.read(20)#是读20个字符！
#     print(data)