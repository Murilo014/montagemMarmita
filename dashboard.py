import streamlit as st
import pandas as pd
import psycopg2

def conexao_banco():
    pgconn = psycopg2.connect(
        host='localhost',
        user='admin',
        password='admin',
        database='bdmarmitas'
    )
    return pgconn

def adicionar_refeicao(dia, refeicao, ingredientes):
    pgconn = conexao_banco()
    pgcursor = pgconn.cursor()
    pgcursor.execute(
        '''
            INSERT INTO tb_refeicao (dia, refeicao, ingredientes)
            VALUES (%s, %s, %s)
        ''', (dia, refeicao, ingredientes))
    pgconn.commit()
    pgcursor.close()
    pgconn.close()

def buscar_refeicoes():
    pgconn = conexao_banco()
    pgcursor = pgconn.cursor()
    pgcursor.execute("SELECT * FROM tb_refeicao ORDER BY id")
    refeicoes = pgcursor.fetchall()
    pgcursor.close()
    pgconn.close()

    return refeicoes

def excluir_refeicao(id):
    pgconn = conexao_banco()
    pgcursor = pgconn.cursor()
    pgcursor.execute("DELETE FROM tb_refeicao WHERE id = %s", (id))
    pgconn.commit()
    pgcursor.close()
    pgconn.close()

def editar_refeicao(id, dia, refeicao, ingredientes):
    pgconn = conexao_banco()
    pgcursor = pgconn.cursor()
    pgcursor.execute(
    '''
        UPDATE tb_refeicao
        SET dia = %s, refeicao = %s, ingredientes = %s
        WHERE id = %s
    ''', (dia, refeicao, ingredientes, id))
    pgconn.commit()
    pgcursor.close()
    pgconn.close()


st.title('Planejamento de Refeições Semanais')

# Formulário para adicionar novas refeições
st.write('### Adicionar Nova Refeição')
novo_dia = st.text_input('Dia da semana (ex: Segunda-feira):')
nova_refeicao = st.text_input('Refeição (ex: Frango ao MOLHO):')
novos_ingredientes = st.text_input('Ingredientes (ex: Arroz, Feijão):')

if st.button('Adicionar Refeição'):
    if novo_dia and nova_refeicao and novos_ingredientes:
        adicionar_refeicao(novo_dia, nova_refeicao, novos_ingredientes)
        st.success('Refeição adicionada com sucesso!')
    else:
        st.error('Por favor, preencha todos os campos.')

#Exibir todas as refeições cadastradas
st.write('### Refeições Cadastradas')
refeicoes = buscar_refeicoes()
if refeicoes:
    for refeicao in refeicoes:
        st.write(f"**ID:** {refeicao[0]}")
        st.write(f"**Dia:** {refeicao[1]}")
        st.write(f"**Refeição:** {refeicao[2]}")
        st.write(f"**Ingredientes:** {refeicao[3]}")

        # Botão para excluir a refeição
        if st.button(f"Excluir Ref. {refeicao[0]}"):
            excluir_refeicao(refeicao[0])
            st.success(f"Refeição {refeicao[0]} Excluida com sucesso!")
            st.experimental_rerun() # Atualiza a página para refletir a exclusão
        
        # Formulário para editar a refeição
        with st.expander(f"Editar Ref. {refeicao[0]}"):
            edit_dia = st.text_input('Dia da semana:', value=refeicao[1], key=f"dia_{refeicao[0]}")
            edit_refeicao = st.text_input('Refeição:', value=refeicao[2], key=f"refeicao_{refeicao[0]}")
            edit_ingredientes = st.text_input('Ingredientes:', value=refeicao[3], key=f"ingredientes_{refeicao[0]}")

            if st.button(f"Salvar Edição Ref. {refeicao[0]}"):
                editar_refeicao(refeicao[0], edit_dia, edit_refeicao, edit_ingredientes)
                st.success(f"Refeição {refeicao[0]} atualizada com sucesso!")
                st.experimental_rerun() 
        st.write("---") 
else:
    st.write('Nenhuma refeição cadastrada ainda.')

# Filtro por dia da semana
st.write('### Filtrar por Dia da Semana')
dias = list(set([refeicao[1] for refeicao in refeicoes])) # Extrair os dias unicos
dia_selecionados = st.selectbox('Selecione o dia:', dias)

# Exibir refeições do dia selecionado
refeicoes_dia = [refeicao for refeicao in refeicoes if refeicao[1] == dia_selecionados]
if refeicoes_dia:
    st.write(f'### Refeições de {dia_selecionados}')
    for refeicao in refeicoes_dia:
        st.write(f"**Refeição:**{refeicao[2]}")
        st.write(f"**Ingredientes:**{refeicao[3]}")
    st.write("---")
else:
    st.write(f'Nenhuma refeição cadastradas para {dia_selecionados}.')
