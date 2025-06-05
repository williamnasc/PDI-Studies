import numpy as np


class SpacialFilters:
    """
    Classe para armazenar e gerenciar filtros espaciais.
    Os filtros são armazenados como tuplas de (constante, matriz_pesos).
    """

    def __init__(self):
        self.filters = {}

        # Adiciona o filtro Gaussiano 5x5
        gaussian_kernel_5x5 = np.array([
            [1,  4,  7,  4,  1],
            [4, 16, 26, 16,  4],
            [7, 26, 41, 26,  7],
            [4, 16, 26, 16,  4],
            [1,  4,  7,  4,  1]
        ])
        gaussian_constant = 1.0 / 273.0
        self.add_filter("gaussian_5x5", gaussian_constant, gaussian_kernel_5x5)

        # Adiciona o filtro Passa Alta 5x5
        highpass_kernel_5x5 = np.array([
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 24, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ])
        highpass_constant = 1.0
        self.add_filter("highpass_5x5", highpass_constant, highpass_kernel_5x5)

        # Adiciona o filtro Passa Baixa 5x5 (Média 5x5)
        lowpass_kernel_5x5 = np.ones((5, 5))
        lowpass_constant = 1.0 / 25.0
        self.add_filter("lowpass_5x5", lowpass_constant, lowpass_kernel_5x5)

        # Adiciona o filtro Passa Baixa 3x3 (Média 3x3)
        lowpass_kernel_3x3 = np.ones((3, 3))
        lowpass_constant = 1.0 / 9.0
        self.add_filter("lowpass_3x3", lowpass_constant, lowpass_kernel_3x3)

        # FILTROS DE AGUÇAMENTO

        # laplaciano 3x3
        laplacian_3x3 = np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ])
        laplacian_constant = 1.0
        self.add_filter("laplacian_3x3", highpass_constant, laplacian_3x3)

        # sobel 3x3
        sobel_3x3 = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])
        constant = 1.0
        self.add_filter("sobel_v_3x3", constant, sobel_3x3)

        # sobel 3x3
        sobel_3x3 = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ])
        constant = 1.0
        self.add_filter("sobel_h_3x3", constant, sobel_3x3)

        # sobel 3x3
        robets_r_2x2 = np.array([
            [-1, 0],
            [ 0, 1]
        ])
        constant = 1.0
        self.add_filter("robets_r_2x2", constant, robets_r_2x2)

        # sobel 3x3
        robets_l_2x2 = np.array([
            [ 0, -1],
            [ 1,  0]
        ])
        constant = 1.0
        self.add_filter("robets_l_2x2", constant, robets_l_2x2)

    def add_filter(self, name, constant, weights_matrix):
        """
        Adiciona um novo filtro à coleção.
        :param name: Nome do filtro (string).
        :param constant: Constante multiplicativa do filtro.
        :param weights_matrix: Matriz numpy de pesos do filtro.
        """
        if not isinstance(weights_matrix, np.ndarray):
            weights_matrix = np.array(weights_matrix)
        self.filters[name] = (constant, weights_matrix)

    def get_filter(self, name):
        """
        Retorna a tupla (constante, matriz_pesos) do filtro especificado.
        :param name: Nome do filtro.
        :return: Tupla (constante, matriz_pesos) ou None se o filtro não for encontrado.
        """
        return self.filters.get(name)

    def list_filters(self):
        """Lista os nomes de todos os filtros disponíveis."""
        return list(self.filters.keys())


# Exemplo de uso:
filters_collection = SpacialFilters()
print("Filtros disponíveis:", filters_collection.list_filters())
# gaussian_filter = filters_collection.get_filter("gaussian_5x5")
# if gaussian_filter:
#     constant, kernel = gaussian_filter
#     print("\nFiltro Gaussiano 5x5:")
#     print("Constante:", constant)
#     print("Kernel:\n", kernel)

# lowpass_filter = filters_collection.get_filter("lowpass_5x5")
# if lowpass_filter:
#     constant, kernel = lowpass_filter
#     print("\nFiltro Passa Baixa 5x5:")
#     print("Constante:", constant)
#     print("Kernel:\n", kernel)

# highpass_filter = filters_collection.get_filter("highpass_5x5")
# if highpass_filter:
#     constant, kernel = highpass_filter
#     print("\nFiltro Passa Alta 5x5:")
#     print("Constante:", constant)
#     print("Kernel:\n", kernel)

