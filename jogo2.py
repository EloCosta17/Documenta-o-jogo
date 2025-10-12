import pygame
import sys
import random

# música
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load("sons/musica_de_fundo.mp3")
pygame.mixer.music.play(-1)

som_certo = pygame.mixer.Sound("sons/aparecer_letra.mp3")
# --------- Configurações ---------
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CORAL = (229, 65, 51, 1)
GRAY = (230, 230, 230)
BLUE = (0, 100, 200)

pygame.display.set_caption("Menu Inicial - Jogo Exemplo")
FONT = pygame.font.SysFont("Goudy Stout", 48)
FONT_MSG = pygame.font.Font(None, 36)

# Temas do jogo
temas = {
    "Professores": ["hugo", "joaildo", "eugenio", "saulo", "geam", "botinni"],
    "Matérias": ["matematica", "geografia", "biologia", "fisica", "quimica", "ingles"],
    "Geral": ["thales", "ricardo", "rose", "bloco d", "max", "artes"],
    "Cursos": {
        "Informática": ["python", "desing web", "iuri", "processador", "romerito", "java"],
        "Vestuário": ["croqui", "laila", "modelagem", "confecção", "cad", "confecção"],
        "Eletrotécnica": ["circuito", "transformador", "jonas", "condutor", "isolamento","francisco"],
        "Têxtil": ["algodão", "beneficiamento", "tecelagem", "tingimento","padronagem","alvejamento"]
    }
}

# Efeito máquina de escrever
def texto_digitado(surface, texto, x, y, cor, delay=20):
    exibindo = ""
    for letra in texto:
        exibindo += letra
        render = FONT_MSG.render(exibindo, True, cor)
        surface.blit(render, (x, y))
        pygame.display.flip()
        pygame.time.delay(delay)

def tela_intro(screen, background):
    screen.blit(background, (0, 0))

    largura = 900
    altura = 200
    screen_width, screen_height = screen.get_size()
    x = (screen_width - largura) // 2
    y = (screen_height - altura) // 2

    # Container semi-transparente
    container = pygame.Surface((largura, altura))
    container.set_alpha(200)
    container.fill(WHITE)
    screen.blit(container, (x, y))

    texto_digitado(screen,"Bem-vindo ao jogo da forca!", x + 20, y + 40, BLACK, delay=20)
    texto_digitado(screen,"Escolha um tema sobre o IFRN-Caicó e acerte as letras para descobrir", x + 20, y + 80, BLACK, delay=20)
    texto_digitado(screen,"a palavra, e lembre-se, você pode errar apenas 6 vezes!", x + 20, y + 120, BLACK, delay=20)

    pygame.display.flip()
    pygame.time.delay(2000)

