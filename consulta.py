import mysql.connector

def criar_conexao(host, user, senha, banco):
    return mysql.connector.connect(host=host, user=user, password=senha, database=banco)

conn = criar_conexao("localhost", "root", "Bruno30042003", "armaz_placas")

def fechar_conexao(con):
    return con.close()