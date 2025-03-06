from header import *

class Polinomio:
    def __init__(self, input_str):
        self.input = input_str.replace(' ', '')  # Remove espaços
        self.grau = 0
        self.v = []
        self.sinal = []
        self.r = []
        self.acha_grau()
        self.cria_vetor()
        pass

    def mod(self, x):
        return abs(x)

    def sinal_trocado(self, a, b):
        if b >= 0:
            return 0 if a >= 0 else 1
        else:
            return 1 if a >= 0 else 0

    def lim_pos(self):
        if self.grau % 2 and self.sinal[self.grau] == '-':
            return -1.0
        elif self.grau % 2 and self.sinal[self.grau] == '+':
            return +1.0
        elif self.sinal[self.grau] == '+':
            return +1
        else:
            return -1

    def lim_neg(self):
        if self.grau % 2 and self.sinal[self.grau] == '-':
            return +1.0
        elif self.grau % 2 and self.sinal[self.grau] == '+':
            return -1.0
        elif self.sinal[self.grau] == '+':
            return +1
        else:
            return -1

    def acha_grau(self):
        max_grau = 0
        for i in range(len(self.input)):
            if self.input[i] == 'x' and max_grau == 0:
                max_grau = 1
            if self.input[i] == '^':
                max_grau = max(max_grau, int(self.input[i + 1]))

        self.grau = max_grau
        self.v = [0] * (max_grau + 1)
        self.r = [0.0] * max_grau
        self.sinal = ['+'] * (max_grau + 1)

    def cria_vetor(self):
        inf = 0
        chave = 0
        while chave < len(self.input):
            if (self.input[chave] == '+' or self.input[chave] == '-') and chave > 0:
                self.exp = 0
                self.coe = 1
                sup = chave
                for i in range(inf, sup):
                    if self.input[i] == 'x':
                        self.exp = 1
                    if self.input[i] == '^':
                        self.exp = int(self.input[i + 1])
                    if self.input[i] == '*':
                        self.coe = int(self.input[i - 1])

                if self.input[inf] in ['+', '-']:
                    self.sinal[self.exp] = self.input[inf]
                    if self.exp == 0:
                        self.coe = int(self.input[inf + 1])
                else:
                    self.sinal[self.exp] = '+'
                    if self.exp == 0:
                        self.coe = int(self.input[inf])

                inf = sup
                self.v[self.exp] = self.coe

            chave += 1

        # Tratando o último termo após o loop
        if inf < chave:
            self.exp = 0
            self.coe = 1
            for i in range(inf, chave):
                if self.input[i] == 'x':
                    self.exp = 1
                if self.input[i] == '^':
                    self.exp = int(self.input[i + 1])
                if self.input[i] == '*':
                    self.coe = int(self.input[i - 1])

            if self.input[inf] in ['+', '-']:
                self.sinal[self.exp] = self.input[inf]
                if self.exp == 0:
                    self.coe = int(self.input[inf + 1])
            else:
                self.sinal[self.exp] = '+'
                if self.exp == 0:
                    self.coe = int(self.input[inf])

            self.v[self.exp] = self.coe

    def ex(self, base, expoente):
        return base ** expoente

    def valor(self, x):
        total = self.v[0] if self.sinal[0] == '+' else -self.v[0]
        for i in range(1, self.grau + 1):
            total += self.v[i] * self.ex(x, i) if self.sinal[i] == '+' else -self.v[i] * self.ex(x, i)
        return total
    
    def __str__(self):
        """Retorna a representação em string do polinômio."""
        partes = []
        for i in range(self.grau + 1):
            coef = self.v[i]
            if coef == 0:
                continue  # Ignora coeficientes zero
            sinal = self.sinal[i]
            parte = f"{'' if i == 0 else ('+' if sinal == '+' else '-')}{abs(coef)}"
            if i > 0:
                parte += f"*x"
            if i > 1:
                parte += f"^{i}"
            partes.append(parte)
        return ''.join(partes).replace('+-', '-').replace('x^1', 'x')  # Formatação adicional


    def derivada(self):
        d = Polinomio('')
        d.grau = self.grau - 1
        d.v = [0] * (d.grau + 1)
        d.sinal = ['+'] * (d.grau + 1)

        for i in range(d.grau + 1):
            d.v[i] = self.v[i + 1] * (i + 1)
            d.sinal[i] = self.sinal[i + 1]
        return d

    def primitiva(self, x):
        total = 0
        for i in range(self.grau + 1):
            total += (self.v[i] * self.ex(x, i + 1)) / (i + 1) if self.sinal[i] == '+' else -(self.v[i] * self.ex(x, i + 1)) / (i + 1)
        return total

    def area(self, a, b):
        return self.primitiva(b) - self.primitiva(a)

    def soma_Riemman(self, a, b, N):
        dx = (b - a) / N
        totalm = sum(self.valor(a + i * dx) * dx for i in range(N))
        totalM = sum(self.valor(a + (i + 1) * dx) * dx for i in range(N))
        total_medio = sum(self.valor(a + (i + 0.5) * dx) * dx for i in range(N))
        
        return totalm, totalM, total_medio

    def aprox(self, x):
        D = [1.0, 0.5, 0.1]
        der1 = self.derivada()
        der2 = der1.derivada()

        results = {}
        results["P(x)"] = self.valor(x)

        for d in D:
            linear = self.valor(x - d) + der1.valor(x - d) * d
            quadratica = (self.valor(x - d) +
                          der1.valor(x - d) * d +
                          der2.valor(x - d) * d**2 / 2)
            results[f'Aproximação linear com d={d}'] = linear
            results[f'Aproximação quadrática com d={d}'] = quadratica
        
        return results