class Button:
    def __init__(self, text, pos, callback, small=False, tema=False):
        self.text = text
        self.callback = callback

        if tema:
            self.default_color = BLACK  
            self.highlight_color = CORAL
        else:
            self.default_color = WHITE   
            self.highlight_color = CORAL

        if small:
            font = pygame.font.SysFont("Goudy Stout", 28)
        else:
            font = FONT

        self.label = font.render(self.text, True, self.default_color)
        self.rect = self.label.get_rect(center=pos)
        self.font = font

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            label = self.font.render(self.text, True, self.highlight_color)
        else:
            label = self.font.render(self.text, True, self.default_color)
        surface.blit(label, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

# Menu principal
class Menu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = pygame.transform.scale(background, screen.get_size())
        screen_width, screen_height = screen.get_size()

        mid_x = screen_width // 2
        start_y = screen_height // 2 - 240
        gap = 80

        self.buttons = [
            Button("Iniciar Jogo", (mid_x, start_y), self.start_game),
            Button("Opções",(mid_x, start_y + gap), self.show_options),
            Button("Sair",(mid_x, start_y + 2 * gap), self.exit_game),
        ]
        self.running = True

    def start_game(self):
        tela_intro(self.screen, self.background)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        escolha = None
        while True:
            temas_menu = Temas(self.screen, self.background)
            escolha = temas_menu.run()

            if escolha == "Cursos":
                while True:
                    cursos = Temas(self.screen, self.background, modo="cursos")
                    escolha_curso = cursos.run()
                    if escolha_curso == "Voltar":
                        break
                    else:
                        escolha = escolha_curso
                        break
                if escolha == "Cursos":
                    continue
                else:
                    break
            else:
                break

        print("Tema escolhido:", escolha)

        # Escolha aleatória da palavra
        if escolha in ["Informática", "Vestuário", "Eletrotécnica", "Têxtil"]:
            palavra = random.choice(temas["Cursos"][escolha])
        else:
            palavra = random.choice(temas[escolha])

        jogar(self.screen, palavra, self.background, escolha)
        self.running = False

    def show_options(self):
        print("Abrindo opções...")

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            self.screen.blit(self.background, (0, 0))
            for btn in self.buttons:
                btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            clock.tick(FPS)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.background = pygame.image.load("imagens/desenho IF.png").convert()

    def run(self):
        menu = Menu(self.screen, self.background)
        menu.run()
        self.game_loop()

    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((30, 30, 30))
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()


class Temas:
    def __init__(self, screen, background, modo="principal"):
        self.screen = screen
        self.background = pygame.transform.scale(background, screen.get_size())
        screen_width, screen_height = screen.get_size()

        mid_x = screen_width // 2
        start_y = screen_height // 2 - 120
        gap = 80

        self.selected = None
        self.modo = modo
        self.running = True

        largura = 720
        altura = 500
        self.container_rect = pygame.Rect(
            (screen_width - largura) // 2,
            (screen_height - altura) // 2,
            largura,altura
        )
        if modo == "principal":
            self.buttons = [
                Button("Professores",(mid_x, start_y),self.select_professores, tema=True),
                Button("Matérias",(mid_x, start_y + gap),self.select_materias, tema=True),
                Button("Geral",(mid_x, start_y + 2 * gap),self.select_geral, tema=True),
                Button("Cursos",(mid_x, start_y + 3 * gap),self.select_cursos, tema=True),
            ]
        elif modo == "cursos":
            self.buttons = [
                Button("Informática",(mid_x, start_y),self.select_informatica, tema=True),
                Button("Vestuário",(mid_x, start_y + gap),self.select_vestuario, tema=True),
                Button("Eletrotécnica",(mid_x, start_y + 2 * gap),self.select_eletrotecnica, tema=True),
                Button("Têxtil",(mid_x, start_y + 3 * gap),self.select_textil, tema=True),
                Button("Voltar",(mid_x, start_y + 4 * gap),self.select_voltar, small=True, tema=True),
            ]

    def select_professores(self):
        self.select("Professores")
    def select_materias(self):
        self.select("Matérias")
    def select_geral(self): 
        self.select("Geral")
    def select_cursos(self): 
        self.select("Cursos")
    def select_informatica(self): 
        self.select("Informática")
    def select_vestuario(self): 
        self.select("Vestuário")
    def select_eletrotecnica(self): 
        self.select("Eletrotécnica")
    def select_textil(self): 
        self.select("Têxtil")
    def select_voltar(self): 
        self.select("Voltar")

    def select(self, nome):
        self.selected = nome
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button== 1:
                    for btn in self.buttons:
                        btn.check_click(event.pos)

            self.screen.blit(self.background, (0, 0))
            container = pygame.Surface((self.container_rect.width, self.container_rect.height))
            container.set_alpha(180)
            container.fill(GRAY)
            self.screen.blit(container, self.container_rect.topleft)

            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            clock.tick(FPS)

        return self.selected


#Forca (desenho da base da forca e o boneco de acordo com a quantidade de erros)
def desenhar_boneco(surface, erros, offset_y=0):
 
    pygame.draw.line(surface, BLACK, (100, 600), (300, 600), 6)                 
    pygame.draw.line(surface, BLACK, (200, 600), (200, 100 + offset_y), 6)       
    pygame.draw.line(surface, BLACK, (200, 100 + offset_y), (400, 100 + offset_y), 6) 
    pygame.draw.line(surface, BLACK, (400, 100 + offset_y), (400, 180 + offset_y), 6)
        

    if erros > 0:
        pygame.draw.circle(surface, BLACK, (400, 220 + offset_y), 40, 6)
    if erros > 1:
        pygame.draw.line(surface, BLACK, (400, 260 + offset_y), (400, 400 + offset_y), 6)
    if erros > 2:
        pygame.draw.line(surface, BLACK, (400, 280 + offset_y), (330, 350 + offset_y), 6)     
    if erros > 3:
        pygame.draw.line(surface, BLACK, (400, 280 + offset_y), (470, 350 + offset_y), 6)
    if erros > 4:
        pygame.draw.line(surface, BLACK, (400, 400 + offset_y), (330, 480 + offset_y), 6)
    if erros > 5:
        pygame.draw.line(surface, BLACK, (400, 400 + offset_y), (470, 480 + offset_y), 6)
      

def jogar(screen, palavra, background, escolha):
    letras_certas = []
    letras_erradas = []
    chances = 6

    #Variáveis de pontuação
    pontuacao = 0

    teclado = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rodando = True
    clock = pygame.time.Clock()
    FONT_SMALL = pygame.font.SysFont("Arial", 35)

 
    fundo_transparente = background.copy()
    fundo_transparente.set_alpha(120)
    
    erros = 6 - chances
    desenhar_boneco(screen, erros)


    inicio_x = 470
    inicio_y = 500  
    largura_tecla = 45
    altura_tecla = 45
    espaco = 8
    max_x = 1130
    

    while rodando:
        screen.fill(WHITE)
        screen.blit(fundo_transparente, (0, 0))  
        
        
        palavra_tema = f"Tema:{escolha}"
        render_tema = FONT_SMALL.render(palavra_tema, True, BLUE)
        screen.blit(render_tema,(500,90))

        #Mostrar pontuação
        texto_pontos = f"Pontuação: {pontuacao}"
        render_pontos = FONT_SMALL.render(texto_pontos, True, BLUE)
        screen.blit(render_pontos, (950, 90))

        # Exibição das palavras
        exibida = ""
        for letra in palavra:
            # Letras acertadas ou espaços já aparecem
            if letra in letras_certas or letra == " ":
                exibida += letra.upper() + " "
            else:
                exibida += "_ "

        render = FONT_SMALL.render(exibida, True, BLACK)
        screen.blit(render, (500, 130))

        
        desenhar_boneco(screen, 6 - chances)

        # Teclado 
        x, y = inicio_x, inicio_y
        for letra in teclado:
            if letra.lower() in letras_certas:
                cor_retangulo = (0, 200, 0)
            elif letra.lower() in letras_erradas:
                cor_retangulo = (200, 0, 0)
            else:
                cor_retangulo = (0, 150, 255)

            pygame.draw.rect(screen, cor_retangulo, (x, y, largura_tecla, altura_tecla))
            screen.blit(FONT_SMALL.render(letra, True, WHITE), (x + 12, y + 5))

            x += largura_tecla + espaco
            if x > max_x:
                x = inicio_x
                y += altura_tecla + espaco

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()
                x, y = inicio_x, inicio_y
                for letra in teclado:
                    rect = pygame.Rect(x, y, largura_tecla, altura_tecla)
                    if rect.collidepoint(mouse):
                        #Sistema de pontuação adaptável
                        if letra.lower() in palavra and letra.lower() not in letras_certas:
                            letras_certas.append(letra.lower())
                            som_certo.play()
                            pontuacao += 10  # +10 pontos por acerto

                        elif letra.lower() not in letras_erradas and letra.lower() not in letras_certas:
                            letras_erradas.append(letra.lower())
                            chances -= 1
                            pontuacao -= 5   # -5 pontos por erro

                    x += largura_tecla + espaco
                    if x > max_x:
                        x = inicio_x
                        y += altura_tecla + espaco
                        
            if chances == 0:
                pontuacao_final = pontuacao
                print(f"Você perdeu! Palavra era: {palavra}")
                print(f"Sua pontuação final foi: {pontuacao_final}")
                rodando = False
            elif all(letra in letras_certas for letra in palavra):
                pontuacao_final = pontuacao
                print("Você venceu!")
                print(f"Sua pontuação final foi: {pontuacao_final}")
                rodando = False

    
        clock.tick(FPS)

if __name__ == "__main__":
    Game().run()




