import mysql.connector
from datetime import datetime

def conectar(host, user, senha, banco):
    return mysql.connector.connect(host=host, user=user, password=senha, database=banco)

conn = conectar("localhost", "root", "Bruno30042003", "armaz_placas")

c = conn.cursor()

def inserir_placa(placa):
    data_hora = datetime.now()
    c.execute("INSERT INTO placas (placa, data_hora_acesso) VALUES (%s, %s)", (placa, data_hora))
    conn.commit()
    print("Placa inserida com sucesso!")

def listar_placas():
    c.execute("SELECT * FROM placas")
    placas = c.fetchall()
    print("Placas armazenadas:")
    for placa in placas:
        print(placa)

inserir_placa("BCC207Z")
inserir_placa("AVF880I")

listar_placas()

c.close()
conn.close()
