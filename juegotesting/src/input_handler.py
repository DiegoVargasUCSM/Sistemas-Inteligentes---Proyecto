import pygame


class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            self._handle_key(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse(event)

    def _handle_key(self, event):
        if event.key == pygame.K_SPACE:
            if self.game.state == self.game.STATE_START:
                self.game._enter_playing()
            elif self.game.state in (self.game.STATE_GAME_OVER, self.game.STATE_LOST):
                self.game.new_game()
                self.game._enter_playing()
        elif event.key == pygame.K_p:
            if self.game.state == self.game.STATE_PLAYING:
                self.game._enter_paused()
            elif self.game.state == self.game.STATE_PAUSED:
                self.game._enter_playing()
        elif event.key == pygame.K_ESCAPE:
            if self.game.state in (self.game.STATE_GAME_OVER, self.game.STATE_LOST):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif self.game.state == self.game.STATE_PLAYING:
                self.game.state = self.game.STATE_START
                self.game.new_game()

    def _handle_mouse(self, event):
        if self.game.state == self.game.STATE_START:
            self.game._enter_playing()
            return
        if self.game.state != self.game.STATE_PLAYING:
            return
        mouse_x, mouse_y = event.pos
        for card in self.game.board.cards:
            x = self.game.renderer.grid_x + card.position[1] * (
                self.game.renderer.card_size + self.game.renderer.card_gap
            )
            y = self.game.renderer.grid_y + card.position[0] * (
                self.game.renderer.card_size + self.game.renderer.card_gap
            )
            rect = pygame.Rect(x, y, self.game.renderer.card_size, self.game.renderer.card_size)
            if rect.collidepoint(mouse_x, mouse_y):
                self.game._handle_card_click(card.position[0], card.position[1])
                break
