import matplotlib.pyplot as plt
import math


class ImagePGMHelper:
    """Classe responsável por carregar e processar os arquivos de imagens."""

    def __init__(self, caminho_arquivo=None):
        """Criar os principais parâmetros da imagem"""
        self.num_linhas = None
        self.num_colunas = None
        self.L = None
        self.matriz = None

        if caminho_arquivo is not None:
            self.load(caminho_arquivo)

    def load(self, caminho_arquivo):
        with open(caminho_arquivo, 'rb') as f:

            tipo = f.readline().strip()
            if tipo not in [b'P2', b'P5']:
                raise ValueError('Apenas imagens PGM nos formatos P2 (ASCII) ou P5 (binário) são suportadas.')

            # Função auxiliar para ler linhas ignorando comentários
            def ler_linha_valida():
                linha = f.readline()
                while linha.startswith(b'#') or linha.strip() == b'':
                    linha = f.readline()
                return linha

            # Lê dimensões
            linha = ler_linha_valida()
            while linha.strip() == b'':
                linha = ler_linha_valida()
            largura, altura = map(int, linha.strip().split())
            self.num_colunas = largura
            self.num_linhas = altura

            # Lê valor máximo de cinza
            max_valor = int(ler_linha_valida().strip())
            self.L = max_valor

            # Lê os dados de pixels
            if tipo == b'P2':
                # ASCII
                dados = []
                for linha in f:
                    if linha.startswith(b'#'):
                        continue
                    dados.extend(map(int, linha.strip().split()))
            else:
                # P5 binário — pula qualquer byte restante antes dos dados de imagem
                resto = f.read(1)
                while resto.isspace():
                    resto = f.read(1)
                dados_bin = resto + f.read(largura * altura - 1)
                dados = list(dados_bin)

            # Converte os dados em matriz 2D
            matriz = []
            for i in range(altura):
                linha = dados[i * largura:(i + 1) * largura]
                matriz.append(linha)

            self.matriz = matriz
            return matriz

    def show(self, name=None):
        plt.imshow(self.matriz, cmap='gray', vmin=0, vmax=self.L)
        plt.axis('off')  # remove eixos
        if name is not None:
            plt.title(name)
        plt.show()
        pass

    def thresholding_transformation(self, k):
        """faz a foto ter apenas os preto (0) e brando (L-1)
        para os pontos que estao a baixo ou acima do k"""

        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                r = self.matriz[i][j]
                if r <= k:
                    self.matriz[i][j] = 0
                else:
                    self.matriz[i][j] = self.L - 1
        pass

    def negative_transformation(self):
        """
        Inverte os niveis de cinza da imagem.
        fazendo
            s = L - 1 - r
        """
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                r = self.matriz[i][j]
                self.matriz[i][j] = self.L - 1 - r
        pass

    def log_transformation(self, c=1.0):
        """
        Transformação logaritmica na sua forma geral.
        fazendo
            s = c*log(1+r)
        onde
            c é a constante de transformação de modo que:
                c > 0 : deixa imagem mais clara
                c < 0 : deixa imagem mais escura
        :param c: constante de transformação
        """
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                r = self.matriz[i][j]
                # APLICA A TRANSFORMACAO
                s = (math.log(1 + r)) * c
                print(f"({i},{j}) r = {r} -> s = {s}")
                # APLICA O VALOR AJUSTADO NA MATRIZ
                self.matriz[i][j] = self._adjust_final_value(s)
        pass

    def _adjust_final_value(self, s):
        """Arredonda o valor para o inteiro superior e satura se passar do L maximo."""
        s = math.ceil(s)
        if s > (self.L - 1):
            s = self.L - 1
        return s

    def gamma_transformation(self, c=1.0, y=1.0):
        """
        Power-Law (Gamma) Transformations
        Uma transformação exponencial
        fazendo
            s = c * r^y
        onde
            c é constante de transformação
                c > 0 : deixa imagem mais clara
                c < 0 : deixa imagem mais escura
            y é constante exponencial
                se (c = 1)
                y < 1 : deixa imagem mais clara
                y = 1 : deixa a transformacao linear
                y > 1 : deixa imagem mais escura
        :param c: constante multiplicativa
        :param y: constante exponencial
        """
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                r = self.matriz[i][j]
                # APLICA A TRANSFORMACAO
                s = c * (r ** y)
                # APLICA O VALOR AJUSTADO NA MATRIZ
                self.matriz[i][j] = self._adjust_final_value(s)


imagem = ImagePGMHelper("einstein.pgm")
print(imagem.L)
print(imagem.num_linhas)
print(imagem.num_colunas)
imagem.show()

# imagem.load("einstein.pgm")
# imagem.thresholding_transformation(k=126)
# imagem.show()

# imagem.load("einstein.pgm")
# imagem.negative_transformation()
# imagem.show()

# c_values = [40]
# for c_value in c_values:
#     imagem.load("einstein.pgm")
#     imagem.log_transformation(c=c_value)
#     imagem.show(name=f"log c={c_value}")

gammas = [0.85, 1 , 1.1]
for gamma in gammas:
    imagem.load("einstein.pgm")
    imagem.gamma_transformation(y=gamma)
    imagem.show(name=f"gamma y={gamma}")


