from header import *

# Função para as operações
def pagina_operacoes():
    st.title("Operações com Matrizes com Visualização 3D")

    st.write("""
        Este aplicativo é uma aplicação da Álgebra Linear na computação gráfica.
    """)


    # Menu lateral para escolher a operação
    opcao = st.sidebar.selectbox("Escolha a operação", ("Ampliação", "Translação", "Rotação"))

    # Entrada de texto para a matriz inicial
    matriz_str = st.text_area("Matriz do CUBO (use notação Python, ex: [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])", 
                              "[[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]")

    # Converter a string de entrada para lista
    try:
        matriz = np.array(eval(matriz_str))
    except Exception as e:
        st.error("Erro ao converter a matriz. Verifique a entrada.")

    # Verificar se a matriz é 3xn
    if matriz.ndim != 2 or matriz.shape[1] != 3:
        st.error("A matriz deve ter 3 colunas.")
    else:
        resultado = None
        
        if opcao == "Ampliação":
            resultado = ampliar(matriz)

        elif opcao == "Translação":
            resultado = transladar(matriz)

        elif opcao == "Rotação":
            resultado = rotacionar(matriz)

        if resultado is not None:
            # Plotar o gráfico 3D do resultado
            st.plotly_chart(plot_matriz_3d(resultado))

            # Exibir o resultado
            st.write("Resultado:")
            st.write(resultado)