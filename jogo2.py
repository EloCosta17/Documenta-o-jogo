import pygame
import sys

# Configurações da música
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load("sons/musica_de_fundo.mp3")
pygame.mixer.music.play(-1)

# --------- Configurações ---------
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CORAL = (229, 65, 51, 1)
GRAY = (230, 230, 230)

pygame.display.set_caption("Menu Inicial - Jogo Exemplo")
FONT = pygame.font.SysFont("Goudy Stout", 48)
FONT_MSG = pygame.font.Font(None, 36)

#Efeito máquina de escrever
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

    #Container semi-transparente
    container = pygame.Surface((largura, altura))
    container.set_alpha(200)
    container.fill(WHITE)
    screen.blit(container, (x, y))

    texto_digitado(screen, "Bem-vindo ao jogo da forca!", x + 20, y + 40, BLACK, delay=20)
    texto_digitado(screen, "Escolha um tema e acerte as letras para descobrir a palavra,", x + 20, y + 80, BLACK, delay=20)
    texto_digitado(screen, "e lembre-se, você pode errar apenas 6 vezes!", x + 20, y + 120, BLACK, delay=20)

    pygame.display.flip()
    pygame.time.delay(2000)

class Button:
    def __init__(self, text, pos, callback, small=False, tema=False):
        self.text = text
        self.callback = callback

        if tema:
            self.default_color = BLACK  
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
            temas = Temas(self.screen, self.background)
            escolha = temas.run()

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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
            largura,
            altura
        )
        if modo == "principal":
            self.buttons = [
                Button("Professores",(mid_x, start_y), self.select_professores, tema=True),
                Button("Matérias",(mid_x, start_y + gap), self.select_materias, tema=True),
                Button("Geral",(mid_x, start_y + 2 * gap), self.select_geral, tema=True),
                Button("Cursos",(mid_x, start_y + 3 * gap), self.select_cursos, tema=True),
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
        print(f"[Temas] selecionado: {nome}")
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

if __name__ == "__main__":
    Game().run()




