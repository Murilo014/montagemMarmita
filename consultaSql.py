import psycopg2

def conexao_banco():
    pgconn = psycopg2.connect(
        host = 'localhost',
        user = 'admin',
        password = 'admin',
        database = 'bdmarmitas'
    )
    return pgconn

