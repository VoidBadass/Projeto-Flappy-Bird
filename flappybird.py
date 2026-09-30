

# ==========================================
# IMPORTAÇÕES
# ==========================================

import json
import math
import os
import random

import pygame


# ==========================================
# CONFIGURAÇÕES
# ==========================================

LARGURA_TELA = 960
ALTURA_TELA = 600
ALTURA_CHAO = 80
TAXA_DE_QUADROS = 60
ARQUIVO_SALVAMENTO = "save.json"
PASTA_SONS = "sounds"


# ==========================================
# CORES
# ==========================================

BRANCO = (250, 250, 250)
PRETO = (25, 28, 40)
CINZA_ESCURO = (53, 60, 77)
CINZA_CLARO = (210, 220, 230)
AMARELO = (255, 210, 64)
LARANJA = (255, 137, 56)
VERMELHO = (224, 75, 75)
VERDE = (73, 180, 99)
AZUL = (72, 156, 235)
ROXO = (137, 90, 200)


# ==========================================
# MOEDAS E SKINS
# ==========================================

SKINS = {
    "padrao": {
        "nome": "PÁSSARO PADRÃO",
        "preco": 0,
        "corpo": AMARELO,
        "asa": (247, 170, 45),
        "bico": LARANJA,
    },
    "neon": {
        "nome": "NEON",
        "preco": 12,
        "corpo": (70, 235, 235),
        "asa": (27, 176, 198),
        "bico": (255, 111, 177),
    },
    "sunset": {
        "nome": "SUNSET",
        "preco": 20,
        "corpo": (255, 142, 111),
        "asa": (219, 77, 83),
        "bico": (255, 210, 77),
    },
}


# ==========================================
# CONFIGURAÇÕES DOS NÍVEIS
# ==========================================

