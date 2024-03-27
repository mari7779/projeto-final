from flask import Flask
import mysql.connector
from datetime import datetime 

app = Flask(__name__)

def conectar(host, user, senha, banco):
    return mysql.connector.connect(host=host, user=user, password=senha, database=banco)

@app.route('/receber_sinal', methods=['GET'])
def receber_sinal():
    placa_recebida = "PLACA-ESP32"  # Substitua pelo dado recebido da ESP32
    conn = conectar("localhost", "root", "Bruno30042003", "armaz_placas")
    c = conn.cursor()
    # Processar o sinal recebido da ESP32
    inserir_placa("PLACA-ESP32", conn, c)  # Coloque a placa correta aqui
    print("Sinal recebido da ESP32!")
    return "Sinal recebido com sucesso!"

def inserir_placa(placa, conn, cursor):
    data_hora = datetime.now()
    cursor.execute("INSERT INTO placas (placa) VALUES (%s, %s)", (placa, data_hora))
    conn.commit()
    print("Placa inserida com sucesso!")

if __name__ == '__main__':
    conn = conectar("localhost", "root", "Bruno30042003", "armaz_placas")
    c = conn.cursor()
    app.run(debug=True)  # Executa o servidor Flask em modo de depuração