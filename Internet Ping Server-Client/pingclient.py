from socket import *
import datetime
import time
import random

def main():
    serverName = '10.0.0.2'
    port = 2018
    Csocket = socket(AF_INET, SOCK_DGRAM)
    data = 'ping'
    #data = input("Enter a message in lowercase")

    LastPing = 10
    count = 0
    Csocket.settimeout(1)
    #print ("Attempting to send " , count , "messages" )

    while count  < LastPing:
        count = count + 1
        startTime = time.time()
        print(data,count,startTime)
        Csocket.sendto(data, (serverName, port))

        try:
            newData, clientAddress = Csocket.recvfrom(1024)
            RTT = ((time.time()) - startTime)
            print ("Message Receieved", newData)
            print ("Trip Time", RTT)
        except timeout:
            print(" Request timed out ")
        except Exception as e:
            print e
    print ("the program is done")
main()