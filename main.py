import matplotlib.pyplot as plt


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

    def show(self):
        plt.imshow(self.matriz, cmap='gray', vmin=0, vmax=self.L)
        plt.axis('off')  # remove eixos
        plt.show()
        pass


imagem = ImagePGMHelper("einstein.pgm")
print(imagem.L)
print(imagem.num_linhas)
print(imagem.num_colunas)
imagem.show()