def inicio():
    
    # Exibir uma imagem a partir de um arquivo local
    imagem_path = "imagem/coordenada.PNG"  # Substitua pelo caminho da sua imagem
    imagem_path2 = "imagem/LambdaLabs.png"

    st.title("Bem-vindo ao Laboratório Lambda")

    st.image(imagem_path2, width=400)
    
    st.write("Aqui serão desenvolvidos alguns projetos, fique à vontade para testar!")
    st.markdown("---")
    st.write("""
    **Pesquisador Principal: Nícolas Auersvalt Marques**\n
    - Mentor: Alan Turing
    - Projetos: Laboratório Lambda (Website StreamLit), Computação Gráfica, Grafos, Criptografia, Polinômios (assistência)
    """)
    st.markdown("[LinkedIn](https://www.linkedin.com/in/nicolas-auersvalt/)" " " "[Portfólio](https://linktr.ee/auersvalt)") 
    st.markdown("---")
    st.write("""
    **Pesquisador Associado: Gabriel Lazari Trevisani**
    - Mentor: Leonhard Euler
    - Projetos: Polinômios
    """)
    st.markdown("[LinkedIn](https://www.linkedin.com/in/gabriel-trevisani-a811131b5/)")
    st.markdown("---")
    st.write("""
    **Pesquisador Assistente: Pedro Eugenio Marin Do Nascimento**
    - Mentor: Robert Oppenheimer
    - Projetos: Grafos (assistência), Criptografia (assistência)
    """)

    st.markdown("---")
    st.write("""
    **Revisor: Guilherme de Souza Carneiro Garcia**
    """)
    st.markdown("---")
    

    st.subheader("Grafos")
    st.write("""
    Esta aplicação é baseada em álgebra linear, utilizando uma matriz de adjacência para representar vértices em um grafo. Existem duas aplicações principais que podemos explorar:

    1. **Descobrir o Caminho Mínimo**: Através da matriz de adjacência, podemos determinar quais cidades (ou vértices) têm exatamente um número específico de caminhos até um determinado objetivo. Por exemplo, se quisermos descobrir quais cidades têm exatamente 5 caminhos até um destino específico, este algoritmo pode ser utilizado. Embora existam mais aplicações, essas são as mais notáveis até agora.

    2. **Contar Caminhos em um Grafo**: Para calcular a quantidade de caminhos entre vértices, elevamos a matriz de adjacência (que contém valores 0 ou 1) a uma potência correspondente ao número de caminhos desejado. A matriz resultante nos fornece informações sobre as possíveis rotas entre as cidades. Por exemplo, se elevamos a matriz à décima potência e encontramos o valor `m[1][2]` igual a 5, isso indica que existem 5 caminhos de comprimento 10 entre a cidade 1 e a cidade 2.

    É importante ressaltar que esse algoritmo pode ter um desempenho insatisfatório para matrizes de alta dimensão (N muito grande), uma vez que requer multiplicações de matrizes. Para otimizar a busca do menor caminho, podemos implementar um loop que varia a potência da matriz, parando na primeira ocorrência em que `m[1][2]` é diferente de zero, o que indicaria a existência do caminho mais curto entre as cidades.

    Além disso, se quisermos determinar quantas cidades têm um caminho de comprimento 5, podemos elevar a matriz à quinta potência e verificar quais valores são diferentes de zero. Isso nos permitirá identificar não apenas quais cidades estão acessíveis a partir de um determinado ponto, mas também a quantidade delas.

    Vale a pena mencionar que essa abordagem é mais uma curiosidade da teoria dos grafos e pode não ser frequentemente solicitada em exercícios práticos. Além disso, o algoritmo é aplicável apenas a grafos direcionados.
""")

    st.markdown("---")
    st.subheader("Computação Gráfica")

    st.write("""
        As operações disponíveis incluem:
        - **Ampliação:** Altera o tamanho da matriz.
            - Primeiro, toma-se em uma Matriz Pontos Iniciais (MPI) de dimensão 3 x N, com todos os pontos da figura;
            - Segundo, recebe-se o valor do Coeficiente de Ampliação (CA);
            - Terceiro, cria-se uma Matriz Transformação Linear (MTL), sendo uma matriz diagonal que neste caso será preenchida com CA;
            - Quarto, cria-se uma Matriz Pontos Finais (MPF) de dimensão 3 x N, inicialmente zerada;
            - Quinto, Realiza a operação MPF = MTL + MPI;
            - Sexto, MPF é uma matriz de dimensão 3 x N, então para cada coluna, plota um vértice;
            - **OBS:** 3 x N pois deverá haver 3 linhas (x, y, z), e N pois podem haver diversos pontos. Além disso, deve-se ter como referência quais são os pontos ligantes.

        - **Translação:** Move a matriz em uma direção especificada.
            - Primeiro, toma-se em uma Matriz Pontos Iniciais (MPI) de dimensão 3 x N, com todos os pontos da figura;
            - Segundo, recebe-se uma Matriz Translação (MT), de dimensões 3 x N;
            - Terceiro, cria-se uma Matriz Pontos Finais (MPF) de dimensão 3 x N, inicialmente zerada;
            - Quarto, realiza-se a operação MPF = MPI + MT;
            - Quinto, MPF é uma matriz de dimensão 3 x N, então para cada coluna, plota um vértice;
            - **OBS:** MT pode ser um vetor (x, y, z), então prolongamos para uma matriz 3 x N com todas as colunas sendo (x, y, z).

        - **Rotação:** Rotaciona a matriz em torno dos eixos X, Y ou Z.
            - Primeiro, toma-se em uma Matriz Pontos Iniciais (MPI) de dimensão 3 x N, com todos os pontos da figura;
            - Segundo, recebe-se os ângulos de rotações (a, b, c) em função dos eixos X, Y e Z;
            - Terceiro, cria-se uma Matriz Pontos Finais (MPF) de dimensão 3 x N, inicialmente zerada;
            - Quarto, cria-se uma Matriz Rotação (MR) para cada rotação (MRx, MRy ou MRz);
            - Quinto, é feito a conversão de x, y e z da seguinte forma:
    """)

    st.image(imagem_path, caption="Conversão para Polar", width=400)

    st.write("""
        - **Sexto:** para uma rotação em Z ficaria [[cos(a), -sen(a), 0], [sen(a), cos(a), 0], [0, 0, 1]];
        - **Sétimo:** opera-se MR = MRx * MRy * MRz;
        - **Oitavo:** MR é uma matriz de dimensão 3 x N, então para cada coluna, plota um vértice.
    """)

    st.markdown("---")

    st.subheader("Criptografia (Cifra de Hill de ordem N)")

    st.write("""
        O intuito é codificar uma mensagem e manter a matriz codificadora (chave) para descriptografá-la futuramente.
        - **Cifra de Hill:**
            - Primeiro, recebe-se a ordem (N) da Cifra de Hill, que será a ordem da matriz codificadora.
            - Segundo, recebe-se a Matriz Codificadora NxN (MC) e a mensagem a ser criptografada (sem considerar espaços).
            - Terceiro, agrupam-se as letras em função da ordem desejada (ex.: ordem 2, agrupa pares).
            - Quarto, caso o tamanho da mensagem não seja divisível pela ordem desejada, armazena-se o resto (R) da divisão do tamanho pela ordem.
            - Quinto, repete-se o último elemento da mensagem R vezes (ex.: teste -> testeee).
            - Sexto, converte-se os agrupamentos para os equivalentes do alfabeto (A = 1, B = 2, ...), como em P=[A,B] => P=[1,2].
            - Sétimo, realiza-se o produto de cada agrupamento Pi pela Matriz Codificadora e armazena-se em um vetor C: C = MC * Pi.
            - Oitavo, o vetor C (codificado) é de dimensão 1xN; logo, unem-se todos os vetores codificados e forma-se o código para converter para o alfabeto.
            - OBS: não inserir matriz diagonal na MC e nem matriz nula.
    """)

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


