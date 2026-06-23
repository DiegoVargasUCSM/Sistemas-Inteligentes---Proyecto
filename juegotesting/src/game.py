import pygame
from src.board import Board
from src.player import Player
from src.renderer import Renderer
from src.input_handler import InputHandler


class Game:
    STATE_START = "start"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game_over"
    STATE_LOST = "lost"
    TIME_LIMIT = 100

    def __init__(self, rows=4, cols=4):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.total_pairs = (rows * cols) // 2
        self.screen = pygame.display.set_mode((800, 700))
        pygame.display.set_caption("Juego de Memoria")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        self.board = None
        self.player = None
        self.state = Game.STATE_START
        self.selected_first = None
        self.waiting_for_flip = False
        self.flip_timer = 0
        self.FLIP_DELAY = 60

        self.start_ticks = 0
        self.paused_ticks = 0
        self.penalty_flash = 0

        self.renderer = Renderer(self)
        self.input_handler = InputHandler(self)

        self.new_game()

    def new_game(self):
        self.board = Board(self.rows, self.cols)
        self.player = Player(total_pairs=self.total_pairs, time_limit=Game.TIME_LIMIT)
        self.selected_first = None
        self.waiting_for_flip = False
        self.flip_timer = 0
        self.start_ticks = pygame.time.get_ticks()
        self.paused_ticks = 0
        self.penalty_flash = 0

    @property
    def time_remaining(self):
        if self.state == Game.STATE_START or self.state == Game.STATE_LOST:
            return Game.TIME_LIMIT
        if self.state == Game.STATE_PAUSED:
            elapsed = (self.paused_ticks - self.start_ticks) / 1000
        else:
            elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        remaining = Game.TIME_LIMIT - elapsed
        return max(0, int(remaining))

    def handle_event(self, event):
        self.input_handler.handle(event)

    def _enter_playing(self):
        if self.state == Game.STATE_PAUSED:
            pause_duration = pygame.time.get_ticks() - self.paused_ticks
            self.start_ticks += pause_duration
        else:
            self.start_ticks = pygame.time.get_ticks()
        self.state = Game.STATE_PLAYING

    def _enter_paused(self):
        self.paused_ticks = pygame.time.get_ticks()
        self.state = Game.STATE_PAUSED

    def update(self):
        if self.state == Game.STATE_PLAYING and self.waiting_for_flip:
            self.flip_timer += 1
            if self.flip_timer >= self.FLIP_DELAY:
                self._finish_turn()

        if self.penalty_flash > 0:
            self.penalty_flash -= 1

        if self.state == Game.STATE_PLAYING and self.board.is_complete():
            self.state = Game.STATE_GAME_OVER

        if self.state == Game.STATE_PLAYING and self.time_remaining <= 0:
            self.state = Game.STATE_LOST

    def _finish_turn(self):
        self.board.reset_selection()
        self.selected_first = None
        self.waiting_for_flip = False
        self.flip_timer = 0

    def _handle_card_click(self, row, col):
        if self.state != Game.STATE_PLAYING or self.waiting_for_flip:
            return
        card = self.board.select_card(row, col)
        if card is None:
            return
        if self.selected_first is None:
            self.selected_first = card
        else:
            self.player.increment_attempts()
            if self.board.check_match():
                self.player.add_pair()
                self.selected_first = None
            else:
                self.start_ticks = max(0, self.start_ticks - 5000)
                self.penalty_flash = 30
                self.waiting_for_flip = True
                self.flip_timer = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)
            self.update()
            self.renderer.draw()
            self.clock.tick(60)
        pygame.quit()
