from header import *

def cifra():
    st.title("Cifra de Hill")

    # Receber o grau
    grau = st.number_input("Digite o Grau:", min_value=1, step=1)

    # Receber a matriz de transformação (CHAVE) como texto
    matriz_input = st.text_area("Digite a Matriz Codificadora (linha por linha, separados por espaços):")
    
    # Processar a entrada da matriz
    if matriz_input:
        matT = []
        linhas = matriz_input.strip().split('\n')
        for linha in linhas:
            matT.append(list(map(int, linha.split())))
        
        matT = np.array(matT)

        if matT.shape != (grau, grau):
            st.error("A matriz deve ser de dimensão {}x{}.".format(grau, grau))
            return

        # Receber a senha
        senha = st.text_area("Digite a String (letras e espaços serão removidos):")

        # Remover espaços da string
        senhaSemEspacos = ''.join(c for c in senha.upper() if c.isalpha())

        # Analisar o Resto
        tamSenha = len(senhaSemEspacos)
        resto = tamSenha % grau

        # Se não for divisível, preenche com o último caractere
        if resto != 0:
            ultimo = senhaSemEspacos[-1]
            senhaSemEspacos += ultimo * (grau - resto)

        criptografado = []

        # Percorrer todos os agrupamentos
        for i in range(0, len(senhaSemEspacos), grau):
            agrupamento = [(ord(senhaSemEspacos[i + j]) - ord('A') + 1) for j in range(grau)]

            # Produto da matriz com vetor agrupamento
            for m in range(grau):
                produto = sum(matT[m][n] * agrupamento[n] for n in range(grau))
                produto = produto % 26 
                if produto == 0: produto = 26 
                criptografado.append(produto) 

        # Exibir o resultado criptografado
        st.subheader("Resultado Criptografado:")
        resultado = ''.join(chr(c + ord('A') - 1) for c in criptografado)
        st.write(resultado)