import pygame
import sys
import random

#músicas
pygame.mixer.init()
pygame.init()
pygame.mixer.music.load("sons_musica_de_fundo.mp3")
pygame.mixer.music.play(-1)

#sons
som_certo = pygame.mixer.Sound("aparecer_letra.mp3")
som_errado = pygame.mixer.Sound("sons_somdeerro.mp3")
som_gameover = pygame.mixer.Sound("sons_gameover.mp3")
som_win = pygame.mixer.Sound("sons_somvitória.mp3")

# --------- Configurações ---------
FPS = 60

#cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CORAL = (229, 65, 51, 1)
GRAY = (230, 230, 230)
BLUE = (0, 100, 200)

pygame.display.set_caption("Jogo da forca - IFCA")
FONT = pygame.font.SysFont("Kristen ITC", 60)
FONT_MSG = pygame.font.Font(None, 36)

#temas
temas = {
    "Professores": ["hugo", "joaildo", "carlos eugenio", "saulo", "gian", "botinni"],
    "Matérias": ["matematica", "geografia", "biologia", "fisica", "quimica", "ingles"],
    "Geral": ["thales", "ricardo", "rose", "bloco d", "max", "artes"],
    "Cursos": {
        "Informática": ["python", "design web", "anderson", "processador", "romerito", "java script"],
        "Vestuário": ["croqui", "laila", "modelagem", "tecido", "cad", "confecçao"],
        "Eletrotécnica": ["circuito", "transformador", "jonas", "condutor", "isolamento","francisco"],
        "Têxtil": ["algodao", "beneficiamento", "tecelagem", "tingimento","padronagem","alvejamento"]
    }
}

# dicas
dicas = {
    #professores
    "hugo": "Professor de Informática no IFRN Caicó.",
    "joaildo": "Professor bastante querido na comunidade acadêmica.",
    "carlos eugenio": "É quem diz: tem que estudar no mínimo duas horas por dia .",
    "saulo": "Professor de Química no IFRN Caicó.",
    "gian": "Professor da área de Eletrotécnica.",
    "botinni": "Um dos coordenadores mais legais do IFRN",

    #materias
    "matematica": "Muito importante para Enem.",
    "geografia": "Faz parte das ciências humanas.",
    "biologia": "O terror dos quartos anos.",
    "fisica": "Área que estuda movimento, energia e forças.",
    "quimica": "Envolve experimentos.",
    "ingles": "Língua estrangeira",

    #geral
    "thales": "O mais temido nos corredores.",
    "ricardo": "Tem uma careca bonita.",
    "rose": "Servidora bastante querida no IFRN Caicó.",
    "bloco d": "Lugar dos namorados(e amantes).",
    "max": "Professor de informática.",
    "artes": "Disciplina ligada à criatividade e expressão.",

    #informatica
    "python": "Cobrinhas.",
    "design web": "Área voltada à criação e estrutura de sites.",
    "anderson": "Professor da disciplina de redes.",
    "processador": "Componente essencial que executa instruções do computador.",
    "romerito": "Corre muito, inclusive dos alunos.",
    "java script": "Linguagem de programação muito usada em grandes sistemas.",

    #vestuario
    "croqui": "Desenho inicial usado para representar modelos de roupa.",
    "laila": "Professora do curso de Vestuário.",
    "modelagem": "Processo de criação de moldes.",
    "tecido": "Material usado na confecção de roupas.",
    "cad": "Ferramenta digital usada para modelagem de roupas.",
    "confeçcao": "Etapa prática de produção de roupas.",

    #eletro
    "circuito": "Base fundamental para qualquer sistema elétrico.",
    "transformador": "Equipamento que altera níveis de tensão elétrica.",
    "jonas": "Meu malvado favorito.",
    "condutor": "Material que permite passagem de corrente elétrica.",
    "isolamento": "Material que impede passagem de corrente elétrica.",
    "francisco": "Professor.",

    #textil
    "algodao": "Fibra natural muito usada na indústria têxtil.",
    "beneficiamento": "Etapa que prepara fibras para uso na produção.",
    "tecelagem": "Processo de transformar fios em tecido.",
    "tingimento": "Processo que dá cor aos tecidos.",
    "padronagem": "Definição de estampas e padrões.",
    "alvejamento": "Processo químico usado para clarear fibras."
}

#efeito máquina de escrever
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

    #container semi-transparente
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
            font = pygame.font.SysFont("Kristen ITC", 32)
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