def pagina_grafo():
    
    st.title("Busca de Caminhos em Grafo")

    # Entradas do usuário
    camI = st.number_input("Valor de partida (nó inicial)", min_value=1, step=1)
    camJ = st.number_input("Valor de destino (nó final)", min_value=1, step=1)
    
    # Entrada do grafo
    grafo_input = st.text_area("Insira o grafo (ex: '1 2\\n1 3\\n3 2')", "1 2\n1 3\n3 2\n2 5\n5 6\n6 7\n5 9\n9 7\n2 4\n4 8\n8 11\n8 10\n8 9\n3 10\n4 5")

    # Processar a entrada do grafo
    edges = [list(map(int, line.split())) for line in grafo_input.strip().split('\n')]

    if not edges:
        st.error("Por favor, insira pelo menos uma aresta no grafo.")
        return
    
    # Determinar o tamanho da matriz
    max_node = max(max(edge) for edge in edges)
    len_mat = max_node

    # Inicialização das matrizes
    mat = np.zeros((len_mat + 1, len_mat + 1), dtype=int)
    apoio = np.zeros((len_mat + 1, len_mat + 1), dtype=int)
    final = np.zeros((len_mat + 1, len_mat + 1), dtype=int)

    # Preencher a matriz de adjacência
    for a, b in edges:
        mat[a][b] = 1
        final[a][b] = 1
        apoio[a][b] = 1

    # Verificar se camI e camJ estão dentro dos limites
    if camI > len_mat or camJ > len_mat or camI < 1 or camJ < 1:
        st.error("Os valores de partida e destino devem estar entre 1 e {}".format(len_mat))
        return

    # Variável que controla se o caminho foi encontrado
    achou = True
    tamCaminho = 0

    # Calcula as potências da matriz de adjacência até encontrar um caminho
    for tamCaminho in range(1, len_mat):
        if mat[camI][camJ]:
            achou = False
            break

        # Multiplica as matrizes mat e apoio
        final = np.dot(mat, apoio)

        # Copia a matriz final para a matriz original
        mat = final.copy()

    # Exibir o resultado
    if achou:
        st.error("Não há caminho válido.")
    else:
        st.success(f"O menor número de caminhos de {camI} até {camJ} é: {tamCaminho}")

    # Visualizar o grafo
    G = nx.DiGraph()
    G.add_edges_from(edges)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)  
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    plt.title("Grafo")
    plt.axis('off') 

    # Exibir o grafo no Streamlit
    st.pyplot(plt)



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


