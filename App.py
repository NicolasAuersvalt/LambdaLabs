from header import *
from page.grafo import *
from page.grafica import *
from page.polinomio import *
from page.cifra import *
from page.main import *


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