NIVEIS = [
    {
        "nome": "PRIMAVERA",
        "tema": "primavera",
        "velocidade": 210,
        "espaco": 195,
        "intervalo": 1.75,
        "meta": 10,
        "cor_obstaculo": (59, 169, 86),
        "cor_ceu": (105, 198, 243),
    },
    {
        "nome": "DESERTO",
        "tema": "deserto",
        "velocidade": 245,
        "espaco": 175,
        "intervalo": 1.62,
        "meta": 15,
        "cor_obstaculo": (74, 150, 73),
        "cor_ceu": (239, 153, 85),
    },
    {
        "nome": "NOITE",
        "tema": "noite",
        "velocidade": 280,
        "espaco": 160,
        "intervalo": 1.50,
        "meta": 20,
        "cor_obstaculo": (70, 119, 177),
        "cor_ceu": (21, 32, 70),
    },
    {
        "nome": "TEMPESTADE",
        "tema": "tempestade",
        "velocidade": 320,
        "espaco": 145,
        "intervalo": 1.37,
        "meta": 25,
        "cor_obstaculo": (77, 106, 133),
        "cor_ceu": (55, 69, 91),
    },
    {
        "nome": "VULCÃO",
        "tema": "vulcao",
        "velocidade": 360,
        "espaco": 132,
        "intervalo": 1.24,
        "meta": 30,
        "cor_obstaculo": (79, 58, 57),
        "cor_ceu": (151, 50, 39),
    },
    {
        "nome": "ESPAÇO",
        "tema": "espaco",
        "velocidade": 405,
        "espaco": 320,
        "intervalo": 1.12,
        "meta": 40,
        "cor_obstaculo": (107, 91, 192),
        "cor_ceu": (15, 18, 48),
    },
    {
        "nome": "FUNDO DO MAR",
        "tema": "mar",
        "velocidade": 405,
        "espaco": 120,
        "intervalo": 1.06,
        "meta": 45,
        "cor_obstaculo": (53, 139, 158),
        "cor_ceu": (9, 67, 111),
    },
    {
        "nome": "NEVE",
        "tema": "neve",
        "velocidade": 425,
        "espaco": 325,
        "intervalo": 1.04,
        "meta": 50,
        "cor_obstaculo": (180, 207, 225),
        "cor_ceu": (155, 202, 230),
    },
    {
        "nome": "CÉU",
        "tema": "ceu",
        "velocidade": 455,
        "espaco": 305,
        "intervalo": 0.96,
        "meta": 60,
        "cor_obstaculo": (216, 183, 104),
        "cor_ceu": (195, 175, 239),
    },
]


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def limitar(valor, minimo, maximo):
    """Mantém um número dentro de um intervalo."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def desenhar_texto(tela, texto, fonte, cor, centro, sombra=True):
    """Desenha um texto centralizado, com uma sombra simples opcional."""
    imagem_texto = fonte.render(texto, True, cor)
    retangulo_texto = imagem_texto.get_rect(center=centro)

    if sombra:
        imagem_sombra = fonte.render(texto, True, (30, 35, 48))
        retangulo_sombra = imagem_sombra.get_rect(center=(centro[0] + 3, centro[1] + 4))
        tela.blit(imagem_sombra, retangulo_sombra)

    tela.blit(imagem_texto, retangulo_texto)
    return retangulo_texto


def desenhar_painel(tela, retangulo, cor=(255, 255, 255, 210), raio=18):
    """Desenha um painel claro e semitransparente com sombra."""
    sombra = pygame.Rect(retangulo.x + 5, retangulo.y + 7, retangulo.width, retangulo.height)
    pygame.draw.rect(tela, (28, 35, 50), sombra, border_radius=raio)

    superficie = pygame.Surface((retangulo.width, retangulo.height), pygame.SRCALPHA)
    pygame.draw.rect(superficie, cor, superficie.get_rect(), border_radius=raio)
    tela.blit(superficie, retangulo)


def cor_clara(cor, quantidade=35):
    """Cria uma cor um pouco mais clara, útil para detalhes visuais."""
    vermelho = limitar(cor[0] + quantidade, 0, 255)
    verde = limitar(cor[1] + quantidade, 0, 255)
    azul = limitar(cor[2] + quantidade, 0, 255)
    return vermelho, verde, azul


def medalha_da_pontuacao(pontuacao):
    """Retorna o nome e a cor da medalha da rodada."""
    if pontuacao >= 50:
        return "ESMERALDA", (27, 182, 103)
    if pontuacao >= 45:
        return "PLATINA", (54, 177, 177)
    if pontuacao >= 30:
        return "OURO", (246, 193, 56)
    if pontuacao >= 20:
        return "PRATA", (190, 202, 215)
    if pontuacao >= 10:
        return "BRONZE", (194, 126, 72)
    return "SEM MEDALHA", (150, 157, 165)


def criar_elementos_cenario(tema):
    """Cria posições iniciais fixas para estrelas, chuva, poeira e nuvens."""
    elementos = []

    quantidade = 24
    if tema == "mar":
        quantidade = 56
    elif tema == "espaco":
        quantidade = 72
    elif tema == "noite":
        quantidade = 48
    elif tema == "tempestade":
        quantidade = 42

    for indice in range(quantidade):
        elemento = {
            "x": random.randint(0, LARGURA_TELA),
            "y": random.randint(25, ALTURA_TELA - ALTURA_CHAO - 20),
            "tamanho": random.randint(2, 7),
            "velocidade": random.randint(15, 90),
        }
        elementos.append(elemento)

    return elementos


def desenhar_nuvem(tela, posicao_x, posicao_y, escala=1.0, cor=(255, 255, 255)):
    """Monta uma nuvem usando círculos e um retângulo."""
    largura = int(78 * escala)
    altura = int(26 * escala)
    pygame.draw.ellipse(tela, cor, (posicao_x, posicao_y, largura, altura))
    pygame.draw.circle(tela, cor, (int(posicao_x + 24 * escala), int(posicao_y + 10 * escala)), int(15 * escala))
    pygame.draw.circle(tela, cor, (int(posicao_x + 47 * escala), int(posicao_y + 5 * escala)), int(19 * escala))


def desenhar_cenario(tela, nivel, tempo, elementos):
    """Desenha o fundo de cada mapa. Os elementos se movem para dar vida ao cenário."""
    tema = nivel["tema"]
    tela.fill(nivel["cor_ceu"])

    if tema == "primavera":
        for indice in range(4):
            posicao_x = (indice * 280 - tempo * (18 + indice * 4)) % 1180 - 100
            desenhar_nuvem(tela, posicao_x, 55 + indice * 65, 0.8 + indice * 0.1)
        pygame.draw.ellipse(tela, (94, 183, 103), (-100, 430, 700, 170))
        pygame.draw.ellipse(tela, (70, 157, 80), (380, 445, 760, 160))
        for indice in range(7):
            arvore_x = indice * 160 - int((tempo * 35) % 160)
            pygame.draw.rect(tela, (112, 77, 52), (arvore_x + 20, 440, 18, 80))
            pygame.draw.circle(tela, (48, 142, 69), (arvore_x + 29, 425), 38)
            pygame.draw.circle(tela, (69, 165, 78), (arvore_x + 5, 440), 27)

    elif tema == "deserto":
        pygame.draw.circle(tela, (255, 224, 128), (790, 105), 54)
        pygame.draw.polygon(tela, (174, 102, 70), [(0, 420), (170, 255), (335, 420)])
        pygame.draw.polygon(tela, (194, 117, 75), [(260, 420), (500, 215), (740, 420)])
        pygame.draw.polygon(tela, (158, 89, 66), [(590, 420), (805, 270), (1050, 420)])
        pygame.draw.ellipse(tela, (231, 177, 93), (-100, 430, 700, 150))
        pygame.draw.ellipse(tela, (212, 151, 72), (340, 455, 770, 125))
        for elemento in elementos:
            poeira_x = (elemento["x"] - tempo * elemento["velocidade"]) % (LARGURA_TELA + 50)
            poeira_y = elemento["y"] % 180 + 390
            pygame.draw.circle(tela, (245, 196, 119), (int(poeira_x), int(poeira_y)), 2)

    elif tema == "noite":
        for elemento in elementos:
            brilho = 150 + int(90 * math.sin(tempo * 2 + elemento["x"]))
            pygame.draw.circle(tela, (brilho, brilho, 220), (elemento["x"], elemento["y"]), max(1, elemento["tamanho"] // 3))
        pygame.draw.circle(tela, (247, 243, 211), (760, 115), 52)
        pygame.draw.circle(tela, (225, 220, 189), (742, 102), 8)
        pygame.draw.circle(tela, (225, 220, 189), (782, 128), 11)
        for indice in range(3):
            posicao_x = (indice * 380 - tempo * 24) % 1200 - 120
            desenhar_nuvem(tela, posicao_x, 190 + indice * 85, 1.15, (54, 67, 108))
        pygame.draw.ellipse(tela, (34, 55, 79), (-80, 465, 1150, 130))

    elif tema == "tempestade":
        for indice in range(5):
            posicao_x = (indice * 250 - tempo * 40) % 1200 - 120
            desenhar_nuvem(tela, posicao_x, 45 + (indice % 2) * 80, 1.55, (62, 74, 91))
        for elemento in elementos:
            chuva_x = (elemento["x"] - tempo * 125) % LARGURA_TELA
            chuva_y = (elemento["y"] + tempo * 380) % (ALTURA_TELA - ALTURA_CHAO)
            pygame.draw.line(tela, (174, 207, 230), (chuva_x, chuva_y), (chuva_x - 5, chuva_y + 13), 2)
        if int(tempo * 2.2) % 17 == 0:
            pygame.draw.polygon(tela, (244, 243, 167), [(190, 155), (165, 240), (205, 240), (183, 320), (250, 215), (212, 215)])
        pygame.draw.ellipse(tela, (39, 55, 69), (-100, 450, 1200, 150))

    elif tema == "vulcao":
        pygame.draw.polygon(tela, (67, 51, 55), [(120, 465), (330, 185), (510, 465)])
        pygame.draw.polygon(tela, (63, 49, 51), [(420, 465), (680, 235), (900, 465)])
        pygame.draw.polygon(tela, (250, 95, 38), [(300, 240), (330, 185), (365, 245), (337, 230)])
        pygame.draw.ellipse(tela, (238, 76, 31), (-100, 485, 1160, 105))
        pygame.draw.ellipse(tela, (255, 151, 40), (-100, 520, 1160, 75))
        for elemento in elementos:
            cinza_x = (elemento["x"] - tempo * elemento["velocidade"] * 0.35) % LARGURA_TELA
            cinza_y = (elemento["y"] + tempo * 25) % 400
            pygame.draw.circle(tela, (107, 85, 79), (int(cinza_x), int(cinza_y)), elemento["tamanho"] // 2 + 1)

    elif tema == "espaco":
        for elemento in elementos:
            estrela_x = (elemento["x"] - tempo * elemento["velocidade"] * 0.2) % LARGURA_TELA
            tamanho = max(1, elemento["tamanho"] // 3)
            pygame.draw.circle(tela, (210, 226, 255), (int(estrela_x), elemento["y"]), tamanho)
        pygame.draw.circle(tela, (107, 87, 182), (785, 175), 80)
        pygame.draw.circle(tela, (147, 120, 220), (760, 148), 22)
        pygame.draw.ellipse(tela, (191, 162, 242), (670, 155, 230, 45), 3)
        meteoro_x = int((tempo * 260) % 1300) - 220
        pygame.draw.line(tela, (255, 181, 92), (meteoro_x, 90), (meteoro_x + 80, 130), 5)
        pygame.draw.ellipse(tela, (24, 29, 64), (-100, 470, 1200, 130))


    elif tema == "mar":
        # Fundo totalmente subaquático, com faixas de luz descendo da superfície.
        pygame.draw.rect(tela, (7, 81, 126), (0, 0, LARGURA_TELA, 520))
        for indice in range(6):
            faixa_x = indice * 190 - int((tempo * 12) % 190)
            pygame.draw.polygon(tela, (35, 137, 167), [
                (faixa_x, 0), (faixa_x + 70, 0),
                (faixa_x + 145, 520), (faixa_x + 35, 520)
            ])

        # Bolhas reaproveitando os elementos do cenário e subindo pela água.
        for elemento in elementos:
            bolha_x = (elemento["x"] - tempo * elemento["velocidade"] * 0.25) % (LARGURA_TELA + 40)
            bolha_y = 40 + ((elemento["y"] - tempo * (24 + elemento["tamanho"])) % 445)
            raio = max(2, elemento["tamanho"] // 2)
            pygame.draw.circle(tela, (160, 235, 239), (int(bolha_x), int(bolha_y)), raio, 2)

        # Silhueta de algas, corais e pedras no fundo do oceano.
        for indice in range(9):
            alga_x = indice * 125 - int((tempo * 18) % 125)
            pygame.draw.line(tela, (24, 119, 111), (alga_x, 518), (alga_x - 8, 470), 6)
            pygame.draw.line(tela, (32, 143, 119), (alga_x + 5, 518), (alga_x + 18, 458), 5)
            pygame.draw.circle(tela, (218, 96, 125), (alga_x + 22, 492), 10)
            pygame.draw.circle(tela, (244, 143, 110), (alga_x + 38, 505), 7)

    elif tema == "neve":
        # Céu frio com montanhas cobertas de neve ao fundo.
        pygame.draw.circle(tela, (244, 250, 255), (790, 105), 42)
        pygame.draw.polygon(tela, (125, 174, 204), [(0, 430), (180, 215), (350, 430)])
        pygame.draw.polygon(tela, (105, 158, 191), [(250, 430), (510, 165), (790, 430)])
        pygame.draw.polygon(tela, (127, 178, 204), [(620, 430), (825, 235), (1060, 430)])
        pygame.draw.polygon(tela, (242, 249, 255), [(180, 215), (125, 285), (160, 270), (205, 310), (235, 270), (285, 330), (350, 430)])
        pygame.draw.polygon(tela, (250, 253, 255), [(510, 165), (445, 255), (485, 240), (530, 285), (570, 250), (625, 315), (790, 430)])

        # Neve caindo em velocidades diferentes para dar profundidade.
        for elemento in elementos:
            neve_x = (elemento["x"] - tempo * elemento["velocidade"] * 0.18) % LARGURA_TELA
            neve_y = (elemento["y"] + tempo * (45 + elemento["tamanho"] * 5)) % 455
            raio = max(2, elemento["tamanho"] // 2)
            pygame.draw.circle(tela, (248, 253, 255), (int(neve_x), int(neve_y)), raio)

        # Pinheiros no horizonte.
        for indice in range(8):
            arvore_x = indice * 145 - int((tempo * 20) % 145)
            pygame.draw.rect(tela, (91, 77, 70), (arvore_x + 28, 400, 10, 65))
            pygame.draw.polygon(tela, (38, 104, 117), [(arvore_x + 33, 300), (arvore_x - 5, 410), (arvore_x + 72, 410)])
            pygame.draw.polygon(tela, (53, 128, 139), [(arvore_x + 33, 335), (arvore_x + 3, 425), (arvore_x + 66, 425)])

    elif tema == "aurora":
        # Penúltimo mundo: uma ponte entre a neve e o céu divino.
        for indice in range(7):
            faixa_x = indice * 180 - int((tempo * 16) % 180)
            pygame.draw.arc(tela, (111, 240, 208), (faixa_x, 80, 300, 300), 0.4, 2.4, 8)
            pygame.draw.arc(tela, (183, 143, 255), (faixa_x + 45, 100, 300, 300), 0.5, 2.3, 6)
        pygame.draw.circle(tela, (244, 236, 255), (780, 120), 50)
        pygame.draw.ellipse(tela, (45, 51, 105), (-100, 465, 1200, 140))
        for elemento in elementos:
            brilho = 150 + int(70 * math.sin(tempo * 2 + elemento["x"]))
            pygame.draw.circle(tela, (brilho, 220, 255), (int(elemento["x"]), int(elemento["y"])), max(1, elemento["tamanho"] // 2))

    elif tema == "ceu":
        # Final game: céu celestial com templo, halo e colunas de luz.
        pygame.draw.circle(tela, (255, 248, 210), (780, 122), 78)
        pygame.draw.circle(tela, (255, 255, 236), (780, 122), 54)
        for indice in range(6):
            raio = 150 + indice * 34
            pygame.draw.arc(tela, (255, 226, 135), (780 - raio, 122 - raio, raio * 2, raio * 2), 0.2, 2.9, 3)
        for indice in range(7):
            faixa_x = indice * 175 - int((tempo * 20) % 175)
            pygame.draw.polygon(tela, (255, 247, 203), [(faixa_x, 0), (faixa_x + 54, 0), (faixa_x + 170, 500), (faixa_x + 110, 500)])
        desenhar_nuvem(tela, 30 - (tempo * 11) % 250, 155, 1.7, (255, 255, 244))
        desenhar_nuvem(tela, 610 - (tempo * 14) % 300, 245, 1.4, (255, 255, 244))
        # Templo dourado no horizonte.
        pygame.draw.polygon(tela, (255, 239, 180), [(335, 430), (480, 275), (625, 430)])
        pygame.draw.polygon(tela, (255, 249, 217), [(360, 405), (480, 300), (600, 405)])
        for coluna_x in (395, 450, 505, 560):
            pygame.draw.rect(tela, (230, 190, 105), (coluna_x, 345, 17, 95), border_radius=5)
        pygame.draw.polygon(tela, (214, 165, 73), [(330, 350), (480, 250), (630, 350)])
        for elemento in elementos:
            estrela_x = (elemento["x"] - tempo * elemento["velocidade"] * 0.12) % LARGURA_TELA
            pygame.draw.circle(tela, (255, 255, 232), (int(estrela_x), int(elemento["y"])), max(1, elemento["tamanho"] // 2))

    # O chão aparece sobre o cenário e muda de cor em cada tema.
    cores_chao = {
        "primavera": (62, 161, 78),
        "deserto": (202, 139, 67),
        "noite": (36, 53, 75),
        "tempestade": (48, 61, 75),
        "vulcao": (83, 45, 41),
        "espaco": (34, 38, 76),
        "mar": (20, 81, 91),
        "neve": (205, 225, 238),
        "aurora": (63, 89, 139),
        "ceu": (250, 222, 153),
    }
    cor_chao = cores_chao[tema]
    pygame.draw.rect(tela, cor_chao, (0, ALTURA_TELA - ALTURA_CHAO, LARGURA_TELA, ALTURA_CHAO))
    pygame.draw.line(tela, cor_clara(cor_chao, 40), (0, ALTURA_TELA - ALTURA_CHAO), (LARGURA_TELA, ALTURA_TELA - ALTURA_CHAO), 4)


# ==========================================
# CLASSE JOGADOR
# ==========================================

class Jogador:
    """Representa o pássaro controlado pelo jogador."""

    def __init__(self, skin="padrao"):
        self.skin = skin if skin in SKINS else "padrao"
        self.posicao_x = 190
        self.posicao_y = ALTURA_TELA // 2
        self.velocidade_vertical = 0.0
        self.gravidade = 1150
        self.impulso = -385
        self.raio_colisao = 19
        self.angulo = 0
        self.tempo_asas = 0

    @property
    def rect(self):
        """Um retângulo simples é suficiente para a colisão didática do pássaro."""
        tamanho = self.raio_colisao * 2
        return pygame.Rect(self.posicao_x - self.raio_colisao, self.posicao_y - self.raio_colisao, tamanho, tamanho)

    def bater_asas(self):
        self.velocidade_vertical = self.impulso
        self.tempo_asas = 0

    def atualizar(self, delta_tempo):
        self.velocidade_vertical += self.gravidade * delta_tempo
        self.posicao_y += self.velocidade_vertical * delta_tempo
        self.tempo_asas += delta_tempo

        # O ângulo acompanha a velocidade e deixa o voo mais expressivo.
        self.angulo = limitar(-self.velocidade_vertical * 0.11, -55, 35)

        if self.posicao_y - self.raio_colisao < 0:
            self.posicao_y = self.raio_colisao
            self.velocidade_vertical = 0

    def desenhar(self, tela):
        superficie_passaro = pygame.Surface((80, 70), pygame.SRCALPHA)
        centro = (40, 35)
        movimento_asas = int(math.sin(self.tempo_asas * 18) * 6)

        cores_skin = SKINS[self.skin]

        # Asa atrás do corpo.
        pygame.draw.ellipse(superficie_passaro, cores_skin["asa"], (14, 30 + movimento_asas, 32, 21))
        # Corpo, barriga e olho.
        pygame.draw.ellipse(superficie_passaro, cores_skin["corpo"], (20, 17, 45, 35))
        pygame.draw.ellipse(superficie_passaro, (255, 229, 133), (33, 29, 24, 18))
        pygame.draw.circle(superficie_passaro, BRANCO, (53, 25), 8)
        pygame.draw.circle(superficie_passaro, PRETO, (55, 26), 3)
        # Bico e uma asa visível.
        pygame.draw.polygon(superficie_passaro, cores_skin["bico"], [(62, 31), (76, 36), (62, 41)])
        pygame.draw.ellipse(superficie_passaro, cores_skin["asa"], (27, 37 - movimento_asas // 2, 26, 15))

        superficie_girada = pygame.transform.rotozoom(superficie_passaro, self.angulo, 1)
        retangulo_girado = superficie_girada.get_rect(center=(self.posicao_x, self.posicao_y))
        tela.blit(superficie_girada, retangulo_girado)


# ==========================================
# CLASSE OBSTÁCULO
# ==========================================

class Obstaculo:
    """Um par de obstáculos: uma parte superior e outra inferior."""

    def __init__(self, posicao_x, altura_superior, nivel):
        self.posicao_x = posicao_x
        self.altura_superior = altura_superior
        self.largura = 72
        self.tamanho_espaco = nivel["espaco"]
        self.velocidade = nivel["velocidade"]
        self.cor = nivel["cor_obstaculo"]
        self.tipo = nivel["tema"]
        self.ja_deu_ponto = False

    @property
    def rect_superior(self):
        return pygame.Rect(self.posicao_x, 0, self.largura, self.altura_superior)

    @property
    def rect_inferior(self):
        inicio_inferior = self.altura_superior + self.tamanho_espaco
        altura_inferior = ALTURA_TELA - ALTURA_CHAO - inicio_inferior
        return pygame.Rect(self.posicao_x, inicio_inferior, self.largura, altura_inferior)

    def mover(self, delta_tempo):
        self.posicao_x -= self.velocidade * delta_tempo

    def saiu_da_tela(self):
        return self.posicao_x + self.largura < -5

    def colidiu_com(self, jogador):
        if jogador.rect.colliderect(self.rect_superior):
            return True
        if jogador.rect.colliderect(self.rect_inferior):
            return True
        return False

    def desenhar_parte(self, tela, retangulo, e_superior):
        """Desenha a mesma hitbox com aparência diferente em cada mapa."""
        pygame.draw.rect(tela, self.cor, retangulo)
        pygame.draw.rect(tela, cor_clara(self.cor, 35), retangulo, 3)

        if self.tipo == "primavera":
            # Tronco e copa fazem o obstáculo parecer uma árvore muito grande.
            pygame.draw.rect(tela, (106, 72, 43), (retangulo.x + 25, retangulo.y, 20, retangulo.height))
            borda_y = retangulo.bottom - 16 if e_superior else retangulo.y
            pygame.draw.ellipse(tela, (51, 143, 66), (retangulo.x - 8, borda_y - 10, 88, 28))

        elif self.tipo == "deserto":
            # Espinhos simples transformam o bloco em um cacto.
            for altura in range(retangulo.y + 12, retangulo.bottom - 8, 22):
                pygame.draw.line(tela, (211, 236, 152), (retangulo.x + 10, altura), (retangulo.x + 2, altura - 4), 2)
                pygame.draw.line(tela, (211, 236, 152), (retangulo.right - 10, altura), (retangulo.right - 2, altura - 4), 2)

        elif self.tipo == "noite":
            # Linhas quebradas dão uma aparência de rocha.
            for altura in range(retangulo.y + 14, retangulo.bottom, 28):
                pygame.draw.line(tela, (118, 163, 212), (retangulo.x + 8, altura), (retangulo.x + 35, altura - 7), 3)

        elif self.tipo == "tempestade":
            for altura in range(retangulo.y + 12, retangulo.bottom, 25):
                pygame.draw.line(tela, (186, 220, 234), (retangulo.x + 12, altura), (retangulo.x + 35, altura + 8), 2)

        elif self.tipo == "vulcao":
            for altura in range(retangulo.y + 16, retangulo.bottom, 30):
                pygame.draw.circle(tela, (213, 73, 35), (retangulo.x + 24, altura), 5)
                pygame.draw.circle(tela, (246, 123, 41), (retangulo.x + 48, altura + 8), 3)

        elif self.tipo == "mar":
            # Corais e pequenas bolhas deixam os obstáculos coerentes com o oceano.
            pygame.draw.rect(tela, (244, 117, 111), (retangulo.x + 10, retangulo.y, 9, retangulo.height))
            pygame.draw.rect(tela, (255, 176, 126), (retangulo.right - 19, retangulo.y, 8, retangulo.height))
            for altura in range(retangulo.y + 18, retangulo.bottom, 34):
                pygame.draw.circle(tela, (255, 212, 151), (retangulo.x + 36, altura), 4, 1)

        elif self.tipo == "neve":
            # Pilares de gelo com pontas nevadas e pequenas rachaduras azuis.
            pygame.draw.rect(tela, (225, 241, 250), (retangulo.x + 7, retangulo.y, 18, retangulo.height))
            pygame.draw.rect(tela, (143, 190, 218), (retangulo.right - 18, retangulo.y, 10, retangulo.height))
            ponta_y = retangulo.bottom - 2 if e_superior else retangulo.y - 2
            pygame.draw.polygon(tela, (248, 253, 255), [
                (retangulo.x - 6, ponta_y),
                (retangulo.centerx, ponta_y + (14 if e_superior else -14)),
                (retangulo.right + 6, ponta_y),
            ])
            for altura in range(retangulo.y + 22, retangulo.bottom, 36):
                pygame.draw.line(tela, (111, 169, 204), (retangulo.x + 28, altura), (retangulo.x + 39, altura + 10), 2)
                pygame.draw.line(tela, (111, 169, 204), (retangulo.x + 39, altura + 10), (retangulo.x + 48, altura + 2), 2)

        elif self.tipo == "espaco":
            pygame.draw.rect(tela, (109, 223, 240), (retangulo.x + 9, retangulo.y, 6, retangulo.height))
            pygame.draw.rect(tela, (157, 121, 231), (retangulo.right - 16, retangulo.y, 6, retangulo.height))
            for altura in range(retangulo.y + 14, retangulo.bottom, 35):
                pygame.draw.circle(tela, (95, 245, 240), (retangulo.x + 36, altura), 4)

    def desenhar(self, tela):
        self.desenhar_parte(tela, self.rect_superior, True)
        self.desenhar_parte(tela, self.rect_inferior, False)


# ==========================================
# CLASSE PARTÍCULA
# ==========================================

class Particula:
    """Uma partícula simples usada em asas, pontos, chuva visual e colisões."""

    def __init__(self, posicao_x, posicao_y, cor, velocidade_x, velocidade_y, tamanho=5, vida=0.7):
        self.posicao_x = posicao_x
        self.posicao_y = posicao_y
        self.cor = cor
        self.velocidade_x = velocidade_x
        self.velocidade_y = velocidade_y
        self.tamanho = tamanho
        self.vida = vida
        self.vida_maxima = vida

    def atualizar(self, delta_tempo):
        self.posicao_x += self.velocidade_x * delta_tempo
        self.posicao_y += self.velocidade_y * delta_tempo
        self.velocidade_y += 180 * delta_tempo
        self.vida -= delta_tempo

    def terminou(self):
        return self.vida <= 0

    def desenhar(self, tela):
        proporcao_vida = self.vida / self.vida_maxima
        raio = max(1, int(self.tamanho * proporcao_vida))
        pygame.draw.circle(tela, self.cor, (int(self.posicao_x), int(self.posicao_y)), raio)


# ==========================================
# CLASSE BOTÃO
# ==========================================

class Botao:
    """Botão reutilizável para todas as telas do jogo."""

    def __init__(self, texto, centro, largura=270, altura=54, cor=AZUL, identificador=""):
        self.texto = texto
        self.retangulo = pygame.Rect(0, 0, largura, altura)
        self.retangulo.center = centro
        self.cor = cor
        self.identificador = identificador

    def contem(self, posicao_mouse):
        return self.retangulo.collidepoint(posicao_mouse)

    def desenhar(self, tela, fonte, posicao_mouse, desabilitado=False):
        esta_sobre = self.contem(posicao_mouse) and not desabilitado
        deslocamento = -3 if esta_sobre else 0
        retangulo_desenho = self.retangulo.move(0, deslocamento)

        if desabilitado:
            cor_botao = (112, 120, 133)
        elif esta_sobre:
            cor_botao = cor_clara(self.cor, 25)
        else:
            cor_botao = self.cor

        pygame.draw.rect(tela, (33, 40, 55), self.retangulo.move(0, 5), border_radius=16)
        pygame.draw.rect(tela, cor_botao, retangulo_desenho, border_radius=16)
        pygame.draw.rect(tela, BRANCO, retangulo_desenho, width=2, border_radius=16)
        desenhar_texto(tela, self.texto, fonte, BRANCO, retangulo_desenho.center)


# ==========================================
# FUNÇÕES DE SALVAMENTO E SOM
# ==========================================

def criar_dados_padrao():
    melhores_pontuacoes = {}
    for numero_nivel in range(1, len(NIVEIS) + 1):
        melhores_pontuacoes[str(numero_nivel)] = 0

    return {
        "nivel_desbloqueado": 1,
        "melhores_pontuacoes": melhores_pontuacoes,
        "moedas": 0,
        "skins_compradas": ["padrao"],
        "skin_equipada": "padrao",
        "ranking_infinito": [],
        "conquistas": {
            "primeiro_voo": False,
            "piloto_habilidoso": False,
            "sobrevivente": False,
            "mestre_do_ceu": False,
        },
        "niveis_concluidos": [],
        "som_ativo": True,
    }


def carregar_progresso():
    """Lê o save.json; se ele não existir ou estiver inválido, cria um novo."""
    dados_padrao = criar_dados_padrao()

    if not os.path.exists(ARQUIVO_SALVAMENTO):
        salvar_progresso(dados_padrao)
        return dados_padrao

    try:
        with open(ARQUIVO_SALVAMENTO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        salvar_progresso(dados_padrao)
        return dados_padrao

    # Garante compatibilidade se uma versão antiga não tiver algum campo novo.
    for chave, valor in dados_padrao.items():
        if chave not in dados:
            dados[chave] = valor

    for numero_nivel in range(1, len(NIVEIS) + 1):
        chave_nivel = str(numero_nivel)
        if chave_nivel not in dados["melhores_pontuacoes"]:
            dados["melhores_pontuacoes"][chave_nivel] = 0

    # Compatibilidade com saves criados antes do sistema de moedas e skins.
    dados["moedas"] = max(0, int(dados.get("moedas", 0)))
    skins_compradas = dados.get("skins_compradas", ["padrao"])
    dados["skins_compradas"] = [skin for skin in skins_compradas if skin in SKINS]
    if "padrao" not in dados["skins_compradas"]:
        dados["skins_compradas"].insert(0, "padrao")
    if dados.get("skin_equipada") not in dados["skins_compradas"]:
        dados["skin_equipada"] = "padrao"
    if not isinstance(dados.get("ranking_infinito"), list):
        dados["ranking_infinito"] = []
    ranking_normalizado = []
    for item in dados["ranking_infinito"]:
        if not isinstance(item, dict):
            continue
        pilares = item.get("pilares", item.get("pontuacao"))
        if isinstance(pilares, int):
            ranking_normalizado.append({
                "nome": item.get("nome", "JOGADOR"),
                "pilares": pilares,
            })
    ranking_normalizado.sort(key=lambda item: item["pilares"], reverse=True)
    dados["ranking_infinito"] = ranking_normalizado[:10]

    salvar_progresso(dados)
    return dados


def salvar_progresso(dados):
    with open(ARQUIVO_SALVAMENTO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def carregar_sons():
    """Tenta carregar sons opcionais sem interromper o jogo se não existirem."""
    sons = {}
    arquivos = {
        "asa": "wing.wav",
        "ponto": "point.wav",
        "colisao": "hit.wav",
        "concluido": "complete.wav",
    }

    for nome, arquivo_som in arquivos.items():
        caminho = os.path.join(PASTA_SONS, arquivo_som)
        if os.path.exists(caminho):
            try:
                sons[nome] = pygame.mixer.Sound(caminho)
            except pygame.error:
                # Arquivos inválidos simplesmente não recebem som.
                pass

    return sons


def tocar_som(sons, nome, som_ativo):
    if som_ativo and nome in sons:
        sons[nome].play()


def registrar_pontuacao(progresso, numero_nivel, pontuacao):
    chave_nivel = str(numero_nivel)
    melhor_atual = progresso["melhores_pontuacoes"][chave_nivel]
    if pontuacao > melhor_atual:
        progresso["melhores_pontuacoes"][chave_nivel] = pontuacao


def registrar_pontuacao_infinita(progresso, pontuacao):
    """Insere pilares ultrapassados no ranking local e conserva o top 10."""
    progresso["ranking_infinito"].append({
        "nome": "JOGADOR",
        "pilares": int(pontuacao),
    })
    progresso["ranking_infinito"].sort(key=lambda item: item["pilares"], reverse=True)
    progresso["ranking_infinito"] = progresso["ranking_infinito"][:10]
    salvar_progresso(progresso)


def atualizar_conquistas(progresso, numero_nivel, pontuacao, nivel_concluido=False):
    """Atualiza conquistas e devolve uma lista com as conquistadas nesta rodada."""
    novas_conquistas = []
    conquistas = progresso["conquistas"]

    if nivel_concluido and numero_nivel == 1 and not conquistas["primeiro_voo"]:
        conquistas["primeiro_voo"] = True
        novas_conquistas.append("PRIMEIRO VOO")

    if pontuacao >= 20 and not conquistas["piloto_habilidoso"]:
        conquistas["piloto_habilidoso"] = True
        novas_conquistas.append("PILOTO HABILIDOSO")

    if pontuacao >= 50 and not conquistas["sobrevivente"]:
        conquistas["sobrevivente"] = True
        novas_conquistas.append("SOBREVIVENTE")

    if nivel_concluido and len(progresso["niveis_concluidos"]) == len(NIVEIS):
        if not conquistas["mestre_do_ceu"]:
            conquistas["mestre_do_ceu"] = True
            novas_conquistas.append("MESTRE DO CÉU")

    return novas_conquistas


# ==========================================
# FUNÇÕES DO MENU
# ==========================================

def desenhar_cabecalho_menu(tela, fontes, tempo):
    """Desenha o título animado compartilhado por telas de menu."""
    deslocamento = int(math.sin(tempo * 2.4) * 7)
    desenhar_texto(tela, "FLIPPY", fontes["titulo"], AMARELO, (LARGURA_TELA // 2, 80 + deslocamento))
    desenhar_texto(tela, "ADVENTURE", fontes["titulo"], BRANCO, (LARGURA_TELA // 2, 142 + deslocamento))

    # Pequeno pássaro decorativo no título.
    pygame.draw.ellipse(tela, AMARELO, (225, 102 + deslocamento, 45, 30))
    pygame.draw.polygon(tela, LARANJA, [(267, 119 + deslocamento), (282, 125 + deslocamento), (267, 131 + deslocamento)])
    pygame.draw.circle(tela, PRETO, (258, 113 + deslocamento), 3)


def desenhar_menu_principal(tela, fontes, tempo, progresso):
    tela.fill((63, 125, 193))
    desenhar_nuvem(tela, 90 - (tempo * 18) % 170, 205, 1.0, (217, 241, 255))
    desenhar_nuvem(tela, 650 - (tempo * 12) % 220, 255, 1.3, (217, 241, 255))
    pygame.draw.ellipse(tela, (54, 139, 80), (-50, 500, 1080, 150))
    desenhar_cabecalho_menu(tela, fontes, tempo)

    botoes = [
        Botao("JOGAR", (LARGURA_TELA // 2, 225), identificador="jogar"),
        Botao("ESCOLHER NÍVEL", (LARGURA_TELA // 2, 287), cor=ROXO, identificador="niveis"),
        Botao("LOJA DE SKINS", (LARGURA_TELA // 2, 349), cor=AMARELO, identificador="loja"),
        Botao("COMO JOGAR", (LARGURA_TELA // 2, 411), cor=VERDE, identificador="ajuda"),
        Botao("SAIR", (LARGURA_TELA // 2, 473), cor=VERMELHO, identificador="sair"),
    ]

    texto_som = "SOM: ON"
    cor_som = VERDE
    if not progresso["som_ativo"]:
        texto_som = "SOM: OFF"
        cor_som = VERMELHO
    botoes.append(Botao(texto_som, (840, 550), 150, 42, cor_som, "som"))
    botoes.append(Botao("RANKING", (280, 550), 150, 42, AZUL, "ranking"))

    posicao_mouse = pygame.mouse.get_pos()
    for botao in botoes:
        botao.desenhar(tela, fontes["botao"], posicao_mouse)

    desenhar_texto(tela, "Cada pilar ultrapassado vale 1 moeda", fontes["pequena"], BRANCO, (LARGURA_TELA // 2, 520))
    desenhar_texto(tela, "MOEDAS: " + str(progresso["moedas"]), fontes["botao"], AMARELO, (480, 550), False)
    if progresso["nivel_desbloqueado"] < len(NIVEIS) + 1:
        desenhar_texto(tela, "Conclua a fase 9 para liberar a fase 10", fontes["pequena"], CINZA_CLARO, (480, 578), False)
    return botoes


# ==========================================
# FUNÇÕES DA LOJA DE SKINS
# ==========================================

def desenhar_preview_skin(tela, skin_id, centro):
    """Desenha uma prévia simples da skin sem alterar o desenho original do jogador."""
    skin = SKINS[skin_id]
    x, y = centro
    pygame.draw.ellipse(tela, skin["asa"], (x - 54, y - 4, 45, 28))
    pygame.draw.ellipse(tela, skin["corpo"], (x - 35, y - 27, 70, 55))
    pygame.draw.ellipse(tela, (255, 229, 133), (x - 10, y - 6, 34, 26))
    pygame.draw.circle(tela, BRANCO, (x + 22, y - 17), 11)
    pygame.draw.circle(tela, PRETO, (x + 24, y - 17), 4)
    pygame.draw.polygon(tela, skin["bico"], [(x + 32, y - 8), (x + 55, y), (x + 32, y + 8)])
    pygame.draw.ellipse(tela, skin["asa"], (x - 12, y + 8, 38, 20))


def desenhar_loja_skins(tela, fontes, progresso):
    tela.fill((38, 56, 88))
    desenhar_texto(tela, "LOJA DE SKINS", fontes["subtitulo"], BRANCO, (LARGURA_TELA // 2, 48))
    desenhar_texto(tela, "Ganhe moedas passando pelos pilares e personalize seu pássaro", fontes["pequena"], CINZA_CLARO, (LARGURA_TELA // 2, 82))
    desenhar_painel(tela, pygame.Rect(350, 95, 260, 48), (20, 30, 48, 220), 14)
    desenhar_texto(tela, "MOEDAS: " + str(progresso["moedas"]), fontes["botao"], AMARELO, (480, 119), False)

    botoes = []
    posicao_mouse = pygame.mouse.get_pos()
    posicoes = [(175, 300), (480, 300), (785, 300)]
    for (skin_id, skin), centro in zip(SKINS.items(), posicoes):
        cartao = pygame.Rect(55 + posicoes.index(centro) * 305, 155, 240, 285)
        desenhar_painel(tela, cartao, (235, 240, 245, 235), 18)
        pygame.draw.rect(tela, AMARELO if progresso["skin_equipada"] == skin_id else CINZA_ESCURO, cartao, 3, border_radius=18)
        desenhar_texto(tela, skin["nome"], fontes["media"], PRETO, (cartao.centerx, cartao.y + 32), False)
        desenhar_preview_skin(tela, skin_id, (cartao.centerx, cartao.y + 112))

        if skin_id in progresso["skins_compradas"]:
            status = "EQUIPADA" if progresso["skin_equipada"] == skin_id else "EQUIPAR"
            cor = VERDE if status == "EQUIPADA" else AZUL
            botao = Botao(status, (cartao.centerx, cartao.bottom - 43), 170, 42, cor, "skin_" + skin_id)
        else:
            preco = skin["preco"]
            status = "COMPRAR " + str(preco) + " MOEDAS"
            cor = VERDE if progresso["moedas"] >= preco else (112, 120, 133)
            botao = Botao(status, (cartao.centerx, cartao.bottom - 43), 190, 42, cor, "skin_" + skin_id)
        botao.desenhar(tela, fontes["pequena"], posicao_mouse, status.startswith("COMPRAR") and progresso["moedas"] < skin["preco"])
        botoes.append(botao)

    desenhar_texto(tela, "A skin padrão é grátis. Existem 2 skins extras nesta versão.", fontes["pequena"], CINZA_CLARO, (LARGURA_TELA // 2, 468), False)
    botao_voltar = Botao("VOLTAR", (LARGURA_TELA // 2, 548), 210, 45, VERMELHO, "voltar")
    botao_voltar.desenhar(tela, fontes["botao"], posicao_mouse)
    botoes.append(botao_voltar)
    return botoes


def desenhar_ranking(tela, fontes, progresso):
    tela.fill((31, 42, 70))
    desenhar_texto(tela, "RANKING INFINITO", fontes["subtitulo"], AMARELO, (LARGURA_TELA // 2, 58))
    desenhar_texto(tela, "Tabela dos pilares ultrapassados na fase 10", fontes["pequena"], CINZA_CLARO, (LARGURA_TELA // 2, 92))

    painel = pygame.Rect(210, 125, 540, 365)
    desenhar_painel(tela, painel, (235, 240, 245, 235), 18)
    desenhar_texto(tela, "POSIÇÃO", fontes["pequena"], CINZA_ESCURO, (285, 155), False)
    desenhar_texto(tela, "PILOTO", fontes["pequena"], CINZA_ESCURO, (470, 155), False)
    desenhar_texto(tela, "PILARES", fontes["pequena"], CINZA_ESCURO, (665, 155), False)

    ranking = progresso["ranking_infinito"]
    if not ranking:
        desenhar_texto(tela, "Ainda não há voos infinitos registrados.", fontes["media"], CINZA_ESCURO, painel.center, False)
    else:
        for indice, item in enumerate(ranking):
            posicao_y = 190 + indice * 27
            cor = (177, 128, 39) if indice == 0 else PRETO
            desenhar_texto(tela, str(indice + 1), fontes["botao"], cor, (285, posicao_y), False)
            desenhar_texto(tela, item.get("nome", "JOGADOR"), fontes["pequena"], PRETO, (470, posicao_y), False)
            desenhar_texto(tela, str(item["pilares"]), fontes["botao"], cor, (665, posicao_y), False)

    botao_voltar = Botao("VOLTAR", (LARGURA_TELA // 2, 548), 210, 45, VERMELHO, "voltar")
    botao_voltar.desenhar(tela, fontes["botao"], pygame.mouse.get_pos())
    return [botao_voltar]


# ==========================================
# FUNÇÕES DA SELEÇÃO DE NÍVEL
# ==========================================

def desenhar_selecao_nivel(tela, fontes, tempo, progresso, deslocamento_rolagem=0):
    tela.fill((38, 56, 88))
    desenhar_texto(tela, "ESCOLHER NÍVEL", fontes["subtitulo"], BRANCO, (LARGURA_TELA // 2, 54))
    desenhar_texto(tela, "Complete cada meta para abrir a próxima aventura", fontes["pequena"], CINZA_CLARO, (LARGURA_TELA // 2, 88))

    botoes = []
    posicao_mouse = pygame.mouse.get_pos()
    area_lista = pygame.Rect(45, 112, 855, 410)
    tela.set_clip(area_lista)

    for indice, nivel in enumerate(NIVEIS):
        coluna = indice % 3
        linha = indice // 3
        posicao_x = 85 + coluna * 295
        posicao_y = 125 + linha * 190 - deslocamento_rolagem
        cartao = pygame.Rect(posicao_x, posicao_y, 245, 175)
        numero_nivel = indice + 1
        desbloqueado = numero_nivel <= progresso["nivel_desbloqueado"]
        melhor = progresso["melhores_pontuacoes"][str(numero_nivel)]

        cor_cartao = nivel["cor_ceu"]
        if not desbloqueado:
            cor_cartao = (79, 86, 105)
        desenhar_painel(tela, cartao, (*cor_cartao, 230))
        pygame.draw.rect(tela, BRANCO, cartao, 2, border_radius=18)
        desenhar_texto(tela, "NÍVEL " + str(numero_nivel), fontes["botao"], BRANCO, (cartao.centerx, cartao.y + 30))
        desenhar_texto(tela, nivel["nome"], fontes["media"], AMARELO if desbloqueado else CINZA_CLARO, (cartao.centerx, cartao.y + 67))

        if desbloqueado:
            status = "DESBLOQUEADO"
            cor_status = (210, 255, 201)
        else:
            status = "BLOQUEADO"
            cor_status = (255, 205, 205)
            pygame.draw.circle(tela, (48, 53, 66), (cartao.centerx, cartao.y + 112), 15)
            pygame.draw.rect(tela, CINZA_CLARO, (cartao.centerx - 8, cartao.y + 112, 16, 13), border_radius=3)
            pygame.draw.arc(tela, CINZA_CLARO, (cartao.centerx - 8, cartao.y + 101, 16, 18), math.pi, 0, 2)

        desenhar_texto(tela, status, fontes["pequena"], cor_status, (cartao.centerx, cartao.y + 108))
        desenhar_texto(tela, "MELHOR: " + str(melhor), fontes["pequena"], BRANCO, (cartao.centerx, cartao.y + 143))

        if cartao.bottom >= area_lista.top and cartao.top <= area_lista.bottom:
            botao_cartao = Botao("", cartao.center, cartao.width, cartao.height, identificador="nivel_" + str(numero_nivel))
            botoes.append(botao_cartao)

    # Fase 10: modo infinito, liberado somente após concluir CÉU.
    numero_nivel = len(NIVEIS) + 1
    coluna = 1
    linha = (numero_nivel - 1) // 3
    posicao_x = 85 + coluna * 295
    posicao_y = 125 + linha * 190 - deslocamento_rolagem
    cartao = pygame.Rect(posicao_x, posicao_y, 245, 175)
    desbloqueado = progresso["nivel_desbloqueado"] >= numero_nivel
    cor_cartao = (100, 76, 151) if desbloqueado else (79, 86, 105)
    desenhar_painel(tela, cartao, (*cor_cartao, 235))
    pygame.draw.rect(tela, AMARELO if desbloqueado else CINZA_CLARO, cartao, 2, border_radius=18)
    desenhar_texto(tela, "FASE 10", fontes["botao"], BRANCO, (cartao.centerx, cartao.y + 30))
    desenhar_texto(tela, "INFINITO", fontes["media"], AMARELO if desbloqueado else CINZA_CLARO, (cartao.centerx, cartao.y + 67))
    status = "DISPONÍVEL" if desbloqueado else "BLOQUEADO"
    cor_status = (210, 255, 201) if desbloqueado else (255, 205, 205)
    desenhar_texto(tela, status, fontes["pequena"], cor_status, (cartao.centerx, cartao.y + 108))
    desenhar_texto(tela, "RANKING POR PILARES", fontes["pequena"], BRANCO, (cartao.centerx, cartao.y + 143))
    if cartao.bottom >= area_lista.top and cartao.top <= area_lista.bottom:
        botoes.append(Botao("", cartao.center, cartao.width, cartao.height, identificador="infinito"))

    tela.set_clip(None)

    # Barra de rolagem visível somente quando a lista ultrapassa a área disponível.
    total_cartoes = len(NIVEIS) + 1
    altura_conteudo = ((total_cartoes + 2) // 3) * 190 + 10
    altura_trilho = area_lista.height
    if altura_conteudo > altura_trilho:
        pygame.draw.rect(tela, (25, 38, 61), (915, area_lista.top, 12, altura_trilho), border_radius=6)
        altura_bolinha = max(48, int(altura_trilho * altura_trilho / altura_conteudo))
        limite_bolinha = altura_trilho - altura_bolinha
        maximo_rolagem = altura_conteudo - altura_trilho
        posicao_bolinha = area_lista.top + int((deslocamento_rolagem / maximo_rolagem) * limite_bolinha)
        pygame.draw.rect(tela, (179, 220, 239), (915, posicao_bolinha, 12, altura_bolinha), border_radius=6)
        desenhar_texto(tela, "ROLE", fontes["pequena"], CINZA_CLARO, (875, 535), False)

    botao_voltar = Botao("VOLTAR", (LARGURA_TELA // 2, 558), 210, 45, VERMELHO, "voltar")
    botao_voltar.desenhar(tela, fontes["botao"], posicao_mouse)
    botoes.append(botao_voltar)
    return botoes


# ==========================================
# FUNÇÕES DE GAMEPLAY
# ==========================================

def iniciar_nivel(numero_nivel, skin="padrao"):
    """Cria todas as variáveis que pertencem a uma nova rodada."""
    nivel = NIVEIS[numero_nivel - 1]
    return {
        "numero_nivel": numero_nivel,
        "nivel": nivel,
        "jogador": Jogador(skin),
        "obstaculos": [],
        "particulas": [],
        "elementos": criar_elementos_cenario(nivel["tema"]),
        "pontuacao": 0,
        "moedas_ganhas": 0,
        "modo_infinito": False,
        "indice_infinito": numero_nivel - 1,
        "tempo": 0.0,
        "tempo_para_obstaculo": 1.1,
        "novas_conquistas": [],
    }


def iniciar_modo_infinito(skin="padrao"):
    """Começa a maratona na fase 1 e permite avançar por todos os mundos."""
    rodada = iniciar_nivel(1, skin)
    rodada["modo_infinito"] = True
    rodada["meta_infinita"] = 0
    return rodada


def criar_particulas_de_asa(particulas, jogador):
    for indice in range(6):
        particula = Particula(
            jogador.posicao_x - 18,
            jogador.posicao_y + 9,
            (255, 234, 154),
            random.randint(-130, -35),
            random.randint(-65, 65),
            random.randint(3, 6),
            0.45,
        )
        particulas.append(particula)


def criar_particulas_de_colisao(particulas, jogador):
    for indice in range(28):
        particula = Particula(
            jogador.posicao_x,
            jogador.posicao_y,
            random.choice([AMARELO, LARANJA, BRANCO]),
            random.randint(-230, 230),
            random.randint(-240, 100),
            random.randint(3, 7),
            0.9,
        )
        particulas.append(particula)


def atualizar_gameplay(rodada, delta_tempo, progresso, sons):
    """Atualiza física, obstáculos, partículas, pontos e colisões."""
    rodada["tempo"] += delta_tempo
    rodada["tempo_para_obstaculo"] -= delta_tempo
    jogador = rodada["jogador"]
    jogador.atualizar(delta_tempo)

    if rodada["tempo_para_obstaculo"] <= 0:
        nivel = rodada["nivel"]
        margem = 80
        altura_maxima = ALTURA_TELA - ALTURA_CHAO - nivel["espaco"] - margem
        altura_superior = random.randint(margem, altura_maxima)
        novo_obstaculo = Obstaculo(LARGURA_TELA + 35, altura_superior, nivel)
        rodada["obstaculos"].append(novo_obstaculo)
        rodada["tempo_para_obstaculo"] = nivel["intervalo"]

    for obstaculo in rodada["obstaculos"]:
        obstaculo.mover(delta_tempo)

        if not obstaculo.ja_deu_ponto and obstaculo.posicao_x + obstaculo.largura < jogador.posicao_x:
            obstaculo.ja_deu_ponto = True
            rodada["pontuacao"] += 1
            rodada["moedas_ganhas"] += 1
            progresso["moedas"] += 1
            salvar_progresso(progresso)
            tocar_som(sons, "ponto", progresso["som_ativo"])

            for indice in range(10):
                rodada["particulas"].append(
                    Particula(jogador.posicao_x, jogador.posicao_y, BRANCO, random.randint(-90, 90), random.randint(-110, 40), 4, 0.45)
                )

    for obstaculo in rodada["obstaculos"]:
        if obstaculo.colidiu_com(jogador):
            return "gameover"

    if jogador.rect.bottom >= ALTURA_TELA - ALTURA_CHAO:
        return "gameover"

    # A lista é filtrada com um for tradicional para facilitar o entendimento.
    obstaculos_restantes = []
    for obstaculo in rodada["obstaculos"]:
        if not obstaculo.saiu_da_tela():
            obstaculos_restantes.append(obstaculo)
    rodada["obstaculos"] = obstaculos_restantes

    particulas_restantes = []
    for particula in rodada["particulas"]:
        particula.atualizar(delta_tempo)
        if not particula.terminou():
            particulas_restantes.append(particula)
    rodada["particulas"] = particulas_restantes

    if rodada["pontuacao"] >= rodada["nivel"]["meta"]:
        if rodada.get("modo_infinito"):
            proximo_indice = (rodada["indice_infinito"] + 1) % len(NIVEIS)
            rodada["indice_infinito"] = proximo_indice
            rodada["numero_nivel"] = proximo_indice + 1
            rodada["nivel"] = NIVEIS[proximo_indice]
            rodada["elementos"] = criar_elementos_cenario(rodada["nivel"]["tema"])
            rodada["obstaculos"] = []
            rodada["tempo_para_obstaculo"] = 0.55
            return "jogando"
        return "concluido"

    return "jogando"


def desenhar_gameplay(tela, fontes, rodada, progresso):
    nivel = rodada["nivel"]
    desenhar_cenario(tela, nivel, rodada["tempo"], rodada["elementos"])

    for obstaculo in rodada["obstaculos"]:
        obstaculo.desenhar(tela)

    for particula in rodada["particulas"]:
        particula.desenhar(tela)

    rodada["jogador"].desenhar(tela)

    desenhar_painel(tela, pygame.Rect(20, 18, 190, 106), (20, 30, 48, 170), 14)
    desenhar_texto(tela, "PONTOS: " + str(rodada["pontuacao"]), fontes["botao"], BRANCO, (115, 45), False)
    desenhar_texto(tela, "META: " + str(nivel["meta"]), fontes["pequena"], AMARELO, (115, 75), False)
    melhor = progresso["melhores_pontuacoes"][str(rodada["numero_nivel"])]
    desenhar_texto(tela, "MELHOR: " + str(melhor), fontes["pequena"], BRANCO, (115, 101), False)
    desenhar_painel(tela, pygame.Rect(225, 18, 150, 58), (20, 30, 48, 170), 14)
    desenhar_texto(tela, "MOEDAS: " + str(progresso["moedas"]), fontes["botao"], AMARELO, (300, 47), False)
    desenhar_texto(tela, "+1 POR PILAR", fontes["pequena"], BRANCO, (300, 67), False)
    desenhar_texto(tela, nivel["nome"], fontes["media"], BRANCO, (LARGURA_TELA - 115, 36))
    desenhar_texto(tela, "ESC: PAUSA", fontes["pequena"], BRANCO, (LARGURA_TELA - 95, 67))


# ==========================================
# FUNÇÕES DO GAME OVER
# ==========================================

def desenhar_game_over(tela, fontes, rodada, progresso):
    desenhar_gameplay(tela, fontes, rodada, progresso)
    camada = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    camada.fill((15, 18, 30, 175))
    tela.blit(camada, (0, 0))

    painel = pygame.Rect(270, 115, 420, 405)
    desenhar_painel(tela, painel)
    desenhar_texto(tela, "GAME OVER", fontes["titulo"], VERMELHO, (LARGURA_TELA // 2, 167))
    desenhar_texto(tela, "PONTUAÇÃO: " + str(rodada["pontuacao"]), fontes["media"], PRETO, (LARGURA_TELA // 2, 224), False)
    melhor = progresso["melhores_pontuacoes"][str(rodada["numero_nivel"])]
    desenhar_texto(tela, "MELHOR: " + str(melhor), fontes["media"], PRETO, (LARGURA_TELA // 2, 256), False)

    botoes = [
        Botao("TENTAR NOVAMENTE", (LARGURA_TELA // 2, 323), 300, 50, AZUL, "reiniciar"),
        Botao("ESCOLHER NÍVEL", (LARGURA_TELA // 2, 385), 300, 50, ROXO, "niveis"),
        Botao("MENU", (LARGURA_TELA // 2, 447), 300, 50, VERMELHO, "menu"),
    ]
    posicao_mouse = pygame.mouse.get_pos()
    for botao in botoes:
        botao.desenhar(tela, fontes["botao"], posicao_mouse)
    desenhar_texto(tela, "Pressione R para reiniciar", fontes["pequena"], CINZA_ESCURO, (LARGURA_TELA // 2, 488), False)
    return botoes


# ==========================================
# FUNÇÕES DA PAUSA
# ==========================================

def desenhar_pausa(tela, fontes, rodada, progresso):
    desenhar_gameplay(tela, fontes, rodada, progresso)
    camada = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    camada.fill((18, 24, 39, 190))
    tela.blit(camada, (0, 0))
    painel = pygame.Rect(290, 130, 380, 345)
    desenhar_painel(tela, painel)
    desenhar_texto(tela, "JOGO PAUSADO", fontes["subtitulo"], ROXO, (LARGURA_TELA // 2, 185))

    botoes = [
        Botao("CONTINUAR", (LARGURA_TELA // 2, 247), 280, 50, VERDE, "continuar"),
        Botao("REINICIAR", (LARGURA_TELA // 2, 310), 280, 50, AZUL, "reiniciar"),
        Botao("SAIR PARA O MENU", (LARGURA_TELA // 2, 373), 280, 50, VERMELHO, "menu"),
    ]
    posicao_mouse = pygame.mouse.get_pos()
    for botao in botoes:
        botao.desenhar(tela, fontes["botao"], posicao_mouse)
    desenhar_texto(tela, "ESC também continua", fontes["pequena"], CINZA_ESCURO, (LARGURA_TELA // 2, 427), False)
    return botoes


# ==========================================
# TELAS COMPLEMENTARES
# ==========================================

def desenhar_como_jogar(tela, fontes):
    tela.fill((44, 86, 132))
    painel = pygame.Rect(150, 55, 660, 475)
    desenhar_painel(tela, painel)
    desenhar_texto(tela, "COMO JOGAR", fontes["subtitulo"], AZUL, (LARGURA_TELA // 2, 100))

    instrucoes = [
        ("ESPAÇO ou CLIQUE", "Bata as asas."),
        ("EVITE OS OBSTÁCULOS", "Passe pelo espaço entre eles."),
        ("GANHE PONTOS", "Cada obstáculo ultrapassado vale 1 ponto."),
        ("COMPLETE OS NÍVEIS", "Alcance a meta para desbloquear o próximo mapa."),
        ("ESC", "Pausa o jogo."),
    ]
    posicao_y = 153
    for titulo, explicacao in instrucoes:
        desenhar_texto(tela, titulo, fontes["botao"], PRETO, (LARGURA_TELA // 2, posicao_y), False)
        desenhar_texto(tela, explicacao, fontes["pequena"], CINZA_ESCURO, (LARGURA_TELA // 2, posicao_y + 25), False)
        posicao_y += 62

    botao_voltar = Botao("VOLTAR", (LARGURA_TELA // 2, 475), 220, 48, VERMELHO, "voltar")
    botao_voltar.desenhar(tela, fontes["botao"], pygame.mouse.get_pos())
    return [botao_voltar]


def desenhar_nivel_concluido(tela, fontes, rodada, progresso):
    desenhar_cenario(tela, rodada["nivel"], rodada["tempo"], rodada["elementos"])
    camada = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    camada.fill((20, 30, 43, 145))
    tela.blit(camada, (0, 0))
    painel = pygame.Rect(250, 70, 460, 470)
    desenhar_painel(tela, painel)
    desenhar_texto(tela, "NÍVEL CONCLUÍDO!", fontes["subtitulo"], VERDE, (LARGURA_TELA // 2, 118))
    desenhar_texto(tela, "Pontuação: " + str(rodada["pontuacao"]), fontes["media"], PRETO, (LARGURA_TELA // 2, 164), False)
    desenhar_texto(tela, "PARABÉNS!", fontes["media"], LARANJA, (LARGURA_TELA // 2, 200), False)

    nome_medalha, cor_medalha = medalha_da_pontuacao(rodada["pontuacao"])
    pygame.draw.circle(tela, cor_medalha, (LARGURA_TELA // 2, 247), 30)
    pygame.draw.circle(tela, BRANCO, (LARGURA_TELA // 2, 247), 30, 2)
    desenhar_texto(tela, nome_medalha, fontes["pequena"], PRETO, (LARGURA_TELA // 2, 247), False)

    if rodada["novas_conquistas"]:
        texto = "CONQUISTA: " + rodada["novas_conquistas"][0]
        desenhar_texto(tela, texto, fontes["pequena"], ROXO, (LARGURA_TELA // 2, 296), False)

    botoes = []
    if rodada["numero_nivel"] < len(NIVEIS):
        proximo_texto = "PRÓXIMO NÍVEL"
        botoes.append(Botao(proximo_texto, (LARGURA_TELA // 2, 366), 300, 52, AZUL, "proximo"))
        botao_menu_y = 432
    else:
        desenhar_texto(tela, "Você dominou todas as aventuras!", fontes["pequena"], ROXO, (LARGURA_TELA // 2, 364), False)
        botao_menu_y = 425

    botoes.append(Botao("MENU", (LARGURA_TELA // 2, botao_menu_y), 300, 52, VERMELHO, "menu"))
    posicao_mouse = pygame.mouse.get_pos()
    for botao in botoes:
        botao.desenhar(tela, fontes["botao"], posicao_mouse)
    return botoes


# ==========================================
# LOOP PRINCIPAL
# ==========================================

def main():
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        # Alguns computadores não possuem dispositivo de áudio disponível.
        pass

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Flippy Adventure")
    relogio = pygame.time.Clock()

    fontes = {
        "titulo": pygame.font.SysFont("arial", 48, bold=True),
        "subtitulo": pygame.font.SysFont("arial", 35, bold=True),
        "media": pygame.font.SysFont("arial", 24, bold=True),
        "botao": pygame.font.SysFont("arial", 20, bold=True),
        "pequena": pygame.font.SysFont("arial", 16),
    }

    progresso = carregar_progresso()
    sons = carregar_sons()
    estado = "menu"
    rolagem_niveis = 0
    rodada = None
    botoes_ativos = []
    rodando = True
    tempo_menu = 0.0

    while rodando:
        delta_tempo = relogio.tick(TAXA_DE_QUADROS) / 1000.0
        tempo_menu += delta_tempo

        # Primeiro tratamos os eventos: teclado, mouse e fechamento da janela.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if estado == "jogando":
                    if evento.key == pygame.K_SPACE:
                        rodada["jogador"].bater_asas()
                        criar_particulas_de_asa(rodada["particulas"], rodada["jogador"])
                        tocar_som(sons, "asa", progresso["som_ativo"])
                    elif evento.key == pygame.K_ESCAPE:
                        estado = "pausado"

                elif estado == "pausado":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "jogando"

                elif estado == "gameover":
                    if evento.key == pygame.K_r:
                        if rodada.get("modo_infinito"):
                            rodada = iniciar_modo_infinito(progresso["skin_equipada"])
                        else:
                            rodada = iniciar_nivel(rodada["numero_nivel"], progresso["skin_equipada"])
                        estado = "jogando"

                elif estado == "ajuda":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "menu"

                elif estado == "loja":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "menu"

                elif estado == "ranking":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "menu"

                elif estado == "niveis":
                    if evento.key == pygame.K_ESCAPE:
                        estado = "menu"

            if evento.type == pygame.MOUSEWHEEL and estado == "niveis":
                altura_conteudo = (((len(NIVEIS) + 1) + 2) // 3) * 190 + 10
                maximo_rolagem = max(0, altura_conteudo - 410)
                rolagem_niveis -= evento.y * 45
                rolagem_niveis = limitar(rolagem_niveis, 0, maximo_rolagem)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                posicao_clique = evento.pos

                if estado == "jogando":
                    rodada["jogador"].bater_asas()
                    criar_particulas_de_asa(rodada["particulas"], rodada["jogador"])
                    tocar_som(sons, "asa", progresso["som_ativo"])
                else:
                    for botao in botoes_ativos:
                        if botao.contem(posicao_clique):
                            acao = botao.identificador

                            if acao == "jogar":
                                nivel_inicial = min(progresso["nivel_desbloqueado"], len(NIVEIS))
                                rodada = iniciar_nivel(nivel_inicial, progresso["skin_equipada"])
                                estado = "jogando"
                            elif acao == "niveis":
                                estado = "niveis"
                                rolagem_niveis = 0
                            elif acao == "loja":
                                estado = "loja"
                            elif acao == "infinito":
                                if progresso["nivel_desbloqueado"] >= len(NIVEIS) + 1:
                                    rodada = iniciar_modo_infinito(progresso["skin_equipada"])
                                    estado = "jogando"
                            elif acao == "ranking":
                                estado = "ranking"
                            elif acao == "ajuda":
                                estado = "ajuda"
                            elif acao == "sair":
                                rodando = False
                            elif acao == "som":
                                progresso["som_ativo"] = not progresso["som_ativo"]
                                salvar_progresso(progresso)
                            elif acao == "voltar":
                                estado = "menu"
                            elif acao == "menu":
                                estado = "menu"
                            elif acao == "continuar":
                                estado = "jogando"
                            elif acao == "reiniciar":
                                if rodada.get("modo_infinito"):
                                    rodada = iniciar_modo_infinito(progresso["skin_equipada"])
                                else:
                                    rodada = iniciar_nivel(rodada["numero_nivel"], progresso["skin_equipada"])
                                estado = "jogando"
                            elif acao == "proximo":
                                proximo_nivel = rodada["numero_nivel"] + 1
                                rodada = iniciar_nivel(proximo_nivel, progresso["skin_equipada"])
                                estado = "jogando"
                            elif acao.startswith("nivel_"):
                                numero_nivel = int(acao.split("_")[1])
                                if numero_nivel <= progresso["nivel_desbloqueado"]:
                                    rodada = iniciar_nivel(numero_nivel, progresso["skin_equipada"])
                                    estado = "jogando"
                            elif acao.startswith("skin_"):
                                skin_id = acao[5:]
                                skin = SKINS[skin_id]
                                if skin_id not in progresso["skins_compradas"]:
                                    if progresso["moedas"] >= skin["preco"]:
                                        progresso["moedas"] -= skin["preco"]
                                        progresso["skins_compradas"].append(skin_id)
                                        progresso["skin_equipada"] = skin_id
                                        salvar_progresso(progresso)
                                else:
                                    progresso["skin_equipada"] = skin_id
                                    salvar_progresso(progresso)

        # A física só é atualizada enquanto a rodada está ativa.
        if estado == "jogando":
            resultado = atualizar_gameplay(rodada, delta_tempo, progresso, sons)

            if resultado == "gameover":
                criar_particulas_de_colisao(rodada["particulas"], rodada["jogador"])
                if rodada.get("modo_infinito"):
                    registrar_pontuacao_infinita(progresso, rodada["pontuacao"])
                else:
                    registrar_pontuacao(progresso, rodada["numero_nivel"], rodada["pontuacao"])
                    atualizar_conquistas(progresso, rodada["numero_nivel"], rodada["pontuacao"])
                salvar_progresso(progresso)
                tocar_som(sons, "colisao", progresso["som_ativo"])
                estado = "gameover"

            elif resultado == "concluido":
                numero_nivel = rodada["numero_nivel"]
                registrar_pontuacao(progresso, numero_nivel, rodada["pontuacao"])
                if numero_nivel not in progresso["niveis_concluidos"]:
                    progresso["niveis_concluidos"].append(numero_nivel)
                if numero_nivel < len(NIVEIS) and progresso["nivel_desbloqueado"] <= numero_nivel:
                    progresso["nivel_desbloqueado"] = numero_nivel + 1
                elif numero_nivel == len(NIVEIS) and progresso["nivel_desbloqueado"] <= numero_nivel:
                    progresso["nivel_desbloqueado"] = len(NIVEIS) + 1
                rodada["novas_conquistas"] = atualizar_conquistas(progresso, numero_nivel, rodada["pontuacao"], True)
                salvar_progresso(progresso)
                tocar_som(sons, "concluido", progresso["som_ativo"])
                estado = "concluido"

        # Por último desenhamos a tela correspondente ao estado atual.
        if estado == "menu":
            botoes_ativos = desenhar_menu_principal(tela, fontes, tempo_menu, progresso)
        elif estado == "niveis":
            botoes_ativos = desenhar_selecao_nivel(tela, fontes, tempo_menu, progresso, rolagem_niveis)
        elif estado == "loja":
            botoes_ativos = desenhar_loja_skins(tela, fontes, progresso)
        elif estado == "ranking":
            botoes_ativos = desenhar_ranking(tela, fontes, progresso)
        elif estado == "ajuda":
            botoes_ativos = desenhar_como_jogar(tela, fontes)
        elif estado == "jogando":
            botoes_ativos = []
            desenhar_gameplay(tela, fontes, rodada, progresso)
        elif estado == "pausado":
            botoes_ativos = desenhar_pausa(tela, fontes, rodada, progresso)
        elif estado == "gameover":
            botoes_ativos = desenhar_game_over(tela, fontes, rodada, progresso)
        elif estado == "concluido":
            botoes_ativos = desenhar_nivel_concluido(tela, fontes, rodada, progresso)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