#menu principal
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
            if escolha == "Voltar":
                return  #volta ao menu inicial

            if escolha == "Cursos":
                while True:
                    cursos = Temas(self.screen, self.background, modo="cursos")
                    escolha_curso = cursos.run()
                    if escolha_curso == "Voltar":
                        break  #volta a seleção de temas
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
        #escolha das palavras aleatoriamente
        if escolha in ["Informática", "Vestuário", "Eletrotécnica", "Têxtil"]:
            palavra = random.choice(temas["Cursos"][escolha])
        else:
            palavra = random.choice(temas[escolha])

        resultado = jogar(self.screen, palavra, self.background, escolha)
        if resultado != "voltar":
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
        self.background = pygame.image.load("desenho IF2.png").convert()

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
                Button("Voltar",(mid_x, start_y + 4 * gap),self.select_voltar, small=True, tema=True),
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
    def select_voltar(self): 
        self.select("Voltar")
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


#desenho da forca e do boneco
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
      

def mostrar_dica(screen, background, texto):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    font_titulo = pygame.font.SysFont("Kristen ITC", 50)
    font_msg = pygame.font.SysFont("Arial", 30)

    titulo = font_titulo.render("DICA", True, (0, 0, 255))
    def split_text(msg, font, max_width):
        palavras = msg.split(" ")
        linhas = []
        atual = ""
        for p in palavras:
            teste = (atual + " " + p).strip()
            if font.size(teste)[0] <= max_width:
                atual = teste
            else:
                linhas.append(atual)
                atual = p
        if atual:
            linhas.append(atual)
        return linhas

   #caixadica
    caixa_w, caixa_h = screen.get_width() - 800, 220
    caixa_rect = pygame.Rect(0, 0, caixa_w, caixa_h)
    caixa_rect.centerx = screen.get_width() // 2
    caixa_rect.y = screen.get_height() // 2 - 200 

    #mensagemdacaixa
    linhas = split_text(texto, font_msg, caixa_w - 60)

    #botao
    btn_ok_rect = pygame.Rect(0, 0, 280, 60)
    btn_ok_rect.centerx = screen.get_width() // 2
    btn_ok_rect.top = caixa_rect.bottom + 20

    clock = pygame.time.Clock()
    esperando = True

    while esperando:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_ok_rect.collidepoint(mouse):
                    esperando = False

        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))

        #caixa
        pygame.draw.rect(screen, (200, 200, 200), caixa_rect, border_radius=20)
       
        #titulo
        screen.blit(titulo, (caixa_rect.centerx - titulo.get_width()//2, caixa_rect.top + 5))

        # Texto da dica (linhas)
        start_y = caixa_rect.top + 80
        for i, linha in enumerate(linhas):
            rendered = font_msg.render(linha, True, (0, 0, 0))
            screen.blit(rendered, (caixa_rect.centerx - rendered.get_width()//2, start_y + i * 34))

        # botão
        if btn_ok_rect.collidepoint(mouse):
            cor = (0, 100, 255)
        else:
            cor = (0, 0, 255)
        pygame.draw.rect(screen, cor, btn_ok_rect, border_radius=10)
        txt_ok = font_msg.render("OK", True, (0, 0, 0))
        screen.blit(txt_ok, txt_ok.get_rect(center=btn_ok_rect.center))

        pygame.display.flip()
        clock.tick(60)


def jogar(screen, palavra, background, escolha):
    letras_certas = []
    letras_erradas = []
    chances = 6
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

    #imagens dos botões
    img_voltar = pygame.image.load("voltar_vermelho.png").convert_alpha()
    img_sair = pygame.image.load("sair_vermelho.png").convert_alpha()
    img_voltar = pygame.transform.scale(img_voltar, (50, 50))
    img_sair = pygame.transform.scale(img_sair, (50, 50))
    pos_voltar = (screen.get_width() - 120, 20)
    pos_sair = (screen.get_width() - 60, 20)
    rect_voltar = pygame.Rect(pos_voltar, img_voltar.get_size())
    rect_sair = pygame.Rect(pos_sair, img_sair.get_size())
    img_dica = pygame.image.load("dica.png").convert_alpha()
    img_dica = pygame.transform.scale(img_dica, (50, 50))
    pos_dica = (screen.get_width() - 180, 20)
    rect_dica = pygame.Rect(pos_dica, img_dica.get_size())

    #controledasdicas
    dica_usada = False
    CUSTO_DICA = 5
    mostrar_dica_texto = ""
    tempo_mensagem = 0
    DURACAO_MENSAGEM = 3000 

    while rodando:
        screen.fill(WHITE)
        screen.blit(fundo_transparente, (0, 0))  
        
        palavra_tema = f"Tema:{escolha}"
        render_tema = FONT_SMALL.render(palavra_tema, True, BLUE)
        screen.blit(render_tema,(500,90))

        texto_pontos = f"Pontuação: {pontuacao}"
        render_pontos = FONT_SMALL.render(texto_pontos, True, BLUE)
        screen.blit(render_pontos, (950, 90))

        exibida = ""
        for letra in palavra:
            if letra in letras_certas or letra == " ":
                exibida += letra.upper() + " " #exibir letra certa 
            else:
                exibida += "_ " #exibir espaço

        render = FONT_SMALL.render(exibida, True, BLACK)
        screen.blit(render, (500, 130))

        desenhar_boneco(screen, 6 - chances)

        #teclado
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

        screen.blit(img_voltar, pos_voltar)
        screen.blit(img_sair, pos_sair)
        screen.blit(img_dica, pos_dica)

        if mostrar_dica_texto and pygame.time.get_ticks() - tempo_mensagem < DURACAO_MENSAGEM:
            msg_render = FONT_MSG.render(mostrar_dica_texto, True, (0, 0, 255))
            screen.blit(msg_render, (screen.get_width()//2 - msg_render.get_width()//2, screen.get_height() - 80))
        elif mostrar_dica_texto:
            mostrar_dica_texto = ""

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse = pygame.mouse.get_pos()

                #verificação dos cliques botões
                if rect_voltar.collidepoint(mouse):
                    return "voltar"
                elif rect_sair.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
                elif rect_dica.collidepoint(mouse):
                    
                    if dica_usada:
                        mostrar_dica_texto = "Você já usou a dica nesta partida."
                        tempo_mensagem = pygame.time.get_ticks()
                    elif pontuacao < CUSTO_DICA:
                        mostrar_dica_texto = "Pontos insuficientes para usar a dica."
                        tempo_mensagem = pygame.time.get_ticks()
                    else:
                        pontuacao -= CUSTO_DICA
                        dica_usada = True
                        dica_text = dicas.get(palavra.lower(), "Sem dica disponível.")
                        mostrar_dica(screen, background, dica_text)

                #clique do teclado
                x, y = inicio_x, inicio_y
                for letra in teclado:
                    rect = pygame.Rect(x, y, largura_tecla, altura_tecla)
                    if rect.collidepoint(mouse):
                        if letra.lower() in palavra and letra.lower() not in letras_certas:
                            letras_certas.append(letra.lower())
                            som_certo.play()
                            pontuacao += 10  

                        elif letra.lower() not in letras_erradas and letra.lower() not in letras_certas:
                            letras_erradas.append(letra.lower())
                            som_errado.play()
                            chances -= 1
                            pontuacao -= 5   

                    x += largura_tecla + espaco
                    if x > max_x:
                        x = inicio_x
                        y += altura_tecla + espaco

            #mensagens finais
            if chances == 0:
                pontuacao_final = pontuacao
                resultado = tela_game_over(screen, background, pontuacao_final)
                if resultado == "jogar_novamente":
                    return "voltar"  # volta ao menu
                rodando = False

            elif all(letra == " " or letra in letras_certas for letra in palavra):
                pontuacao_final = pontuacao
                resultado = tela_win(screen, background, pontuacao_final)
                if resultado == "jogar_novamente":
                    return "voltar"
                rodando = False

        clock.tick(FPS)


        def tela_game_over(screen, background, pontuacao_final):
            som_gameover.play(-1)
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))

            font_gameover = pygame.font.SysFont("Kristen ITC", 120)
            texto = font_gameover.render("GAME OVER", True, (255, 0, 0))
            rect_texto = texto.get_rect(center=(screen.get_width() // 2, 130))
            screen.blit(texto, rect_texto)

            font_msg = pygame.font.SysFont("Arial", 40)
            msg = font_msg.render("Você foi enforcado! Tente novamente.", True, (255, 255, 255))
            msg_rect = msg.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(msg, msg_rect)

            msg_pontos = font_msg.render(f"Sua pontuação: {pontuacao_final}", True, (255, 255, 255))
            pontos_rect = msg_pontos.get_rect(center=(screen.get_width() // 2, 310))
            screen.blit(msg_pontos, pontos_rect)

            font_botao = pygame.font.SysFont("Kristen ITC", 40)
            cor_normal = (255, 255, 255)
            cor_hover = (255, 0, 0)

            btn_jogar_rect = pygame.Rect(470, 440, 350, 70)
            btn_sair_rect = pygame.Rect(470, 540, 350, 70)

            clock = pygame.time.Clock()
            esperando = True

            while esperando:
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if btn_jogar_rect.collidepoint(mouse):
                            som_gameover.stop() 
                            return "jogar_novamente"
                        elif btn_sair_rect.collidepoint(mouse):
                            pygame.quit()
                            sys.exit()

                screen.blit(background, (0, 0))
                screen.blit(overlay, (0, 0))
                screen.blit(texto, rect_texto)
                screen.blit(msg, msg_rect)
                screen.blit(msg_pontos, pontos_rect)

                if btn_jogar_rect.collidepoint(mouse):
                    cor_jogar = cor_hover
                else:
                    cor_jogar = cor_normal
                pygame.draw.rect(screen, cor_jogar, btn_jogar_rect, border_radius=10)
                txt_jogar = font_botao.render("Jogar Novamente", True, (0, 0, 0))
                screen.blit(txt_jogar, txt_jogar.get_rect(center=btn_jogar_rect.center))

                if btn_sair_rect.collidepoint(mouse):
                    cor_sair = cor_hover
                else:
                    cor_sair = cor_normal
                pygame.draw.rect(screen, cor_sair, btn_sair_rect, border_radius=10)
                txt_sair = font_botao.render("Sair", True, (0, 0, 0))
                screen.blit(txt_sair, txt_sair.get_rect(center=btn_sair_rect.center))

                pygame.display.flip()
                clock.tick(60)

        def tela_win(screen, background, pontuacao_final):
            som_win.play(-1)
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))

            font_gameover = pygame.font.SysFont("Kristen ITC", 120)
            texto = font_gameover.render("YOU WON", True, (0, 255, 0))
            rect_texto = texto.get_rect(center=(screen.get_width() // 2, 130))
            screen.blit(texto, rect_texto)

            font_msg = pygame.font.SysFont("Arial", 40)
            msg = font_msg.render("Quer tentar ganhar novamente?", True, (WHITE))
            msg_rect = msg.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(msg, msg_rect)

            #exibir pontuação final
            msg_pontos = font_msg.render(f"Sua pontuação: {pontuacao_final}", True, (WHITE))
            pontos_rect = msg_pontos.get_rect(center=(screen.get_width() // 2, 310))
            screen.blit(msg_pontos, pontos_rect)

            #botões
            font_botao = pygame.font.SysFont("Kristen ITC", 40)
            cor_normal = (WHITE)
            cor_hover = (0, 255, 0)

            btn_jogar_rect = pygame.Rect(470, 440, 350, 70)
            btn_sair_rect = pygame.Rect(470, 540, 350, 70)

            clock = pygame.time.Clock()
            esperando = True

            while esperando:
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if btn_jogar_rect.collidepoint(mouse):
                            som_win.stop() 
                            return "jogar_novamente"
                            
                        elif btn_sair_rect.collidepoint(mouse):
                            pygame.quit()
                            sys.exit()

                #redesenhar tudo
                screen.blit(background, (0, 0))
                screen.blit(overlay, (0, 0))
                screen.blit(texto, rect_texto)
                screen.blit(msg, msg_rect)
                screen.blit(msg_pontos, pontos_rect)

                #botão Jogar Novamente
                if btn_jogar_rect.collidepoint(mouse):
                    cor_jogar = cor_hover
                else:
                    cor_jogar = cor_normal
                pygame.draw.rect(screen, cor_jogar, btn_jogar_rect, border_radius=10)
                txt_jogar = font_botao.render("Jogar Novamente", True, (0, 0, 0))
                screen.blit(txt_jogar, txt_jogar.get_rect(center=btn_jogar_rect.center))

                #botão Sair
                if btn_sair_rect.collidepoint(mouse):
                    cor_sair = cor_hover
                else:
                    cor_sair = cor_normal
                pygame.draw.rect(screen, cor_sair, btn_sair_rect, border_radius=10)
                txt_sair = font_botao.render("Sair", True, (0, 0, 0))
                screen.blit(txt_sair, txt_sair.get_rect(center=btn_sair_rect.center))

                pygame.display.flip()
                clock.tick(60)

            
if __name__ == "__main__":
    Game().run()





