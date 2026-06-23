import math
import pygame


class Renderer:
    COLORS = {
        "bg": (30, 30, 60),
        "card_back": (100, 100, 180),
        "card_front": (240, 240, 255),
        "card_matched": (100, 200, 100),
        "text": (255, 255, 255),
        "accent": (255, 200, 50),
        "danger": (255, 60, 60),
        "warning": (255, 200, 50),
        "button": (60, 60, 120),
        "button_hover": (80, 80, 160),
    }

    def __init__(self, game):
        self.game = game
        self.card_size = 100
        self.card_gap = 10
        self._calculate_layout()
        self.start_button_rect = None

    def _calculate_layout(self):
        total_w = self.game.cols * self.card_size + (self.game.cols - 1) * self.card_gap
        total_h = self.game.rows * self.card_size + (self.game.rows - 1) * self.card_gap
        self.grid_x = (800 - total_w) // 2
        self.grid_y = (700 - total_h) // 2 + 40

    def draw(self):
        screen = self.game.screen
        screen.fill(self.COLORS["bg"])
        if self.game.state == self.game.STATE_START:
            self._draw_start_screen()
        elif self.game.state in (self.game.STATE_PLAYING, self.game.STATE_PAUSED):
            self._draw_game_screen()
        elif self.game.state == self.game.STATE_GAME_OVER:
            self._draw_game_over_screen()
        elif self.game.state == self.game.STATE_LOST:
            self._draw_lost_screen()
        pygame.display.flip()

    def _draw_start_screen(self):
        screen = self.game.screen
        title = self.game.font_large.render("Juego de Memoria", True, self.COLORS["accent"])
        title_rect = title.get_rect(center=(400, 200))
        screen.blit(title, title_rect)
        instructions = [
            "Encuentra todos los pares de cartas!",
            "",
            "Haz clic en una carta para descubrirla.",
            "Haz clic en una segunda carta para buscar su par.",
            "Si coinciden, quedan descubiertas.",
            "Si no, se voltean tras un momento.",
            "",
            "Encuentra todos los pares para ganar!",
            "",
            f"Tienes {self.game.TIME_LIMIT} segundos. Cada fallo resta 5s al reloj!",
        ]
        y = 280
        for line in instructions:
            text = self.game.font_small.render(line, True, self.COLORS["text"])
            rect = text.get_rect(center=(400, y))
            screen.blit(text, rect)
            y += 30
        start_text = self.game.font_medium.render("Presiona ESPACIO o Haz Clic para Iniciar", True, self.COLORS["accent"])
        start_rect = start_text.get_rect(center=(400, 560))
        screen.blit(start_text, start_rect)
        self.start_button_rect = start_rect

    def _draw_game_screen(self):
        screen = self.game.screen
        score_text = self.game.font_small.render(
            self.game.player.score, True, self.COLORS["text"]
        )
        screen.blit(score_text, (20, 20))
        remaining = self.game.time_remaining
        timer_color = self.COLORS["danger"] if remaining <= 10 else self.COLORS["text"]
        timer_text = self.game.font_small.render(
            f"Tiempo: {remaining}s", True, timer_color
        )
        timer_rect = timer_text.get_rect(center=(400, 20))
        screen.blit(timer_text, timer_rect)
        if self.game.penalty_flash > 0:
            flash_text = self.game.font_small.render("-5s", True, self.COLORS["danger"])
            flash_rect = flash_text.get_rect(midleft=(timer_rect.right + 10, timer_rect.centery))
            screen.blit(flash_text, flash_rect)
        pause_text = self.game.font_small.render(
            "Presiona P para Pausar" if self.game.state == self.game.STATE_PLAYING else "PAUSA - Presiona P para Reanudar",
            True,
            self.COLORS["accent"] if self.game.state == self.game.STATE_PLAYING else (255, 100, 100),
        )
        pause_rect = pause_text.get_rect(topright=(780, 20))
        screen.blit(pause_text, pause_rect)
        for card in self.game.board.cards:
            self._draw_card(card)
        if self.game.state == self.game.STATE_PAUSED:
            overlay = pygame.Surface((800, 700))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            paused_text = self.game.font_large.render("PAUSA", True, self.COLORS["accent"])
            paused_rect = paused_text.get_rect(center=(400, 350))
            screen.blit(paused_text, paused_rect)

    def _draw_card(self, card):
        screen = self.game.screen
        x = self.grid_x + card.position[1] * (self.card_size + self.card_gap)
        y = self.grid_y + card.position[0] * (self.card_size + self.card_gap)
        if card.is_matched:
            color = self.COLORS["card_matched"]
        elif card.is_revealed:
            color = self.COLORS["card_front"]
        else:
            color = self.COLORS["card_back"]
        pygame.draw.rect(screen, color, (x, y, self.card_size, self.card_size), border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, self.card_size, self.card_size), 2, border_radius=8)
        if card.is_revealed or card.is_matched:
            cx = x + self.card_size // 2
            cy = y + self.card_size // 2
            s = self.card_size // 4
            color = (30, 30, 60)
            if card.symbol == "circle":
                pygame.draw.circle(screen, color, (cx, cy), s, 3)
            elif card.symbol == "square":
                pygame.draw.rect(screen, color, (cx - s, cy - s, s * 2, s * 2), 3)
            elif card.symbol == "triangle":
                pts = [(cx, cy - s), (cx - s, cy + s), (cx + s, cy + s)]
                pygame.draw.polygon(screen, color, pts, 3)
            elif card.symbol == "diamond":
                pts = [(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)]
                pygame.draw.polygon(screen, color, pts, 3)
            elif card.symbol == "star":
                pts = []
                for i in range(10):
                    r = s if i % 2 == 0 else s // 2
                    a = i * 36 - 90
                    pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
                pygame.draw.polygon(screen, color, pts, 3)
            elif card.symbol == "heart":
                pts = []
                for a in range(0, 360, 5):
                    t = math.radians(a)
                    hx = cx + s * 0.8 * (16 * math.sin(t) ** 3) / 16
                    hy = cy - s * 0.8 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 16
                    pts.append((hx, hy))
                pygame.draw.polygon(screen, color, pts, 3)
            elif card.symbol == "pentagon":
                pts = []
                for i in range(5):
                    a = i * 72 - 90
                    pts.append((cx + s * math.cos(math.radians(a)), cy + s * math.sin(math.radians(a))))
                pygame.draw.polygon(screen, color, pts, 3)
            elif card.symbol == "hexagon":
                pts = []
                for i in range(6):
                    a = i * 60 - 90
                    pts.append((cx + s * math.cos(math.radians(a)), cy + s * math.sin(math.radians(a))))
                pygame.draw.polygon(screen, color, pts, 3)
            else:
                text = self.game.font_large.render(card.symbol[0].upper(), True, (30, 30, 60))
                trect = text.get_rect(center=(cx, cy))
                screen.blit(text, trect)

    def _draw_game_over_screen(self):
        screen = self.game.screen
        overlay = pygame.Surface((800, 700))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        win_text = self.game.font_large.render("Ganaste!", True, self.COLORS["accent"])
        win_rect = win_text.get_rect(center=(400, 200))
        screen.blit(win_text, win_rect)
        stats = [
            f"Pares Encontrados: {self.game.player.pairs_found}",
            f"Intentos Totales: {self.game.player.attempts}",
        ]
        y = 300
        for line in stats:
            text = self.game.font_medium.render(line, True, self.COLORS["text"])
            rect = text.get_rect(center=(400, y))
            screen.blit(text, rect)
            y += 60
        restart_text = self.game.font_medium.render("Presiona ESPACIO para Jugar de Nuevo", True, self.COLORS["accent"])
        restart_rect = restart_text.get_rect(center=(400, 500))
        screen.blit(restart_text, restart_rect)
        quit_text = self.game.font_small.render("Presiona ESC para Salir", True, self.COLORS["text"])
        quit_rect = quit_text.get_rect(center=(400, 560))
        screen.blit(quit_text, quit_rect)

    def _draw_lost_screen(self):
        screen = self.game.screen
        overlay = pygame.Surface((800, 700))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        lost_text = self.game.font_large.render("Tiempo Agotado!", True, self.COLORS["danger"])
        lost_rect = lost_text.get_rect(center=(400, 200))
        screen.blit(lost_text, lost_rect)
        stats = [
            f"Pares Encontrados: {self.game.player.pairs_found}",
            f"Intentos Totales: {self.game.player.attempts}",
        ]
        y = 300
        for line in stats:
            text = self.game.font_medium.render(line, True, self.COLORS["text"])
            rect = text.get_rect(center=(400, y))
            screen.blit(text, rect)
            y += 60
        restart_text = self.game.font_medium.render("Presiona ESPACIO para Intentar de Nuevo", True, self.COLORS["accent"])
        restart_rect = restart_text.get_rect(center=(400, 500))
        screen.blit(restart_text, restart_rect)
        quit_text = self.game.font_small.render("Presiona ESC para Salir", True, self.COLORS["text"])
        quit_rect = quit_text.get_rect(center=(400, 560))
        screen.blit(quit_text, quit_rect)
