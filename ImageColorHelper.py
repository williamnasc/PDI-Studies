import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImageColorHelper:
    """Classe para processamento de imagens coloridas usando OpenCV"""

    def __init__(self, caminho_arquivo=None):
        """
        Inicializa os parâmetros da imagem colorida
        :param caminho_arquivo: caminho para a imagem (suporta JPEG, PNG, etc)
        """
        self.imagem_original = None  # Armazena a imagem original
        self.imagem = None  # Imagem atual (pode ser modificada)
        self.canais = None  # Dicionário com os canais separados
        self.espaco_cores = 'BGR'  # Padrão OpenCV

        if caminho_arquivo is not None:
            self.load(caminho_arquivo)

    def load(self, caminho_arquivo):
        """
        Carrega uma imagem colorida usando OpenCV
        :param caminho_arquivo: caminho para o arquivo de imagem
        """
        try:
            # Carrega a imagem no formato BGR (padrão OpenCV)
            self.imagem_original = cv2.imread(caminho_arquivo)
            if self.imagem_original is None:
                raise ValueError(f"Não foi possível carregar a imagem: {caminho_arquivo}")

            self.imagem = self.imagem_original.copy()
            self._extrair_canais()

        except Exception as e:
            print(f"Erro ao carregar imagem: {str(e)}")
            raise

    def _extrair_canais(self):
        """Extrai os canais de cores da imagem"""
        if self.imagem is not None:
            self.canais = {
                'B': self.imagem[:, :, 0],  # Canal Blue
                'G': self.imagem[:, :, 1],  # Canal Green
                'R': self.imagem[:, :, 2]  # Canal Red
            }

    def show(self, title="Imagem Colorida"):
        """Mostra a imagem usando matplotlib (converte BGR para RGB)"""
        if self.imagem is not None:
            plt.imshow(cv2.cvtColor(self.imagem, cv2.COLOR_BGR2RGB))
            plt.title(title)
            plt.axis('off')
            plt.show()

    def show_canais(self):
        """Mostra os canais de cores separadamente"""
        if self.canais is not None:
            fig, axs = plt.subplots(1, 3, figsize=(15, 5))

            axs[0].imshow(self.canais['B'], cmap='Blues')
            axs[0].set_title('Canal Blue')
            axs[0].axis('off')

            axs[1].imshow(self.canais['G'], cmap='Greens')
            axs[1].set_title('Canal Green')
            axs[1].axis('off')

            axs[2].imshow(self.canais['R'], cmap='Reds')
            axs[2].set_title('Canal Red')
            axs[2].axis('off')

            plt.tight_layout()
            plt.show()

    def add_warm_tint(self, tint_color="yellow", alpha=0.3):
        """
        Adiciona um tom quente (amarelo ou marrom) à imagem via blend.

        Parâmetros:
        -----------
        tint_color : str
            Tipo de tom: "yellow" (amarelo) ou "brown" (marrom).
        alpha : float (0.0 a 1.0)
            Intensidade do efeito (0 = sem efeito, 1 = cor sólida).
        """
        if self.imagem is None:
            raise ValueError("Nenhuma imagem carregada.")

        # Define a cor base (BGR)
        if tint_color.lower() == "yellow":
            base_color = (0, 255, 255)  # Amarelo puro (B=0, G=255, R=255)
        elif tint_color.lower() == "brown":
            base_color = (30, 60, 120)  # Marrom (ajuste estes valores conforme necessário)
        else:
            raise ValueError("Cor inválida. Use 'yellow' ou 'brown'.")

        # Cria uma camada com a cor escolhida
        color_layer = np.zeros_like(self.imagem)
        color_layer[:] = base_color

        # Aplica o blend
        self.imagem = cv2.addWeighted(self.imagem, 1 - alpha, color_layer, alpha, 0)
        self._extrair_canais()  # Atualiza os canais BGR


    def apply_sepia_hsv(self, hue=20, saturation_boost=1.0, value_scale=0.9, y_alpha=0.0, b_alpha=0.0):
        """
        Aplica efeito sépia via HSV.
        :param hue: Matiz do sépia (20-40 é o range comum para sépia).
        :param saturation_boost: Ganho de saturação.
        :param value_scale: Ganho de brilho.
        :param y_alpha: Soma uma porcentagem de amarelo a imagem.
        :param b_alpha: Soma uma porcentagem de marrom a imagem.
        """
        if self.imagem is None:
            raise ValueError("Nenhuma imagem carregada.")

        # Converte BGR → HSV
        hsv_img = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2HSV)

        # Ajusta a matiz para o tom sépia (canal H)
        hsv_img[:, :, 0] = hsv_img[:, :, 0] + (hue - hsv_img[:, :, 0])  # empurra a matiz para o amarelo indicado no hue

        # Aumenta a saturação (canal S)
        hsv_img[:, :, 1] = np.clip(saturation_boost*(hsv_img[:, :, 1]) , 0, 255)

        # Reduz o brilho (canal V) para um look "envelhecido"
        hsv_img[:, :, 2] = np.clip(hsv_img[:, :, 2] * value_scale, 0, 255)

        # Converte HSV → BGR
        self.imagem = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
        self.add_warm_tint(tint_color="yellow", alpha=y_alpha)
        self.add_warm_tint(tint_color="brown", alpha=b_alpha)
        self._extrair_canais()  # Atualiza os canais BGR


# Exemplo de uso:
if __name__ == "__main__":

    img_color = ImageColorHelper("exemplo.jpg")
    img_color.show("exemplo antes")
    img_color.apply_sepia_hsv(hue=25, saturation_boost=0.8, value_scale=0.85, y_alpha=0.2, b_alpha=0.1)
    img_color.show("exemplo depois")

    img_color = ImageColorHelper("exemplo2.jpg")
    img_color.show("exemplo2 antes")
    img_color.apply_sepia_hsv(hue=25, saturation_boost=0.8, value_scale=0.85, y_alpha=0.2, b_alpha=0.1)
    img_color.show("exemplo2 depois")

    img_color = ImageColorHelper("exemplo3.jpg")
    img_color.show("exemplo3 antes")
    img_color.apply_sepia_hsv(hue=25, saturation_boost=0.8, value_scale=0.85, y_alpha=0.2, b_alpha=0.1)
    img_color.show("exemplo3 depois")
