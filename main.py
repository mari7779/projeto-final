from consulta import criar_conexao, fechar_conexao

def insere_placa(con, id, placa):
    cursor = con.cursor()
    sql = "INSERT INTO armaz_placas (id, placa) values (%s, %s)"
    valores = (id, placa)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()
    
def select_todos_usuarios(con):
    cursor = con.cursor()
    sql = "SELECT id, placa FROM armaz_placas"
    cursor.execute(sql)

    for (id, placa) in cursor:
        print(id, placa)

    cursor.close()

def main():
    con = criar_conexao("localhost", "root", "Bruno30042003", "armaz_placas")
    
    insere_placa(con, "maria", "", "16")
    select_todos_usuarios(con)

    fechar_conexao(con)


if __name__ == "__main__":
    main()