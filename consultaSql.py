import psycopg2

def conexao_banco():
    """Conecta ao banco de dados."""
    try:
        pgconn = psycopg2.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='bdmarmitas'
        )
        return pgconn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def fechar_conexao(pgconn, pgcursor):
    """Fecha a conexão e o cursor do banco de dados."""
    if pgcursor:
        pgcursor.close()
    if pgconn:
        pgconn.close()

def cadastro_refeicao(dia, nome_refeicao, ingredientes, porcoes):
    """Insere uma nova refeição e associa os tipos de porção."""
    pgconn = conexao_banco()
    if pgconn:
        try:
            pgcursor = pgconn.cursor()

            # Inserir na tabela tb_refeicao (sem especificar o ID)
            query_refeicao = """
                INSERT INTO tb_refeicao (dia, refeicao, ingredientes)
                VALUES (%s, %s, %s)
                RETURNING id
            """
            pgcursor.execute(query_refeicao, (dia, nome_refeicao, ingredientes))
            id_refeicao = pgcursor.fetchone()[0]  # Obtém o ID gerado automaticamente

            # Inserir na tabela intermediária tb_refeicao_porcao
            for id_porcao in porcoes:
                query_refeicao_porcao = """
                    INSERT INTO tb_refeicao_porcao (id_refeicao, id_porcao)
                    VALUES (%s, %s)
                """
                pgcursor.execute(query_refeicao_porcao, (id_refeicao, id_porcao))

            pgconn.commit()
        except Exception as e:
            print(f"Erro ao inserir refeições: {e}")
            return False
        finally:
            fechar_conexao(pgconn, pgcursor)
        return True
    return False

def listar_refeicao():
    """Lista todas as refeições cadastradas com seus tipos de porção."""
    pgconn = conexao_banco()
    if pgconn:
        try:
            pgcursor = pgconn.cursor()

            # Consulta principal para obter refeições
            query_refeicao = """
                SELECT r.id, r.dia, r.refeicao, r.ingredientes
                FROM tb_refeicao r
            """
            pgcursor.execute(query_refeicao)
            refeicoes = pgcursor.fetchall()

            # Consulta para obter os tipos de porção associados a cada refeição
            query_porcoes = """
                SELECT rp.id_refeicao, p.porcao
                FROM tb_refeicao_porcao rp
                JOIN tb_porcao p ON rp.id_porcao = p.id
            """
            pgcursor.execute(query_porcoes)
            porcoes_refeicoes = pgcursor.fetchall()

            # Organizar os dados
            resultado = []
            for refeicao in refeicoes:
                id_refeicao, dia, nome_refeicao, ingredientes = refeicao
                tipos_refeicao = [
                    porcao for id_r, porcao in porcoes_refeicoes if id_r == id_refeicao
                ]
                resultado.append((id_refeicao, dia, nome_refeicao, ingredientes, ", ".join(tipos_refeicao)))

        except Exception as e:
            print(f"Erro ao listar as refeições: {e}")
            return []
        finally:
            fechar_conexao(pgconn, pgcursor)
        return resultado
    return []

def obter_porcoes():
    """Lista todos os tipos de porção cadastrados."""
    pgconn = conexao_banco()
    if pgconn:
        try:
            pgcursor = pgconn.cursor()
            query = "SELECT id, porcao FROM tb_porcao"
            pgcursor.execute(query)
            porcoes = pgcursor.fetchall()
        except Exception as e:
            print(f"Erro ao obter porções: {e}")
            return []
        finally:
            fechar_conexao(pgconn, pgcursor)
        return porcoes
    return []