# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:17:44 2023

@author: wLeon
"""
import win32com.client as win32
import smtplib
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import time
import paho.mqtt.client as paho
from paho import mqtt
from datetime import datetime
import subprocess
import os
import pandas as pd
import pyodbc 
import pymssql  

# Configurações para envio de e-mail
EMAIL_RECIPIENT = 'iotcore@yahoo.com'

serverdb = '192.168.1.29' 
database = 'IOT' 
username = 'sa' 
password = 'Wlp23@280@03' 

#Conexao DB SQL Server
conn = pymssql.connect(server=serverdb, user=username, password=password, database=database)  
cursor = conn.cursor()


def alarme():
    # Obtenha o valor máximo do buffer
    valor_maximo = max(buffer)

    # Obtenha a hora atual (você precisa importar o módulo datetime)
    hora_ocorrencia = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Envie um e-mail com o valor máximo e a hora de ocorrência
    enviar_email(f'⚠ ALARME IOT CORE! Valor máximo de desbalanceamento de fase lido: {valor_maximo}. Ocorreu às: {hora_ocorrencia}', 
                 '''
1) Verifique a fonte de alimentação: Verifique se a rede elétrica está fornecendo uma tensão equilibrada nas três fases. Verifique a tensão de linha e a tensão de fase em cada fase usando um voltímetro adequado. Se houver uma diferença significativa nas tensões de fase, entre em contato com a companhia de energia elétrica para solucionar o problema.

2) Verifique a conexão do motor: Verifique as conexões elétricas do motor e certifique-se de que estão corretas. Verifique se não há fios soltos ou conexões defeituosas. Um problema de conexão incorreta pode levar ao desbalanceamento de fase.

3) Verifique os componentes do sistema: Verifique os componentes do sistema, como contatores, relés de sobrecarga e dispositivos de proteção térmica. Certifique-se de que estão funcionando corretamente e não estão causando desequilíbrio nas correntes trifásicas.

4) Verifique o motor: Se todas as outras possibilidades forem descartadas e o desbalanceamento de fase persistir, pode haver um problema interno no motor. Nesse caso, é recomendado entrar em contato com um técnico especializado em motores elétricos para fazer uma análise mais detalhada e realizar as medidas corretivas necessárias.
                 '''
                 )
  
    # Print log
    print(f'alarm with {valor_maximo} imbalance at {hora_ocorrencia}')

def enviar_email(assunto, mensagem):
    # Criar objeto do Outlook
    outlook = win32.Dispatch('Outlook.Application')
    # Criar e-mail
    email = outlook.CreateItem(0)
    email.Subject = assunto
    email.Body = mensagem
    email.To = EMAIL_RECIPIENT
    # Enviar e-mail
    email.Send()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global buffer  # Declarar a variável buffer como global
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    if msg.topic == "esp32/imbalance_est_kf":
        valor = float(msg.payload.decode())

        # Adicionar valor ao buffer
        buffer.append(valor)

        # Verificar se o buffer atingiu o limite de 1800
        if len(buffer) >= 1800:
            print('verificando anomalias ...')
            # Verificar se existem valores acima de 30% no buffer
            if any(valor > 30 for valor in buffer):
                # Chamar a função de alarme
                alarme()
                # Salva o valor no banco de dados
                query = 'INSERT INTO ALARMS (topic_, value_, time_) VALUES (%s, %s, %s)'
                val = (str(msg.topic), valor, current_time)
                cursor.execute(query,val)
                conn.commit()
                print('alarm saved in database!')
            else:
                print('nenhuma anomalia encontrada!')

            # Zerar o buffer
            buffer = []
        
# Variável de buffer
buffer = []
    
client = paho.Client(client_id="python_alarms", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.username_pw_set("", "")
client.connect("192.168.1.100", 1883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.subscribe("esp32/#", qos=0)
client.loop_forever()