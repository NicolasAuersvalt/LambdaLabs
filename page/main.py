import streamlit as st
import json
import os

text_path = os.path.join('assets', 'textos', 'main.json')

# Carregar os dados do arquivo JSON
with open(text_path, 'r', encoding='utf-8') as f:
    dados = json.load(f)

def inicio():
    
    # Exibir uma imagem a partir de um arquivo local
    imagem_path = "assets/coordenada.PNG"  # Substitua pelo caminho da sua imagem
    imagem_path2 = "assets/LambdaLabs.png"

    st.title("Bem-vindo ao Laboratório Lambda")

    st.image(imagem_path2, width=400)
    
    # Exibir mensagem inicial
    st.write(dados['mensagem_inicial'])
    st.markdown("---")

        # Exibir dados do Pesquisador Principal
    st.write("**Pesquisador Principal: {}**".format(dados['pesquisador_principal']))
    st.write("- Mentor: {}".format(dados['mentor_principal']))
    st.write("- Projetos: {}".format(dados['projetos_principal']))
    st.markdown("LinkedIn: [{}]({})".format(dados['pesquisador_principal'], dados['linkedin_principal']))
    st.markdown("Portfólio: [{}]({})".format(dados['pesquisador_principal'], dados['portfolio_principal']))
    st.markdown("---")

    # Exibir dados do Pesquisador Associado
    st.write("**Pesquisador Associado: {}**".format(dados['pesquisador_associado']['nome']))
    st.write("- Mentor: {}".format(dados['pesquisador_associado']['mentor']))
    st.write("- Projetos: {}".format(dados['pesquisador_associado']['projetos']))
    st.markdown("LinkedIn: [{}]({})".format(dados['pesquisador_associado']['nome'], dados['pesquisador_associado']['linkedin']))
    st.markdown("---")

    # Exibir dados do Pesquisador Assistente
    st.write("**Pesquisador Assistente: {}**".format(dados['pesquisador_assistente']['nome']))
    st.write("- Mentor: {}".format(dados['pesquisador_assistente']['mentor']))
    st.write("- Projetos: {}".format(dados['pesquisador_assistente']['projetos']))
    st.markdown("---")

    # Exibir dados do Revisor
    st.write("**Revisor: {}**".format(dados['revisor']))
    st.markdown("---")

    st.subheader("Grafos")
    st.write(dados['Grafos'])

    st.markdown("---")
    st.subheader("Computação Gráfica")
    st.write(dados['Grafica'])
    

    st.image(imagem_path, caption="Conversão para Polar", width=400)

    st.write(dados['Grafica2'])

    st.markdown("---")

    st.subheader("Criptografia (Cifra de Hill de ordem N)")

    st.write(dados['Criptografia'])