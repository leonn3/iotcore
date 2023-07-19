# -*- coding: utf-8 -*-
"""
Created on Wed May 31 18:06:44 2023

@author: Woldson Leonne
"""
import time
import pyodbc
from influxdb_client import InfluxDBClient
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações do SQL Server
serverdb = '192.168.1.29'
database = 'IOT'
username = 'sa'
password = ''

# Configurações do InfluxDB
token = "A2XVvXFY5l2iA=="
org = "UFPA"
bucket = "IOT"
url = "http://localhost:8086"

# Parâmetros para o intervalo de amostras
inicio = 10
intervalo = 200000
final = 10000000  # Para 10 milhões de amostras

# Criar lista de números de amostras
num_samples = list(range(inicio, final + 1, intervalo))

# Tempo de consulta para o SQL Server
sql_server_query_times = []

# Tempo de consulta para o InfluxDB
influxdb_query_times = []

# Conectar ao SQL Server
sql_server_connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + serverdb + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# Conectar ao InfluxDB
influxdb_client = InfluxDBClient(url=url, token=token)

# Executar consultas para cada número de amostra
for num in num_samples:
    # Consulta no SQL Server
    sql_server_start_time = time.time()
    sql_server_cursor = sql_server_connection.cursor()
    sql_server_cursor.execute(f'SELECT TOP {num} * FROM IOT')
    sql_server_rows = sql_server_cursor.fetchall()
    sql_server_query_times.append(time.time() - sql_server_start_time)

    # Consulta no InfluxDB
    influxdb_start_time = time.time()
    query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "esp32/imbalance") |> limit(n: {num})'
    tables = influxdb_client.query_api().query(org=org, query=query)
    influxdb_query_times.append(time.time() - influxdb_start_time)

    print(num)

# Configurações de estilo e cores
sns.set(style='whitegrid')
palette = sns.color_palette('husl', 2)

# Criar a figura e os eixos
fig, ax = plt.subplots(figsize=(8, 6), dpi=120)

# Plotar o gráfico
ax.plot(num_samples, sql_server_query_times, label='SQL Server', color=palette[0])
ax.plot(num_samples, influxdb_query_times, label='InfluxDB', color=palette[1])

# Personalizar o gráfico
ax.set_xlabel('Número de Amostras')
ax.set_ylabel('Tempo de Consulta (segundos)')
ax.set_title('Comparação de Velocidade de Consulta')
ax.legend()

# Ajustar o layout
plt.tight_layout()

# Exibir o gráfico
plt.show()