def pagina_polinomios():
    st.title("Calculadora de Polinômios")

    entrada = st.text_input("Digite o polinômio (exemplo: 2*x^2 - 3*x + 5):")
    
    if entrada:
        polinomio = Polinomio(entrada)
        
        # Geração do gráfico
        x_values = np.linspace(-10, 10, 400)  # Gera 400 pontos de -10 a 10
        y_values = [polinomio.valor(x) for x in x_values]  # Avalia o polinômio em cada ponto

        plt.figure(figsize=(10, 5))
        plt.plot(x_values, y_values, label=f'P(x) = {polinomio}', color='blue')
        plt.title("Gráfico do Polinômio")
        plt.xlabel("x")
        plt.ylabel("P(x)")
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.grid()
        plt.legend()
        

        opcoes = st.selectbox("Escolha uma operação:", ["Derivada", "Primitiva", "Soma de Riemann", "Aproximação"])
        
        if opcoes == "Derivada":
            resultado = polinomio.derivada()
            st.write(f"A derivada do polinômio é: {resultado}")
        
        elif opcoes == "Primitiva":
            x = st.number_input("Digite o ponto para calcular a primitiva:", value=0.0)
            resultado = polinomio.primitiva(x)
            st.write(f"A primitiva do polinômio em x={x} é: {resultado}")
        
        elif opcoes == "Soma de Riemann":
            a = st.number_input("Digite o limite inferior:", value=0.0)
            b = st.number_input("Digite o limite superior:", value=1.0)
            n = st.number_input("Digite o número de subintervalos:", value=10)
            resultado_totalm, resultado_totalM, resultado_total_medio = polinomio.soma_Riemman(a, b, n)
            st.write(f"A soma de Riemann (mínima) é: {resultado_totalm}")
            st.write(f"A soma de Riemann (máxima) é: {resultado_totalM}")
            st.write(f"A soma de Riemann (média) é: {resultado_total_medio}")
        
        elif opcoes == "Aproximação":
            x = st.number_input("Digite o ponto de aproximação:", value=0.0)
            resultado = polinomio.aprox(x)
            st.write(f"A aproximação em x={x} é:")
            for key, value in resultado.items():
                st.write(f"- {key}: {value}")
                
        st.pyplot(plt)

def main():
    # Menu lateral para selecionar páginas
    menu = ["Início", "Computação Gráfica", "Busca de Caminhos em Grafo", "Criptografia", "Polinômios"]
    escolha = st.sidebar.selectbox("Escolha a página:", menu)

    if escolha == "Início":
        inicio()
    elif escolha == "Computação Gráfica":
        pagina_operacoes()
    elif escolha == "Busca de Caminhos em Grafo":
        pagina_grafo()
    elif escolha == "Criptografia":
        cifra()
    elif escolha == "Polinômios":
        pagina_polinomios()

if __name__ == "__main__":
    main()
