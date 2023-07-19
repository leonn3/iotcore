# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:17:44 2023

@author: wLeon
"""

from opcua import Server
import time
import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime
import random
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
from influxdb import DataFrameClient
import subprocess
import os
import pandas as pd
import pyodbc 
import pymssql  
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
serverdb = '192.168.1.23' 
database = 'IOT' 
username = 'sa' 
password = 'Wlp23@280@03' 
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+serverdb+';DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = cnxn.cursor()

#Conexao DB SQL Server
conn = pymssql.connect(server=serverdb, user=username, password=password, database=database)  
cursor = conn.cursor()
# cursor.execute('SELECT * FROM dbo.spt_monitor')

#################### OPC UA SERVER SETUP #######################################

server = Server()

url = "opc.tcp://192.168.1.29:4850" #server.stop() -> command for stop server
server.set_endpoint(url)

name = "OPCUA_IOT_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Time = Param.add_variable(addspace, "Time", 0)
Temp = Param.add_variable(addspace, "Temperature",0)
rotX = Param.add_variable(addspace, "RotationX",0)
rotY = Param.add_variable(addspace, "RotationY",0)
rotZ = Param.add_variable(addspace, "RotationZ",0)
accX = Param.add_variable(addspace, "accX",0)
accY = Param.add_variable(addspace, "accY",0)
accZ = Param.add_variable(addspace, "accZ",0)
iR = Param.add_variable(addspace, "iR",0)
iS = Param.add_variable(addspace, "iS",0)
iT = Param.add_variable(addspace, "iT",0)
pR = Param.add_variable(addspace, "pR",0)
pS = Param.add_variable(addspace, "pS",0)
pT = Param.add_variable(addspace, "pT",0)
imbalance = Param.add_variable(addspace, "imbalance",0)
imbalance_kf = Param.add_variable(addspace, "imbalance_est_kf",0)
status = Param.add_variable(addspace, "status",0)
horimetro = Param.add_variable(addspace, "horimetro",0)


Time.set_writable()
Temp.set_writable()
rotX.set_writable()
rotY.set_writable()
rotZ.set_writable()
accX.set_writable()
accY.set_writable()
accZ.set_writable()
iR.set_writable()
iS.set_writable()
iT.set_writable()
pR.set_writable()
pS.set_writable()
pT.set_writable()
imbalance.set_writable()
imbalance_kf.set_writable()
status.set_writable()
horimetro.set_writable()


server.start()
print("Server started at {}".format(url))

#############OffLINE RUN########################################################
#You can generate a Token from the "Tokens Tab" in the UI
token = "A2XxKTpfiKsBqbdNolpd0LrHty2LB2GO6pnmJZqC2GKzihJlTvPF_YkffhkOSJCuJWhctu7NdTmSVvXFY5l2iA=="
org = "UFPA"
bucket = "IOT"
url_="http://localhost:8086"
hostname = os.popen('hostname -I').read()[0:14]
port_=8086

#############OnLINE RUN########################################################
# token = "tWcz-iDE-UDKAzjBdyhlqtTpXyPO0aaYfA76sYXX8rMN0HV4HAJFqtjg_SwT4rOqAqLRRqyePol-6zfYzspsgg==" #online
# org = "woldson.gomes@albras.net" 
# bucket = "IOT"
# url_ = "https://eastus-1.azure.cloud2.influxdata.com" 
# hostname = os.popen('hostname -I').read()[0:14]
# port_=8086

client_DB = InfluxDBClient(url=url_, token=token)

write_api = client_DB.write_api(write_options=SYNCHRONOUS)


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    if msg.topic != "esp32/horimetro":
        json_body = [
            {
                "measurement": str(msg.topic),
                "tags": {
                    "host": hostname,
                },
                "time": current_time,
                "fields": {
                    "value": float(msg.payload.decode())
                }
            }
        ]
        
        query = 'INSERT INTO IOT (topic_, value_, time_) VALUES (%s, %s, %s)'
        val = (str(msg.topic), float(msg.payload.decode()), current_time)
        cursor.execute(query,val)
        conn.commit()
        print('data saved in database!')
    else:
        json_body = [
            {
                "measurement": str(msg.topic),
                "tags": {
                    "host": hostname,
                },
                "time": current_time,
                "fields": {
                    "value": str(msg.payload.decode())
                }
            }
        ]
        
        query = f'''UPDATE HORIMETRO SET value_ = '{msg.payload.decode()}', time_ = GETDATE() WHERE topic_ = 'esp32/horimetro';'''
        #query = f"UPDATE HORIMETRO SET value_ = '{str(msg.payload.decode())}', time_ = {current_time} WHERE topic_ = 'esp32/horimetro'"
        cursor.execute(query)
        conn.commit()
    
    #print(json_body)
    #print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
    write_api.write(bucket, org, json_body)
    
    
    #Send to OPC UA Server
    Time.set_value(current_time)
    if msg.topic == "esp32/temperature": Temp.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/rotationX": rotX.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/rotationY": rotY.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/rotationZ": rotZ.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/accelerationX": accX.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/accelerationY": accY.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/accelerationZ": accZ.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/current_R": iR.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/current_S": iS.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/current_T": iT.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/watt_R": pR.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/watt_S": pS.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/watt_T": pT.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/imbalance": imbalance.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/imbalance_est_kf": imbalance_kf.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/status": status.set_value(float(msg.payload.decode()))
    if msg.topic == "esp32/horimetro": horimetro.set_value(str(msg.payload.decode()))
    
    #time.sleep(2) #time to refresh Grafana dashboard
        

client = paho.Client(client_id="python_linux", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
#client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("", "")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("192.168.1.100", 1883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("esp32/#", qos=0)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()


# cursor.execute('SELECT * FROM dbo.PyTemp')

# for row in cursor:
#     print(row)
